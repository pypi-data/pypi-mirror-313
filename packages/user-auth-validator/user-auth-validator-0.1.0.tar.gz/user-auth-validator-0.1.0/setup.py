from setuptools import setup, find_packages

setup(
    name="user-auth-validator",
    version="0.1.0",
    description="A library for validating usernames, emails, and passwords.",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/user-auth-validator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)