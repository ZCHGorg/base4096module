from setuptools import setup, find_packages

setup(
    name='base4096',
    version='2.0',
    packages=find_packages(),  # Finds the base4096/ package automatically
    include_package_data=True,
    description='Base4096 encoding and decoding functions',
    author='Josef Kulovany',
    author_email='charg.chg.wecharg@gmail.com',
    url='https://github.com/ZCHGorg/base4096',
    license='https://zchg.org/t/legal-notice-copyright-applicable-ip-and-licensing-read-me/440',
    keywords='base4096 encoder decoder',
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
)
