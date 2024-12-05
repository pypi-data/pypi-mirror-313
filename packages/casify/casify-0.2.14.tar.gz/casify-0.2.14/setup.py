import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="casify",
    version="0.2.14",
    author="René Alexander Ask",
    author_email="rene.ask@icloud.com",
    description="A CAS-library wrapped around sympy to simplify use of CAS-functionality in mathematics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/reneaas/casify",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "sympy",
        "plotmath",
        "numpy",
    ],
    python_requires=">=3.7",
)
