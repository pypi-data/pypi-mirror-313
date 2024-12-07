# setup.py
from setuptools import setup, find_packages

setup(
    name='nginx_set_conf',
    version='1.0.8',
    description='Ein Werkzeug zur Verwaltung von Nginx-Konfigurationen',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Equitania Software GmbH',
    author_email='info@equitania.de',
    url='https://github.com/equitania/nginx-set-conf',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'PyYAML',
    ],
    entry_points={
        'console_scripts': [
            'nginx-set-conf = nginx_set_conf.nginx_set_conf:start_nginx_set_conf',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

