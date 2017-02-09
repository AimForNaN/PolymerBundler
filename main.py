#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, sys;

from build import *;
from dependencies import *;
from sandbox import *;

if __name__ == '__main__':
	parser = argparse.ArgumentParser(usage='main.py [--build-dir] [--doc-root] [--source-file]');
	parser.add_argument('--build-dir', dest='BuildDir', type=str, default='');
	parser.add_argument('--doc-root', dest='DocRoot', type=str, default='');
	parser.add_argument('--source-file', dest='SourceFiles', type=str, action='append', default=[]);
	args = parser.parse_args();

	builder = Build();
	builder.DocumentRoot = args.DocRoot;
	builder.Directory    = args.BuildDir;
	builder.Sources      = args.SourceFiles;

	builder.addStep(Dependencies());
	builder.addStep(Sandbox());

	builder.run();
