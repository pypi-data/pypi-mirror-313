from setuptools import setup, find_packages

setup(
    name='peleren',  # Nom du package
    version='1.0.2',  # Version initiale
    description='A simple WSGI server optimized for AI applications',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Marc Arold ROSEMOND',
    author_email='rosemondmarcarold@gmail.com',
    url='https://github.com/Marc-Arold/peleren',  # Remplacez avec votre URL
    packages=find_packages(),  # Recherche automatique des packages
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # Placez ici vos dépendances comme Flask, Django, etc.
    ],
    entry_points={
        'console_scripts': [
            'wsgi-server=wsgi_server.server:main',  # Remplacez "main" par votre point d’entrée
        ],
    },
)
