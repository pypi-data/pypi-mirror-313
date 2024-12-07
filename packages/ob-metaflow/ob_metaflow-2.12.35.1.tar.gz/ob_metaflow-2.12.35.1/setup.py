from setuptools import setup, find_packages

with open("metaflow/version.py", mode="r") as f:
    version = f.read().splitlines()[0].split("=")[1].strip(" \"'")

setup(
    include_package_data=True,
    name="ob-metaflow",
    version=version,
    description="Metaflow: More Data Science, Less Engineering",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Netflix, Outerbounds & the Metaflow Community",
    author_email="help@outerbounds.co",
    license="Apache License 2.0",
    packages=find_packages(exclude=["metaflow_test"]),
    py_modules=[
        "metaflow",
    ],
    package_data={
        "metaflow": [
            "tutorials/*/*",
            "plugins/env_escape/configurations/*/*",
            "py.typed",
            "**/*.pyi",
        ]
    },
    entry_points="""
        [console_scripts]
        metaflow=metaflow.cmd.main_cli:start
      """,
    install_requires=[
        "requests",
        "boto3",
        "pylint",
        "kubernetes",
    ],
    extras_require={
        "stubs": ["metaflow-stubs==%s" % version],
    },
)
