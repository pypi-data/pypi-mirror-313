from setuptools import setup, find_packages

setup(
    name='traductor_cron',
    version='0.1.1',
    author='Claudiano Maniega',
    author_email='cmaniega@ovosoftware.cl',
    description='Una librería para traducir expresiones cron al español y calcular próximas ejecuciones.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ClauMS/traductor_cron',
    packages=find_packages(),
    install_requires=[
        'croniter',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
