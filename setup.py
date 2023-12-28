from setuptools import setup, find_packages

setup(
    name='sfbugs',
    version='1.0.0',
    author='Mehmet Yilmaz',
    author_email='email@example.com',
    description='A tool to scan and flag sensitive data in files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MehmetMHY/sfbugs',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'phonenumbers==8.13.26',
        'PyMuPDF==1.23.3',
    ],
    entry_points={
        'console_scripts': [
            'sfbugs = sfbugs.main:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

