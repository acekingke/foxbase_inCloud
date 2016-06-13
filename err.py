# -*- coding:utf-8 -*-
class ParserError(Exception):
    def __init__(self, error_str):
        self.message = error_str
    def __str__(self):
        return  self.message
class AcceptError(Exception):
    def __init__(self):
        pass
