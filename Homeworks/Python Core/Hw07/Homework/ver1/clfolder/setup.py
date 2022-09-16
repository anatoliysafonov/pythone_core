from setuptools import setup

setup(
    name='clean_folder',
    version='1',
    description='User for clean any folder',
    url='https://github.com/anatoliysafonov/pythone_core/blob/main/Homeworks/Python%20Core/Hw07/Homework/clfolder/clfolder/clean.py',
    author='anatoliy safonov',
    author_email='anatoliy.safonov.ua@gmail.com',
    license='MIT',
    packages='',
    entry_points={'console_scripts': [
        'cleanfolder = clfolder.clean:main']}
)
