from setuptools import setup, find_packages

setup(
    name='Reado',
    version='0.1',
    description='A CLI tool to generate README files based on project structure and configuration',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='Pezhvak', 
    author_email='m.8562.m@gmail.com', 
    url='https://github.com/pezhvak98/Reado',
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    keywords="CLI, project-structure, readme-generator",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'reado=reado.main:main',
        ],
    },
    install_requires=[
        'requests',
        'nimblex'  
    ],
    python_requires='>=3.6', 
    project_urls={
        "Bug Reports": "https://github.com/pezhvak98/Reado/issues",
        "Source": "https://github.com/pezhvak98/Reado",
    }, 
)
