mknew
#####

make new files, dirs, projects from jinja2 templates

Outdated, use https://github.com/audreyr/cookiecutter

Install
=======

TODO


Usage
=====

Setting up template directories
-------------------------------

TODO

Listing templates
-----------------

List all::

  > mknew
  
List subset matching templates::

  > mknew py
  
Instantiate file
----------------

Instantiate with given name::

  > mknew python/main.py myprog.py
  
Instantiate with template name

  > mknew python/Makefile

Instantiate tree (project)
--------------------------

Instantiate project::

  > mknew python-prj aproject
  
Make context file
-----------------

  > mkdir -p ~/.config/mknew/
  > echo "author: My Name" > ~/.config/mknew/context.yml

Get context jinja2 variable information
---------------------------------------

  > mknew -i












