from setuptools import setup, find_packages

setup(
    name='zack_liu_package',  # 包的名称
    version='1.1.2',  # 包的版本
    packages=find_packages(),  # 自动找到包
    install_requires=[],  # 依赖的其他包
    author='刘志敏',  # 作者
    author_email='liu.zhimin.2019@gmail.com',  # 作者邮箱
    description='zack_liu_package',  # 简短描述
    long_description=open('README.md').read(),  # 详细描述
    long_description_content_type='text/markdown',  # 描述格式
    url='https://github.com/liuzhimin2019/soho-ui.git',  # 项目网址
    classifiers=[  # 分类信息
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Python 版本要求
)