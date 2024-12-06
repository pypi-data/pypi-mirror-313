from setuptools import setup

setup(
    name='bamboo_weather_mxtchapanda',
    version='1.0.0',
    description='Simple Weather Package for Python',
    author='Panda Bear',
    author_email='mxtchapanda@gmail.com',
    packages=['bamboo_weather'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ]
)