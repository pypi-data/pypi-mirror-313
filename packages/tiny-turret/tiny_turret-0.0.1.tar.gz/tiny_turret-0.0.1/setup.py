import os

from setuptools import setup, find_packages

here = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(here, "README.md"))
long_description = f.read().strip()
f.close()


setup(
    name="tiny-turret",
    description="Tiny django exception handler",
    version="0.0.1",
    author="Tiny Turret Team",
    url="https://github.com/jacqueswww/tiny-turret",
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests*",)),
    zip_safe=False,
    include_package_data=True,
    py_modules=["django_spam"],
    setup_requires=["pytest-runner"],
    install_requires=[
        "Django>=2.0.0",
        "filelock>=3.16.1",
        "tabulate>=0.9.0",
        "tblib==3.0.0"
    ],
    entry_points={
        'console_scripts': ['tiny-turret=tinyturret.cli:main']
    },
    extras_require={
        "test": [
             "pytest",
        ]
    },
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
    ],
)
