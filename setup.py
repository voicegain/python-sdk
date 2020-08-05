import setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="voicegain-speech",
    version="0.0.1",
    author="Huishen Zhan, Kuo Zhang, Jacek Jarmulak",
    author_email="huishen@voicegain.ai, kuo@voicegain.ai, jacek@voicegain.ai",
    description="voicegain speech api python client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=REQUIRES,
    packages=setuptools.find_packages(),
    include_package_data=True,
)