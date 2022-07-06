from setuptools import setup, find_packages

setup(name='GTFS-flex-to-GOFS-lite',
      version='0.0.1',
      description='Convert GTFS Flex to GOFS lite',
      url='https://github.com/TransitApp/GTFS-flex-to-GOFS-lite',
      author='Jonathan Milot',
      license='License :: OSI Approved :: MIT License',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          # 'py-gtfs-loader'
      ])