from setuptools import setup, find_packages
setup(
    name="pgEdge_pulumi_pgedge",
    version="0.0.33",
    packages=find_packages(),
    install_requires=[
        "pulumi>=3.0.0,<4.0.0",
    ],
)
