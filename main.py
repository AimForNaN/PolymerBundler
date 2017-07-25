#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, sys;

from build import *;
from dependencies import *;
from sandbox import *;

if __name__ == '__main__':
	parser = argparse.ArgumentParser(usage='main.py [--build-dir] [--doc-root] [--source-file] [--html] [--js]');
	parser.add_argument('--build-dir', dest='BuildDir', type=str, default='');
	parser.add_argument('--doc-root', dest='DocRoot', type=str, default='');
	parser.add_argument('--source-file', dest='SourceFiles', type=str, action='append', default=[]);
	parser.add_argument('--html', dest='HtmlFile', type=str, default=None);
	parser.add_argument('--js', dest='JsFile', type=str, default=None);
	args = parser.parse_args();

	# Overwrite some defaults!
	if args.HtmlFile is not None:
		Sandbox.HtmlDump = args.HtmlFile;
	if args.JsFile is not None:
		Sandbox.JsDump = args.JsFile;

	# Some preparation!
	builder = Build();
	builder.DocumentRoot = args.DocRoot;
	builder.Directory    = args.BuildDir;
	builder.Sources      = args.SourceFiles;

	# Add some steps!
	builder.addStep(Dependencies());
	builder.addStep(Sandbox());

	# Start the engines!
	builder.run();
