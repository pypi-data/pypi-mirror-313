from distutils.core import setup
from setuptools import find_packages, setup, Command
import io
import os
import sys
from shutil import rmtree

DESCRIPTION = '****'
here = os.path.abspath(os.path.dirname(__file__))
  
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

REQUIRED = [
    'requests',
    'websockets>=11.0.3',
]


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()

setup(
    name='zerocap_api_new_test',  # 包名
    version='0.1.53',  # 版本号
    description='zerocap_api',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='zerocap',
    author_email='jiayu.gao@eigen.capital',
    url='https://zerocap.com/',
    install_requires=REQUIRED,
    setup_requires=REQUIRED,
    license='MIT',
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 对python的最低版本要求
)
