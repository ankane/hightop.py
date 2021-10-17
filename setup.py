from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='hightop',
    version='0.1.1',
    description='A nice shortcut for group count queries with Django',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
