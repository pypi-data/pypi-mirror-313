# -*- coding:utf-8 -*-
# Author: hankcs
# Date: 2022-04-13 02:15
import copy
import io
from datetime import date
import pygraphviz as pgv

from perin_parser.thirdparty.mtool.graph import Graph


def to_dot(mrp: dict, anchors=False):
    mrp = copy.deepcopy(mrp)
    if not anchors:
        for n in mrp['nodes']:
            n.pop('anchors', None)
    mrp['time'] = str(date.today())
    g = Graph.decode(mrp)
    with io.StringIO() as out:
        g.dot(out)
        return out.getvalue()


def to_svg(dot):
    try:
        G = pgv.AGraph(dot)
        return G.draw(format='svg', prog='dot').decode("utf-8").strip()
    except Exception as e:
        return f'Failed due to {e}.'


def main():
    mrp = {'id': '0',
           'input': '男孩 希望 女孩 相信 他 。',
           'nodes': [{'id': 0,
                      'label': '男孩',
                      'anchors': [{'from': 0, 'to': 2}, {'from': 12, 'to': 13}]},
                     {'id': 1, 'label': '希望-01', 'anchors': [{'from': 3, 'to': 5}]},
                     {'id': 2, 'label': '女孩', 'anchors': [{'from': 6, 'to': 8}]},
                     {'id': 3, 'label': '相信-01', 'anchors': [{'from': 9, 'to': 11}]}],
           'edges': [{'source': 1, 'target': 3, 'label': 'arg1'},
                     {'source': 1, 'target': 0, 'label': 'arg0'},
                     {'source': 3, 'target': 2, 'label': 'arg0'},
                     {'source': 3, 'target': 0, 'label': 'arg1'}],
           'tops': [1],
           'framework': 'amr'}
    dot = to_dot(mrp)
    svg = to_svg(dot)
    print(svg)


if __name__ == '__main__':
    main()
