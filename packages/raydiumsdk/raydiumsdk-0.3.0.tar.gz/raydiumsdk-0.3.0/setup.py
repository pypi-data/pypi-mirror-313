from setuptools import setup

long_des = open("README.md" ,"r",encoding="utf-8").read()
setup(

    name = 'raydiumsdk',
    version = '0.3.0',
    description = 'Solana Python API',
    long_description = long_des,
    long_description_content_type="text/markdown",
    author="Huang",
    license="MIT",
    install_requires = [
        'solana',
        'solders'
    ],

    
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Topic :: Terminals",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    
    packages = [
        'raydium'
    ],

    package_data = {'': ['*']}

)
