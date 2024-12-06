from setuptools import setup, find_packages

setup(
    name="my_little_ansible",
    version="1.0.2",
    description="A mini Ansible-like tool for configuring remote hosts",
    author="Ton Nom",
    author_email="tonemail@example.com",
    packages=find_packages(),
    install_requires=[
        "paramiko",  # SSH
        "pyyaml",    # YAML
        "jinja2"     # templates
    ],
    entry_points={
        "console_scripts": [
            "mla=my_little_ansible.mla:main"  # `mla` for launch
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
