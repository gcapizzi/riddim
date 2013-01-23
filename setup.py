from distutils.core import setup

setup(
    name='riddim',
    version='0.1.0',
    author='G. Capizzi',
    author_email='g.capizzi@gmail.com',
    packages=['riddim'],
    scripts=['bin/riddim'],
    description='A command-line tool to get info about reggae songs.',
    install_requires=[
        "beautifulsoup4 >= 4.1.3",
        "requests >= 1.1.0"
    ],
)
