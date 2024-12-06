from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='jamcalci',
  version='0.0.2',
  description='A basic calculator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/plain',  # Or 'text/markdown'
  url='https://github.com/ONKARJAMMA/Jamcalci',  # Update with your repository URL
  author='Onkar Jamma',
  author_email='onkarjamma1@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='calculator',
  packages=find_packages(),
  install_requires=[],  # No external dependencies
  python_requires='>=3.6'  # Optional, but good practice to specify the Python version
)
