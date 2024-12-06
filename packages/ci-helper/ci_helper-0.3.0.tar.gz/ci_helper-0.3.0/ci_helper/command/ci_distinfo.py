from setuptools import Command
import json
from pathlib import Path


def get_pyproject_toml_entry(proj, *keys):
    """Return [build-system] requires as read from proj/pyproject.toml, if any"""
    # this import is here to avoid bootstrapping issues when building wheels for this
    # package itself
    import toml
    pyproject_toml = Path(proj, 'pyproject.toml')
    if not pyproject_toml.exists():
        return None
    config = toml.load(pyproject_toml)
    try:
        for key in keys:
            config = config[key]
        return config
    except KeyError:
        return None


def has_environment_markers(setup_requires, install_requires, extras_requires):
    """Given a list of install_requires and a dict of extras_requires, return if there
    are any environment markers"""
    for item in install_requires:
        if ';' in item:
            return True
    for key in extras_requires:
        if key.startswith(':'):
            # an extras_requires item being used as an environment marker, an old
            # pattern allowed by setuptools
            return True
    return False


class ci_distinfo(Command):
    description = "Get package info useful for building on CI"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        setup_requires = get_pyproject_toml_entry('.', 'build-system', 'requires')
        if setup_requires is None:
            setup_requires = self.distribution.setup_requires

        info = {
            'name': self.distribution.get_name(),
            'version': self.distribution.get_version(),
            'is_pure': not (
                self.distribution.has_ext_modules()
                or self.distribution.has_c_libraries()
            ),
            'has_env_markers': has_environment_markers(
                setup_requires,
                self.distribution.install_requires,
                self.distribution.extras_require,
            ),
        }
        print(json.dumps(info, indent=4))
