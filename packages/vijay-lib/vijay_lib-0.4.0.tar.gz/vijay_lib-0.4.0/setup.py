from setuptools import setup, find_packages

setup(
    name="vijay_lib",               # Name of your library
    version="0.4.0",                # Initial version
    author="Vijayraje Jadhav",      # Your name
    author_email="jadhavvijayraje1137@gmail.com",  # Your email
    description="A library to calculate upper and lower IQR values.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/vijay_lib",  # Replace with your GitHub repo
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["numpy"],  # External dependencies
)

