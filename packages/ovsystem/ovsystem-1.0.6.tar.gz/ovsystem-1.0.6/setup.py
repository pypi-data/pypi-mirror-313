from setuptools import setup, find_packages

setup(
    name="ovsystem",
    version="1.0.6",
    author="ArsTech",
    author_email="arstechai@gmail.com",
    description="Online Variables System: Manage variables with Firebase",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/e500ky/ovs-system",  # Replace with your GitHub repository URL
    packages=find_packages(),  # Automatically finds packages in the project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "firebase-admin>=6.0.0",
        "python-dotenv>=1.0.0",
    ],
)
