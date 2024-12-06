from setuptools import setup, find_packages

setup(
    name="bk_return_sales",  
    version="0.1.4", 
    description="bk_return_sales",
    long_description=open('README.md').read(),  
    long_description_content_type="text/markdown", 
    author="bk", 
    author_email="brktmbrt@gmail.com",  
    url="",  #  GitHub
    packages=find_packages(),  # Automatically find all packages in the project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[  
        "numpy", "openpyxl" 
    ],
    python_requires='>=3.6',  
    entry_points={  
        'console_scripts': [
            'mycommand=mypackage.module:main_function',  # Example of a CLI command
        ],
    },
)
