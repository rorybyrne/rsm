import setuptools

setuptools.setup(
    name='msr',
    version='0.1.0',
    py_modules=['msr'],
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        msr=msr.cli:msr
    ''',
)