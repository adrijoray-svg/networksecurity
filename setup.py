from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    requirement_lst = []
    try:
        with open("requirements.txt",'r') as file:
            #Read lines from the file
            lines = file.readlines()
            ##Process each line
            for line in lines:
                requirement = line.strip()
                ##Ignore the empty lines and _e .
                if requirement and requirement!= "-e .":
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
    
    return requirement_lst

setup(
    name = "NetworkSecurity",
    version = "0.0.1",
    author = "Adrijo Ray",
    author_email = "adrijoray@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)