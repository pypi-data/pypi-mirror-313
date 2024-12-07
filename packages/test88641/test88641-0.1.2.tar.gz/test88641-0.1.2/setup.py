from setuptools import setup, find_packages

setup(
    name="test88641",                          
    version="0.1.2",                            
    author="user8864",
    description="A test upload",
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown", 
    url="https://github.com/ftnworld/test88641",  
    packages=find_packages(),                  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",                   
    install_requires=[                         
        "numpy",
        "pandas",
        "matplotlib",
    ],
)
