from setuptools import setup, find_packages

setup(
    name='dsfns',  # The name of your package
    version='3.0',
    author='Mafia',
    author_email='zeta9097@gmail.com',
    description='data Preprocessing fns',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/zeta9097/fns',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
