from setuptools import setup, find_packages

setup(
    name='artifact_map',
    version='0.3',
    packages=find_packages(),  # Automatically discovers all packages in your directory
    install_requires=[         # External dependencies
        'numpy', 'pandas'
    ],
    description="A short description of your package",
    # long_description=open('README.md').read(),  # Optional: If you have a README.md
    # long_description_content_type='text/markdown',  # Optional: Format of the README
    author="shashankSS1205",
    author_email="shashankshekharsingh1205@gmail.com",
    # url="https://github.com/yourusername/your_package_name",  # Optional: URL to your package repository
    # classifiers=[              # Optional: Additional metadata
    #     'Programming Language :: Python :: 3',
    #     'License :: OSI Approved :: MIT License',
    #     'Operating System :: OS Independent',
    # ],
)
