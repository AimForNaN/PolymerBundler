#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup;
from pathlib import Path;
from pprint import pprint;

from buildstep import *;
from pathsresolver import *;

def importFilter(tag):
	if tag.name in ['html', 'body', 'head', 'title']:
		return False;

	if tag.name == 'link':
		if 'import' in tag['rel']:
			if tag['href'].startswith('http'):
				return True;
			else:
				return False;

	return True;

class Welder(BuildStep):
	BuildDirectory = '';
	HtmlDump       = 'build.html';
	JsDump         = 'build.js';
	WhiteList      = ['dom-module', 'iron-iconset-svg', 'link', 'script', 'style']

	"""Compile all dependencies."""
	def __init__(self):
		super(Welder, self).__init__()

	def process(self, data):
		with Path(self.BuildDirectory).joinpath(self.JsDump).open('w') as js:
			with Path(self.BuildDirectory).joinpath(self.HtmlDump).open('w') as html:
				html.write('<script src="build.js" defer=""></script>\n');

				for path, node in data:
					doc = BeautifulSoup(node.open(), 'html5lib');

					elements = doc.find_all(importFilter);
					for el in elements:
						if el.name in self.WhiteList:
							if el.name == 'script':
								# Skip the scripts within the dom-module elements!
								#   We'll be removing them when we handle the dom-module elements!
								parent = el.find_parent('dom-module');
								if parent is not None:
									pass;
								# Handle external JS!
								else:
									if el.has_attr('src'):
										if el['src'].startswith('http'):
											html.write('\n'+el.prettify(formatter='html')+'\n');
										# Add JS file contents to JS build file!
										else:
											cwd  = Path(path).parent;
											path = cwd.joinpath(el['src']);
											try:
												path.resolve();
												with path.open('r') as js_file:
													js.write(js_file.read() + ';');
											except Exception as e:
												pass;
									# Handle inline JS that is not in a dom-module!
									else:
										js.write(' '.join(el.contents) + ';');
							elif el.name == 'style':
								# Skip the styles within the dom-module elements!
								#   They'll be written with the dom-module!
								parent = el.find_parent('dom-module');
								if parent is not None:
									pass;
								# Handle inline styles!
								else:
									html.write('\n'+el.prettify(formatter='html')+'\n');
							else:
								# Handle script from dom-module!
								script = el.script;
								if script is not None:
									# Write script to file before removal!
									js.write(' '.join(script.contents) + ';');
									# Remove script from dom-module!
									script.decompose();

								html.write('\n'+el.prettify(formatter='html')+'\n');

	def run(self, data):
		# Make sure cache is clean before starting!
		self._DumpCache = set();
		return self.process(data);
