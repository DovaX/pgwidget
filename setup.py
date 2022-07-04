import setuptools
    
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='pgwidget',
    version='0.4.3',
    author='DovaX',
    author_email='dovax.ai@gmail.com',
    description='Widgets for pygame',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/DovaX/pgwidget',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'pygame','pandas','multinherit','doxyplot','remi'
     ],
    python_requires='>=3.6',
)
    