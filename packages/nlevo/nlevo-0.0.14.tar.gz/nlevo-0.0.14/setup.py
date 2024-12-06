from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='nlevo',
    version='0.0.14',
    author='nextlab',
    author_email='swhan@nextlab.co.kr',
    description='Common library for evo.B',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=['python-dateutil==2.8.2',
                    'paramiko==3.4.0',
                    'pytz==2024.1',
                    'python-dotenv==1.0.1',
                    'pika==1.3.2'],
    python_requires=">=3.8",
    packages=find_packages()
)
