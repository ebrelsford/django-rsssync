from setuptools import setup, find_packages
import os

import rsssync


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
]

setup(
    author='Eric Brelsford',
    author_email='ebrelsford@gmail.com',
    name='rsssync',
    version=rsssync.__version__,
    description="Synchronize with an external RSS source.",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    url='https://github.com/ebrelsford/django-rsssync/',
    license='License :: OSI Approved :: BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'Django>=1.6.1',
        'django-classy-tags==0.4',
        'feedparser>=5.1.3',
    ],
    packages=find_packages(),
    include_package_data=True,
)
