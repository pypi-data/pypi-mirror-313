#!/usr/bin/env python3
# conding=utf-8
#
# Copyright 2020 Institute of Formal and Applied Linguistics, Faculty of
# Mathematics and Physics, Charles University, Czech Republic.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from perin_parser.utility import parser_utils as utils
from perin_parser.data.parser.from_mrp.abstract_parser import AbstractParser


class RequestParser(AbstractParser):
    def __init__(self, sentences, args, language: str, fields, tokenizer):

        self.data = {i: {"id": i, "sentence": sentence} for i, sentence in enumerate(sentences)}

        for i, sentence in enumerate(sentences):
            if isinstance(sentence[0], str):
                tokens = lemmas = sentence
            else:
                tokens = [x[0] for x in sentence]
                lemmas = [x[1] for x in sentence]
            example = {"id": str(i), "sentence": ' '.join(tokens), 'input': tokens, 'lemmas': lemmas}
            utils.create_token_anchors(example)
            example["token anchors"] = [[a["from"], a["to"]] for a in example["token anchors"]]
            self.data[i] = example

        utils.create_bert_tokens(self.data, tokenizer)
        super(RequestParser, self).__init__(fields, self.data)
