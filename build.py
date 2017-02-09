#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Build(object):
	Directory = None;
	DocumentRoot = None;
	Sources = [];
	Steps = [];

	"""Build"""
	def __init__(self):
		super(Build, self).__init__();

	def addStep(self, step):
		self.Steps.append(step);

	def run(self):
		data = None;
		for step in self.Steps:
			data = step.run(self, data);
