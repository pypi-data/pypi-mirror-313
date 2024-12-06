#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Abstract class for function implementation symexpress3

    Copyright (C) 2024 Gien van den Enden - swvandenenden@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.



"""

from abc import ABC, abstractmethod

from symexpress3 import symexpress3

#
# base class for a specific function
#
class OptimizeBase( ABC ):
  """
  Base class for defining a optimization class
  """
  def __init__( self ):
    self._name         = None  # must be set by in the real class
    self._symtype      = ""    # symexpression type, use "all" for all expression types
    self._desc         = ""    # description of the function

  @property
  def name(self):
    """
    Name of the function
    """
    return self._name

  @property
  def symType(self):
    """
    The supported expression type
    """
    return self._symtype

  @property
  def description(self):
    """
    Description of the function
    """
    return self._desc

  def checkExpression( self, symExpr, action ):
    """
    Check if the given symexpress is correct for this optimization class
    """
    if action != self.name :
      return False

    if symExpr == None:
      return False

    if not isinstance( symExpr, symexpress3.SymExpress ):
      return False

    if symExpr.symType != self.symType and self.symType != "all":  # pylint: disable=consider-using-in
      return False

    return True # correct call

  @abstractmethod
  def optimize( self, symExpr, action ):
    """
    Optimization method
    """
    # pass
