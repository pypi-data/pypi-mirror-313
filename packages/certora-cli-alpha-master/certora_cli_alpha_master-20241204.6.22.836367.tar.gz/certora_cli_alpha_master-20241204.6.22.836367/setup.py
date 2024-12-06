
import setuptools

setuptools.setup(
    name="certora-cli-alpha-master",
    version="20241204.6.22.836367",
    author="Certora",
    author_email="support@certora.com",
    description="Runner for the Certora Prover",
    long_description="Commit bd10584.                    Build and Run scripts for executing the Certora Prover on Solidity smart contracts.",
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/certora-cli-alpha-master",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['click', 'json5', 'pycryptodome', 'requests', 'rich', 'sly', 'tabulate', 'tqdm', 'StrEnum', 'tomli', 'universalmutator'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "certoraRun = certora_cli.certoraRun:entry_point",
            "certoraMutate = certora_cli.certoraMutate:mutate_entry_point",
            "certoraEqCheck = certora_cli.certoraEqCheck:equiv_check_entry_point"
        ]
    },
    python_requires='>=3.8',
)
