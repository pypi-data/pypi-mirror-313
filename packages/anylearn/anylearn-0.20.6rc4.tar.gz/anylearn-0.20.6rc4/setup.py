import io

import setuptools


SDK_INFO = {}
with open("./anylearn/__about__.py") as f:
    exec(f.read(), SDK_INFO)


try:
    with io.open("README.md", encoding="utf-8") as f:
        LONG_DESCRIPTION = f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = ""

REQUIRES = []
with open('requirements.txt') as f:
    for line in f:
        line, _, _ = line.partition('#')
        line = line.strip()
        REQUIRES.append(line)

setuptools.setup(
    name=SDK_INFO['__package_name__'],
    version=SDK_INFO['__version__'],
    license=SDK_INFO['__license__'],
    description=SDK_INFO['__description__'],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author_email=SDK_INFO['__author_email__'],
    author=SDK_INFO['__author__'],
    install_requires=REQUIRES,
    python_requires='>=3.7',
    packages=setuptools.find_packages(),
    package_data={
        'anylearn': [
            "storage/db/migrations/alembic.ini",
        ],
    },
    include_package_data=True,
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points = '''
        [console_scripts]
        anyctl = anylearn.cli.cli:app
    ''',
)
