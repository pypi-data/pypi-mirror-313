from setuptools import setup, find_packages
import os

setup(
    name='NavEcho',
    version='0.80.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'collect_logs=logger.NavEcho:collect_logs',  # Update this to match your logger's structure
        ],
    },
    author='aayush chaudhary',  # Replace with your actual name
    author_email='aayush.chaudhary@navikenz.com',  # Replace with your actual email
    description='A standalone library for collecting and logging errors from external applications.',
    long_description=open('README.md').read() if os.path.exists('README.md') else 'Long description missing.',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
