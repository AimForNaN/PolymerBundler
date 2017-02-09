#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['Sandbox'];

from bs4 import BeautifulSoup;
from pathlib import Path;

from buildstep import *;
from dependencies import *;

class Sandbox(BuildStep):
	_DumpCache = set();
	HtmlDump   = 'build.html';
	JsDump     = 'build.js';

	"""Sandbox all dependencies."""
	def __init__(self):
		super(Sandbox, self).__init__()

	def process(self, data, directory):
		with Path(directory).joinpath(self.JsDump).open('w') as js:
			with Path(directory).joinpath(self.HtmlDump).open('w') as html:
				html.write('<script src="build.js" defer=""></script>\n');

				for node in data:
					# print(node.Source);

					attrs = node.Attributes;
					if node.Type == 'Link':
						if attrs['href'] in self._DumpCache:
							continue;

						self._DumpCache.add(attrs['href']);
						if node.isRemotePath:
							html.write('<link rel="'+ ' '.join(attrs['rel']) +'" href="'+ attrs['href'] +'">\n');
						else:
							doc = BeautifulSoup(Path(node.Source).open(), 'html5lib');
							scripts = doc.find_all('script');
							for script in scripts:
								script = script.extract();
								# bs4.contents returns UTF-8-encoded HTML entities,
								#   but I don't expect that to be an issue for scripts!
								js.write(' '.join(script.contents));

							# html5lib makes it possible to commit this kind of select:
							modules = doc.select('body > *, head > style');
							for module in modules:
								# formatter="html" converts UTF-8-encoded HTML entities into their
								#  original ampersand format.
								html.write('\n'+module.prettify(formatter='html')+'\n');
					elif node.Type == 'Script':
						if attrs['src'] in self._DumpCache:
							continue;

						self._DumpCache.add(attrs['src']);
						if node.isRemotePath:
							js.write('<script src="'+ attrs['src'] +'"></script>\n');
						else:
							with Path(node.Source).open() as module:
								js.write('\n'+ module.read() +'\n');

	def run(self, builder=None, data=None):
		# Make sure cache is clean before starting!
		self._DumpCache = set();

		if builder and data:
			self.process(data, builder.Directory);

		return data;
