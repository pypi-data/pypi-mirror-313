# setup.py

from setuptools import setup, find_packages
from setuptools import setup, Extension
from setuptools import  find_namespace_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='il2pred',
    version='1.0.3',
    description='il2pred: A tool for predicting IL2 inducing or non-IL2 inducing peptides',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    author='Naman Kumar Mehta',
    author_email='namanm@iiitd.ac.in',
    url='https://github.com/namanm04/il2pred',
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'il2pred': ['Data/**/*']},
    entry_points={'console_scripts' : ['il2pred = il2pred.python_script.il2pred:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires= [ 'numpy', 'pandas', 'scikit-learn==1.5.2','tqdm','joblib' ]
)

