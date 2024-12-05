import os
from json import dump

from .CodeAnalyzer import CodeAnalyzer
from ..file_manager import FileManager
from ..graph_dot import Digraph, NodeExistsException, generate_dot_file_by_dot_data, generate_png_from_dot_data, \
    get_dot_data, generate_pos_from_dot_data, EdgeExistsException


def get_modules(module_parent_dir: str) -> list[str]:
    """
    Return a list of module's name under the given parent directory.
    :param module_parent_dir: The parent directory of modules.
    """
    abs_analysis_dir = os.path.abspath(module_parent_dir)
    os.makedirs(abs_analysis_dir, exist_ok=True)
    # 过滤pytest文件，只保留py文件，且不是__init__这种配置py文件
    return [i for i in os.listdir(abs_analysis_dir) if '.py' in i and 'pytest' not in i and '__' not in i]


# 这个导包的方式容易报导包的问题，解决太麻烦了，就不用了
# import inspect
# from types import ModuleType
# def analyze_module_through_import_module(module_path: str, module_name: str) -> {str: list[str]}:
#     """
#     Analyze the module, get module's imported modules, functions, classes and global variables.
#     :param module_path: The path of the module, such as '/path/to/your/module/your_module.py'.
#     :param module_name: The name of the module, such as 'your_module'.
#     """
#     # import module
#     print(os.path.abspath(module_path))
#     with FileManager(os.path.abspath(module_path), 'r', encoding='utf-8') as f:
#         module_code = f.read()
#     module = ModuleType(module_name)
#     exec(module_code, module.__dict__)
#
#     # 获取模块中导入的模块、全局变量、函数、类
#     imported_modules = set()
#     functions = []
#     classes = []
#     global_vars = []
#     for name, obj in inspect.getmembers(module):
#         if inspect.ismodule(obj):
#             imported_modules.add(obj.__name__)
#         elif inspect.isfunction(obj):
#             functions.append(name)
#         elif inspect.isclass(obj):
#             classes.append(name)
#         elif not (name.startswith('__') and name.endswith('__')):  # Exclude built-in attributes
#             global_vars.append(name)
#
#     return {'imported_modules': imported_modules, 'functions': functions, 'classes': classes,
#             'global_vars': global_vars}


def analyze_module_through_module_code(module_path: str, ignore_standard_modules: bool = True) -> {str: list[str]}:
    """
    Analyze the module, get module's imported modules, functions, classes and global variables.
    :param module_path: The path of the module, such as '/path/to/your/module/your_module.py'.
    :param ignore_standard_modules: 是否忽略标准库模块
    """
    # read module code and analyze it
    with FileManager(os.path.abspath(module_path), 'r', encoding='utf-8') as f:
        code_line_generator = (line for line in f.readlines())
        code_analyzer = CodeAnalyzer(code_line_generator)
        try:
            module_data = code_analyzer.analyze(ignore_standard_modules)
        except Exception as e:
            print(e)
    return module_data


def analyze_modules(analysis_dir: str, ignore_standard_modules: bool = True) -> {str: dict}:
    """
    分析目录下所有模块的信息(导入的包、函数、类、全局变量)
    :param analysis_dir: The analysis directory, the parent directory of modules
    :param ignore_standard_modules: 是否忽略标准库模块
    """
    # 根据目录列举所有对应目录下的所有py文件名的list
    modules = get_modules(analysis_dir)
    data = {}
    # 所有的module
    for module in modules:
        module_name = module.split('.')[0]
        # 分析py文件(get_modules分析过路径analysis_dir的有效性了，函数内部不重复了)
        module_data = analyze_module_through_module_code(os.path.join(analysis_dir, module), ignore_standard_modules)
        data[module_name] = module_data
    return data


def get_modules_relationship_digraph(modules_data: dict) -> Digraph:
    """
    Get the relationship between modules throughout the modules_data
    :param modules_data: the info of all the modules, including the imported modules, functions, classes and global_vars
    :return: the relationship graph
    """
    g = Digraph()
    modules = modules_data.keys()
    for module_name, module_data in modules_data.items():
        # 分析过程中，py文件的节点加入，若加入过了捕捉重复异常不进行操作
        try:
            g.add_node(module_name, color='red')
        except NodeExistsException:
            pass  # 因为后续会判断toNode是否是module，会添加为红色节点，就不需要再修改节点的颜色为红色了
        # 将当前模块导入的包都加入节点，并添加边
        imported_modules = module_data['imported_modules']
        for imported_module in imported_modules:
            # 这里获取imported_module的主包或模块，一是将导入的包压缩到主包或唯一的模块，二是用于区分module和第三方库或标准库
            fp = imported_module.split('.')[0]  # 主包或唯一的模块（这里不考虑相对导入方式，所以直接.分割取第一个）
            if fp in modules:  # 如果当前导入包是属于modules中的，那加点需要是红色
                color = 'red'
            else:  # 反之，就是第三方库或标准库（如果没有忽略的话）
                color = 'blue'
            # 尝试加点和加边，若存在了就无事发生. 两个都会抛出异常不能放一个try中
            try:
                g.add_node(fp, color=color)
            except NodeExistsException:
                pass
            try:
                g.add_edge(module_name, fp)
            except EdgeExistsException:
                pass
    return g


def analyze_module_imports(analysis_dir: str, output_dot_path: str, output_json_path: str = None,
                           output_png_path: str = None, output_pos_path: str = None,
                           ignore_standard_modules: bool = True) -> None:
    """
    分析模块的依赖关系。同时可以通过传入对应文件输出路径，选择输出模块的其他信息（包含的类、函数、全局变量）。
    :param analysis_dir: 需要分析模块的父目录
    :param output_dot_path: 输出的模块依赖关系信息，通过dot的方式（必填）
    :param output_json_path: 输出模块的其他信息（选填）
    :param output_png_path: 输出dot文件对应的关系图（选填）
    :param output_pos_path: pos格式文件对应的关系图（选填）
    :param ignore_standard_modules: 是否忽略标准库模块
    """
    # 分析目录下所有模块的信息(导入的包、函数、类、全局变量)
    modules_data = analyze_modules(analysis_dir, ignore_standard_modules)
    g = get_modules_relationship_digraph(modules_data)
    dot_data = get_dot_data(g)

    # 将模组的关系写到dot文件中
    generate_dot_file_by_dot_data(dot_data, output_dot_path)

    if output_json_path is not None:  # 将模组信息都写入json文件中
        with FileManager(output_json_path, 'w') as f:
            dump(modules_data, f)

    if output_png_path is not None:  # 将模组的关系从dot数据变为png图片
        generate_png_from_dot_data(dot_data, output_png_path)

    if output_pos_path is not None:  # 将模组的关系从dot数据变为pos格式（思维导图格式）
        generate_pos_from_dot_data(dot_data, output_pos_path)
