from pathlib import Path

from setuptools import find_packages
from setuptools import setup

print('     setup: version:  v$$version$$')
print('     setup: module :  $$mod_dir_name$$')

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
        '$$classifier_license$$',
    ],

    # common attributes from here on
    name='$$mod_name$$',
    packages=find_packages(include='$$root_dir$$/$$mod_dir_name$$*', ),
    include_package_data=True,
    exclude_package_data={'$$root_dir$$/$$mod_dir_name$$/lib': ['.gitignore']},
    version='$$version$$',
    license='$$license$$',
    long_description=(Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='$$long_desc_type$$',
    author='$$author$$',
    author_email='$$email$$',
    url='$$homepage_url$$',
    download_url='$$download_url$$',
)
# @formatter:on

print('     setup: done')
