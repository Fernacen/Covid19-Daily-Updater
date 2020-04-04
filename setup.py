from setuptools import setup

setup(name='Covid19-Daily-Updater',
      version='0.1',
      url='https://github.com/Fernacen/Covid19-Daily-Updater',
      author='Fernacen',
      description='A Covid19 tracker that sends text messages to your phone',
      license='MIT',
      keywords='covid19 coronavirus',
      packages=['Covid19-Daily-Updater'],
      install_requires=[
          'boto3',
          're',
          'os',
          'csv',
          'sqlite3',
          'pycryptodome',
          'enum',
          'requests'
          'datetime'
      ]
)