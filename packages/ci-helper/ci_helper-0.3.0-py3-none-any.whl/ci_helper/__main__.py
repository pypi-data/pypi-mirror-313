import sys
from pathlib import Path
import argparse
import json
import subprocess
import requests

from .__version__ import __version__


# Command line args that can be used in place of "setup.py" for projects that lack a
# setup.py, runs a minimal setup.py similar to what pip does for projects with no
# setup.py.
_SETUP_PY_STUB = [
    "-c",
    'import sys, setuptools; sys.argv[0] = __file__ = "setup.py"; setuptools.setup()',
]


def setup_py(project_dir):
    """Returns a list of command line arguments to be used in place of ["setup.py"]. If
    setup.py exists, then this is just ["setup.py"]. Otherwise, if setup.cfg or
    pyproject.toml exists, returns args that pass a code snippet to Python with "-c" to
    execute a minimal setup.py calling setuptools.setup(). If none of pyproject.toml,
    setup.cfg, or setup.py exists, raises an exception."""
    if Path(project_dir, 'setup.py').exists():
        return ['setup.py']
    elif any(Path(project_dir, s).exists() for s in ['setup.cfg', 'pyproject.toml']):
        return _SETUP_PY_STUB
    msg = f"""{project_dir} does not look like a python project directory: contains no
        setup.py, setup.cfg, or pyproject.toml"""
    raise RuntimeError(' '.join(msg.split()))


def get_pythons():
    """Return stable, non-end-of-life Python versions in X.Y format"""
    URL = "https://raw.githubusercontent.com/python/devguide/refs/heads/main/include/release-cycle.json"
    response = requests.get(URL, timeout=30)
    if not response.ok:
        raise ValueError(f"{response.status_code} {response.reason}")
    pythons = response.json()
    pythons = [p for p in pythons if pythons[p]['status'] in ('bugfix', 'security')]
    pythons.sort(key=lambda ver: [int(part) for part in ver.split('.')])
    return pythons


def main():
    # Since setuptools_conda is self-hosting, it needs toml and distlib to read its own
    # requirements just to know that it needs to install toml and distlib! So bootstrap
    # that up if necessary.

    parser = argparse.ArgumentParser(prog='ci-helper')
    parser.add_argument(
        '--version',
        action='version',
        version=__version__,
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Action to perform"
    )
    parser_pythons = subparsers.add_parser(
        "pythons",
        help="Output list of stable Python versions that have not yet reached end of "
        + "life, see `ci-helper pythons -h`",
    )
    parser_pythons.add_argument(
        "--cibw",
        action="store_true",
        help="Output as a space-separated list in the format "
        + "`cpXY-* cpXY-*` as appropriate for the  CIBW_BUILD environment variable "
        + "to build for all stable CPython versions, otherwise versions are output as "
        "a comma-separated list in the format X.Y,X.Y",
    )
    _ = subparsers.add_parser(
        "defaultpython",
        help="Output the second-latest stable Python version in X.Y format, "
        "useful as a good choice for a default python version",
    )
    parser_distinfo = subparsers.add_parser(
        "distinfo",
        help="Output info about the distribution, see `ci-helper distinfo -h`",
    )
    parser_distinfo.add_argument(
        "field",
        choices=['name', 'version', 'is_pure', 'has_env_markers'],
        nargs="?",
        help="Name of field to output as a single json value, "
        + "if not given, all info is output as json",
    )
    parser_distinfo.add_argument(
        'project_directory',
        help="Directory of Python project",
    )

    args = parser.parse_args()

    if args.command == 'pythons':
        pythons = get_pythons()
        if args.cibw:
            print(' '.join([f"cp{p.replace('.', '')}-*" for p in pythons]))
        else:
            print(','.join(pythons))

    elif args.command == 'defaultpython':
        pythons = get_pythons()
        print(pythons[-2])

    elif args.command == 'distinfo':
        cmd = [
            sys.executable,
            *setup_py('.'),
            '-q',
            '--command-packages=ci_helper.command',
            'ci_distinfo',
        ]
        try:
            result = subprocess.run(
                cmd, cwd=args.project_directory, check=True, capture_output=True
            )
        except subprocess.CalledProcessError as e:
            sys.stderr.write(e.stderr.decode('utf8'))
            raise
        info = result.stdout.decode('utf8')
        if args.field is not None:
            info = json.loads(info)
            value = info[args.field]
            if isinstance(value, str):
                print(value)
            else:
                print(json.dumps(value))
        else:
            print(info)

    sys.exit(0)


if __name__ == '__main__':
    main()
