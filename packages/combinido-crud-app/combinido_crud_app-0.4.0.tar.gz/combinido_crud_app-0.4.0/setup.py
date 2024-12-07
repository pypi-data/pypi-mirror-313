from setuptools import setup, find_packages

setup(
    name="combinido_crud_app",  # Name of the package
    version="0.4.0",  # Package version
    packages=find_packages(),  # Automatically finds packages in the directory
    install_requires=[  # List dependencies here
        "ttkbootstrap"
    ],
    entry_points={  # Entry point for your app (if it's a command-line tool)
        "console_scripts": [
            "combinido_crud_app = combinido_crud_app.main:main",  # Points to the `main()` function
        ],
    },
    author="Rico Combinido",
    author_email="ricocombinido9@gmail.com",
    description="A simple database CRUD application with SQLite and TKinter",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)