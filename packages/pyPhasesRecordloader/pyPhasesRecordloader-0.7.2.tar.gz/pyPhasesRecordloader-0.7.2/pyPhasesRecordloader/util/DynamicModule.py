import importlib


class DynamicModule:
    def __init__(self, path) -> None:
        self.modPath = path
        self.module = None
        self.moduleName = None
        self.moduleOptions = {}
        self.dynOptions = {}

    def get(self, packageName=None):
        if self.module is None:
            modelClass = self.loadModelByModule(packageName)
            self.module = modelClass(**self.moduleOptions)
            for field in self.dynOptions:
                self.module.__setattr__(field, self.dynOptions[field])

        return self.module

    def set(self, name, options={}, dynOptions={}) -> None:
        self.moduleName = name
        self.moduleOptions = options
        self.dynOptions = dynOptions
        self.module = None

    def loadModelByModule(self, packageName):
        if self.moduleName is None:
            raise Exception("The DynamicModule setter needs to be called with a name!")
        name = self.moduleName
        module = importlib.import_module(f".{name}", package=packageName)
        return getattr(module, name)
