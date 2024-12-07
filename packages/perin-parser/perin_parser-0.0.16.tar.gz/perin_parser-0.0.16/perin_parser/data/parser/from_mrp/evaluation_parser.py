#!/usr/bin/env python3
# conding=utf-8
#
# Copyright 2020 Institute of Formal and Applied Linguistics, Faculty of
# Mathematics and Physics, Charles University, Czech Republic.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import json
import os

from perin_parser.utility import parser_utils as utils
from perin_parser.data.parser.from_mrp.abstract_parser import AbstractParser


class EvaluationParser(AbstractParser):
    def __init__(self, args, framework: str, language: str, fields, tokenizer):
        path = args.test_data[(framework, language)]
        cache_path = f"{path}_cache"
        if not os.path.exists(cache_path):
            self.data = utils.load_dataset(path, framework=framework, language=language)

            utils.add_companion(self.data, args.companion_data[(framework, language)], language)
            utils.tokenize(self.data, mode="aggressive")

            for sentence in self.data.values():
                sentence["token anchors"] = [[a["from"], a["to"]] for a in sentence["token anchors"]]

            with open(cache_path, 'w') as out:
                json.dump(self.data, out, ensure_ascii=False)
        else:
            with open(cache_path) as src:
                self.data = json.load(src)

        utils.create_bert_tokens(self.data, tokenizer)
        super(EvaluationParser, self).__init__(fields, self.data)
