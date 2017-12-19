#!/usr/bin/env python
# -*- coding: utf-8 -*-

from build import *;
from buildstep import *;
from debug import *;
from pathsresolver import *;
from welder import *;

import argparse, sys;

if __name__ == '__main__':
	parser = argparse.ArgumentParser(usage='main.py [--build-dir] [--doc-root] [--source-file] [--html] [--js]');
	parser.add_argument('--build-dir', dest='BuildDir', type=str, default='');
	parser.add_argument('--doc-root', dest='DocRoot', type=str, default='');
	parser.add_argument('--source-file', dest='SourceFiles', type=str, action='append', default=[]);
	parser.add_argument('--html', dest='HtmlFile', type=str, default=None);
	parser.add_argument('--js', dest='JsFile', type=str, default=None);
	args = parser.parse_args();

	PathsResolver.DocRoot     = args.DocRoot;
	PathsResolver.SourceFiles = args.SourceFiles;

	Welder.BuildDirectory = args.BuildDir;

	build = Build();
	build.add(PathsResolver());
	build.add(Welder());

	build.run();
