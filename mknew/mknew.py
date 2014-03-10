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


def find_entries(roots, entries):
  """ entries as dict of name as str to entry as Entry is a
  collection of template things to instantiate. entries dict is
  filled by this function. """
  for root in roots:
    for name in os.listdir(root):
      if is_ignored(name):
        continue
      if name not in entries:
        entries[name] = Entry(root,name)
  return entries 


class Entry:
  def __init__(self, root, name):
    self._root = root
    self._name = name
    self._files = None

  @property
  def path(self):
    return j(self._root, self._name)

  @property
  def files(self):
    if not self._files:
      self._files = list()
      if os.path.isfile(self.path):
        self._files.append(self._name)
      for top, dirnames, filenames in os.walk(self.path):
        for filename in filenames:
          path = j(top,filename)[len(self._root)+1:]
          self._files.append(path)
    return self._files



def show_entries(entries, match=None):
  """ """
  print("Templates")
  if match is None:
    for name in sorted(entries):
      entry = entries[name]
      print(" *", name, len(entry.files))
  else:
    for name in sorted(entries):
      if name.find(match) > -1:
        print(" *",name)

ARGS = argparse.ArgumentParser()
ARGS.add_argument("tmpl", nargs="?",                  
                  help="thing (file,dir,project,..) to create")
ARGS.add_argument("dest", nargs="?",                  
                  help="thing (file,dir,project,..) to create")
ARGS.add_argument("-d", "--debug", action="store_true",
                  help="set debugging on")
ARGS.add_argument("-f","--frm",nargs=1,
                  help="Template name to instantiate from")


def instantiate_file(entry, file, path):
  jinja2


def instantiate(entry, thing):
  for file in entry.files:
    path = file.split(os.sep)
    path[0] = thing
    path = os.sep.join(path)
    D("%s => %s", file, path)
    instantiate_file(entry, file, path)


def updatefunc():
  return True

def load_tmpl(name):
  file = _files[name]
  with open(file.apath) as fo:
    source = fo.read()  
  return source, file.apath, updatefunc

class File(object):
    
  def __init__(self, root, path):
    self._root = root
    self._path = path

  @property
  def apath(self):
    return j(self._root, self._path)

def find_files(roots, files_store):
  for root in roots:
    for top, dirs, files in os.walk(root):
      for dir in list(dirs):
        if is_ignored(dir):
          dirs.remove(dir)
      for file in files:
        if is_ignored(file):
          continue
        path = j(top,file)[len(root)+1:]
        files_store[path] = File(root, path) 

def make_file(tmpl, dest):
  jtmpl = _jenv.get_template(tmpl)
  with open(dest,"w") as fo:
    fo.write(jtmpl.render({}))

def main():
  args = ARGS.parse_args()
  logging.basicConfig()
  if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
  global _jenv
  _jenv = jinja2.Environment(loader=jinja2.FunctionLoader(load_tmpl))
  roots = find_tmpl_roots()
  find_files(roots,_files)
  if args.tmpl not in _files:
    for file in sorted(_files):
      print(file)
  else:
    make_file(args.tmpl, args.dest)
  D("done.")

if __name__ == "__main__":
  main()
