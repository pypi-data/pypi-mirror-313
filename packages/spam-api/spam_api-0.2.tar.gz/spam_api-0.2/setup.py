from setuptools import setup, find_packages

setup(
    name="spam-api", 
    version="0.2",  # Versión de la librería
    packages=find_packages(),
    install_requires=[
        "fastapi", 
        "uvicorn", 
        "scikit-learn",
        "joblib", 
        "pandas", 
        "requests",
        "python-multipart" 
    ],
    author="Joaquin Vasquez",
    author_email="joacovasquez0@gmail.com",
    description="API para la detección de spam usando machine learning",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/limbow/spam-api",  # URL de tu repositorio
    classifiers=[ 
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        'console_scripts': [
            'spam-api=spam_api.anti_spam:run',
        ],
    },
    include_package_data=True,
)
