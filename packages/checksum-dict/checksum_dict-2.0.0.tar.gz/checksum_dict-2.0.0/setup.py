from setuptools import setup, find_packages

setup(
    name="checksum_dict",
    description="checksum_dict's objects handle the simple but repetitive task of checksumming addresses before setting/getting dictionary values.",
    author="BobTheBuidler",
    author_email="bobthebuidlerdefi@gmail.com",
    url="https://github.com/BobTheBuidler/checksum_dict",
    packages=find_packages(),
    use_scm_version={
        "root": ".",
        "relative_to": __file__,
        "local_scheme": "no-local-version",
        "version_scheme": "python-simplified-semver",
    },
    setup_requires=["setuptools_scm"],
    install_requires=["cchecksum>=0.0.3"],
    package_data={
        "checksum_dict": ["py.typed"],
    },
    include_package_data=True,
)
