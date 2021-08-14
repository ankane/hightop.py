from setuptools import setup

setup(
    name='hightop',
    version='0.1.0',
    description='A nice shortcut for group count queries with Django',
    url='https://github.com/ankane/hightop.py',
    author='Andrew Kane',
    author_email='andrew@ankane.org',
    license='MIT',
    packages=[
        'hightop'
    ],
    python_requires='>=3.6',
    install_requires=[
        'Django'
    ],
    zip_safe=False
)
