from setuptools import setup, find_packages

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="lightshow",
    version="1.0.0",
    description="Simple music visualisation for Holiday LED lights",
    long_description=long_description,
    url="https://github.com/spikelynch/lightshow"
    packages=find_packages()

        # Author details
    author='Mike Lynch',
    author_email='Michael.Lynch@uts.edu.au',

    # Choose your license
    license='GPL3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Hobbyists',
        'License :: OSI Approved :: GPL3',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='visualisation music audio',

    py_modules=[],

    install_requires=[
        'pyaudio', 'numpy'
        ],

    package_data={},

    test_suite='nose.collector',
    tests_require=['nose'],
    

)

