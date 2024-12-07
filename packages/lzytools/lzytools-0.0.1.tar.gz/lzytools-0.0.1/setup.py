import setuptools



setuptools.setup(
    name="lzytools", # Replace with your own username  #自定义封装模块名与文件夹名相同
    version="0.0.1", #版本号，下次修改后再提交的话只需要修改当前的版本号就可以了
    author="作者", #作者
    author_email="tagnaign2145u12985h@faktauigniag.com", #邮箱
    description="描述", #描述
    long_description='描述', #描述
    long_description_content_type="text/markdown", #markdown
    url="https://github.com/PPJUST/lzytools", #github地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #License
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',  #支持python版本
)