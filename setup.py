from setuptools import setup

setup(
    name='LASG_website_basecamp_vis',
    version='0.1',
    packages=['vis', 'vis.migrations', 'pages', 'pages.migrations', 'upload', 'upload.migrations', 'scripts', 'website',
              'products', 'products.migrations', 'mess_by_year', 'mess_by_year.migrations', 'sent_analysis',
              'sent_analysis.migrations'],
    url='https://github.iu.edu/jackclar/LASG_website',
    license='',
    author='Jack Clarke',
    author_email='jackclar@iu.edu',
    description='A visualization tool for Basecamp JSON files for LASG.'
)
