from setuptools import setup, find_packages
import configparser
#from bomancli.Config import Config

config = configparser.ConfigParser()
config.read('setup.cfg')
environment = config['metadata']['environment']
version = config['metadata']['version']
name = config['metadata']['name']
base_url = config['metadata']['saas_base_url']
#Config.boman_base_url = base_url

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()



entry_points = {}

if environment == 'uat':
    entry_points = {
        'console_scripts': ['boman-cli-uat=bomancli.main:default'],
    }
elif environment == 'prod':
    entry_points = {
        'console_scripts': ['boman-cli=bomancli.main:default'],
    }
else:
     entry_points = {
        'console_scripts': ['boman-cli-uat=bomancli.main:default'],
    }


setup(
    name= name,
    version=version,    
    description='CLI tool of boman.ai',
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://boman.ai',
    author='Sumeru Software Solutions Pvt. Ltd.',
    author_email='support@boman.ai',
    license='BSD 2-clause',
    entry_points = entry_points,
    packages=['bomancli'],
    package_data={'bomancli': ['templates/template_plan.yaml']},
    install_requires=['docker<=7.0.0',
                      'requests<=2.31.0',
                      'pyyaml',
                      'coloredlogs<=15.0.1','xmltodict<=0.13.0','pyfiglet<=1.0.2'                     
                      ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: OS Independent',        
    ],
)
