import setuptools



setuptools.setup(
    name="lzytools", #自定义封装模块名，与文件夹名相同
    version="0.0.4", #版本号
    author="PPJUST", #作者
    author_email="tagnaign2145u12985h@faktauigniag.com", #邮箱
    description="描述", #描述
    long_description='描述', #描述
    long_description_content_type="text/markdown", #markdown
    url="https://github.com/PPJUST/lzytools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #License
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',  #支持python版本
)