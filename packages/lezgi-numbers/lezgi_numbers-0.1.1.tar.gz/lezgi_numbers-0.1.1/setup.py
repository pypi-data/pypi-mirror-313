from setuptools import setup, find_packages

setup(
    name='lezgi-numbers',
    version='0.1.1',
    description='A Python package for converting numbers to Lezgi numerals and back.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Kamran Tadzjibov',
    url='https://github.com/LekiTech/lezgi-numbers-python',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Localization',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='lezgi numbers conversion localization',
    python_requires='>=3.6',
)
