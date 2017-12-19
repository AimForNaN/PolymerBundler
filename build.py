#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Build(object):
	"""Build"""
	def __init__(self):
		super(Build, self).__init__();
		self.Steps = [];

	def add(self, step):
		self.Steps.append(step);

	def run(self):
		data = None;
		for step in self.Steps:
			data = step.run(data);
