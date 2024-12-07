from setuptools import find_packages, setup

with open("README.md") as readme_file:
    README = readme_file.read()

with open("HISTORY.md") as history_file:
    HISTORY = history_file.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup_args = dict(
    name='icds_data_definitions',
    version='0.0.13',
    description='Data definitions for IC Discovery Services as Pydantic objects',
    long_description_content_type="text/markdown",
    long_description=README + "\n\n" + HISTORY,
    license="Apache-2.0",
    packages=find_packages(),
    author="Dr. Hrishikesh Ballal",
    author_email="hrishikeshballal@yahoo.com",
    keywords=["ICDS"],
    url="https://github.com/openskies-sh/icds_data_definitions",
    download_url="https://pypi.org/project/icds_data_definitions/",
)

if __name__ == "__main__":
    setup(**setup_args, install_requires=required)
