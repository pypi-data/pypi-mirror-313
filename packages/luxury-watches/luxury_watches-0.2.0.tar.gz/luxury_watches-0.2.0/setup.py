from setuptools import setup, find_packages

setup(
    name="luxury_watches",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'get-watch=luxury_watches.main:get_watch_name',
        ],
    },
    author="James Montague",
    author_email="james@coveted.com",
    description="A package to get random watch information",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
        'luxury_watches': ['db.json'],
    },
    project_urls={
        'Homepage' : 'https://www.coveted.com/watches',
    },
)
