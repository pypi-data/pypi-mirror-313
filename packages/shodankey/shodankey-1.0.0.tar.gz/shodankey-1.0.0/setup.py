from setuptools import setup, find_packages

setup(
    name='shodankey',
    version='1.0.0',
    description='A package to validate and retrieve information from the Shodan API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Fidal',
    author_email='mrfidal@proton.me',
    url='https://github.com/ByteBreach/shodankey',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    keywords=[
        'shodan',
        'MrFidal',
        'api',
        'security',
        'network-scanning',
        'information-gathering',
        'api-key-validation'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Security',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
