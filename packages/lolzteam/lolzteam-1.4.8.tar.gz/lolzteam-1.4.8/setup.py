import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ["pydantic", "httpx", "httpx[http2]", "httpx[socks]"]

setuptools.setup(
    name="lolzteam",
    version="1.4.8",
    author="AS7RID",
    author_email="as7ridwork@gmail.com",
    description="A library that contains all the methods of the Lolzteam API (Market/Forum/Antipublic)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AS7RIDENIED/LOLZTEAM",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=["Programming Language :: Python :: 3.11"],
    python_requires='>=3.9'
)
