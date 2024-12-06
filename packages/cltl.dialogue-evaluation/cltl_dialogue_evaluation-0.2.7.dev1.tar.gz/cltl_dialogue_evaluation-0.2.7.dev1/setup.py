from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as fh:
    version = fh.read().strip()

setup(
    name="cltl.dialogue_evaluation",
    description="The Leolani Language module for evaluating interactions",
    version=version,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leolani/cltl-dialogueevaluation",
    license='MIT License',
    authors={
        "Baez Santamaria": ("Selene Baez Santamaria", "s.baezsantamaria@vu.nl"),
        "Baier": ("Thomas Baier", "t.baier@vu.nl")
    },
    package_dir={'': 'src'},
    packages=find_namespace_packages(include=['cltl.*'], where='src'),
    package_data={'cltl.dialogue_evaluation': ['data/*']},
    python_requires='>=3.7',
    install_requires=[
        'rdflib~=6.1.1',
        'networkx~=2.6.3',
        'numpy~=1.21.5',
        'pandas',
        'scipy~=1.7.3',
        'seaborn~=0.11.2',
        'transformers~=4.19.4',
        'emissor~=0.0.dev5',
        'torch~=1.11.0'
    ],
    setup_requires=['flake8']
)
