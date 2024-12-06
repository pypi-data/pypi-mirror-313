from setuptools import setup, find_packages

setup(
    name="genopen",
    version="1.1.0",
    author="Mathieu Bourgois",
    author_email="bourgois.mathieu+genopen@gmail.com",
    description="Markdown to blog generator",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MathieuBourgois/genopen/',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "click==8.1.7",
        "Markdown==3.7",
        "PyYAML==6.0.2",
    ],
    entry_points={
        'console_scripts': [
            'genopen=genopen.cli:cli',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
