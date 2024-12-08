from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='disnake_dyn_components',
    version='0.1.1',
    author='Lord_Nodus',
    author_email='LordNodus@mail.ru',
    description="Module for quick creation of functional buttons for disnake",
    long_description=Path("readme.md").read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/NodusLorden/DisnakeDynComponents',
    packages=find_packages(),
    install_requires=["disnake>=2.9.2"],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='discord disnake',
    project_urls={},
    python_requires='>=3.11'
)
