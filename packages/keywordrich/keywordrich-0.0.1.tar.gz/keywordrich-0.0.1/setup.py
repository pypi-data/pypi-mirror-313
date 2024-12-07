from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'keywordrich'

setup(
    name="keywordrich",
    version=VERSION,
    author="feng wang",
    author_email="Sysiphus6@2925.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md',encoding="UTF8").read(),
    packages=find_packages(),
    install_requires=['langchain', 'langchain_openai'],
    keywords=['python', 'keyword rich', 'ai'],
    entry_points={
    'console_scripts': [
        'keywordrich = keywordrich.main:main'
    ]
    },
    license="MIT",
    # url="https://github.com/",
    scripts=['keywordrich/keywordrich.py'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)