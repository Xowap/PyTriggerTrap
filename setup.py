import os
import codecs
from distutils.core import setup
from pip.req import parse_requirements
from pip.download import PipSession

with codecs.open(os.path.join(os.path.dirname(__file__), 'README.txt'), 'r') as readme:
    README = readme.read()

requirements = parse_requirements(
    os.path.join(os.path.dirname(__file__), 'requirements.txt'),
    session=PipSession()
)

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='pytriggertrap',
    version='0.1.0',
    packages=[
        'pytriggertrap',
    ],
    scripts=[
        'bin/pytt',
    ],
    include_package_data=True,
    license='WTFPL',
    description='Control a TriggerTrap device without the smartphone app.',
    long_description=README,
    url='https://github.com/Xowap/PyTriggerTrap',
    author='Rémy Sanchez',
    author_email='remy.sanchez@hyperthese.net',
    install_requires=[str(x.req) for x in requirements],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Development Status :: 3 - Alpha',
    ]
)
