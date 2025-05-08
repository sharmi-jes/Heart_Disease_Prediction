from setuptools import find_packages,setup
from typing import List

HYPHEN_E_DOT="-e ."


# define the function for get requiremets
def get_requirements(file_path)->List[str]:
    '''This function is responsible for read all libraries and install them'''
    # requirements=[]

    
    with open(file_path) as file_obj:
        requirement=file_obj.readlines()
        requirement=[req.strip() for req in requirement]

        # check if hyphen e dot in requirements
        if HYPHEN_E_DOT in requirement:
    
            requirement.remove(HYPHEN_E_DOT)
    return requirement

setup(
    name="Heart_Disease_prediction",
    version="0.0.1",
    author="sharmi",
    author_email="anyumsharmila@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)