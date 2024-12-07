from setuptools import setup, find_packages

setup(
    name="pyawscronversion1",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    description="A customized version of pyawscron limited to DXC",
    author="AWS Platform Engineering",
    author_email="abc@example.com",
    url="https://github.com/pitchblack408/pyawscron.git",
    python_requires=">=3.6",
    install_requires=["python-dateutil>=2.8.1"],
)
