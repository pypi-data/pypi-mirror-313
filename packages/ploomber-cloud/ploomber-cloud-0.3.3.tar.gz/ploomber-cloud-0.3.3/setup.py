import re
import ast
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages
from setuptools import setup

_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("src/ploomber_cloud/__init__.py", "rb") as f:
    VERSION = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )

REQUIRES = [
    "click",
    "requests",
    # we added the custom api_key arg to Telemetry.from_package in this version
    "ploomber-core>=0.2.26",
    "python-dotenv",
    "cloudpickle==3.0.0",
]

DEV = [
    "pytest",
    "flake8",
    "twine",
    "pkgmt",
    "ipdb",
    "ipython",
]

setup(
    name="ploomber-cloud",
    version=VERSION,
    description=None,
    license=None,
    author=None,
    author_email=None,
    url=None,
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    classifiers=[],
    keywords=[],
    install_requires=REQUIRES,
    extras_require={
        "dev": DEV,
    },
    entry_points={
        "console_scripts": [
            "ploomber-cloud=ploomber_cloud.cli:cli",
            "pc=ploomber_cloud.cli:cli",
        ],
    },
)
