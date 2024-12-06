"""Module for code inspection"""

# setup module import such that failed imports get mocked
import __builtin__
from types import ModuleType

class MockModule(ModuleType):
    def __getattr__(self, key):
        return None

    __all__ = []   # support wildcard imports

def try_import(name, globals={}, locals={}, fromlist=[], level=-1):
    try:
        return real_import(name, globals, locals, fromlist, level)
    except ImportError:
        return MockModule(name)

real_import, __builtin__.__import__ = __builtin__.__import__, try_import

import pkgutil
import inspect
import importlib


def getModules(package_name):
    # package = importlib.import_module(package_name)
    return [n for _, n, _ in pkgutil.iter_modules([package_name])]


def getModuleMembers(package_name, module_name):
    module = importlib.import_module('%s.%s' % (package_name, module_name))
    return [m for n,m in inspect.getmembers(module) if inspect.getmodule(m) == module]

def getClasses(module_members):
    return [c for c in module_members if inspect.isclass(c)]

def getMethods(myclass):
    return [method for name, method in inspect.getmembers(myclass) if inspect.ismethod(method)]

def getFunctions(module_members):
    return [function for name, function in module_members if inspect.isfunction(function)]

def getGlobalVars(module_members):
    return [v for v in module_members if not (inspect.isfunction(v) or
                                              inspect.isclass(v))]

def getLocalFuncVars(func):
    return func.__func__.func_code.co_varnames

def getGlobalFuncVars(func):
    func_global_names = func.__func__.func_globals.keys()
    func_var_names = func.__func__.func_code.co_names
    used_global_vars = [n for n in func_var_names if n in func_global_names]
    return used_global_vars