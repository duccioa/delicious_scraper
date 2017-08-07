from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='delicious-scraper',
      version='0.1',
      description='Scrape your bookmark on del.icio.us',
      long_description=readme(),
      keywords='funniest joke comedy flying circus',
      url='http://github.com/storborg/funniest',
      author='Duccio Aiazzi',
      author_email='aiazziduccio@gmail.com',
      license='MIT',
      packages=['delicious-scraper'],
      install_requires=[
          'requests',
          'bs4'


      ],
      include_package_data=True,
      zip_safe=False)