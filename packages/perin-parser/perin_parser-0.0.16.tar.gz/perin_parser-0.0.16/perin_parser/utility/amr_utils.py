# -*- coding:utf-8 -*-
# Author: hankcs
# Date: 2022-04-12 18:43
from collections import Counter, defaultdict
import string

from hanlp.components.amr.seq2seq.dataset.penman import AMRGraph
from perin_parser.utility.scc import strongly_connected_components_iterative


def mrp_to_amr(mrp: dict, keep_meta=()):
    # Check connectivity
    vertices = list(range(len(mrp['nodes'])))
    edges = defaultdict(set)
    for e in mrp['edges']:
        u = int(e['source'])
        v = int(e['target'])
        edges[u].add(v)
        edges[v].add(u)
    scc = max(strongly_connected_components_iterative(vertices, edges), key=len)

    triples = []
    vocab = Counter()
    node_to_name = dict()
    for node in mrp['nodes']:
        nid = int(node['id'])
        if nid not in scc:
            continue
        label: str = node['label']
        name = label[0] if label else label
        if name not in string.ascii_letters:
            name = 'x'
        vocab[name] += 1
        name += str(vocab[name])
        triples.append((name, ':instance', label))
        node_to_name[int(node['id'])] = name
    for e in mrp['edges']:
        if int(e['source']) not in scc or int(e['target']) not in scc:
            continue
        triples.append((node_to_name[e['source']], e['label'], node_to_name[e['target']]))
    meta = {'id': mrp['id']}
    for k in list(meta.keys()):
        if k not in keep_meta:
            meta.pop(k)
    top = node_to_name[mrp['tops'][0]] if mrp['tops'][0] in node_to_name else None
    return AMRGraph(triples=triples, top=top, metadata=meta)


def main():
    mrp = {'id': '0', 'input': '男孩 希望 女孩 相信 他 。',
           'nodes': [{'id': 0, 'label': '男孩', 'anchors': [{'from': 0, 'to': 2}, {'from': 12, 'to': 13}]},
                     {'id': 1, 'label': '希望-01', 'anchors': [{'from': 3, 'to': 5}]},
                     {'id': 2, 'label': '女孩', 'anchors': [{'from': 6, 'to': 8}]},
                     {'id': 3, 'label': '相信-01', 'anchors': [{'from': 9, 'to': 11}]}],
           'edges': [{'source': 1, 'target': 3, 'label': 'arg1'}, {'source': 1, 'target': 0, 'label': 'arg0'},
                     {'source': 3, 'target': 2, 'label': 'arg0'}, {'source': 3, 'target': 0, 'label': 'arg1'}],
           'tops': [1], 'framework': 'amr'}
    print(mrp_to_amr(mrp))


if __name__ == '__main__':
    main()
