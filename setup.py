from setuptools import setup, find_packages

setup(name='GTFS-flex-to-GOFS-lite',
      version='0.1.3',
      description='Convert GTFS Flex to GOFS lite',
      url='https://github.com/TransitApp/GTFS-flex-to-GOFS-lite',
      author='Nicholas Paun, Jonathan Milot',
      license='License :: OSI Approved :: MIT License',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          'py-gtfs-loader @ git+https://github.com/transitapp/py-gtfs-loader@v0.1.5'
      ])
