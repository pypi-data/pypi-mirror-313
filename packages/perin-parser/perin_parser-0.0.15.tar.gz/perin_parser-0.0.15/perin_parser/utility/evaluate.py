#!/usr/bin/env python3
# conding=utf-8
#
# Copyright 2020 Institute of Formal and Applied Linguistics, Faculty of
# Mathematics and Physics, Charles University, Czech Republic.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import json
import multiprocessing as mp

import perin_parser.thirdparty.mtool.main
import perin_parser.thirdparty.mtool.score.mces
from hanlp.metrics.metric import Metric


def parse_arguments():
    parser = argparse.ArgumentParser(description="Hyperparameters")
    parser.add_argument("--epoch", type=int, default=0, help="Epoch.")
    parser.add_argument("--framework", type=str, default="", help="Framework.")
    parser.add_argument("--language", type=str, default="", help="Language.")
    parser.add_argument("--input_dir", type=str, default="", help="Path to the run directory.")
    parser.add_argument("--gold_file", type=str, default="", help="Path to the gold file.")
    return parser.parse_args()


def evaluate(input_dir, framework, language, gold_file):
    normalize = {"anchors", "case", "edges", "attributes"}
    cores = mp.cpu_count()

    with open(f"{input_dir}/prediction_{framework}_{language}.json", encoding="utf8") as f:
        graphs, _ = perin_parser.thirdparty.mtool.main.read_graphs(f, format="mrp", frameworks=[framework], normalize=normalize)
        for graph in graphs:
            graph._language = None

    with open(gold_file, encoding="utf8") as f:
        gold_graphs, _ = perin_parser.thirdparty.mtool.main.read_graphs(f, format="mrp", frameworks=[framework], normalize=normalize)
        for graph in gold_graphs:
            graph._language = None

    limits = {"rrhc": 2, "mces": 50000}
    result = perin_parser.thirdparty.mtool.score.mces.evaluate(gold_graphs, graphs, limits=limits, cores=cores)

    with open(f"{input_dir}/full_results_{framework}_{language}.json", mode="w") as f:
        json.dump(result, f)

    result = {
        f"tops": result["tops"]["f"],
        f"anchors": result["anchors"]["f"],
        f"labels": result["labels"]["f"],
        f"properties": result["properties"]["f"],
        f"edges": result["edges"]["f"],
        f"attributes": result["attributes"]["f"],
        f"all": result["all"]["f"],
    }

    # with open(f"{input_dir}/results_{framework}_{language}.json", mode="w") as f:
    #     json.dump(result, f)
    return result


class F1(Metric):
    def __init__(self, f) -> None:
        super().__init__()
        self.f = f

    @property
    def score(self):
        return self.f

    def __call__(self, pred, gold):
        raise NotImplementedError()

    def reset(self):
        self.f = 0

    def __repr__(self) -> str:
        return f"F1: {self.f:.2%}"


if __name__ == "__main__":
    args = parse_arguments()
    evaluate(args.input_dir, args.framework, args.language, args.gold_file)
