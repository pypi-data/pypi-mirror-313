from setuptools import setup, find_packages
from tomli import load

# Read configuration from pyproject.toml
with open("pyproject.toml", "rb") as f:
    data = load(f)
    project_data = data["project"]
    version = project_data["version"]
    # Convert dependencies list to install_requires format
    # Remove any version-specific markers (e.g., python_version)
    install_requires = [
        dep.split(";")[0].strip() 
        for dep in project_data["dependencies"]
    ]

setup(
    name="at-common-workflow",
    version=version,
    packages=find_packages(),
    install_requires=install_requires,
)