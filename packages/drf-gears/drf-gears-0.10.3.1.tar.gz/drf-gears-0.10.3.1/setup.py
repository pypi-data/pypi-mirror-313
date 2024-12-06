import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drf-gears",
    version="0.10.3.1",
    author="Alexander Yudkin",
    author_email="san4ezy@gmail.com",
    description="Some gears collection for getting life a little bit better.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/san4ezy/drf-gears",
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
    install_requires=[
    ],
)
