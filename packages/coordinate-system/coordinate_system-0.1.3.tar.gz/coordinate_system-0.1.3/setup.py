from setuptools import setup, find_packages

setup(
    name='coordinate_system',  # 包名
    version='0.1.3',  # 版本号
    packages=find_packages(),  # 自动找到包
    include_package_data=True,  # 包含非Python文件
    description='A package for coordinate systems',  # 简短描述
    long_description=open('README.md').read(),  # 详细描述
    long_description_content_type='text/markdown',
    author='romeosoft',  # 作者
    author_email='18858146@qq.com',  # 作者邮箱
    url='https://github.com/panguojun/Coordinate-System',  # 项目网址
    classifiers=[  # 分类
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Python版本要求
    install_requires=[],  # 依赖包，如果没有可以留空
    package_data={
        'coordinate_system': ['coordinate_system.pyd'],  # 确保这里的路径是正确的
    },
)