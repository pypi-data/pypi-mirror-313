# -*- coding: UTF-8 -*-
# Copyright©2022 xiangyuejia@qq.com All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

"""
from typing import Dict, Union, List, Any, NoReturn, Tuple, Iterator


class Node:
    # 使用本包的函数时，节点的数据格式应继承本类
    def __init__(self, name, children=None):
        self.name = name
        if children:
            self.children = children
        else:
            self.children = []

    def get_children(self):
        return self.children

    def has_children(self):
        if len(self.children) > 0:
            return True
        return False


def _is_leaf(node: Node):
    if node.has_children():
        return False
    return True


def _get_names(nodes):
    rst = [n.name for n in nodes]
    return rst


def dfs(node, target=_is_leaf, action=_get_names, revisit=False, visited=None, track=None) -> Iterator:
    if visited is None:
        visited = set()
    if track is None:
        track = []
    if (not revisit) and (node in visited):
        return
    visited.add(node)
    track.append(node)

    if target(node):
        yield action(track)

    for next_node in node.get_children():
        yield from dfs(next_node, target, action, revisit, visited, track.copy())


def ranked_permutation(ranked_list: List[List[Any]]) -> List[List[Any]]:
    # 输入数组[[1,2],[3,4,5]]
    # 输出有序的全排列：[[1,3],[1,4],[1,5],[2,3],[2,4],[2,5]]
    ranked_list = [['root_node']] + ranked_list
    ranked_nodes = []
    for i in range(len(ranked_list)):
        level_nodes = []
        for j, v in enumerate(ranked_list[i]):
            level_nodes.append(Node(v))
        ranked_nodes.append(level_nodes)
    for i in range(len(ranked_nodes) - 1):
        for n in ranked_nodes[i]:
            n.children = ranked_nodes[i + 1]
    rst = [_[1:] for _ in list(dfs(ranked_nodes[0][0], revisit=True))]
    return rst


if __name__ == '__main__':
    d = Node('d')
    e = Node('e')
    c = Node('c', [d, e])
    b = Node('b')
    a = Node('a', [b, c])
    for t in dfs(a):
        print(t)

    print(ranked_permutation([[1, 2], ['a', 'b'], [1.5, 2.5]]))
