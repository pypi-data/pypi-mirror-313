from setuptools import setup, find_packages

setup(
    name='componentsDjangoType',
    version='2.0.32',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Comandos para crear archivos html, css y js',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jose-CR/componentsDjangoType',
    author='Alejandro',
    author_email='hjosealejandro21@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django :: 3.2',
    ],
    install_requires=[
        'Django>=3.2',
    ],
)
