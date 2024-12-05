import setuptools #导入setuptools打包工具

setuptools.setup(
    name="mark_cont_area", 
    version="1.1.0",   
    author="Mingxi Zhang",   
    author_email="zhang.mingxi@outlook.com",    
    description="Mark continuous areas with positive natural numbers (1,2,3,...,N)",
    packages=setuptools.find_packages(),
)