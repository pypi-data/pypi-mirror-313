from setuptools import setup, find_packages, Extension

setup(
    name="BUILDER_ADDON_PCA",  # Replace with your package name (must be unique on PyPI)
    version="0.0.7",
    author="e-matica",
    author_email="software@e-matica.it",
    description="package for installation of PCA Addon on Seeq",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license="Custom",
    include_package_data=True,
    data_files=[('BUILDER_ADDON_PCA', ['BUILDER_ADDON_PCA/addon.json']),
                ('BUILDER_ADDON_PCA', ['BUILDER_ADDON_PCA/.credentials.json']),
                ('BUILDER_ADDON_PCA', ['BUILDER_ADDON_PCA/pca-addon-tool/Principal Component Analysis.ipynb']),
                ('BUILDER_ADDON_PCA/dist', ['BUILDER_ADDON_PCA/dist/com.seeq.pca-0.0.1.addon']),
                ('BUILDER_ADDON_PCA/dist', ['BUILDER_ADDON_PCA/dist/com.seeq.pca-0.0.1.addonmeta'])],

    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
