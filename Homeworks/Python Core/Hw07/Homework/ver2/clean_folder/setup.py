from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='2',
    description='Usefull for clean folder',
    url='',
    author='anatoliy safonov',
    author_email='antoliy.safonov.ua@gmail.com',
    entry_points={'console_scripts': [
        'clean = clean_folder.main:main']}
)
