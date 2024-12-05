from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="insightconnect-plugin-runtime",
    version="6.2.2",
    description="InsightConnect Plugin Runtime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rapid7 Integrations Alliance",
    author_email="integrationalliance@rapid7.com",
    url="https://github.com/rapid7/komand-plugin-sdk-python",
    packages=find_packages(),
    install_requires=[
        "requests==2.32.2",
        "python_jsonschema_objects==0.5.2",
        "jsonschema==4.21.1",
        "certifi==2024.07.04",
        "Flask==3.0.2",
        "gunicorn==22.0.0",
        "greenlet==3.1.1",
        "gevent==24.10.1",
        "marshmallow==3.21.0",
        "apispec==6.5.0",
        "apispec-webframeworks==1.0.0",
        "blinker==1.7.0",
        "structlog==24.1.0",
        "python-json-logger==2.0.7"
    ],
    tests_require=[
        "pytest",
        "docker",
        "dockerpty",
        "swagger-spec-validator",
    ],
    test_suite="tests",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Software Development :: Build Tools",
    ],
)
