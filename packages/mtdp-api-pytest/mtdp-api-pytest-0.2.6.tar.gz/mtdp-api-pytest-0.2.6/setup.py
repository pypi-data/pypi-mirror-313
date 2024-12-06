from setuptools import setup, find_packages
 
setup(
    name='mtdp-api-pytest',                                 # 你的 Python 包的名称，当用户使用 pip 安装时，会使用这个名称
    version='0.2.6',                                        # 版本号，数值大的会优先被pip
    packages=find_packages(),                               # 自动发现并包含所有包（和子包），即包含同一目录下的 __init__.py 文件
    install_requires=[],                                    # 项目依赖的第三方库列表，安装时会自动安装这些依赖项（install_requires = ["numpy", "pillow"]）
    author='cloudflere',                                     # 作者
    author_email='cloudflere@example.com',                  # 作者邮箱
    description='mtdp-api-pytest',                 # 包描述
    long_description=open('README.md').read(),              # 读取 README.md 文件的内容作为包的长描述
    long_description_content_type='text/markdown',          # 指定长描述的格式为 Markdown
    url='https://github.com/cloudflere/cloudflere',  # 项目的主页 URL
    classifiers=[                                           # 分类器，用于给包打标签，以便在 PyPI 上进行分类和搜索
        'Programming Language :: Python :: 3',              # 指定该包使用的编程语言及其版本
        'License :: OSI Approved :: MIT License',           # 指定该包的许可证类型
        'Operating System :: OS Independent',               # 指定该包与操作系统无关，可以在任何操作系统上运行
    ],
    python_requires='>=3.6',                             # 指定 Python 的最低版本要求
)