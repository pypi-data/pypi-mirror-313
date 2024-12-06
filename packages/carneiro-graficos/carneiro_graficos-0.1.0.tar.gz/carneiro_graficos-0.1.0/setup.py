from setuptools import setup, find_packages

setup(
    name="carneiro_graficos",
    version="0.1.0",
    author="Antonio Anerão",
    author_email="anerao.junior@gmail.com",
    description="Uma simples biblioteca para criar gráficos usando matplotlib",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/antonioanerao/carneiro_graficos",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "matplotlib",  # Adiciona a dependência do matplotlib
    ],
)
