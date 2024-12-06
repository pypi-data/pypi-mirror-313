from distutils.core import setup
from setuptools import find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='pmonitor',
      version='1.2.9',
      description='pc monitor',
      long_description=long_description,
      author='cfr',
      author_email='1354592998@qq.com',
      install_requires=[],
      license='MIT',
      packages=find_packages(),
      package_data={
          'monitor': ['DLL/*', 'exec/*'],
      },
      platforms=['all'],
      classifiers=[],
      python_requires='>=3.6',

      entry_points={
          'console_scripts': ['pmonitor=monitor.run_monitor:main']  # 增加命令行指令运行的参数设置
      },

      )
