import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0' #Versión de la librería
PACKAGE_NAME = 'mderanklib' #Debe coincidir con el nombre de la carpeta 
AUTHOR = 'Pablo Calleja'
AUTHOR_EMAIL = 'pablo@gmail.com' 
URL = 'https://github.com/oeg-upm/mderanklib' 

LICENSE = 'Apache' #Tipo de licencia
DESCRIPTION = 'Librería para realizar ranking multilingüe de entidades.' #Descripción corta
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') 
LONG_DESC_TYPE = "text/markdown"


#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
    #'numpy>=1.21.0',
    #'scikit-learn>=1.0',
    #'pandas>=1.3.0',
    #'nltk>=3.6.0',

    'pandas==1.3.5',
    'StanfordCoreNLP==3.9.1.1',
    'transformers==4.37.2',
    'accelerate==0.5.1',
    #'git+https://github.com/boudinfl/pke.git'
    'pke==2.0.0',
    'torch==2.1.2',
    'torchvision==0.16.2',
    'torchaudio==2.1.2',
    #--index-url https://download.pytorch.org/whl/cpu
    'nltk==3.8.1',
    'allennlp==3.1.0'
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)
