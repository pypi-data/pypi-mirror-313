# coding=utf8
__author__ = 'Zhong.PengQun'

from setuptools import setup

setup(name='flask_doc_z',
      version='0.0.1',
      description='Simple Flask API doc generator，forked from https://github.com/ipconfiger/flask-apidoc',
      url='',
      author='Zhong.PengQun',
      author_email='',
      license='',
      packages=['flask_doc'],
      package_data = {
            "flask_doc": ["*.html", "*.gif"],
      },
      install_requires=[
          'flask','markdown'
      ],
      entry_points = {
        'console_scripts': ['fkapidoc=flask_doc.generator:main'],
      },
      zip_safe=False)