from setuptools import setup, find_packages
from tomli import load

# Read configuration from pyproject.toml
with open("pyproject.toml", "rb") as f:
    data = load(f)
    project_data = data["project"]
    version = project_data["version"]
    # Convert dependencies list to install_requires format
    # Handle version markers more robustly
    install_requires = [
        dep.split(";")[0].strip() 
        for dep in project_data["dependencies"]
        if not any(marker in dep for marker in ["python_version", "platform_system"])
    ]

setup(
    name="at-common-workflow",
    version=version,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=install_requires,
    python_requires=">=3.11",
)