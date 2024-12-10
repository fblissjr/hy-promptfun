from setuptools import setup, find_packages

setup(
    name="hy-promptfun",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
        "typer>=0.9.0",
        "rich>=10.0.0",
    ],
    entry_points={
        'console_scripts': [
            'hyprompt=hyprompt.cli:main',
        ],
    },
    description="A lightweight prompt generator matching Hunyuan's patterns",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hy-promptfun",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)