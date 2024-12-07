# -*- coding:utf-8 -*-
# Author: hankcs
# Date: 2022-04-10 18:44
import json
from collections import defaultdict

import torch
from hanlp_common.constant import NULL
from transformers import PreTrainedTokenizer

from perin_parser import utility as utils
from data import AMRParser
from data import EDSParser
from hanlp.common.dataset import TransformableDataset
from perin_parser.utility.bert_tokenizer import bert_tokenizer


class AbstractMeaningRepresentationDataset(TransformableDataset):

    def load_file(self, filepath: str):
        data = {}
        with open(filepath, encoding="utf8") as reader:
            for line in reader:
                sentence = json.loads(line)
                data[sentence["id"]] = sentence

        node_counter, edge_counter, no_edge_counter = 0, 0, 0

        for node, sentence in utils.node_generator(data):
            node_counter += 1
            node["properties"] = {"transformed": int("property" in node)}

        utils.create_aligned_rules(data, constrained_anchors=False)
        rule_counter = utils.count_rules(data, 0.1)

        # utils.create_bert_tokens(data, args.encoder)
        utils.assign_labels_as_best_rules(data, rule_counter)
        utils.create_edge_permutations(data, AMRParser.node_similarity_key)

        # create edge vectors

        for sentence in data.values():
            N = len(sentence["nodes"])

            edge_count = utils.create_edges(sentence, attributes=False, normalize=True)
            edge_counter += edge_count
            no_edge_counter += N * (N - 1) - edge_count

            sentence["anchor edges"] = [N, len(sentence["input"]), []]
            sentence["id"] = [sentence["id"]]
            sentence["top"] = sentence["tops"][0]
            sentence["token anchors"] = [[]]

        anchor_freq = 0.0
        input_count = sum(len(sentence["input"]) for sentence in data.values())
        for each in data.values():
            yield each


class ElementaryDependencyStructures(TransformableDataset):
    def load_file(self, filepath: str):
        data = {}
        with open(filepath, encoding="utf8") as reader:
            for line in reader:
                sentence = json.loads(line)
                data[sentence["id"]] = sentence

                if all(x == '_' for x in sentence['lemmas']):
                    sentence["lemmas"] = sentence["input"]

        node_counter, edge_counter, no_edge_counter = 0, 0, 0
        anchor_count, n_node_token_pairs = 0, 0

        for node, sentence in utils.node_generator(data):
            node_counter += 1
            node["properties"] = {"transformed": int("property" in node)}
            # assert len(node["anchors"]) > 0

        utils.create_aligned_rules(data, constrained_anchors=True)
        rule_counter = utils.count_rules(data, 0.1)

        utils.assign_labels_as_best_rules(data, rule_counter)
        utils.create_edge_permutations(data, EDSParser.node_similarity_key)

        # create edge vectors
        for sentence in data.values():
            N = len(sentence["nodes"])

            edge_count = utils.create_edges(sentence, attributes=False, normalize=True)
            edge_counter += edge_count
            no_edge_counter += N * (N - 1) - edge_count

            sentence["anchor edges"] = [N, len(sentence["input"]), []]
            for i, node in enumerate(sentence["nodes"]):
                for anchor in node["anchors"]:
                    sentence["anchor edges"][-1].append((i, anchor))

                anchor_count += len(node["anchors"])
                n_node_token_pairs += len(sentence["input"])

            sentence["id"] = [sentence["id"]]
            sentence["top"] = sentence["tops"][0]

        for each in data.values():
            yield each


class ToChar(object):
    def __init__(self, src, dst='char') -> None:
        if dst is None:
            dst = src
        self.src = src
        self.dst = dst

    def __call__(self, sample: dict) -> dict:
        src = sample[self.src]
        if isinstance(src, str):
            sample[self.dst] = self.to_chars(src)
        elif isinstance(src, list):
            sample[self.dst] = [self.to_chars(x) for x in src]
        return sample

    def to_chars(self, word: str):
        return [c for i, c in enumerate(word) if i < 10 or len(word) - i <= 10]


def transformer_tokenize(sentence, tokenizer: PreTrainedTokenizer):
    to_scatter, bert_input = bert_tokenizer(sentence, tokenizer, tokenizer.name_or_path)
    sentence["scatter_id"] = to_scatter
    sentence["subtoken_id"] = bert_input
    return sentence


def edge_permutation(sentence, device=None):
    example = sentence["edge permutations"]
    permutations = torch.LongTensor(example["permutations"], device=device)
    masks = generate_mask(len(example["permutations"][0]), example["greedy"], device)
    greedies = [torch.LongTensor(p, device=device) for p in example["greedy"]]

    sentence['edge_permutations'] = permutations, masks, greedies
    return sentence


def generate_mask(length, greedy, device):
    mask = torch.zeros(length, dtype=torch.bool, device=device)
    for g in greedy:
        mask[g] = True
    return mask


def unpack_relative_labels(sentence):
    nodes = sentence['nodes']
    example = [n["possible rules"] for n in nodes]
    n_nodes, n_tokens = len(example), example[0][0]
    tensor = []
    for i_word, word in enumerate(example):
        row = [NULL] * n_tokens
        for anchor, count, rule in word[1]:
            row[anchor] = rule  # TODO: they use rule + 1
        tensor.append(row)
    sentence['relative_labels'] = tensor
    return sentence


def unpack_edge_labels(sentence):
    m, n, edges = sentence['edge labels']
    tensor = [[NULL] * n for _ in range(m)]
    for u, v, w in edges:
        tensor[u][v] = w
    sentence['edge_labels'] = tensor
    return sentence


def create_property(sentence):
    properties = defaultdict(list)
    for node in sentence['nodes']:
        for k, v in node['properties'].items():
            properties[k].append(v)
    sentence.update(properties)
    return sentence


def edge_field(sentence, name='edge presence'):
    m, n, edges = sentence[name]
    mat = torch.zeros((m, n), dtype=torch.long)
    for u, v, w in edges:
        mat[u, v] = w
    sentence[name.replace(' ', '_')] = mat
    return sentence


def anchor_edges(sentence):
    m, n, anchor = sentence["anchor edges"]
    tensor = torch.zeros(m, n, dtype=torch.long)
    for u, v in anchor:
        tensor[u, v] = 1
    mask = tensor.sum(-1) == 0
    sentence['anchor'] = anchor
    sentence['anchor_mask'] = mask
    return sentence


def mark_dataset_framework(sentence, framework, language):
    sentence['framework'] = ' '.join([framework, language])
    return sentence

# def create_relative_labels_tensor(sentence, label_smoothing=0.1):
#     nodes = sentence['nodes']
#     example = [n["possible rules"] for n in nodes]
#     n_nodes, n_tokens = len(example), example[0][0]
#     relative_labels_id = sentence['relative_labels_id']
#     tensor = torch.full([n_nodes, n_tokens], dtype=torch.long)
#     return sentence
