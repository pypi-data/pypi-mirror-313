import os
import sys
import importlib
import types


class ChangeDirectoryAndPath:
    """Context manager to change the current working directory and sys.path."""

    def __init__(self, module_path):
        self.module_path = module_path
        self.old_path = None

    def __enter__(self):
        self.old_path = os.getcwd()
        sys.path.insert(0, self.module_path)
        os.chdir(self.module_path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.path.remove(self.module_path)
        os.chdir(self.old_path)
        

class ModuleManager:
    """Context manager for handling module imports and sys.modules state."""

    def __init__(self, module_path):
        self.module_path = module_path
        self.original_modules = sys.modules.copy()

    def __enter__(self):
        """Enter the runtime context related to this object."""
        self.change_dir = ChangeDirectoryAndPath(self.module_path)
        self.change_dir.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context related to this object."""
        self.change_dir.__exit__(exc_type, exc_value, traceback)
        self.cleanup_modules()

    def cleanup_modules(self):
        """Restore the original sys.modules state."""
        importlib.invalidate_caches()
        for key in list(sys.modules.keys()):
            if key not in self.original_modules:
                del sys.modules[key]
                

def wrapped_func(item, module_path):
    original_tool_function = item.func

    def _wrapped(*args, **kwargs):
        try:
            print(f"调用了 {item.name}")
        except:
            print(f"called unknown")
        with ChangeDirectoryAndPath(module_path):
            result = original_tool_function(*args, **kwargs)
        try:
            if isinstance(result, types.GeneratorType):
                result = list(result)
            print(f"{item.name} 调用完毕,结果为:", result)
        except:
            pass
        return result

    return _wrapped


