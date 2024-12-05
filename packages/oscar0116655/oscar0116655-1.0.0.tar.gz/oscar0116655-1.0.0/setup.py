from setuptools import setup

setup(name='oscar0116655',
      version='1.0.0',
      description='A print test for PyPI',
      author='winycg',
      author_email='win@163.com',
      url='https://www.python.org/',
      license='MIT',
      keywords='ga nn',
      project_urls={
            'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
            'Funding': 'https://donate.pypi.org',
            'Source': 'https://github.com/pypa/sampleproject/',
            'Tracker': 'https://github.com/pypa/sampleproject/issues',
      },
      packages=['oscar0116655'],
      install_requires=['numpy>=1.14', 'tensorflow>=1.7'],
      python_requires='>=3'
     )