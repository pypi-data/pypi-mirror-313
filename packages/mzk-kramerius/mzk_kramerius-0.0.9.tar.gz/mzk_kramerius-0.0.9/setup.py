from setuptools import setup, find_packages

setup(
    name="mzk_kramerius",
    version="0.0.9",
    description="Partial Kramerius client for Kramerius version v7.0.39",
    author="Robert Randiak",
    author_email="randiak@mzk.com",
    packages=find_packages(),
    install_requires=["lxml", "pydantic", "requests"],
    setup_requires=["wheel"],
    python_requires=">=3.6",
)
