from setuptools import setup, find_packages

setup(
    name='opmentis',
    version='0.1.9',
    author='opmentis',
    author_email='admin@opmentis.xyz',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',  # Ensure you include all necessary dependencies
    ],
    python_requires='>=3.6',
    description='Library to register opmentis miners and check data and start new chat and many more',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/OpMentis-Ai',  # Replace with the URL to your project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)