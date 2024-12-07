from setuptools import setup, find_packages

setup(
    name="website-monitoring-software",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "requests",
        "beautifulsoup4",
        "pandas",
        "openpyxl",
        "reportlab",
        "lxml",
    ],
    entry_points={
        'console_scripts': [
            'website-monitor=main:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="",
    author="Name",
    author_email="youremail@example.com",
    license="MIT",
)
