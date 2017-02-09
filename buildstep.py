#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['BuildStep'];

from abc import *

class BuildStep(object, metaclass=ABCMeta):
	@abstractmethod
	def run(self, builder=None, data=None):
		raise NotImplementedError;
