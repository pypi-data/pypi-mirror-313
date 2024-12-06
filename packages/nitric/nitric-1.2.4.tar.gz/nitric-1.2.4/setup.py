import setuptools
import re
from subprocess import Popen, PIPE


def get_current_version_tag():
    process = Popen(["git", "describe", "--tags", "--match", "v[0-9]*"], stdout=PIPE)
    (output, err) = process.communicate()
    process.wait()

    tags = str(output, "utf-8").strip().split("\n")

    version_tags = [tag for tag in tags if re.match(r"^v?(\d*\.){2}\d$", tag)]
    rc_tags = [tag for tag in tags if re.match(r"^v?(\d*\.){2}\d*-rc\.\d*$", tag)]

    if len(version_tags) == 1:
        return version_tags.pop()[1:]
    elif len(rc_tags) == 1:
        base_tag, num_commits = rc_tags.pop().split("-rc.")[:2]
        return "{0}.dev{1}".format(base_tag, num_commits)[1:]
    else:
        return "0.0.0.dev0"


with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="nitric",
    version=get_current_version_tag(),
    author="Nitric",
    author_email="team@nitric.io",
    description="The Nitric SDK for Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nitrictech/python-sdk",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    package_data={"nitric": ["py.typed"]},
    license_files=("LICENSE.txt",),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    setup_requires=["wheel"],
    install_requires=[
        "asyncio",
        "protobuf==4.23.3",
        "betterproto==2.0.0b6",
        "opentelemetry-api",
        "opentelemetry-sdk",
        "opentelemetry-exporter-otlp-proto-grpc",
        "opentelemetry-instrumentation-grpc",
    ],
    extras_require={
        "dev": [
            "tox==3.20.1",
            "twine==3.2.0",
            "pytest==7.3.2",
            "pytest-cov==4.1.0",
            "pre-commit==2.12.0",
            "black==22.3",
            "flake8==3.9.1",
            "flake8",
            "flake8-bugbear",
            "flake8-comprehensions",
            "flake8-string-format",
            "pydocstyle==6.0.0",
            "pip-licenses==3.3.1",
            "licenseheaders==0.8.8",
            "pdoc3==0.9.2",
            "markupsafe==2.0.1",
            "betterproto[compiler]==2.0.0b6",
            # "grpcio==1.33.2",
            "grpcio-tools==1.62.0",
            "twine==3.2.0",
            "mypy==1.3.0",
        ]
    },
    python_requires=">=3.11",
)
