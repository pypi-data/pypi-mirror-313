from setuptools import setup, find_packages

setup(
  name='QuickBPE',         # Package name
  version='1.8.1',           # Package version
  license='MIT',           # License type
  description='A fast BPE implementation in C',  # Short description
  author='Johannes Voderholzer',                 # Author name
  author_email='invenis2@gmail.com',             # Author email
  url='https://github.com/JohannesVod/QuickBPE', # Project URL
  download_url='https://github.com/JohannesVod/QuickBPE/archive/refs/tags/v1.8.1.tar.gz',  # Source archive
  keywords=['BPE', 'LLM', 'tokenization'],       # Keywords
  install_requires=[                             # Dependencies
      'numpy',
      'tiktoken',
      'regex',
  ],
  packages=find_packages(),                      # Automatically include subpackages
  package_data={
      "QuickBPE.fastfuncs": ["*.dll", "*.so"],   # Include DLL/SO files in fastfuncs
  },
  include_package_data=True,                     # Include MANIFEST.in files if present
  classifiers=[
    'Development Status :: 3 - Alpha',           # Development status
    'Intended Audience :: Developers',           # Target audience
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',    # License type
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
  ],
)
