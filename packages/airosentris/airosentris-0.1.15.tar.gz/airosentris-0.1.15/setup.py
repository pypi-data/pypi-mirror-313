from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='airosentris',
    version='0.1.15',
    description='A sentiment analysis platform with AI runner and trainer components',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/sindika/project/airosentris/airosentris-python-lib',
    author='Willy Achmat Fauzi',
    author_email='willy.achmat@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
