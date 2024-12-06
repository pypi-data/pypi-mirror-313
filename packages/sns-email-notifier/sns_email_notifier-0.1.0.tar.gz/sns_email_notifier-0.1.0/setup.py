from setuptools import setup, find_packages

setup(
    name='sns-email-notifier',
    version='0.1.0',
    description='A library to send email notifications via AWS SNS.',
    author='Aakash',
    author_email='aakashbabu75399@gmail.com',
    packages=find_packages(),
    install_requires=['boto3'],
    python_requires='>=3.6',
    
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
