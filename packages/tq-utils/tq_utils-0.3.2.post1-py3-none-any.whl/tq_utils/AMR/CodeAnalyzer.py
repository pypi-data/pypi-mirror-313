from collections.abc import Generator


# TODO 后续可以考虑用 AST，抽象语法树进行代码分析; 或者还是使用导入模块的方式，使用解释器进行解析得了
class CodeAnalyzer:
    def __init__(self, line_generator: Generator):
        """
        通过代码行的生成器，分析代码块。
        for now: 不能辨析代码的正确与否，所以得保证代码没有错误，同时需要
        :param line_generator: 代码行的生成器
        """
        self.line_generator = line_generator

    def is_line_continuation(self, line: str) -> bool:
        line = line.strip()
        if line.endswith('\\'):
            return True
        return False

    def is_comment(self, line: str) -> bool:
        """
        判断当前行是否是注释。优先于其他判断is_comment.
        如果是单行注释直接返回True。如果是多行注释开头，则将生成器next到多行注释结尾，再返回True。其余情况返回False。
        :param line: 当前分析的代码行
        """
        line = line.strip()
        if line.startswith('#'):
            # 如果是单行注释直接返回True
            return True
        # 如果不是多行注释的开头，那就直接返回False
        if not line.startswith("'''") and not line.startswith('"""'):
            return False
        elif line.startswith("'''"):
            multi_comment_sign = "'''"
        else:
            multi_comment_sign = '"""'
        # 根据多行注释的符号，当找到代码行以它为结尾则跳出循环
        for line in self.line_generator:
            # print(line.rstrip())
            if line.strip().endswith(multi_comment_sign):
                break
        return True

    def is_import(self, line: str) -> bool:
        """
        判断当前行是否是导包(包含import关键字)。
        后于判断is_comment，就不用考虑注释的内容了.
        :param line: 当前分析的代码行
        """
        if 'import ' in line:
            return True
        return False

    def is_function(self, line) -> bool:
        """
        判断当前行是否是函数('def '开头)。
        后于判断is_comment，就不用考虑注释的内容了.
        :param line: 当前分析的代码行
        """
        if not line.startswith('def '):
            return False  # 如果不是def打头，那就不是函数定义，都为False
        # 需要直接跳过类的内部定义内容，根据标准的Python格式，函数定义完成最后会有空行分隔，以其为结尾则跳出循环
        for line in self.line_generator:
            # print(line.rstrip())
            if line.strip() == '':
                break
        return True

    def is_class(self, line) -> bool:
        """
        判断当前行是否是类('class '开头)。
        后于判断is_comment，就不用考虑注释的内容了.
        :param line: 当前分析的代码行
        """
        if not line.startswith('class '):
            return False  # 如果不是class打头，那就不是类定义，都为False
        # 需要直接跳过类的内部定义内容，根据标准的Python格式，类定义完成最后会有空行分隔，以其为结尾则跳出循环
        for line in self.line_generator:
            # print(line.rstrip())
            if line.strip() == '':
                break
        return True

    def is_global_variable(self, line) -> bool:
        """
        判断当前行是否是全局变量(不是空行 and 没有缩进 and 不是类/函数/包)。
        后于判断is_comment/is_import/is_function/is_class.(所以这里class、import、comment、function就不用再过滤了)
        :param line: 当前分析的代码行
        """
        if '=' not in line:
            return False  # 全局变量必定需要通过赋值进行定义，直接大筛一遍没有'='的(else/空行/...)
        elif line.startswith('\t') or line.startswith(' '):
            return False  # 若为函数、类等内部代码，返回False
            # 就剩下全局的一些语句，包括：assert语句、del、if、elif、except try、for、finally、lambda、raise、while with
        elif line.startswith('assert ') or line.startswith('assert('):
            return False
        elif line.startswith('del ') or line.startswith('del('):
            return False
        elif line.startswith('if ') or line.startswith('if(') or line.startswith('elif ') or line.startswith('elif('):
            return False
        elif line.startswith('try ') or line.startswith('try:'):
            return False
        elif line.startswith('except ') or line.startswith('except:') or line.startswith('except('):
            return False
        elif line.startswith('finally:') or line.startswith('finally '):
            return False
        elif line.startswith('lambda '):
            return False
        elif line.startswith('while ') or line.startswith('while('):
            return False
        elif line.startswith('for ') or line.startswith('for('):
            return False
        elif line.startswith('with ') or line.startswith('with('):
            return False
        elif line.startswith('raise ') or line.startswith('raise('):
            return False
        # 区分各种赋值数据类型，多行导致的问题。格式规范，一般是首行(/{/[结尾，然后进行了分行，随后)/}/]最后单独一行。那我就按这个规则分下
        last_c = line.strip()[-1]
        index = last_c.find('({[')
        if index != -1:
            p = ')}]'[index]
            for line in self.line_generator:
                if line.startswith(p):
                    break
        return True

    def line_join(self, line: str) -> str:
        line = line.strip()[:-1]  # 使用函数之前判断过line是续行，所以strip后取到最后一位之前
        # 如果使用了\，进行多行分割，要将多行进行合并
        for l in self.line_generator:
            l = l.strip()
            if not l.endswith('\\'):
                line += l  # 没有续行符了，即最后一行，直接加上
            else:
                line += l[:-1]  # 添加续行，去除最后一位续行符
        return line

    def analyze(self, ignore_standard_modules: bool = True) -> {str: list[str]}:
        """
        获取模块中导入的模块、全局变量、函数、类
        :param ignore_standard_modules: 是否忽略标准库模块
        """
        imported_modules = set()  # set存放去重
        functions = []
        classes = []
        global_vars = []
        for line in self.line_generator:
            # 逻辑判断顺序(一定要遵守)，空行过滤->注释过滤->续行合并->import/function/class -> global variable
            if line.strip() == '':  # 若为空行跳过
                continue
            elif self.is_comment(line):
                # 如果是注释（单行和多行）则跳过
                continue

            if self.is_line_continuation(line):
                # 如果是续航，需要对续行进行合并
                line = self.line_join(line)

            if self.is_import(line):  # line包含import关键字
                prefix = ''  # 如果有from，需要将from的内容连上，prefix就是存这个的
                import_index = line.find('import ')
                if 'from ' in line:  # 截取from-import之间的包
                    prefix = line[len('from '):import_index].strip() + '.'
                # 截取import之后部分(strip过了直接取到最后)，根据都逗号分割
                imports = line[import_index + len('import '):].split(',')
                for item in imports:
                    as_index = item.find('as ')
                    # 如果存在as关键字取别名(会再strip直接从头取)，那么就取原名
                    package_name = prefix + item.strip() if as_index == -1 else prefix + item[:as_index].strip()
                    if ignore_standard_modules and package_name in PYTHON311_STANDARD_MODULES:
                        break  # 如果启用忽略标准库模块并且就是标准库模块，则直接跳过
                    imported_modules.add(package_name)
            elif self.is_function(line):  # 'def '开头
                # 因为'def '开头，根据规范def和(之间实际内容仅有函数名。取就完事儿了
                def_index = line.find('def ')
                bracket_index = line.find('(')
                functions.append(line[def_index + len('def '): bracket_index].strip())
            elif self.is_class(line):  # 'class '开头
                # 因为'class '开头，根据规范class和:之间可能会有用于继承的(。有就到(为止截取，反之到:。
                line = line.strip()
                class_index = line.find('class ')
                bracket_index = line.find('(')
                if bracket_index == -1:
                    classes.append(line[class_index + len('class '): -1].strip())
                else:
                    classes.append(line[class_index + len('class '): bracket_index].strip())
            elif self.is_global_variable(line):  # 不是空行 and 没有缩进 and 不是类/函数/包
                # 无缩进==顶格，全局变量的定义就是赋值一块的，那就根据=截取完事儿
                equal_index = line.find('=')
                global_vars.append(line[:equal_index].strip())
        return {'imported_modules': list(imported_modules), 'functions': functions, 'classes': classes,
                'global_vars': global_vars}


PYTHON311_STANDARD_MODULES = [
    'abc',
    'argparse',
    'array',
    'ast',
    'asynchat',
    'asyncio',
    'atexit',
    'base64',
    'binascii',
    'binhex',
    'bisect',
    'bz2',
    'calendar',
    'cgi',
    'cgitb',
    'chunk',
    'collections',
    'colorsys',
    'compileall',
    'concurrent',
    'configparser',
    'contextlib',
    'copy',
    'copyreg',
    'crypt',
    'csv',
    'ctypes',
    'curses',
    'dataclasses',
    'datetime',
    'dbm',
    'decimal',
    'difflib',
    'dis',
    'distutils',
    'doctest',
    'email',
    'encodings',
    'enum',
    'errno',
    'exceptions',
    'filecmp',
    'fileinput',
    'fnmatch',
    'fractions',
    'ftplib',
    'functools',
    'gc',
    'getopt',
    'getpass',
    'gettext',
    'glob',
    'gzip',
    'hashlib',
    'heapq',
    'http',
    'imaplib',
    'importlib',
    'inspect',
    'io',
    'ipaddress',
    'itertools',
    'json',
    'keyword',
    'linecache',
    'locale',
    'logging',
    'lzma',
    'mailbox',
    'mailcap',
    'marshal',
    'math',
    'mmap',
    'modulefinder',
    'multiprocessing',
    'netrc',
    'nntplib',
    'numbers',
    'opcode',
    'operator',
    'optparse',
    'os',
    'pathlib',
    'pdb',
    'pickle',
    'pickletools',
    'pipe',
    'platform',
    'plistlib',
    'poplib',
    'pprint',
    'profile',
    'pstats',
    'pty',
    'pwd',
    'pyclbr',
    'pydoc',
    'queue',
    'quopri',
    'random',
    're',
    'readline',
    'reprlib',
    'rpc',
    'sched',
    'secrets',
    'select',
    'shelve',
    'shlex',
    'shutil',
    'signal',
    'site',
    'smtpd',
    'smtplib',
    'socket',
    'socketserver',
    'sqlite3',
    'ssl',
    'stat',
    'string',
    'stringprep',
    'struct',
    'subprocess',
    'sunau',
    'sys',
    'sysconfig',
    'tabnanny',
    'tarfile',
    'telnetlib',
    'tempfile',
    'textwrap',
    'threading',
    'time',
    'timeit',
    'tkinter',
    'token',
    'tokenize',
    'trace',
    'traceback',
    'tracemalloc',
    'typing',
    'unittest',
    'urllib',
    'uuid',
    'venv',
    'warnings',
    'wave',
    'weakref',
    'webbrowser',
    'winreg',
    'wsgiref',
    'xml',
    'xmlrpc',
    'zipfile',
    'zlib'
]
