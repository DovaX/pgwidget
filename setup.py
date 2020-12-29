import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pgwidget", # Replace with your own username
    version="0.1.10",
    author="DovaX",
    author_email="dovax.ai@gmail.com",
    description="Widgets for pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DovaX/pgwidget",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    setup_requires=['setuptools_scm'],
    include_package_data=True,
)


