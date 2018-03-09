import sys
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    deps = [dep for dep in f.read().split('\n') if dep.strip() != ''
            and not dep.startswith('-e')]
    install_requires = deps

with open('README.rst') as f:
    description = f.read()


setup(name='system-metrics',
      version="0.1",
      long_description=description.strip(),
      description=("System probe."),
      author="Tarek Ziade",
      author_email="tarek@ziade.org",
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires=install_requires,
      entry_points="""
      [console_scripts]
      system-metrics = sysmetrics:main
      """)
