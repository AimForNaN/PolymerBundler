#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['Dependencies', 'HashableDict'];

from bs4 import BeautifulSoup;
from collections import defaultdict,OrderedDict;
from pathlib import Path;

from buildstep import *;

class HashableDict(dict):
	def __hash__(self):
		values = [x if type(x) == str else ' '.join(x) for x in self.values()];
		return hash((frozenset(self), frozenset(values)))

class DependencyNode(object):
	Attributes = None;
	Children   = None;
	References = None;
	Source     = None;
	Type       = None;

	"""DependencyNode."""
	def __init__(self, src, t, attrs, **kargs):
		super(DependencyNode, self).__init__()
		self.Attributes = attrs;
		self.Children   = dict();
		self.References = 1;
		self.Type       = t;

		root = kargs['root'] if 'root' in kargs else None;
		cwd  = kargs['cwd'] if 'cwd' in kargs else None;
		self.Source = self._findPath(src, root, cwd);

	def __eq__(self, other):
		if isinstance(other, DependencyNode):
			return self.Source == other.Source;
		elif type(other) == str:
			return str(self.Source) == other;
		else:
			return super(DependencyNode, self).__eq__(other);

	def __hash__(self):
		return hash((self.Source));

	def _findPath(self, path, root=None, cwd=None):
		if path.startswith('http'): return path;

		path = Path(path);
		if path.exists() == False:
			if path.as_posix().startswith('/') and root:
				root = Path(root);
				path = Path(root.as_posix() + '/' + path.as_posix());
			elif cwd:
				cwd  = Path(cwd);
				path = Path(cwd.as_posix() + '/' + path.as_posix());
		return path.resolve();

	@property
	def isRemotePath(self):
		if isinstance(self.Source, Path):
			return str(self.Source).startswith('http');
		elif type(self.Source) == str:
			return self.Source.startswith('http');
		return False;

class Dependencies(BuildStep):
	_cache  = dict();
	Product = [];

	"""Dependency walker."""
	def __init__(self):
		super(Dependencies, self).__init__()

	def _resolve(self, node):
		if node not in self.Product:
			self.Product.append(node.Source);

		for child in self.Tree[node]:
			if child.Source not in self.Product:
				self._resolve(child);

	def addNode(self, node, el):
		nSrc  = str(node.Source);
		elSrc = str(el.Source);

		# Make sure we have a node reference to pull from the cache!
		if nSrc not in self._cache:
			self._cache[nSrc] = node;

		# Make sure we store child in cache!
		if elSrc not in self._cache:
			self._cache[elSrc] = el;

		# Make sure to use the references from the cache before we do
		#   anything with them!
		node = self._cache[nSrc];
		el   = self._cache[elSrc];

		# Make sure we add the child from the cache to the parent node!
		if elSrc not in node.Children:
			node.Children[elSrc] = self._cache[elSrc];

		# Make sure to increment all available children!
		self.incrementChildrenReferences(node);

	def incrementChildrenReferences(self, node):
		if hasattr(node, 'Children'):
			for ch in node.Children:
				ch = node.Children[ch];
				# Increment references if possible!
				if hasattr(ch, 'References'):
					ch.References += 1;
				# Increment children if any!
				if hasattr(ch, 'Children'):
					self.incrementChildrenReferences(ch);

	def processTree(self, node, **kargs):
		root = kargs['root'] if 'root' in kargs else None;
		cwd  = kargs['cwd'] if 'cwd' in kargs else None;

		if not node.isRemotePath:
			doc = BeautifulSoup(node.Source.open(), 'html.parser');

			# Get all links!
			links = doc.find_all('link');
			for link in links:
				link = DependencyNode(link['href'], 'Link', link.attrs, root=root, cwd=cwd);

				self.addNode(node, link);

				if link.isRemotePath == False:
					self.processTree(link, root=root, cwd=link.Source.parent.resolve());

			# Get all scripts!
			scripts = doc.find_all('script');
			for script in scripts:
				if script.has_attr('src'):
					script = DependencyNode(script['src'], 'Script', script.attrs, root=root, cwd=cwd);

					self.addNode(node, script);

					if script.isRemotePath == False:
						self.processTree(script, root=root, cwd=script.Source.parent.resolve());

	def run(self, builder=None, data=None):
		self.Product = [];

		if builder:
			sources = builder.Sources[:];
			for source in sources:
				source = DependencyNode(source, 'Link', { 'href': source, 'rel': ['import'] });
				self._cache[str(source.Source)] = source;
				self.processTree(source, root=Path(builder.DocumentRoot).resolve(), cwd=source.Source.parent.resolve());

			ss = sorted(self._cache.items(), key=lambda x: x[1].References, reverse=True);

			for x in ss:
				self.Product.append(x[1]);

			return self.Product;
