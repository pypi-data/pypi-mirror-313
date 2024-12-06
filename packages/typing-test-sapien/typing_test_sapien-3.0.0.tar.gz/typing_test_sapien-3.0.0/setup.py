from setuptools import setup, find_packages

setup(
    name="typing-test-sapien",
    version="3.0.0",
    author="Prasad SDH",
    author_email="prasad@audiomob.com",
    description="A CLI-based typing speed test application",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/prasad-sdh/typing_test.git",
    packages=find_packages(),  # Automatically includes all packages with __init__.py
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "typing-test-sapien=typing_test.cli:main",  # Correctly points to the cli.py main function
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.1",
)