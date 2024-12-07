from setuptools import Extension
from setuptools.command.build_py import build_py as _build_py
import numpy

# Modules to be compiled and include_dirs when necessary
extensions = [
    Extension(
        "eqc_models.base.polyeval",
        ["eqc_models/base/polyeval.pyx"], include_dirs=[numpy.get_include()],
    ),
]

class build_py(_build_py):
    def run(self):
        self.run_command("build_ext")
        return super().run()

    def initialize_options(self):
        super().initialize_options()
        if self.distribution.ext_modules == None:
            self.distribution.ext_modules = []

        self.distribution.ext_modules.extend(extensions)
