from setuptools import setup

installation_requirements = [
    "pydantic==2.8.2",
    "pika==1.3.2"
]

setup(
    name="ratatosk_errands",
    description="errands for ratatosk",
    version="0.24",
    url="https://github.com/freeflock/ratatosk",
    author="(~)",
    package_dir={"": "packages"},
    packages=["ratatosk_errands"],
    install_requires=installation_requirements
)
