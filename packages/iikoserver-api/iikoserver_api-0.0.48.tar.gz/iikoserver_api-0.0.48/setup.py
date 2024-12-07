from setuptools import setup, find_packages

setup(
    name="iikoserver_api",
    version="0.0.48",
    packages=find_packages(),
    install_requires=['pydantic>=2.0.0', 'requests>=2.22.0', 'xmltodict>=0.12.0'],
    author="Eugene",
    author_email="zenjagems@gmail.com",
    description="iikoserver api connector",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/sizlik/iikoserver_api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)

