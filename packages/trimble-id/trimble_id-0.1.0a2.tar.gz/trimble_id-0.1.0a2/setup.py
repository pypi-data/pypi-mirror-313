# setup.py
import re
import os.path
from setuptools import setup

PACKAGE_NAME = "trimble-id"
PACKAGE_PPRINT_NAME = "Authentication module"

package_folder_path = PACKAGE_NAME.replace('-', '/')

with open(os.path.join(package_folder_path, 'version.py')
          if os.path.exists(os.path.join(package_folder_path, 'version.py'))
          else os.path.join(package_folder_path, '_version.py'), 'r') as fd:
    version = re.search(r'^VERSION\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(name=PACKAGE_NAME,
      version=version,
      description='Trimble {} Client Library for Python'.format(PACKAGE_PPRINT_NAME),
      url='https://github.com/trimble-oss/trimble-id-sdk-docs-for-python',
      long_description=readme,
      long_description_content_type="text/markdown",
      license="MIT License",
      author="Trimble Inc.",
      author_email="sdk@trimble.com",
      keywords="Trimble, TrimbleID, Trimble Identity",
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      scripts=[],
      packages=['trimble.id'],
      setup_requires=[],
      install_requires=[
            'aiohttp>=3.7.4',
            'PyJWT>=2.4.0',
            "requests>=2.28.1",
            "cryptography>=38.0.3"
            ],
      tests_require=[],
      extras_require=dict()
)
