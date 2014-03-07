#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, License LGPL 2.1

import logging
log = logging.getLogger(__name__)
D = log.debug
import argparse
import os
j = os.path.join

TMPL_DIR = "Templates"


def find_tmpl_roots():
  """ Find template directory roots. Resolving priority order.
  1) Up to the file-system root from current working directory.
  2) $HOME/Templates """
  result = list()
  ## find upwards
  path = os.getcwd().split(os.sep)
  while len(path):
    apath = os.path.normpath(j(os.sep, os.sep.join(path), TMPL_DIR))
    result.append(apath)
    path.pop()
  ## find home
  apath = j(os.environ["HOME"], TMPL_DIR)
  result.append(apath)
  result2 = list()
  for d in result:
    if os.path.isdir(d) and d not in result2:
      result2.append(d)
  return result2


class Entry:
  def __init__(self, root, name):
    self._root = root
    self._name = name

_entries = dict()  # name as str -> entry as Entry


ARGS = argparse.ArgumentParser()
ARGS.add_argument("thing", nargs=1,
                  help="thing (file,dir,project,..) to create")
ARGS.add_argument("-d", "--debug", action="store_true",
                  help="set debugging on")


def find_entries(roots, entries):
  """ entries as dict of name as str to entry as Entry is a
  collection of template things to instantiate. entries dict is
  filled by this function. """
  for root in roots:
    for name in os.listdir(root):
      D(name)  # TODO: to be continued ..


def main():
  args = ARGS.parse_args()
  logging.basicConfig()
  if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
  roots = find_tmpl_roots()
  find_entries(roots, _entries)
  D("done.")

if __name__ == "__main__":
  main()
