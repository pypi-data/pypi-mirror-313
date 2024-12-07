
#import pybind11
#from distutils.core import setup
#from distutils.extension import Extension
#from Cython.Build import cythonize
from setuptools import setup ,find_packages ,Extension

def readme():
  with open('README.md', 'r') as f:
    return f.read()

#bmf = [
#    Extension(
#        'bmf', #pназвание нашей либы
#        ['bmf.cpp', 'main.cpp'], # файлики которые компилируем
##        include_dirs=[pybind11.get_include()],  # не забываем добавить инклюды pybind11
##        language='c++',
#        extra_compile_args=['-std=c++17'],  # используем с++17
#    ),
#]


setup(
  name='bimorph',
  version='1.1.30',
  author='@mpak2',
  author_email='mpak2@yandex.ru',
  description='Algorythm ML',
  ext_modules=[
		Extension("bimorph", ['bmf.cpp'],
			extra_compile_args=['-std=c++17'],
			library_dirs=['/usr/include/boost/']
		)
	],
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='http://xn--90aomiky.xn--p1ai/',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: OS Independent'
  ],
  keywords='example python',
  project_urls={
    'Documentation': 'http://xn--90aomiky.xn--p1ai/'
  },
  python_requires='>=3.7'
)

