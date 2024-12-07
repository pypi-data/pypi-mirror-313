from os import path
from setuptools import setup, find_packages
from platform import platform


def get_tf_dep():
  platform_string = platform()
  if 'macOS' in platform_string and 'arm64' in platform_string:
    tf_name = 'tensorflow-macos'
  else:
    tf_name = 'tensorflow'
  return tf_name + '>=2.15.0, <2.16.0'


# Read the contents of the README file
directory = path.abspath(path.dirname(__file__))
with open(path.join(directory, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='quantizeml',
      version='0.13.1',
      description='Base layers and quantization tools',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Kevin Tsiknos',
      author_email='ktsiknos@brainchip.com',
      maintainer='Kevin Tsiknos',
      maintainer_email='ktsiknos@brainchip.com',
      url='https://doc.brainchipinc.com',
      license='Apache 2.0',
      license_files=['LICENSE'],
      packages=find_packages(),
      entry_points={
        'console_scripts': [
            'quantizeml = quantizeml.cli:main',
        ]
      },
      install_requires=[get_tf_dep(), 'keras>=2.15.0, <2.16.0',
                        'onnx==1.16.1', 'onnxruntime~=1.19.0',
                        'matplotlib<3.9', 'tensorboardX<2.6.1'],
      python_requires='>=3.9')
