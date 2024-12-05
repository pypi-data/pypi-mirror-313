#
# Pavlin Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact pavlin@softel.bg.
#
# 2023
#

import time

from sciveo.tools.logger import *


class FPSCounter:
  def __init__(self, period=10, tag=""):
    self.period = period
    self.tag = tag
    self.n = 0
    self.t1 = time.time()

  def update(self):
    self.n += 1
    t2 = time.time()
    if t2 - self.t1 > self.period:
      debug(self.tag, "FPS", self.n / (t2 - self.t1))
      self.n = 0
      self.t1 = time.time()


class TimerExec:
  def __init__(self, fn, period=1.0):
    self.fn = fn
    self.period = period
    self.t1 = time.time()

  def run(self):
    t2 = time.time()
    if t2 - self.t1 > self.period:
      self.fn()
      self.t1 = time.time()


class Timer:
  def __init__(self):
    self.start()

  def start(self):
    self.start_at = time.time()

  def stop(self):
    self.end_at = time.time()
    return self.elapsed()

  def elapsed(self):
    return self.end_at - self.start_at
