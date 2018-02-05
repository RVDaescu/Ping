from setuptools import setup

setup(name='Monitor App',
      version='0.1',
      description='Network monitoring tool',
      url='https://github.com/RVDaescu/Ping',
      author='Radu-V D',
      author_email='office@daescu.ro',
      license='Free',
      packages=['gnu.py','mail.py', 'main.py', 'run.py', 'sql_lib.py', 'traffic.py', 'utils.py'],
      zip_safe=False)
