from setuptools import setup, find_packages

setup(
  name='ixi_drag_n_drop',
  version='1.0.0',
  author='ixslea',
  description='13',
  packages=find_packages(),
  install_requires=['Pillow>=11.0.0', 'tkinterdnd2>=0.4.2'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
  ],
  python_requires='>=3.7'
)