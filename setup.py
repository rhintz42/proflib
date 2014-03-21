import os

from setuptools import setup, find_packages

#import pdb;pdb.set_trace()
os_file = os.__file__
path_list = os_file.split('/')
project_name = path_list[3]
command_path = '/opt/webapp/' + project_name + '/'
working_directory = command_path + 'src/' + project_name + '/'
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'waitress',
    ]

setup(name='proflib',
      version='0.0',
      description='proflib',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="proflib",
      entry_points="""\
      [paste.app_factory]
      main = proflib:main
      """,
      )
