import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mtunn',
    packages=['mtunn'],
    version='1.1.9',
    python_requires=">=3.6",
    license='Apache 2.0',
    description='Easy open tcp, http ports from localhost to internet.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='MishaKorzhik_He1Zen',
    author_email='developer.mishakorzhik@gmail.com',
    url='https://github.com/mishakorzik/mtunn',
    project_urls={
        "Bug Tracker": "https://github.com/mishakorzik/mtunn/issues",
        "Donate": "https://www.buymeacoffee.com/misakorzik"
    },
    install_requires=["requests>=2.25.0", "PyYAML>=6.0.1", "ipaddress>=1.0.21"],
    keywords=["linux" ,"windows", "make", "mtunn", "tcp", "http", "open", "port", "easy", "tunnel", "alpha", "beta","stable", "pip", "pypi", "ping", "firewall", "domain", "vpn", "tor", "console", "control", "ipv4", "ipv6"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
    ],

)
