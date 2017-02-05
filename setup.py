try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
        'description': 'Barringer Flask App',
        'author': 'Ysgard',
        'url': 'https://github.com/ysgard/barringer_flask',
        'download_url': 'https://github.com/ysgard/barringer_flask',
        'author_email': 'ysgard@gmail.com',
        'version': '0.1',
        'install_requires': ['nose'],
        'packages': ['barringer_flask'],
        'scripts': [],
        'name': 'barringer_flask'
}

setup(**config)

