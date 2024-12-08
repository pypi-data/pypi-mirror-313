from setuptools import setup, find_packages


setup(
    name="chatterpyv1",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'faiss-cpu',  
        'sentence-transformers',
        'openai',
        'numpy',
    ],
    author="Mamlesh",
    author_email="mamleshsurya6@gmail.com",
    description="A Python library for FAISS indexing and OpenAI query processing.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mamlesh18/chatterPy",  # Update with your GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
