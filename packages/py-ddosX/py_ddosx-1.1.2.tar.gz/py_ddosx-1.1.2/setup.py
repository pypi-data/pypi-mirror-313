from setuptools import setup, find_packages

setup(
    name="py-ddosX",
    version="1.1.2",
    author="MohamedLunar",
    author_email="contact.mohamedlunardev@gmail.com",
    description="🔗 Package Guide On https://github.com/mohamedlunar/py-ddos3",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mohamedlunar/py-ddos3",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pyweb-server=pyweb:main",
        ]
    },
)
