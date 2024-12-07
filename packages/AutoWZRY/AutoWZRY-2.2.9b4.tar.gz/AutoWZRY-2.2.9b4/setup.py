from setuptools import setup, find_packages

setup(
    name='AutoWZRY',
    version='2.2.9b4',
    author='cndaqiang',
    author_email='who@cndaqiang.ac.cn',
    description='王者荣耀自动化农活脚本。',
    long_description=open('AutoWZRY/README.md', encoding='utf-8').read(),  # 从 AutoWZRY/README.md 读取 long description
    long_description_content_type='text/markdown',
    packages=find_packages(),  # 自动查找所有子包
    # 需要在AutoWZRY下面创建__init__.[y]
    package_data={             # 指定需要包含的额外文件
        'AutoWZRY': [
            'assets/*',         # 包括 AutoWZRY/assets 下的所有文件
            'README.md',         # 包括 AutoWZRY/assets 下的所有文件
            'LICENSE',         # 包括 AutoWZRY/assets 下的所有文件
        ],
    },
    include_package_data=True,  # 自动包含 package_data 中指定的文件
    url='https://github.com/cndaqiang/WZRY',
    install_requires=[
        'airtest-mobileauto>=2.0.12',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
)
