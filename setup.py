import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="greenhub",
    version="0.0.2",
    author="Alvaro Mateo",
    author_email="alvaromateo9@gmail.com",
    description="Tool that manages your local commits to push a few each day instead of all at the same time.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gbenejam/greenhub",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3"
    ),
    entry_points={
        'console_scripts': [
            'greenhub=greenhub:execute_script'
        ]
    }
)
