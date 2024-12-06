from setuptools import find_packages, setup

requires = [
    'boto3==1.34.130',
    'pandas==2.2.2',
    'sqlalchemy==2.0.31',
    'tenacity==8.5.0',
    'python-dotenv==0.18.0',
    'psycopg2-binary==2.9.9',
    'typeguard==4.3.0',  # to enforce types
]

linting_requires = ['flake8==7.1.0', 'isort==5.10.1', 'pre-commit', 'importlib_metadata==4.8.3']

testing_requires = [
    'pytest',
    'pytest-cov',
    'freezegun',
]

setup(
    name='tommytomato_operation_utils',
    version='2.0.0',
    description='Utility package for hash generation and database operations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='felix_bithero',
    author_email='felixl@bithero.com',
    url='https://github.com/felix_bithero/tommytomato_operation_utils',
    packages=find_packages(),
    install_requires=requires,
    extras_require={
        'linting': linting_requires,
        'testing': testing_requires,
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
