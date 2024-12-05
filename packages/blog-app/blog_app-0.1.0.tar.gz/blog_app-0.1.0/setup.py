from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="blog-app",
    version="0.1.0",
    author="Team IT",
    author_email="y.karzal@campus.unimib.it",
    description="A simple blog application with Flask backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/y.karzal/2024_assignment2_blogpss",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
    ],
    python_requires=">=3.11",
    install_requires=[
        'flask>=3.1.0',
        'flask-sqlalchemy>=5.0.0',
        'flask-cors>=3.1.1',
        'python-dotenv>=1.0.1',
    ],
    entry_points={
        'console_scripts': [
            'blog-app=app:main',
        ],
    },
)