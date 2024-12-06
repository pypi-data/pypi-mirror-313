from setuptools import setup
import os

base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

setup(
  name = 'py-EasyClean',         
  packages = ['EasyClean'],   
  version =  'v1.1.1',            
  description = 'EasyClean - Automated Data Preprocessing & Cleaning using python', 
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Junaid Ahmed',                  
  author_email = 'ahmedjunaid109@gmail.com', 
  url = 'https://github.com/Junaidd-Ahmedd109/EasyClean', 
  keywords = ['automated', 'cleaning', 'preprocessing', "Easyclean"],  
  install_requires=[          
          'scikit-learn',
          'numpy',
          'pandas',
          'loguru'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',   
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',    
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)