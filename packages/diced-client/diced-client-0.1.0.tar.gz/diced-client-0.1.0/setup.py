import setuptools

setuptools.setup(
    name="diced-client",
    version="0.1.0",
    packages=["diced"],
    install_requires=[
        "httpx==1.6.9",
        "pydantic==2.5.2",
    ],
)
