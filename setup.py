from setuptools import find_packages,setup
from typing import List

HYPHEN_E_DOT='-e .'

def get_requirements(file_path:str)->List[str]:
    requirements=[]
    with open(file_path,'r') as file_obj:
        requirement=file_obj.readlines()
        requirements=[line.replace('\n','') for line in requirement]

    if HYPHEN_E_DOT in requirements:
        requirements.remove(HYPHEN_E_DOT)
    return requirements
setup(
    name='Sensor Fault Prediction Model',
    version='1.0.0',
    author='Dyuti Dutta',
    author_email='duttadyuti4@gmail.com',
    packages=find_packages(),
    description='Sensor Fault Prediction Model',
    install_requires=get_requirements('requirements.txt')
)