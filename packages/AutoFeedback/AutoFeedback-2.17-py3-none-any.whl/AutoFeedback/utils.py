"""utilities for ensuring modules are installed"""


def _import_location():
    """check the context and specify whence the objects should be imported"""
    import sys
    if any(["kernel_launcher.py" in j for j in sys.argv]):
        # If running a notebook, import from local __main__
        importfrom = '__main__'
    else:
        # If running a file, import from file main.py
        importfrom = 'main'
    return importfrom


def exists(objname, isfunc=False):
    """Check that main.objname exists (objname is string)
    if isfunc=True, then also check that objname is a function
    """
    importfrom = _import_location()
    try:
        testfunc = getattr(__import__(
            importfrom, fromlist=[objname]), objname)
        if isfunc:
            from inspect import isfunction
            return isfunction(testfunc)
        else:
            return True
    except Exception:
        return False


def get(objname):
    """import main.objname (objname is string)"""
    importfrom = _import_location()
    testobj = getattr(__import__(importfrom, fromlist=[objname]), objname)
    return testobj


def get_internal(objname):
    """check main.objname exists, then import main.objname
    (objname is string)"""
    if not exists(objname):
        print(f"""In order to check your code, the variable {objname}
              must be set.""")
        from .variable_error_messages import print_error_message
        print_error_message("existence", objname, exp=None, res=None)
        raise AssertionError
    else:
        return get(objname)


def check_module(modname):
    """ check if modname is installed, and if not, attempt to use pip to
    install it"""
    from importlib.util import find_spec
    installed = find_spec(modname) is not None
    if not installed:
        import subprocess
        import sys
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", modname])
    return


def run_tests():
    import unittest
    unittest.main(argv=[''], verbosity=0, exit=False)
