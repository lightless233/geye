#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
from lupa import LuaRuntime

lua = LuaRuntime()
lua.eval("1+1")


# rule_content = "'password' in {{content}} and 'token' not in {{content}}".replace("\'", "\"")
rule_content = '[x for x in {}.__class__.__bases__[0].__subclasses__() if x.__name__ == "zipimporter"]'
# rule_content = '[].__class__.__mro__[-1].__subclasses__()'
# filter_content = "aaaabbbcccdde\naaacccbdbadjf"
filter_content = "aaaabbbcccdde\naaacccbdbadjf\npassword=123"

code = rule_content.replace("{{content}}", "filter_content")
code = "python.eval(\'{code}\')".format(code=code)
print("final code: {}".format(code))

result = lua.eval(code)
print("result: {}".format(result))
