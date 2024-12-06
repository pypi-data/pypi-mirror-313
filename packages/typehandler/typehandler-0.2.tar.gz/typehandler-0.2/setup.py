from setuptools import setup, find_packages

setup(
    name='typehandler',
    version='0.2',
    packages=find_packages(),
    install_requires=[],
    author='Prosamo',
    author_email='prosamo314@gmail.com',
    description='タイピングゲーム用のモジュール',
    long_description=open('README.md', encoding = 'utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/prosamo/typehandler',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)