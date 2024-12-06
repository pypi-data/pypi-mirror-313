from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        name="bitads_security.checkers",
        sources=["bitads_security/checkers.pyx"],
    )
]

setup(
    name="bitads_security",
    version="0.2.2",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Cython module for secure hash checking",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sensitive_module",
    ext_modules=cythonize(extensions),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Cython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)