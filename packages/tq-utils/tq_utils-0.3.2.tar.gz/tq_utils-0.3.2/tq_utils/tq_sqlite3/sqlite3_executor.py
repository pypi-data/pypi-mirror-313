import sqlite3
from abc import abstractmethod
from typing import Optional


class Sqlite3Template:
    def __init__(self, db_file):
        self.db_file = db_file
        self._last_result: Optional[dict] = None
        self.__conn: Optional[sqlite3.Connection] = None

    def __connect(self):
        """
        创建数据库链接，db_file(数据库名称)在创建对象时传入
        """
        self.__conn = sqlite3.connect(self.db_file)  # 如果db文件不存在，connect函数将创建不存在的db文件
        self.__conn.row_factory = sqlite3.Row

    def do_operate(self, query_statement):
        """
        :param query_statement: SQL 语句
        e.g.
        do_operate('CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, name VARCHAR(100) NOT NULL );')
        do_operate('INSERT INTO users VALUES (2, "Tommy")')
        """
        cursor = None
        try:
            self.__connect()
            cursor = self.__conn.execute(query_statement)
            self._last_result = {'rowcount': cursor.rowcount, 'fetchall': cursor.fetchall()}
            self.__conn.commit()
        finally:
            if cursor is not None:
                cursor.close()
            if self.__conn is not None:
                self.__conn.close()

    def do_operate_with_parameters(self, query_statement, parameters):
        """
        :param query_statement: SQL 语句
        :param parameters: 如果有很多值需要传入，在字符串中直接拼接SQL是不安全的，可以使用占位符解决.
        e.g.
        do_operate_with_parameters('INSERT INTO users VALUES (?, ?)', (3, "Jessica"))
        """
        cursor = None
        try:
            self.__connect()
            cursor = self.__conn.execute(query_statement, parameters)
            self._last_result = {'rowcount': cursor.rowcount, 'fetchall': cursor.fetchall()}
            self.__conn.commit()
        finally:
            if cursor is not None:
                cursor.close()
            if self.__conn is not None:
                self.__conn.close()

    def do_operates_with_parameters(self, query_statement, parameters=None):
        """
        批量操作，如批量插入
        data = [(1, "Ridesharing"), (2, "Water Purifying"), (3, "Forensics"), (4, "Botany")]
        do_operates_with_parameters("INSERT INTO projects VALUES(?, ?)", data)
        """
        cursor = None
        try:
            self.__connect()
            cursor = self.__conn.executemany(query_statement, parameters)
            self._last_result = {'rowcount': cursor.rowcount, 'fetchall': cursor.fetchall()}
            self.__conn.commit()
        finally:
            if cursor is not None:
                cursor.close()
            if self.__conn is not None:
                self.__conn.close()

    @abstractmethod
    def format_result(self):  # 返回格式化的结果，由子类实现
        raise NotImplementedError()

    @abstractmethod
    def get_result(self):  # 返回列表(行之间)的结果，由子类实现
        raise NotImplementedError()


class ExecuteUpdate(Sqlite3Template):
    """ ExecuteUpdate用于执行update、delete、insert语句等等，返回一个整数 """

    def format_result(self):
        """ 返回数据样式的举例: 'n'(为执行返回的整数) """
        output = str(self._last_result['rowcount'])
        return output

    def get_result(self):
        """ 返回数据样式的举例: n(为执行返回的整数) """
        output = int(self._last_result['rowcount'])
        return output


class ExecuteQuery(Sqlite3Template):
    """ ExecuteQuery用于执行SELECT语句，用于产生单个结果集 """

    def format_result(self):
        """
        返回数据样式的举例: "1,202031990141,张三\n2,202031990121,李四"
        """
        output = []
        # 在父类的operate_with_parameters函数中，操作的结果存储在result中
        for row_dict in self._last_result['fetchall']:  # fetchall函数，从结果集中获取所有行(list)
            lst = []  # 存放每行的数据
            for k in dict(row_dict):  # 通过for循环遍历一行的结果，将每个列值存放到lst中
                lst.append(str(row_dict[k]))
            output.append(', '.join(lst))
        return '\n'.join(output)  # 每行直接通过两个回车连接，最后返回的是字符串类型

    def get_result(self):
        """
        返回数据样式的举例:
        [{'id':1,'studentId':'202031990141','name':'张三'},{'id':2,'studentId':'202031990121','name':'李四'}]
        """
        output = []
        for row_dict in self._last_result['fetchall']:
            output.append(dict(row_dict))  # 行之间以列表的形式存储，列之间为字典形式存储
        return output
