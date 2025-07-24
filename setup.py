import os
from setuptools import find_packages
from setuptools import setup

requirements = []

if os.path.isfile("requirements.txt"):
    with open("requirements.txt") as file:
        content = file.readlines()
    requirements.extend([x.strip() for x in content if 'git+' not in x])

setup(name="Nutricheck_FoodDB",
      version="0.0.1",
      author="Simon Fournier",
      author_email="simon.fournier64@gmail.com",
      description="Technical test Nutricheck",
      packages=find_packages(),
      install_requires=requirements,
      include_package_data=True,
      zip_safe=False
      )
