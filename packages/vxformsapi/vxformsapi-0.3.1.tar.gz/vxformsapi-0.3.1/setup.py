from setuptools import setup

setup(
    name='vxformsapi',
    version='0.3.1',
    packages=['vxformsapi'],
    install_requires=['requests', 'pandas'],
    url='https://github.com/M9-Calibre/BD_API_Materials',
    license='',
    author='Afonso Campos <afonso.campos@ua.pt>, Lucius Vinicius <luciusviniciusf@ua.pt>',
    description='API for the VxForms Material Database.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
)