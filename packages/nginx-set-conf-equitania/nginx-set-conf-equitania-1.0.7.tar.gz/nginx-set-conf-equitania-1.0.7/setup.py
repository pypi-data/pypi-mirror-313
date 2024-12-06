import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nginx-set-conf-equitania",
    version="1.0.7",
    author="Equitania Software GmbH",
    author_email="info@equitania.de",
    description="A package to create configurations for nginx for different web applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["nginx_set_conf"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points="""
    [console_scripts]
    nginx-set-conf=nginx_set_conf.nginx_set_conf:start_nginx_set_conf
    """,
    install_requires=["click>=8.0.4", "PyYaml>=5.4.1"],
)
