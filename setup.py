"""
Required to to create package
"""
import setuptools

setuptools.setup(
    name='portfolio_report',
    version='0.0.1',
    author='Joanne Norris',
    description='Stock Portfolio calculator',
    packages=['portfolio_report'],
    entry_points={
        'console_scripts': ['portfolio=portfolio_report.portfolio:main']
    },
    install_requires=[
        "requests>=2"
    ]
)
