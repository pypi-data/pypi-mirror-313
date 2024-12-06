from setuptools import setup

# Read dependencies from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:  # Ensure proper encoding
    requirements = f.read().splitlines()

setup(
    name="Credito_SQLViaCode",  # The name of your package
    version="0.2.1",  # Incremented version to avoid conflicts
    description="A Python package to execute SQL queries and procedures and manage backups.",
    long_description=open("README.md", "r", encoding="utf-8").read(),  # Ensure proper encoding
    long_description_content_type="text/markdown",
    author="Afik Ratzon",
    author_email="afik.ratzon@gmail.com",
    packages=["Credito_SQLViaCode"],  # Automatically find all packages
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    install_requires=requirements,  # Use dependencies from requirements.txt
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Ensure compatibility with Python versions >= 3.6
)
