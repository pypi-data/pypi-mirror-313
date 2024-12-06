import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="is3_python_sdk",
    version="1.2.1",
    author="chaser",
    author_email="sxing.liu@foxmail.com",
    description="is3 python kafka server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['colorama==0.4.6',
                      'Flask==3.0.3',
                      'pydantic==2.9.1',
                      'confluent_kafka==2.3.0',
                      'Requests==2.32.3'
                      ],
    entry_points={
        'console_scripts': [
            'is3_run_app=app:main'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    include_package_data=True,
)
