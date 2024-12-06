from setuptools import setup, find_packages

setup(
    name="PyLinkedList2905", 
    version="0.1.7",  
    description="A simple linked list implementation in Python",
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown',
    author="RAKOTONIRINA Manankasina Nomentsoa",
    author_email="nomentsua@gmail.com",
    url="https://github.com/Nouments/linked_list",  
    packages=find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    install_requires=[],  
    python_requires=">=3.6", 
)
