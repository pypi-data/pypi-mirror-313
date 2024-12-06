import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# you need to change all these
VERSION = '0.0.8'
DESCRIPTION = 'sample wsgi server'

setup(
    name="kongfu-api",
    version=VERSION,
    author="smart_long",
    author_email="smart_long@outlook.com",
    description=DESCRIPTION,
    # 长描述内容的类型设置为markdown
    long_description_content_type="text/markdown",
    # 长描述设置为README.md的内容
    long_description=long_description,
    # 使用find_packages()自动发现项目中的所有包
    packages=find_packages(),
    # 包含的模块
    py_modules=['kongfu_api'],
    # 许可协议
    license='MIT',
    # 要安装的依赖包
    install_requires=[
        'urllib3==1.26.15',
        'Click',
        'pymysql',
        'peewee',
        'peewee-migrate',
        'PyJWT',
        'xmldict',
    ],
    entry_points={
        'console_scripts': [
            'kongfu=kongfu_api.tool:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
    ]
)


# python3 setup.py sdist bdist_wheel
# twine upload dist/*
# twine upload --skip-existing dist/*
