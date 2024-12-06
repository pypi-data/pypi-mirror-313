import os
import setuptools

# 如果readme文件中有中文，那么这里要指定encoding='utf-8'，否则会出现编码错误
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as readme:
    README = readme.read()
 
# 允许setup.py在任何路径下执行
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
 
setuptools.setup(
    name="llm_inferencer", # 库名，需要在pypi中唯一
    version="0.0.18",                          # 版本号
    author="Peiwen Jiang (Wayne)",            # 作者
    author_email="wayne_roaming@163.com",     # 作者邮箱
    description="A collection of commonly used code", # 简介
    long_description=README,              # 详细描述（一般会写在README.md中）
    long_description_content_type="text/markdown",  # README.md中描述的语法（一般为markdown）
    url="https://github.com/jiangpw41/llm_inferencer",   # 库/项目主页，一般我们把项目托管在GitHub，放该项目的GitHub地址即可
    packages=setuptools.find_packages(),    #默认值即可，这个是方便以后我们给库拓展新功能的
    include_package_data=True,
    classifiers=[                           # 指定该库依赖的Python版本、license、操作系统之类的
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "inference_start=llm_inferencer.server_gateway:main",  # 定义命令行工具名和入口
        ],
    },
    extras_require={
    },
    install_requires=[                      # 该库需要的依赖库
        'flask',
        'wayne_utils',
        "openai"
        #'Django >= 1.11, != 1.11.1, <= 2',
    ],
    python_requires='>=3.6',
)