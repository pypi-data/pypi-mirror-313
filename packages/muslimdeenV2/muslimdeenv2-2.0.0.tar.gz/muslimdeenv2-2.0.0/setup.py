from setuptools import setup, find_packages

# Lire les dépendances depuis requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

# Lire le README.md pour la description longue
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='muslimdeenV2',
    version='2.0.0',
    packages=find_packages(),
    install_requires=required,
    description='MuslimDeen: Package pour gérer les sourates, noms d\'Allah, ablutions et salat',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="personne monsieur",
    author_email="monsieurnobody01@gmail.com",
    url='https://gitlab.com/misternobody01/muslimdeen#',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
