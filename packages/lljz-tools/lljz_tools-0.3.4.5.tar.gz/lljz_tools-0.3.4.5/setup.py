import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()


kwargs = dict(
    name="lljz_tools",
    version="0.3.4.5",
    author="liulangjuanzhou",
    author_email="liulangjuanzhou@gmail.com",
    description="常用工具封装",
    long_description_content_type="text/markdown",
    url="",
    package_data={
        "lljz_tools/source": ["*.html", "*.js"]
    },
    install_requires=[
        # 'pymysql>=1.1.0', 'dbutils>=3.0.3', 'sshtunnel>=0.4.0',
        # 'requests>=2.31.0', 'urllib3>=2.1.0',
        'openpyxl>=3.1.2', 'colorlog>=6.8.2',
        'better-exceptions>=0.3.3', 'concurrent-log-handler>=0.9.23'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
setuptools.setup(
    **kwargs,  # type: ignore
    long_description=long_description,
    packages=setuptools.find_packages(),
)
