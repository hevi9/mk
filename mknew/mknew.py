#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, License LGPL 2.1

import logging
log = logging.getLogger(__name__)
D = log.debug
import argparse
import os
j = os.path.join
from fnmatch import fnmatch
import jinja2
import sys

TMPL_DIR = "Templates"


_entries = dict()  # name as str -> entry as Entry
_files = dict()
_jenv = None


def is_ignored(name):
  ignored = [
    ".project",
    ".pydevproject",
    ".settings",
    ".svn",
    ".git"
  ]
  for pat in ignored:
    if fnmatch(name, pat):
      return True
  return False


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


def updatefunc():
  return True


def load_tmpl(name):
  file = _files[name]
  with open(file.apath) as fo:
    source = fo.read()
  return source, file.apath, updatefunc


class Thing(object):

  def __init__(self, root, path):
    self._root = root
    self._path = path

  @property
  def path(self):
    return self._path

  @property
  def root(self):
    return self._root

  @property
  def apath(self):
    return j(self._root, self._path)


class File(Thing):

  def __init__(self, root, path):
    super().__init__(root, path)
    self.files = [self]

  def show(self):
    return "F {}".format(self.path)


class Dir(Thing):

  def __init__(self, root, path):
    super().__init__(root, path)
    self.files = list()

  def show(self):
    return "D {} {}".format(self.path, len(self.files))


def _add_path_to_dirs(files, thing):
  dir = os.path.dirname(thing.path)
  while len(dir):
    files[dir].files.append(thing)
    dir = os.path.dirname(dir)


def find_files(roots, files_store):
  for root in roots:
    for top, dirs, files in os.walk(root):
      for dir in list(dirs):
        if is_ignored(dir):
          dirs.remove(dir)
          continue
        path = j(top, dir)[len(root) + 1:]
        files_store[path] = Dir(root, path)
        _add_path_to_dirs(files_store, files_store[path])
      for file in files:
        if is_ignored(file):
          continue
        path = j(top, file)[len(root) + 1:]
        files_store[path] = File(root, path)
        _add_path_to_dirs(files_store, files_store[path])


def show_files(files, match=None):
  print("Templates ({}):".format(len(files)))
  if match is None:
    match = "*"
  else:
    match = "*" + match + "*"
  for file in sorted(files):
    if fnmatch(file, match):
      print(" ", files[file].show())


def make_file(thing, dest):
  print("mk", thing.path, "=>", dest)
  if isinstance(thing, Dir):
    os.mkdir(dest)
  else:
    jtmpl = _jenv.get_template(thing.path)
    with open(dest, "w") as fo:
      fo.write(jtmpl.render({}))


def make_files(files, tmpl, dest):
  thing = files[tmpl]
  make_set = list()
  if isinstance(thing, Dir):
    make_set.append((thing, dest))
  for thing in thing.files:
    path = thing.path.split(os.sep)
    path[0] = dest
    path = os.sep.join(path)
    make_set.append((thing, path))
  ## check is dest files exists
  for thing, path in make_set:
    if os.path.exists(path):
      print(path, "already existing, not making files")
      sys.exit(1)
  ## make
  for thing, path in make_set:
    make_file(thing, path)


ARGS = argparse.ArgumentParser()
ARGS.add_argument("tmpl", nargs="?",
                  help="thing (file,dir,project,..) to create")
ARGS.add_argument("dest", nargs="?",
                  help="thing (file,dir,project,..) to create")
ARGS.add_argument("-d", "--debug", action="store_true",
                  help="set debugging on")


def main():
  args = ARGS.parse_args()
  logging.basicConfig()
  if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
  global _jenv
  _jenv = jinja2.Environment(loader=jinja2.FunctionLoader(load_tmpl))
  roots = find_tmpl_roots()
  find_files(roots, _files)
  if args.tmpl not in _files:
    show_files(_files, args.tmpl)
    sys.exit(3)
  else:
    if args.dest is None:
      args.dest = args.tmpl
    make_files(_files, args.tmpl, args.dest)
  D("done.")
  sys.exit(0)

if __name__ == "__main__":
  main()
