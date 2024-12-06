from setuptools import setup

setup(name='Pipx40',
      version='1.4',
      description='Python wrapper for Pickering PXI VISA-compliant driver',
      url='',
      author='Pickering Interfaces',
      author_email='support@pickeringtest.com',
      packages=['Pipx40', 'Examples'],
	  install_requires=[
          'pyvisa',
      ],
      zip_safe=False)