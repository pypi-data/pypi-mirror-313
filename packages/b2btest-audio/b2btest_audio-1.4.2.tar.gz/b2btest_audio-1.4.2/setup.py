#!/usr/bin/env python
from setuptools import setup, find_packages
from io import open

readme = open('README.md', encoding='utf8').read()

setup(
	name = "b2btest-audio",
	version = "1.4.2",
	install_requires=[
		'setuptools>40.5', # markdown readme
		'b2btest>=1.4',
		'wavefile',
	],
	python_requires='>=3.9',
	description = "Audio file support for b2btest, a framework to test against checked outputs",
	author = "David Garcia Garzon",
	author_email = "voki@canvoki.net",
	url = 'https://github.com/vokimon/back2back_audio',
	long_description = readme,
	long_description_content_type = 'text/markdown',
	license = 'GNU General Public License v3 or later (GPLv3+)',
	test_suite = 'b2btest_audio',
	packages=find_packages(exclude=['*_test']),
	classifiers = [
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Intended Audience :: Developers',
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Operating System :: OS Independent',
		],
	entry_points={
		'console_scripts': [
			'diffaudio=b2btest_audio.diffaudio:main',
		],
		'back2back.diff': [
			'audio=b2btest_audio.diffaudio:differences',
			]
		},
	)

