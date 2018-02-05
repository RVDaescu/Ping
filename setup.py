from setuptools import setup

setup(name='Monitor App',
      version='0.1',
      description='Network monitoring tool',
      url='https://github.com/RVDaescu/Ping',
      author='Radu-V D',
      author_email='office@daescu.ro',
      license='Free',
      #packages=['gnu','mail', 'main', 'run', 'sql_lib', 'traffic', 'utils'],
      install_requires=['smtplib', 'base64', 'sqlite3', 'random', 'time', 'string',
                          'pexpect', 're', 'statistics', 'os', 'Gnuplot', 'scapy'],
      zip_safe=False)
