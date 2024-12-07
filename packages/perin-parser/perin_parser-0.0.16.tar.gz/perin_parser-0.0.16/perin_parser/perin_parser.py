# -*- coding:utf-8 -*-
# Author: hankcs
# Date: 2022-04-11 21:13
import copy
import json
import logging
from typing import Callable

import torch
from hanlp.common.dataset import SamplerBuilder, SortingSamplerBuilder
from hanlp.common.structure import History
from hanlp.common.torch_component import TorchComponent
from hanlp.layers.transformers.pt_imports import AutoModel_, AutoTokenizer_
from hanlp.metrics.mtl import MetricDict
from hanlp.utils.time_util import CountdownTimer
from hanlp_common.util import merge_locals_kwargs
from torch.utils.data import DataLoader
from transformers import PreTrainedTokenizer, AutoTokenizer

from perin_parser.data.batch import Batch
from perin_parser.data.shared_dataset import SharedDataset
from perin_parser.model.model import Model
from perin_parser.utility.adamw import AdamW
from perin_parser.utility.amr_utils import mrp_to_amr
from perin_parser.utility.autoclip import AutoClip
from perin_parser.utility.evaluate import evaluate, F1
from perin_parser.utility.loss_weight_learner import LossWeightLearner
from perin_parser.utility.predict import sentence_condition
from perin_parser.utility.schedule.multi_scheduler import multi_scheduler_wrapper


class PerinParser(TorchComponent):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._tokenizer: PreTrainedTokenizer = None
        self._dataset: SharedDataset = None
        self.model: Model = None

    def build_dataloader(self, data, batch_size, shuffle=False, device=None, logger: logging.Logger = None,
                         sampler_builder=None, gradient_accumulation=1, workers=0,
                         **kwargs) -> DataLoader:
        if shuffle:
            args = self.config
            dataset = SharedDataset(args)
            dataset.load_datasets(args, device, 1, self._tokenizer, sampler_builder)
            self._dataset = dataset
        elif isinstance(data, dict):
            args = self.config
            args.validation_data = data
            dataset = self._dataset
            backup = copy.copy(dataset.child_datasets)
            for each in backup.keys() - data.keys():
                dataset.child_datasets.pop(each)
            dataset.load_datasets(args, device, 1, self._tokenizer, sampler_builder, load_all=False)
            # dataset.child_datasets = backup
        return data

    def build_optimizer(self, balance_loss_weights, encoder_weight_decay, decoder_weight_decay, beta_2,
                        n_encoder_layers, **kwargs):
        model = self.model
        parameters = [{"params": p, "weight_decay": encoder_weight_decay} for p in
                      model.get_encoder_parameters(n_encoder_layers)] + [
                         {"params": model.get_decoder_parameters(), "weight_decay": decoder_weight_decay}
                     ]
        optimizer = AdamW(parameters, betas=(0.9, beta_2))
        scheduler = multi_scheduler_wrapper(optimizer, self.config)
        autoclip = AutoClip([p for name, p in model.named_parameters() if "loss_weights" not in name])
        if self.config.balance_loss_weights:
            loss_weight_learner = LossWeightLearner(self.config, model, 1)
        else:
            loss_weight_learner = None
        return optimizer, scheduler, autoclip, loss_weight_learner

    def build_criterion(self, **kwargs):
        pass

    def build_metric(self, **kwargs):
        pass

    def execute_training_loop(self, trn: DataLoader, dev: DataLoader, epochs, criterion, optimizer, metric, save_dir,
                              logger: logging.Logger, devices, ratio_width=None, patience=100,
                              **kwargs):
        best_epoch, best_metric = 0, -1
        timer = CountdownTimer(epochs)
        history = History()
        for epoch in range(1, epochs + 1):
            logger.info(f"[yellow]Epoch {epoch} / {epochs}:[/yellow]")
            self.fit_dataloader(trn, criterion, optimizer, metric, logger, history=history, ratio_width=ratio_width,
                                epoch=epoch,
                                **self.config)
            dev_metric = self.evaluate_dataloader(dev, criterion, logger=logger, ratio_width=ratio_width,
                                                  save_dir=save_dir)
            dev_metric = float(torch.mean(torch.tensor([float(x) for x in dev_metric.values()])))
            timer.update()
            report = f"{timer.elapsed_human} / {timer.total_time_human} ETA: {timer.eta_human}"
            if dev_metric > best_metric:
                best_epoch, best_metric = epoch, dev_metric
                self.save_weights(save_dir)
                report += ' [red](saved)[/red]'
            else:
                report += f' ({epoch - best_epoch})'
                if epoch - best_epoch >= patience:
                    report += ' early stop'
            logger.info(report)
            if epoch - best_epoch >= patience:
                break
        if not best_epoch:
            self.save_weights(save_dir)
        elif best_epoch != epoch:
            self.load_weights(save_dir)
        logger.info(f"Max score of dev is {best_metric:.2%} at epoch {best_epoch}")
        logger.info(f"Average time of each epoch is {timer.elapsed_average_human}")
        logger.info(f"{timer.elapsed_human} elapsed")
        return best_metric

    def fit_dataloader(self, trn: DataLoader, criterion, optimizer, metric, logger: logging.Logger,
                       history: History = None,
                       accumulation_steps=1, epoch=None, ratio_width=None, **kwargs):
        optimizer, scheduler, autoclip, loss_weight_learner = optimizer
        trn = self._dataset.train
        gpu = self.device
        model = self.model
        self.model.train()
        timer = CountdownTimer(history.num_training_steps(len(trn), gradient_accumulation=accumulation_steps))
        accu_loss = 0
        for idx, batch in enumerate(trn):
            batch = Batch.to(batch, gpu)
            total_loss, losses, stats = model(batch)
            if loss_weight_learner:
                loss_weight_learner.compute_grad(losses, epoch)

            # if accumulation_steps and accumulation_steps > 1:
            #     total_loss /= accumulation_steps
            total_loss.backward()
            accu_loss += float(total_loss)
            if history.step(accumulation_steps):
                grad_norm = autoclip()
                if loss_weight_learner:
                    loss_weight_learner.step(epoch)
                scheduler(epoch)
                optimizer.step()
                model.zero_grad()
                report = f'loss: {accu_loss / (idx + 1):.4f} norm: {float(grad_norm):.4f}'
                timer.log(report, logger=logger, ratio_percentage=False, ratio_width=ratio_width)

    def evaluate_dataloader(self, data: DataLoader, criterion: Callable, metric=None, output=False, save_dir=None,
                            logger=None,
                            **kwargs):
        model = self.model
        args = self.config
        input_paths = args.validation_data if data == 'dev' else data
        data = self._dataset.val
        gpu = self.device
        output_directory = save_dir
        input_files = {(f, l): input_paths[(f, l)] for f, l in args.frameworks}
        model.eval()

        sentences = {(f, l): {} for f, l in args.frameworks}
        for framework, language in args.frameworks:
            with open(input_files[(framework, language)], encoding="utf8") as f:
                for line in f.readlines():
                    line = json.loads(line)

                    if not sentence_condition(line, framework, language):
                        continue

                    line["nodes"] = []
                    line["edges"] = []
                    line["tops"] = []
                    line["framework"] = framework
                    line["language"] = language
                    sentences[(framework, language)][line["id"]] = line

        timer = CountdownTimer(len(data))
        for i, batch in enumerate(data):
            with torch.no_grad():
                all_predictions = model(Batch.to(batch, gpu), inference=True)
                timer.log('Predicting ...')

            for (framework, language), predictions in all_predictions.items():
                for prediction in predictions:
                    for key, value in prediction.items():
                        sentences[(framework, language)][prediction["id"]][key] = value

        results = dict()
        metrics = MetricDict()
        timer = CountdownTimer(len(args.frameworks))
        for framework, language in args.frameworks:
            output_path = f"{output_directory}/prediction_{framework}_{language}.json"
            with open(output_path, "w", encoding="utf8") as f:
                for sentence in sentences[(framework, language)].values():
                    json.dump(sentence, f, ensure_ascii=False)
                    f.write("\n")
                    f.flush()

            scores = evaluate(output_directory, framework, language, input_files[(framework, language)])
            results[(framework, language)] = scores
            section = MetricDict(primary_key='all')
            for k, v in scores.items():
                section[k] = F1(v)
            metrics[f'{framework}-{language}'] = section
            timer.log(metrics.cstr(), logger=logger)

        return metrics

    def build_model(self, training=True, encoder='xlm-roberta-base', **kwargs) -> torch.nn.Module:
        encoder = AutoModel_.from_pretrained(encoder, training=training, output_hidden_states=True)
        self.config.hidden_size = encoder.config.hidden_size
        return Model(self._dataset, self.config, encoder, initialize=training)

    def predict(self, tokens, framework=None, language=None, sampler_builder: SamplerBuilder = None,
                output_amr=False, **kwargs):
        flat = isinstance(tokens[0], (str, tuple))
        if flat:
            tokens = [tokens]
        dataset = self._dataset
        args = self.config
        model = self.model
        device = self.device
        if framework is None:
            framework = args.frameworks[-1][0]
        if language is None:
            language = args.frameworks[-1][1]
        if sampler_builder is None:
            sampler_builder = SortingSamplerBuilder(args.batch_size)
        batches = dataset.load_sentences(tokens, args, framework, language, self._tokenizer,
                                         sampler_builder=sampler_builder)
        output = batches.dataset.datasets[dataset.framework_to_id[(framework, language)]].data
        output = list(output.values())

        for batch in batches:
            # parse and postprocess
            prediction = model(Batch.to(batch, device), inference=True)[(framework, language)]
            for i, each in enumerate(prediction):
                _id: str = each['id']
                if _id.isdigit():
                    i = int(_id)
                for key, value in each.items():
                    output[i][key] = value

                # clean the output
                output[i]["input"] = output[i]["sentence"]
                output[i] = {k: v for k, v in output[i].items() if k in {"id", "input", "nodes", "edges", "tops"}}
                output[i]["framework"] = framework
                # maybe amr?
                if output_amr:
                    output[i] = mrp_to_amr(output[i])
        if flat:
            output = output[0]
        return output

    # noinspection PyMethodOverriding
    def fit(self,
            training_data,
            validation_data,
            companion_data,
            frameworks,
            save_dir,
            sampler_builder: SamplerBuilder,
            devices=None,
            logger=None,
            seed=None,
            accumulation_steps=1,
            activation='relu',
            balance_loss_weights=True,
            batch_size=32,
            beta_2=0.98,
            blank_weight=1.0,
            char_embedding=True,
            char_embedding_size=128,
            decoder_delay_steps=0,
            decoder_learning_rate=0.0006,
            decoder_weight_decay=1.2e-06,
            dropout_anchor=0.5,
            dropout_edge_label=0.5,
            dropout_edge_presence=0.5,
            dropout_edge_attribute=0.5,
            dropout_label=0.5,
            dropout_property=0.7,
            dropout_top=0.9,
            dropout_transformer=0.1,
            dropout_transformer_attention=0.1,
            dropout_word=0.1,
            encoder='xlm-roberta-base',
            encoder_delay_steps=2000,
            encoder_freeze_embedding=True,
            encoder_learning_rate=6e-05,
            encoder_weight_decay=0.01,
            epochs=100,
            focal=True,
            grad_norm_alpha=1.5,
            grad_norm_lr=0.001,
            group_ops=False,
            hidden_size_ff=3072,
            hidden_size_anchor=128,
            hidden_size_edge_label=256,
            hidden_size_edge_presence=512,
            hidden_size_edge_attribute=128,
            label_smoothing=0.1,
            layerwise_lr_decay=1.0,
            n_attention_heads=8,
            n_layers=3,
            n_mixture_components=15,
            normalize=True,
            query_length=3,
            pre_norm=True,
            warmup_steps=6000,
            n_encoder_layers=12,
            workers=0,
            patience=100,
            framework=None,
            language=None,
            output_amr=False,
            **kwargs
            ):
        trn_data = 'trn'
        dev_data = 'dev'
        return super().fit(**merge_locals_kwargs(locals(), kwargs))

    def on_config_ready(self, encoder, **kwargs):
        self._tokenizer = AutoTokenizer_.from_pretrained(encoder)

    @property
    def _savable_config(self):
        backup = copy.copy(self.config)
        for key in 'training_data', 'validation_data', 'test_data', 'companion_data':
            self.config.pop(key, None)
        save_config = super()._savable_config
        self.config = backup
        return save_config

    def save_config(self, save_dir, filename='config.json'):
        super().save_config(save_dir, filename)
        # Save other config too
        dataloader = self._dataset.state_dict()
        torch.save(dataloader, f'{save_dir}/dataloader.pt')

    def load_config(self, save_dir, filename='config.json', **kwargs):
        super().load_config(save_dir, filename, **kwargs)
        args = self.config
        self._dataset = SharedDataset(args)
        self._dataset.load_state_dict(args, torch.load(f'{save_dir}/dataloader.pt'))

    def load_vocabs(self, save_dir, filename='vocabs.json'):
        pass
