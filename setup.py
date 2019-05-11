import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="sprich",
    version="0.1",
    author="Lars Martens",
    author_email="contact@haselkern.com",
    description="A compiler for interactive dialogs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haselkern/sprich",
    packages=setuptools.find_packages(),
    install_requires=[
        "lark-parser==0.7.1",
    ],
    setup_requires=[
        "lark-parser==0.7.1",
    ],
    entry_points={
        "console_scripts": ['sprich=sprich.sprich:main'],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
)
