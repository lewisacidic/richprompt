#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Rich Lewis
# License: MIT license
"""Timing execution."""
import time


class Timer(object):
    """Object for keeping track of execution time."""
    def __init__(self, ipython):
        self.shell = ipython
        self.time = time.time()

    def pre_execute(self):
        self.time = time.time()

    def post_execute(self):
        time_taken = time.time() - self.time
        self.shell.push({"time_taken": time_taken})

    def register(self):
        self.shell.events.register("pre_execute", self.pre_execute)
        self.shell.events.register("post_execute", self.post_execute)
