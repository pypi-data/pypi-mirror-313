from setuptools import setup

setup(
    name="hello_pckg",
    version="0.2",
    packages=["hello_pckg"],
    description="Hello ouou!",
    author="Omar",
    author_email="omarfessy@gmail.com",
    install_requires=[],
    entry_points={ "console_scripts": ["hello=hello_pckg.main:hello"] }
)
