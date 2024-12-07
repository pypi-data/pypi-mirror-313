import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="petljapub",
    version="2.1.11",
    author="Filip Maric, Petlja",
    author_email="filip.maric@petlja.org",
    description="Petlja publishing system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/petljapub",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/petljapub/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=['invoke', 'requests', 'pyyaml', 'pypandoc', 'pandoc-xnos', 'pandoc-fignos',  'pandoc-eqnos', 'pandoc-tablenos', 'appdirs', 'matplotlib>=3.4', 'petlja-api'],
    entry_points={
        'console_scripts': ['petljapub = petljapub.main:program.run']
    },
    package_data={"petljapub": ["data/_task_template/*",
                                "data/_task_template/en/*",
                                "data/_task_template/sr-Cyrl/*",
                                "data/_task_template/sr-Latn/*",
                                "data/tgen/*",
                                "data/compile-cs.sh",
                                "data/template.yaml",
                                "data/html/*",
                                "data/md/*",
                                "data/tex/*"]}
)
