#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup;
from pathlib import Path;
from pprint import pprint;

from buildstep import *;

class PathNode(object):
	def __init__(self, path):
		super(PathNode, self).__init__()

		self.Children = {};
		self.Path     = Path(path);
		self.Count    = 0;

	def __getattr__(self, attr):
		if attr in self.__dict__:
			return getattr(self, attr);
		return getattr(self.Path, attr);

	def __eq__(a, b):
		return str(a) == str(b);

	def __ge__(a, b):
		return a.Count >= b.Count;

	def __gt__(a, b):
		return a.Count > b.Count;

	def __iadd__(self, x):
		if type(x) == int:
			self.Count += x;

	def __le__(a, b):
		return a.Count <= b.Count;

	def __lt__(a, b):
		return a.Count < b.Count;

	def __ne__(a, b):
		return str(a) != str(b);

	def __str__(self):
		return str(self.Path);

	@property
	def isAbsolute(self):
		return str(self.Path).startswith('/') or str(self.Path).startswith('\\') or self.Path.is_absolute();

	@property
	def isRelative(self):
		return not self.isAbsolute;

	def resolve(self, parent=None):
		if not self.exists():
			if self.isAbsolute:
				self.Path = Path(PathsResolver.DocRoot + str(self.Path));
			elif parent is not None:
				self.Path = Path(parent, self.Path);
		try:
			self.Path  = self.Path.resolve();
		except Exception as e:
			pass;

class PathsResolver(BuildStep):
	DocRoot     = '';
	SourceFiles = [];

	def __init__(self):
		super(PathsResolver, self).__init__();
		self.Paths = {};

	def incrementAll(self, node, inc = 0):
		node.Count += 1 + inc;
		for child in node.Children.values():
			self.incrementAll(child, 1 + inc);

	def processSourceFile(self, sourceFile):
		node = PathNode(sourceFile);
		node.resolve();

		if node.exists():
			# Add source file to listing!
			if str(node) not in self.Paths:
				self.Paths[str(node)] = node;

			if str(node) in self.Paths:
				node = self.Paths[str(node)];

			# Start the parser!
			doc = BeautifulSoup(node.open(), 'html.parser');

			# Get all links! All we care about are links!
			links = doc.find_all('link');
			for link in links:
				if 'stylesheet' in link['rel']:
					pass; # All we care about are imports!
				elif 'import' in link['rel']:
					childNode = PathNode(link['href']);
					childNode.resolve(node.parent);

					if childNode.exists():
						childPath = str(childNode);
						if childPath not in self.Paths:
							self.Paths[childPath] = childNode;
						else:
							childNode = self.Paths[childPath];

						if childPath not in node.Children:
							node.Children[childPath] = childNode;

						self.processSourceFile(childPath);

		return node;

	def processSourceFiles(self):
		nodes = [];
		for sourceFile in self.SourceFiles:
			node = self.processSourceFile(sourceFile);
			self.incrementAll(node);
			nodes.append(node);

		return nodes;

	def resolve(self, path):
		pass

	def run(self, data):
		nodes = self.processSourceFiles();
		# return nodes;
		return sorted(self.Paths.items(), key=lambda x: x[1], reverse=True);
