from setuptools import setup, find_packages

setup(
    name="bk_return_sales",  # The name of your package
    version="0.1.3",  # Version number of your package
    description="bk_return_sales",
    long_description=open('README.md').read(),  # Read the README file for a longer description
    long_description_content_type="text/markdown",  # Type of long description (e.g., markdown)
    author="bk",  # Author of the package
    author_email="brktmbrt@gmail.com",  # Author email
    url="",  # URL to the project (e.g., GitHub)
    packages=find_packages(),  # Automatically find all packages in the project
    classifiers=[  # Optional list of classifiers to help categorize your project
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[  # List of dependencies that are required to run the package
        "numpy",  # Example dependency
    ],
    python_requires='>=3.6',  # Specify the minimum Python version required
    entry_points={  # Optional: if you want to define command-line tools for your package
        'console_scripts': [
            'mycommand=mypackage.module:main_function',  # Example of a CLI command
        ],
    },
)
