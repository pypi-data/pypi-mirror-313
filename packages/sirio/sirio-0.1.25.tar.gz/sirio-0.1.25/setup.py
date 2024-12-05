from setuptools import setup, find_packages

from distutils.core import setup
setup(
    name='sirio',
    packages=find_packages(),
    version='0.1.25',
    description='Sirio',
    author='Pasquale Rombolà',
    license='BSD',
    author_email='pasquale.rombola@cerved.com',
    url='https://github.com/pask-xx/sirio.git',
    keywords=['sirio', 'template', 'package', ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
    ],
    install_requires=['requests'],
)