from setuptools import setup

setup(name='sweps-utils',
      version='0.1',
      description='SWEPS group code utilities',
      long_description='',
      url='http://github.com/hpmartins/sweps-utils',
      author='H. P. Martins',
      author_email='hpmartins@gmail.com',
      license='MIT',
      packages=['sweps_utils'],
      install_requires=[
          'numpy',
      ],
      include_package_data=True,
      zip_safe=False)
