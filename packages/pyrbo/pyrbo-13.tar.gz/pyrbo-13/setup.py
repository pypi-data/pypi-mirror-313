from setuptools import setup

def long_description():
    with open('README.md') as f:
        return f.read()

class SourceInfo:

    class PYXPath:

        def __init__(self, module, path):
            self.module = module
            self.path = path

        def make_ext(self):
            g = {}
            with open("%sbld" % self.path) as f: # Assume project root.
                exec(f.read(), g)
            return g['make_ext'](self.module, self.path)

    def __init__(self, rootdir):
        def addextpaths(dirpath, moduleprefix, suffix = '.pyx'):
            for name in sorted(os.listdir(os.path.join(rootdir, dirpath))):
                if name.endswith(suffix):
                    module = "%s%s" % (moduleprefix, name[:-len(suffix)])
                    if module not in extpaths:
                        extpaths[module] = self.PYXPath(module, os.path.join(dirpath, name))
        from setuptools import find_packages
        import os
        self.packages = find_packages(rootdir)
        extpaths = {}
        addextpaths('.', '')
        for package in self.packages:
            addextpaths(package.replace('.', os.sep), "%s." % package)
        self.extpaths = extpaths.values()

    def setup_kwargs(self):
        kwargs = dict(packages = self.packages)
        if self.extpaths:
            from Cython.Build import cythonize
            kwargs['ext_modules'] = cythonize([path.make_ext() for path in self.extpaths])
        return kwargs

sourceinfo = SourceInfo('.')
setup(
    name = 'pyrbo',
    version = '13',
    description = 'Python JIT compiler for near-native performance of low-level arithmetic',
    long_description = long_description(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/combatopera/pyrbo',
    author = 'Andrzej Cichocki',
    author_email = '3613868+combatopera@users.noreply.github.com',
    py_modules = [],
    install_requires = ['diapyr>=26'],
    package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt']},
    entry_points = {'console_scripts': []},
    **sourceinfo.setup_kwargs(),
)
