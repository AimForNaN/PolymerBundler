#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['BuildStep'];

from abc import *

class BuildStep(object, metaclass=ABCMeta):
	@abstractmethod
	def run(self, data=None):
		raise NotImplementedError;
