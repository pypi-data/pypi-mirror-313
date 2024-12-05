#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 下午4:08
# @Author  : @Zhenxi Zhang
# @File    : df_filter_lang_parser.py
# @Software: PyCharm


class CharWorker:
    """
    用于接收字符流中的单个字符串，并做相应处理，返回到解析器中
    """

    def __init__(self, symbol, root_parser, end_symbol=None):
        if end_symbol is None:
            end_symbol = [";", "(", ")"]
        self._symbol = symbol  # 设置字段标识
        self.loading_flag = False  # 用于指示是否触碰到字段标识
        self._mem = ""  # 缓存
        self.root_parser = root_parser  # 所属的解析器
        self._end_symbol = end_symbol

    def run(self, char):
        if not isinstance(char, str) or len(char) != 1:
            raise ValueError("Expected a single character string")
        if char in self._end_symbol:
            self._upload_string()
            self._mem += char
            self._upload_string()
            return
        if char == self._symbol:
            self.if_detected_symbol()
        else:
            self._mem += char

    def if_detected_symbol(self):
        if self.loading_flag:
            # 如果已经是读取字段状态，则关闭读取状态，并上传字符串
            self.loading_flag = False
            self._upload_string()
        else:
            # 说明此时仍未进入读取字段状态，如果缓存内容不为空，将缓存内容去空格上传，缓存内容应为运算符
            self.loading_flag = True
            if self._mem != "":
                self._mem = self._mem.strip()
                self._upload_string()

    def _upload_string(self):
        if self._mem == "":
            return
        self._mem = self._mem.strip()

        self.root_parser.append2cache(self._mem)
        self._mem = ""

    def check_if_in_end_symbol(self, string):
        if string in self._end_symbol:
            return True
        else:
            return False


class CalcUnit:
    def __init__(self, root, total_sentence):
        self.root = root
        self.total_sentence = total_sentence
        self.df = self.root.df
        self.result = None

    def run(self):
        for string in self.total_sentence:
            if string in [")", "(", ";"]:
                continue
            self._calculator_calc(string)
        return self.result

    def _calculator_calc(self, string):
        def _test_type(_a):
            try:
                _a = float(_a)
            except ValueError:
                try:
                    _a = self.df[_a]
                except IndexError:
                    raise Exception(f"类型测试错误，非字段也不可转为浮点数 {_a}")
            return _a

        if len(string) == 3:
            a = _test_type(string[0])
            b = _test_type(string[2])
            opt = string[1]
        elif len(string) == 2:
            a = self.result
            b = _test_type(string[1])
            opt = string[0]
        else:
            raise ValueError("不支持的表达式")
        if opt == "+":
            self.result = a * b
        elif opt == "-":
            self.result = a - b
        elif opt == "*":
            self.result = a * b
        elif opt == "/":
            self.result = a / b
        else:
            raise ValueError(f"不支持的运算符{opt}")


class FilterUnit:
    def __init__(self, root, total_sentence):
        self.buffers = total_sentence
        self.val_stack = []
        self.opt_stack = []
        self._iter_flag = True
        self.root = root

    def run(self):
        for sec in self.buffers:
            if self._iter_flag:
                self._each(sec)
            else:
                break

        while self.opt_stack:
            opt = self.opt_stack.pop()
            b = self.val_stack.pop()
            a = self.val_stack.pop()
            self.val_stack.append(self._calc(a, b, opt))
            # print(self.val_stack, ',', self.opt_stack)

        return self.val_stack[0]

    def _each(self, string):
        if string == ";":
            self._iter_flag = False
            return
        if string == "(":
            self.val_stack.append(None)
        elif string == ")":
            opt = self.opt_stack.pop()
            b = self.val_stack.pop()
            a = self.val_stack.pop()
            if opt in self.root._logical_operator:
                self.val_stack.pop()
            self.val_stack.append(self._calc(a, b, opt))
        elif string in self.root._logical_operator:
            self.opt_stack.append(string)
        else:
            self.val_stack.append(string)
            if self.root.lang_type == "DfFilter":
                self.opt_stack.append("filter")
            elif self.root.lang_type == "CalcFilter":
                self.opt_stack.append("calc")
        # print(self.val_stack, ',',self.opt_stack)

    def _calc(self, a, b, opt):
        if opt == "and":
            return a & b
        elif opt == "or":
            return a | b
        elif a is None and opt == "filter":
            return self._get_boolean_series(b)
        else:
            raise ValueError("不支持的运算符", a, b, opt)

    def _get_boolean_series(self, string):
        a = self.root.df[string[0]]
        b = string[2]
        opt = string[1]
        if opt == "==":
            tmp_res = a == b
        elif opt == "!=":
            tmp_res = a != b
        elif opt == "<":
            tmp_res = a < b
        elif opt == ">":
            tmp_res = a > b
        elif opt == "<=":
            tmp_res = a <= b
        elif opt == ">=":
            tmp_res = a >= b
        else:
            raise ValueError(f"不支持的运算符{opt}")
        return tmp_res.values


class LangParser:
    def __init__(self, df):
        self.df = df
        self.cw = CharWorker('"', self)
        self.status_code = 0
        self.lang_type_flag = False
        self.lang_type = None

        self._relation_operator = ["==", "!=", "<", ">", "<=", ">="]
        self._numerical_operator = ["+", "-", "*", "/"]
        self._logical_operator = ["and", "or", "xor"]
        self._mem = []

        self._sentence_tmp = []
        self._status_barrier = 3
        self._cache = []

        self.unit = None

    def get_buffers(self, string):
        self._cache = []
        self.lang_type = None
        self.lang_type_flag = False
        for char in string:
            self.cw.run(char)

    def append2cache(self, string):
        if not self.lang_type_flag:
            if string in self._relation_operator:
                self.lang_type = "DfFilter"
                self.lang_type_flag = True
            if string in self._numerical_operator:
                self.lang_type = "CalcFilter"
                self.lang_type_flag = True

        self._mem.append(string)
        if self.cw.check_if_in_end_symbol(string):
            self._cache.append(string)
            return
        if string in self._logical_operator:
            self._cache.append(string)
            self._opt_tmp = string
            return
        self._sentence_tmp.append(string)
        self.status_code += 1
        if self.status_code == self._status_barrier:
            if self.lang_type == "CalcFilter":
                self._status_barrier = 2
            self._cache.append(self._sentence_tmp)
            self._sentence_tmp = []
            self.status_code = 0

    def run(self, string):
        self.get_buffers(string)

        if self.lang_type == "DfFilter":
            self.unit = FilterUnit(self, self._cache)
        if self.lang_type == "CalcFilter":
            self.unit = CalcUnit(self, self._cache)
        return self.unit.run()
