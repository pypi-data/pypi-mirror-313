import os
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

class CustomBuildPy(build_py):
    def run(self):
        # Generate git info
        os.system('python generate_git_info.py')
        # Continue with the regular build
        build_py.run(self)

setup(
    name='modelbest_sdk',
    version='0.3',
    author='HankyZhao',
    author_email='zhq980115@gmail.com',
    description='Everything about modelbest data include data format mbtable, dataset, dataloader, and tools',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://codeup.aliyun.com/64ddb0a87f62ff9b3d23ca15/modelbest_sdk',
    packages=find_packages(),
    cmdclass={'build_py': CustomBuildPy},
    package_data={'': ['git_info.txt']},
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
