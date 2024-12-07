from __future__ import annotations

# pylint: disable=C0330
import pathlib
from itertools import chain

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

EXTRAS_REQUIRE = {
  'gcp': [
    'google-cloud-firestore',
    'google-cloud-pubsub',
    'appengine-python-standard>=1.0.0',
  ]
}
EXTRAS_REQUIRE['full'] = list(set(chain(*EXTRAS_REQUIRE.values())))

setup(
  name='googleads-housekeeper',
  version='0.1.0.dev.87',
  long_description=README,
  long_description_content_type='text/markdown',
  author='Google Inc. (gTech gPS CSE team)',
  author_email='no-reply@google.com',
  license='Apache 2.0',
  python_requires='>3.8',
  packages=find_packages(),
  install_requires=[
    'google-ads-api-report-fetcher[pandas]>=1.15.3',
    'SQLAlchemy==1.4.46',
    'beautifulsoup4',
    'google-api-python-client',
    'psycopg2-binary',
    'croniter',
    'aiohttp',
    'slack_sdk',
    'numpy',
  ],
  extras_require=EXTRAS_REQUIRE,
  setup_requires=['pytest-runner'],
  tests_requires=['pytest', 'pytest-mock'],
)
