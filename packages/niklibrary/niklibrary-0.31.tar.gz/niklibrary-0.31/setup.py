from setuptools import setup, find_packages

setup(
    name="niklibrary",
    version="0.31",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.sh', '*.yml'],
        'NikGapps.helper': ['assets/*'],
        'NikGapps.helper.assets': ['*'],
    },
    author="Nikhil Menghani",
    author_email="nikhil@menghani.com",
    description="A short description of your project",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/nikhilmenghani/niklibrary",
    install_requires=[
        'colorama~=0.4.6',
        'pytz~=2024.2',
        'setuptools~=75.3.0',
        'nikassets~=0.10',
        'GitPython~=3.1.43',
        'PyGithub~=2.4.0',
        'python-gitlab~=5.0.0',
        'beautifulsoup4==4.12.3',
        'requests~=2.32.3',
        'python-dotenv~=1.0.1',
        'pysftp~=0.2.9',
        'pexpect~=4.9.0',
        'psutil~=6.1.0',
        'cryptography~=43.0.3'
    ],
    entry_points={
        'console_scripts': [
            'niklibrary=main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.12',
)