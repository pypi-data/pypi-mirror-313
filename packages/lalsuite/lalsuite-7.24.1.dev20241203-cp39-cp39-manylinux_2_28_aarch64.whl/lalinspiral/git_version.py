# -*- coding: utf-8 -*-
# git_version.py - vcs information module
#
# Copyright (C) 2010 Nickolas Fotopoulos
# Copyright (C) 2012-2013 Adam Mercer
# Copyright (C) 2016 Leo Singer
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with with program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

id = "e17b68dd402720c7b7551a6b3d79cad3f1764d33"
date = "2024-11-27 14:49:39 +0000"
branch = "None"
tag = "None"
if tag == "None":
    tag = None
author = "Karl Wette <karl.wette@ligo.org>"
builder = "Unknown User <>"
committer = "Karl Wette <karl.wette@ligo.org>"
status = "UNCLEAN: Modified working tree"
version = id
verbose_msg = """Branch: None
Tag: None
Id: e17b68dd402720c7b7551a6b3d79cad3f1764d33

Builder: Unknown User <>
Repository status: UNCLEAN: Modified working tree"""

import warnings

class VersionMismatchError(ValueError):
    pass

def check_match(foreign_id, onmismatch="raise"):
    """
    If foreign_id != id, perform an action specified by the onmismatch
    kwarg. This can be useful for validating input files.

    onmismatch actions:
      "raise": raise a VersionMismatchError, stating both versions involved
      "warn": emit a warning, stating both versions involved
    """
    if onmismatch not in ("raise", "warn"):
        raise ValueError(onmismatch + " is an unrecognized value of onmismatch")
    if foreign_id == "e17b68dd402720c7b7551a6b3d79cad3f1764d33":
        return
    msg = "Program id (e17b68dd402720c7b7551a6b3d79cad3f1764d33) does not match given id (%s)." % foreign_id
    if onmismatch == "raise":
        raise VersionMismatchError(msg)

    # in the backtrace, show calling code
    warnings.warn(msg, UserWarning)
