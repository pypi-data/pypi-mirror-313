from uuid import uuid4

import string


def int_to_alpha_string(n, alphabet):
    base = len(alphabet)
    alpha_str = ''
    while n:
        n, rem = divmod(n, base)
        alpha_str = alphabet[rem] + alpha_str
    return alpha_str


def hash_to_custom_alpha(value):
    # Define a custom alphabet (a-z, A-Z)
    alphabet = string.ascii_letters

    # Get the hash value (ensuring it's positive)
    hash_value = abs(hash(value))

    # Convert the hash value to a string using the custom alphabet
    alpha_hash = int_to_alpha_string(hash_value, alphabet)

    return alpha_hash


class SameNodeException(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class NodeExistsException(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class NodeNotExistsException(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class EdgeExistsException(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class Node:
    def __init__(self, label=None, shape='circle', color='black', style='filled'):
        self.label = label
        if label is None:
            self.label = uuid4()
        self.name = hash_to_custom_alpha(self.label)
        self.shape = shape
        self.color = color
        self.style = style

    def edit_node_info(self, shape, color, style):
        if shape is not None:
            self.shape = shape
        if color is not None:
            self.color = color
        if style is not None:
            self.style = style

    def __str__(self):
        return f'{self.name} [label="{self.label}", shape={self.shape}, color={self.color}, style={self.style}];'


class Edge:
    def __init__(self, fromNode: Node, toNode: Node, label='', color='black', arrowhead='diamond'):
        if fromNode.name == toNode.name:
            raise SameNodeException('fromNode and toNode is same')
        self.name = f'{fromNode.name}->{toNode.name}'
        self.fromNode = fromNode
        self.toNode = toNode
        self.label = label
        self.arrowhead = arrowhead
        self.color = color

    def __str__(self):
        return f'{self.fromNode.name} -> {self.toNode.name} [label="{self.label}", color={self.color}, arrowhead={self.arrowhead}];'


class Digraph:
    def __init__(self, name='G', rankdir='TB'):
        self.__nodes = {}  # key: node.name, value: Node
        self.__edges = {}  # key: edge.name, value: Edge
        self.name = name
        self.rankdir = rankdir

    def add_node(self, label=None, shape='circle', color='black', style='filled'):
        node = Node(label, shape, color, style)
        if node.name in self.__nodes.keys():
            raise NodeExistsException('this node already exists, failed to add node.')
        self.__nodes[node.name] = node

    def edit_node(self, label='', shape=None, color=None, style=None):
        """
        只能修改除了node_label以外的信息(name是label的哈希，同理不可变)
        """
        try:
            node = self.__nodes[hash_to_custom_alpha(label)]
        except KeyError:
            raise NodeNotExistsException('this node is not exists, failed to edit node.')
        node.edit_node_info(shape, color, style)

    def add_edge(self, from_node_label: str, to_node_label: str, label='', color='black', arrowhead='diamond'):
        node_name = from_node_label
        try:
            from_node = self.__nodes[hash_to_custom_alpha(from_node_label)]
            node_name = to_node_label
            to_node = self.__nodes[hash_to_custom_alpha(to_node_label)]
        except KeyError:
            raise NodeNotExistsException(f'node {node_name} is not exists, failed to edit node.')
        edge = Edge(from_node, to_node, label, color, arrowhead)
        if edge.name in self.__edges.keys():
            raise EdgeExistsException('this edge already exists')
        self.__edges[edge.name] = edge

    def __str__(self):
        lines = [f'digraph {self.name} ' + '{', f'graph [rankdir={self.rankdir}];', '// 定义节点']
        lines.extend([str(node) for node in self.__nodes.values()])
        lines.append('// 定义边')
        lines.extend([str(edge) for edge in self.__edges.values()])
        lines.append('}')
        return '\n'.join(lines)
