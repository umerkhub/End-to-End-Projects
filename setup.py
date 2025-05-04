from setuptools import find_packages,setup
from typing import List


E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    This function will return list of requirments
    '''
    requirments=[]
    with open(file_path) as file_obj:
        requirments=file_obj.readlines()
        requirments=[req.replace("\n","") for req in requirments]

        if E_DOT in requirments:
            requirments.remove(E_DOT)

    return requirments


setup(
name='End to End Project',
version='0.0.1',
author='Umer Khan',
author_email='umairk2001@gmail.com',
packages=find_packages(),
install = get_requirements('requirements.txt')
)