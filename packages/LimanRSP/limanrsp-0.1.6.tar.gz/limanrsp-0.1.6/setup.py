from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='LimanRSP',
  version='0.1.6',
  author='Nikita Besednyi',
  author_email='nikmac10x@gmail.com',
  description='Liman the realtime signal processing library',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://liman-trade.com',
  packages=find_packages(),
  install_requires=[
    'scipy==1.14.1'
  ],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='realtime signal processing',
  project_urls={
    'GitHub': 'https://github.com'
  },
  python_requires='>=3.6'
)