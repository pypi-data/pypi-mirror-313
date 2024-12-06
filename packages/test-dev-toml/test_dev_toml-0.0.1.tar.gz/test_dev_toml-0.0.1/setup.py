from pathlib import Path

from setuptools import find_packages
from setuptools import setup

print('     setup: version:  v0.0.1')
print('     setup: module :  test_dev_toml')

# @formatter:off
setup(
    description='python module to generate Makefiles for arduino, GTest, /CC++, etc.',
    keywords=['makefile', 'generation', 'python'],
    install_requires=[
    ],
    classifiers=[
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],

    # common attributes from here on
    name='test-dev-toml',
    packages=find_packages(include='./test_dev_toml*', ),
    include_package_data=True,
    exclude_package_data={'./test_dev_toml/lib': ['.gitignore']},
    version='0.0.1',
    license='MIT',
    long_description=(Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    author='J. Arrizza',
    author_email='cppgent0@gmail.com',
    url='https://bitbucket.org/arrizza-public/test-dev-toml/src/master',
    download_url='https://bitbucket.org/arrizza-public/test-dev-toml/get/master.zip',
)
# @formatter:on

print('     setup: done')
