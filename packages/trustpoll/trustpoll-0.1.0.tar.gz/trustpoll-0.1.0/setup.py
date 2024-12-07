from setuptools import setup, find_packages

setup(
    name='trustpoll',
    version='0.1.0',
    author='Rishi Agarwal',
    author_email='maharishi459@gmail.com',
    description='Package for creating and interacting  with surveys on your applications',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RsAgBansal/blockchain',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
