import os

from setuptools import setup, find_packages

setup(
    name="sqlalchemy-hsqldb",
    version="0.1.0",
    description="SQLAlchemy dialect for HyperSQL 2.0 (HSQLDB)",
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    author="Pebble94464",
    author_email="sqlalchemy-hsqldb@pebble.plus.com",
    license="MIT",
    url="https://github.com/Pebble94464/sqlalchemy-hsqldb",
    classifiers=[
		'Development Status :: 4 - Beta',
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Topic :: Database :: Front-Ends",
		"Operating System :: OS Independent",
    ],
    keywords="SQLAlchemy dialect hsqld hsqldb hypersql",
    project_urls={
        "Documentation": "https://github.com/Pebble94464/sqlalchemy-hsqldb/wiki",
        "Source": "https://github.com/Pebble94464/sqlalchemy-hsqldb",
        "Tracker": "https://github.com/Pebble94464/sqlalchemy-hsqldb/issues",
    },
    packages=find_packages(include=["sqlalchemy_hsqldb"]),
    include_package_data=True,
    install_requires=["SQLAlchemy", "jaydebeapi-hsqldb"],
    zip_safe=False,
    entry_points={
        "sqlalchemy.dialects": [
            "hsqldb.jaydebeapi = sqlalchemy_hsqldb.jaydebeapi:HyperSqlDialect_jaydebeapi",
        ]
    },
)

