from setuptools import setup, find_packages

setup(
    name="flask-structure-creator",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "create-flask-structure=flask_structure_creator.creator:create_flask_folder_structure",
        ],
    },
    author="Your Name",
    author_email="your_email@example.com",
    description="A library to create Flask project folder structure.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/flask-structure-creator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
