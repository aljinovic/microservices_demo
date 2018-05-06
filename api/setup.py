from setuptools import find_packages, setup

with open('requirements.txt') as f:
    install_requires = [line for line in f if line and line[0] not in '#-']

setup(
    name='ms',
    version='0.1',
    url='',
    author='ante.aljinovic',
    author_email='ante.aljinovic@seekandhit.com',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=[],
    include_package_data=True,
    classifiers=[
        'Private :: Do Not Upload',
        'Development Status :: Alpha',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
