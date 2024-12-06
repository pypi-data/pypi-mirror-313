from setuptools import setup, find_packages

setup(
    name='simple_pkg_by_zxz',                          # 包名
    version='0.1.0',                             # 版本号
    packages=find_packages(),                   # 自动查找包
    install_requires=[],                        # 依赖（如果有的话）
    long_description=open('README.md').read(),  # 长描述
    long_description_content_type='text/markdown',  # 内容类型
    author='Your Name',                         # 作者信息
    author_email='your.email@example.com',       # 作者邮箱
    description='A simple greeting package',    # 简短描述
    license='MIT',                              # 许可协议
    url='https://github.com/yourusername/simple_pkg',  # 项目链接
    classifiers=[                               # 分类
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
