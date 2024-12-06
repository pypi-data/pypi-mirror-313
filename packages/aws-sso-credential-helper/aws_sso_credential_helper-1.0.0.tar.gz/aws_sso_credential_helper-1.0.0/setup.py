from setuptools import setup, find_packages

def requirements_from_file(file_name):
    return open(file_name).read().splitlines()

with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()
LONG_DESCRIPTION = readme

setup(
    name='aws_sso_credential_helper',
    author='nbtd',
    author_email="baconss11@gmail.com",
    url = 'https://github.com/nbtd/aws-sso-credential-helper',
    license='MIT',
    python_requires='>=3.6',
    version='1.0.0',
    keywords='aws sso credential helper',
    packages=find_packages(),
    install_requires=requirements_from_file('requirements.txt'),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.12'
        ],
    long_description=LONG_DESCRIPTION,    
    long_description_content_type='text/markdown'
)