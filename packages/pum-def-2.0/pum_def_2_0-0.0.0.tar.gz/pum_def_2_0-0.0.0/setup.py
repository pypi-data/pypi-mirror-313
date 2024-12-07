from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='pum-def-2.0',
  version='0.0.0',
  author='USEC',
  author_email='karasevich.evg903@gmail.com',
  description='',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.13',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='',
  project_urls={

  },
  python_requires='>=3.13.1'
)