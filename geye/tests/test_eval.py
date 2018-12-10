#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import ast


# rule_content = "'password' in {{content}} and 'token' not in {{content}}"
rule_content = '[x for x in {}.__class__.__bases__[0].__subclasses__() if x.__name__ == "zipimporter"]'
# rule_content = '[].__class__.__mro__[-1].__subclasses__()'
filter_content = "aaaabbbcccdde\naaacccbdbadjf"
# filter_content = "aaaabbbcccdde\naaacccbdbadjf\npassword=123"

# print("globals: {}".format(globals()))
# print("locals: {}".format(locals()))

code = rule_content.replace("{{content}}", "filter_content")
print("final code: {}".format(code))

result = eval(code, {"__builtins__": None}, {"filter_content": filter_content})
print(result)


# class ASTNode(ast.NodeVisitor):
#     def generic_visit(self, node):
#         print("node: {}".format(dir(node.body)))
#         print("node: {}".format(node.body.keywords))
#         print("node name: {}".format(type(node)))
#
#
# n = ast.parse(code, '<usercode>', "eval")
# v = ASTNode()
# v.visit(n)
#
# print("global node: {}".format(n))
