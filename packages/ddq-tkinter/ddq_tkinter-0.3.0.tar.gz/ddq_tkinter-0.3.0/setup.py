from setuptools import setup, find_packages

setup(
    name="ddq_tkinter",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        'tkinter',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
    test_suite='tests',
    python_requires='>=3.6',
) 