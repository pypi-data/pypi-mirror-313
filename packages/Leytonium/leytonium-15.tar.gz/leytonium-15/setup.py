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
    name = 'Leytonium',
    version = '15',
    description = 'Tools for developing git-managed software',
    long_description = long_description(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/combatopera/Leytonium',
    author = 'Andrzej Cichocki',
    author_email = '3613868+combatopera@users.noreply.github.com',
    py_modules = [],
    install_requires = ['aridity>=62', 'autopep8>=1.5.4', 'awscli>=1.19.53', 'docutils>=0.15.2', 'importlib-metadata>=2.1.1', 'lagoon>=35', 'PyGObject>=3.42.2', 'pytz>=2020.4', 'pyven>=90', 'PyYAML>=5.2', 'setuptools>=44.1.1', 'termcolor>=1.1.0', 'Unidecode>=1.3.2'],
    package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt', '*.bash']},
    entry_points = {'console_scripts': ['diffuse=diffuse.diffuse:main', 'abandon=leytonium.abandon:main', 'agi=leytonium.agi:main', 'agil=leytonium.agil:main', 'autokb=leytonium.autokb:main', 'autopull=leytonium.autopull:main', 'awslogs=leytonium.awslogs:main', 'bashrc=leytonium.bashrc:main', 'br=leytonium.br:main', 'brown=leytonium.brown:main', 'ci=leytonium.ci:main', 'co=leytonium.co:main', 'd=leytonium.d:main', 'dp=leytonium.dp:main', 'drclean=leytonium.drclean:main', 'drop=leytonium.drop:main', 'drst=leytonium.drst:main', 'dup=leytonium.dup:main', 'dx=leytonium.dx:main', 'dxx=leytonium.dxx:main', 'eb=leytonium.eb:main', 'encrypt=leytonium.encrypt:main', 'examine=leytonium.examine:main', 'extractaudio=leytonium.extractaudio:main', 'fetchall=leytonium.fetchall:main', 'fixemails=leytonium.fixemails:main', 'gag=leytonium.gag:main', 'gimports=leytonium.gimports:main', 'git-completion-path=leytonium.git_completion_path:main', 'git-functions-path=leytonium.git_functions_path:main', 'gpgedit=leytonium.gpgedit:main', 'gt=leytonium.gt:main', 'halp=leytonium.halp:main', 'hgcommit=leytonium.hgcommit:main', 'imgdiff=leytonium.imgdiff:main', 'insertshlvl=leytonium.insertshlvl:main', 'isotime=leytonium.isotime:main', 'ks=leytonium.ks:main', 'mdview=leytonium.mdview:main', 'multimerge=leytonium.multimerge:main', 'n=leytonium.n:main', 'next=leytonium.next:main', 'pb=leytonium.pb:main', 'pd=leytonium.pd:main', 'prepare=leytonium.prepare:main', 'publish=leytonium.publish:main', 'pullall=leytonium.pullall:main', 'pushall=leytonium.pushall:main', 'rd=leytonium.rd:main', 'rdx=leytonium.rdx:main', 'readjust=leytonium.readjust:main', 'reks=leytonium.reks:main', 'ren=leytonium.ren:main', 'resimp=leytonium.resimp:main', 'rol=leytonium.rol:main', 'rx=leytonium.rx:main', 'scrape85=leytonium.scrape85:main', 'scrub=leytonium.scrub:main', 'setparent=leytonium.setparent:main', 'shove=leytonium.shove:main', 'show=leytonium.show:main', 'showstash=leytonium.showstash:main', 'slam=leytonium.slam:main', 'spamtrash=leytonium.spamtrash:main', 'splitpkgs=leytonium.splitpkgs:main', 'squash=leytonium.squash:main', 'st=leytonium.st:main', 'stacks=leytonium.stacks:main', 'stmulti=leytonium.stmulti:main', 't=leytonium.t:main', 'taskding=leytonium.taskding:main', 'tempvenv=leytonium.tempvenv:main', 'touchb=leytonium.touchb:main', 'unpub=leytonium.unpub:main', 'unslam=leytonium.unslam:main', 'upgrade=leytonium.upgrade:main', 'vcp=leytonium.vcp:main', 'vpn=leytonium.vpn:main', 'vunzip=leytonium.vunzip:main', 'watchdesk=leytonium.watchdesk:main']},
    **sourceinfo.setup_kwargs(),
)
