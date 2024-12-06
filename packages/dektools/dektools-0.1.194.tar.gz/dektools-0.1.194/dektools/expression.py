from RestrictedPython.compile import compile_restricted_eval
from RestrictedPython.Guards import safe_builtins


# https://github.com/odoo/odoo/blob/fa6a577cc95b604ae3684010107cf5d04a3ce078/odoo/tools/safe_eval.py
# RestrictedPython
# evalidate


def eval_unsafe(code_str, loc=None, glo=None, delay=True):
    def func():
        return eval(code_str, glo, loc)

    if not delay:
        try:
            return func(), None
        except Exception as e:
            return None, e
    return func, None


def eval_safe(code_str, loc=None, glo=None, delay=True):
    def func():
        return eval(code.code, restricted_globals, loc)

    restricted_globals = dict(__builtins__=safe_builtins, **(glo or {}))
    code = compile_restricted_eval(code_str, '<string>')
    if code.errors:
        return None, code.errors
    if not delay:
        try:
            return func(), None
        except Exception as e:
            return None, e
    return func, None
