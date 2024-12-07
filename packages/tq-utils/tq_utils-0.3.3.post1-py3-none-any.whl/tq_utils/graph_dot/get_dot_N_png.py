import pydot
import pygraphviz as pgv

from .Model import Digraph
from ..file_manager import FileManager

# 使用 pydot 渲染图

ENCODING = 'utf-8'


def get_dot_data(g: Digraph):
    return '# Written by TQUtils.AMR\n' + str(g)


def generate_dot_file_by_digraph(g: Digraph, dot_path: str = 'graph.dot'):
    with FileManager(dot_path, 'w', encoding=ENCODING) as f:
        f.write(get_dot_data(g))


def generate_dot_file_by_dot_data(dot_data: str, dot_path: str = 'graph.dot'):
    with FileManager(dot_path, 'w', encoding=ENCODING) as f:
        f.write(dot_data)


def generate_png_from_dot_data(s: str, png_path: str = 'graph.png'):
    graphs = pydot.graph_from_dot_data(s)
    first_graph = graphs[0]
    first_graph.write_png(png_path)


def generate_png_from_dot_file(dot_file_path: str, png_path: str = 'graph.png'):
    graphs = pydot.graph_from_dot_file(dot_file_path, encoding=ENCODING)
    print(graphs)
    first_graph = graphs[0]
    first_graph.write_png(png_path)


"""
pos 格式不对，WPS 用不了，白瞎
"""


def parse_dot_to_pos(graph):
    # 定义一个递归函数来遍历图结构并生成 POS 格式
    def traverse(node, level, visited):  # 递归函数，从根节点开始遍历图的结构，并生成POS格式的内容
        if node in visited:
            return
        visited.add(node)
        pos_lines.append(f"{'  ' * level}{node}")
        for successor in graph.successors(node):
            traverse(successor, level + 1, visited)

    # 通过检查入边数为零的节点，找到图的根节点
    roots = [node for node in graph.nodes() if graph.in_degree(node) == 0]
    pos_lines = []
    visited_nodes = set()
    for root in roots:  # 从根节点开始递归遍历，并生成 POS 格式的字符串，包含合适的缩进表示层次结构
        traverse(root, 0, visited_nodes)
    return "\n".join(pos_lines)


def generate_pos_from_dot_data(dot_data: str, output_pos_path: str = 'graph.pos'):
    graph = pgv.AGraph(string=dot_data)  # 读取dot字符串数据，并解析内容为图
    pos_content = parse_dot_to_pos(graph)
    # 导出 POS 内容到文件
    with FileManager(output_pos_path, "w") as f:
        f.write(pos_content)


def generate_pos_from_dot_file(dot_file_path: str, output_pos_path: str = 'graph.pos'):
    graph = pgv.AGraph(dot_file_path)  # 读取dot文件，并解析内容为图
    pos_content = parse_dot_to_pos(graph)
    # 导出 POS 内容到文件
    with FileManager(output_pos_path, "w") as f:
        f.write(pos_content)
