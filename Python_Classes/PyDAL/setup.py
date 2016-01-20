from distutils.core import setup
setup(name='pydal',
      version='3.1.0',
      packages=['pydal'],
      data_files=[('/etc', ['etc/serversetting.xml.empty'])],
      author='Kristopher Landon',
      author_email='landon.tek@gmail.com',
      description='Python Data Access Layer for connecting ODBC to all DBs and including postgresql,redshift,vertica,mssql',
      )


