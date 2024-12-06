from setuptools import setup, find_packages
import pathlib

# 读取 README 文件内容
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README_ZH.MD').read_text(encoding='utf-8')

# 读取版本号
about = {}
exec((here / 'llmer' / '__version__.py').read_text(), about)

setup(
    name='llmer',
    version=about['__version__'],  # 动态获取版本号
    packages=find_packages(),
    description='llmer is a lightweight Python library designed to streamline the development of applications leveraging large language models (LLMs). It provides high-level APIs and utilities for parallel processing, runtime management, file handling, and prompt generation, reducing the overhead of repetitive tasks.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='pydaxing',
    author_email='pydaxing@gmail.com',
    url='https://github.com/pydaxing/llmer',
    python_requires='>=3.6',
    install_requires=[
        'jsonlines>=4.0.0',
        'PyYAML>=6.0.2',
        'setuptools>=75.6.0',
        'tqdm>=4.67.1',
        'openai>=1.56.1',
        'fastapi>=0.115.6',
        'uvicorn>=0.32.1',
    ],
    entry_points={},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Typing :: Typed',
    ],
    keywords='llmer leveraging large language models',
)
