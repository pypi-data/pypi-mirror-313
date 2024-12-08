# src/pyinstaller/module_loader.py
import importlib.util
import os
import sys
class ModuleLoader:
    def __init__(self):
        self.modules = {}

    def load_module(self, module_name, relative_path):
        # 获取当前工作目录作为基准路径
        base_path = os.getcwd()  # 这里改为当前工作目录
        external_path = os.path.join(base_path, relative_path)
        internal_path = os.path.join(os.path.dirname(__file__), relative_path)
        print(f"external_path {external_path} internal_path: {internal_path}")  # 打印加载路径 
        # 优先加载外部文件，如果不存在则加载内部文件
        if os.path.exists(external_path):
            lib_path = external_path
        else:
            lib_path = internal_path

        #print(f"Loading {module_name} from: {lib_path}")  # 打印加载路径

        spec = importlib.util.spec_from_file_location(module_name, lib_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.modules[module_name] = {
            'module': module,
            'path': lib_path,
            'mtime': os.path.getmtime(lib_path),
            'instance': getattr(module, module_name.capitalize())()
        }
        return self.modules[module_name]['instance']

    def reload_modules(self):
        #print(f"Current modules: {list(self.modules.items())}")  # 打印 self.modules.items()
        for module_name, module_info in self.modules.items():
            current_mtime = os.path.getmtime(module_info['path'])
            #print(f"Checking {module_name}: current_mtime={current_mtime}, saved_mtime={module_info['mtime']}")  # 添加调试信息
            if current_mtime != module_info['mtime']:
                #print(f"Reloading {module_name} from: {module_info['path']}")
                spec = importlib.util.spec_from_file_location(module_name, module_info['path'])
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.modules[module_name]['module'] = module
                self.modules[module_name]['mtime'] = current_mtime
                self.modules[module_name]['instance'] = getattr(module, module_name.capitalize())()
                setattr(self, module_name, self.modules[module_name]['instance'])