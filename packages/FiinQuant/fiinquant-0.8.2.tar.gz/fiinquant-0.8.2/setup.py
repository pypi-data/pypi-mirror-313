from setuptools import setup, find_packages

setup(
    name='FiinQuant',
    version='0.8.2',
    packages=find_packages(),
    description='A Simple indicator library for stock tickers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='NgocAn',
    author_email='anlam9614@gmail.com',
    install_requires=['requests', 'pandas', 'numpy','signalrcore'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)

# python setup.py sdist bdist_wheel

### Officical

# twine upload dist/*
# pypi-AgEIcHlwaS5vcmcCJDU2NDIxZjcwLWM2YTUtNDlmYS1hYjVmLTE5ZmFiMjVmZjcwMwACKlszLCI5YTc2YzRmMi0xMmI3LTQ3NWItYjY1ZS03ZjFiMWMyMzVmNzUiXQAABiAuqTmRLdREvJzCGjiGcWkz987IzkLy7c54rmJHXFOKVA

### Testing

# twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# pypi-AgENdGVzdC5weXBpLm9yZwIkN2Q1ZTE5ZDQtZWRlNC00YmJjLWI4OTMtMzg5MDMyZTJjNTAwAAIqWzMsIjk1YzY2ZjY4LTgzZTMtNGNkZS1iZGJkLWIwNGM3ZDNiMGUxMSJdAAAGIOJAtZSe398TqMradwFtIguM3zr52fphUfkY1o9ODAiW