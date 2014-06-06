#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, License LGPL 2.1

import logging
import getpass
import yaml
log = logging.getLogger(__name__)
D = log.debug
import argparse
import os
j = os.path.join
from fnmatch import fnmatch
import jinja2
import sys
import time


## control
APP_NAME = "mknew" # TODO: use pkg_* something
TMPL_DIR = "Templates"
CTRL_DIR = j(os.environ["HOME"], ".config", APP_NAME)
CTRL_CTX_FILE = j(CTRL_DIR, "context.yml")


## module globals 
_entries = dict()  # name as str -> entry as Entry
_files = dict()
_jenv = None
_ctx = dict()


## context spec
_ctx_spec = {
  "day": "current local day of month",
  "month": "current local month",
  "year": "current local year",
  "user": "local user name",
  "author": "Author real name",
  "tmpl": "template file",
  "dest": "destination file or dir",
  "name": "given name for new thing to create, a file or a dir"
}


def is_ignored(name): # TODO: this to control
  """ Lookup if name, file or either name should be ignored in processing. """
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


# template file source check function for jinja2
def updatefunc():
  return True

# template file load function for jinja2
def load_tmpl(name):
  file = _files[name]
  with open(file.apath) as fo:
    source = fo.read()
  return source, file.apath, updatefunc


class Thing(object):
  """ Base class for some Thing that will be templated into instance. """

  def __init__(self, root, path):
    self._root = root
    self._path = path

  @property
  def path(self):
    """ Relative path from template directory root """
    return self._path

  @property
  def root(self):
    """ Root of template tree. """
    return self._root

  @property
  def apath(self):
    """ Absolute path in OS filesystem. """
    return j(self._root, self._path)


class File(Thing):

  def __init__(self, root, path):
    super().__init__(root, path)
    self.files = [self]

  def show(self):
    return "* {}".format(self.path)

  def make(self, dest):
    print("mk file", self.path, "=>", dest)
    jtmpl = _jenv.get_template(self.path)
    with open(dest, "w") as fo:
      fo.write(jtmpl.render(_ctx))


class Dir(Thing):

  def __init__(self, root, path):
    super().__init__(root, path)
    self.files = list()

  def show(self):
    return "/ {} ({} files)".format(self.path, len(self.files))

  def make(self, dest):
    print("mk dir", self.path, "=>", dest)
    os.mkdir(dest)


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
  print("Templates (all {}):".format(len(files)))
  if match is None:
    match = "*"
  else:
    match = "*" + match + "*"
  for file in sorted(files):
    if fnmatch(file, match):
      print(" ", files[file].show())


def fill_ctx(ctx):
  """ Fill context dict ctx with default or system values. """
  c = ctx
  c["year"] = time.localtime().tm_year
  c["month"] = time.localtime().tm_mon
  c["day"] = time.localtime().tm_mday
  c["user"] = getpass.getuser()


def fill_ctx_file(ctx, path):
  """ Fill context dict ctx with data from given file path as yaml format. """
  if not os.path.isfile(path):
    D("no context file %s, pass", path)
    return
  try:
    with open(path) as fo:
      D("loading context from %s", path)
      db = yaml.load(fo)
  except yaml.parser.ParserError as ex:
    print("Context file syntax error:",str(ex))
    sys.exit(1)
  ctx.update(db)


def make_files(files, tmpl, dest):
  thing = files[tmpl]
  make_set = list()
  ## if dir then replace root with dest and map subtree files under that name  
  if isinstance(thing, Dir):
    make_set.append((thing, dest))
    for thing in thing.files:
      path = thing.path.split(os.sep)
      path[0] = dest
      path = os.sep.join(path)
      make_set.append((thing, path))
  else: # just one file
    make_set.append((thing, os.path.basename(dest)))
  ## check is dest files exists
  for thing, path in make_set:
    if os.path.exists(path):
      print(path, "already existing, not making files")
      sys.exit(1)
  ## replace dest path/dir parts with context values if exists
  make_set2 = list()
  for thing, path in make_set:
    npath = list()
    for part in path.split(os.sep):
      if part in _ctx:
        npath.append(_ctx[part])
      else:
        npath.append(part)
    make_set2.append((thing, os.sep.join(npath)))
  make_set = make_set2
  ## replace dest path file basename with context values if exists
  make_set2 = list()
  for thing, path in make_set:
    head, ext = os.path.splitext(path)
    name = os.path.basename(head)
    dirname = os.path.dirname(head)
    if name in _ctx:
      name = _ctx[name]
    path = j(dirname,name + ext)
    make_set2.append((thing, path))
  make_set = make_set2
  ## make
  for thing, path in make_set:
    thing.make(path)


def show_info():
  print("Context values to be used in jinja2 template file:")
  keys = set()
  for key in _ctx.keys():
    keys.add(key)
  for key in _ctx_spec.keys():
    keys.add(key)  
  for name in sorted(keys):
    value = _ctx.get(name ,"(not set (yet))")
    desc = _ctx_spec.get(name ,"no desc")
    print(" ",name,"=",value,"--",desc)

##############################################################################

ARGS = argparse.ArgumentParser(formatter_class=
                               argparse.ArgumentDefaultsHelpFormatter)
ARGS.add_argument("tmpl", nargs="?",
                  help="thing (file,dir,project,..) to create")
ARGS.add_argument("dest", nargs="?",
                  help="thing (file,dir,project,..) to create")
ARGS.add_argument("-d", "--debug", action="store_true",
                  help="set debugging on")
ARGS.add_argument("-i", "--info", action="store_true",
                  help="show operation information")
ARGS.add_argument("--context", 
                  metavar="FILE",
                  default=CTRL_CTX_FILE,
                  help="Context file".format(CTRL_CTX_FILE))


def main():
  args = ARGS.parse_args()
  logging.basicConfig()
  if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
  global _jenv
  _jenv = jinja2.Environment(loader=jinja2.FunctionLoader(load_tmpl),
                             undefined=jinja2.StrictUndefined)
  roots = find_tmpl_roots()
  find_files(roots, _files)
  fill_ctx(_ctx)
  fill_ctx_file(_ctx, args.context)
  ## execute
  if args.info:
    show_info()
    sys.exit(0)
  if args.tmpl not in _files:
    show_files(_files, args.tmpl)
    sys.exit(3)
  else:    
    if args.dest is None:
      args.dest = args.tmpl
    _ctx["tmpl"] = args.tmpl
    _ctx["dest"] = args.dest
    _ctx["name"] = args.dest
    try:
      make_files(_files, args.tmpl, args.dest)
    except jinja2.exceptions.UndefinedError as ex:
      print("?? context variable",ex,", empty substitution applied")
  D("done.")
  sys.exit(0)

if __name__ == "__main__":
  main()
