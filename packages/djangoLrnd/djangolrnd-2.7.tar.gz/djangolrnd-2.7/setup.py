from setuptools import setup, find_packages

setup(
    name='djangoLrnd',
    version='2.7',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A Django middleware for LRND validation.',
    author='Lrnd',
    author_email='hafiztamvan15@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django',
        'requests',
        'cryptography',
    ],
)
