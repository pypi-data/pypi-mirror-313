from setuptools import setup, find_packages

setup(
    name="typing-test-sapien",
    version="3.0.1",
    author="Prasad SDH",
    author_email="prasad@audiomob.com",
    description="A CLI-based typing speed test application",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/prasad-sdh/typing_test.git",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add dependencies here, e.g.,:
        # "requests>=2.25.1"
    ],
    entry_points={
        "console_scripts": [
            "typing-test-sapien=typing_test.cli:main",  # Links the CLI command to your `main` function
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.1",  # Minimum Python version
)