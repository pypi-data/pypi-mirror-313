from setuptools import setup, find_packages

setup(
    name="solugenerics",
    version="0.5.5",
    packages=find_packages(),
    install_requires=["Flask>=2.0.0", "python-dotenv==1.0.1", "loguru==0.7.2"],
    description="Reusable tools for Solugen workers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/solugenerics/",
    author="Elad Laor",
    author_email="elad.l@solugen.ai",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
