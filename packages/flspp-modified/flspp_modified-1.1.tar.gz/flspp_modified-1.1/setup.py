# -*- coding: utf-8 -*-
from setuptools import setup

from setuptools import Extension
from setuptools.command.build_ext import build_ext

extension = Extension(
    name="flspp._core",
    sources=[
        "flspp/_core.cpp",
        "flspp/cpp/clustering_algorithm.cpp",
        "flspp/cpp/clustering.cpp",
        "flspp/cpp/makros.cpp",
        "flspp/cpp/random_generator.cpp",
    ],
    include_dirs=["flspp"],
)

# Thank you https://github.com/dstein64/kmeans1d!


class BuildExt(build_ext):
    """A custom build extension for adding -stdlib arguments for clang++."""

    def build_extensions(self) -> None:
        # '-std=c++11' is added to `extra_compile_args` so the code can compile
        # with clang++. This works across compilers (ignored by MSVC).
        for extension in self.extensions:
            extension.extra_compile_args.append("-std=c++11")

        try:
            build_ext.build_extensions(self)
        except:
            # Workaround Issue #2.
            # '-stdlib=libc++' is added to `extra_compile_args` and `extra_link_args`
            # so the code can compile on macOS with Anaconda.
            for extension in self.extensions:
                extension.extra_compile_args.append("-stdlib=libc++")
                extension.extra_link_args.append("-stdlib=libc++")
            build_ext.build_extensions(self)


def build(setup_kwargs) -> None:
    setup_kwargs.update(
        {"ext_modules": [extension], "cmdclass": {"build_ext": BuildExt}}
    )


packages = \
['flspp']

package_data = \
{'': ['*'], 'flspp': ['cpp/*']}

install_requires = \
['numpy1.23.5', 'scikit-learn0.23.2']

setup_kwargs = {
    'name': 'flspp_modified',
    'version': '1.1',
    'description': 'Implementation of the FLS++ algorithm for K-Means clustering.',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


build(setup_kwargs)

setup(**setup_kwargs)
