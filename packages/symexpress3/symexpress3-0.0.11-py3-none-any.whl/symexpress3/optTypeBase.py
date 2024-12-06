#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Abstract class for optimize type` implementation symexpress3

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

#
# base class for a specific sym type
#
class OptTypeBase( ABC ):
  """
  Base class for type optimization
  """
  def __init__( self ):
    self._name         = None  # must be set by in the real class
    self._symtype      = None  # symexpress3 type class, example symexpress3.SymNumber, symexpress3.SymVariable, symexpress3.SymFunction
    self._desc         = ""    # description of the optimization

  @property
  def name(self):
    """
    Name of the function
    """
    return self._name

  @property
  def symType(self):
    """
    The supported sym type`
    """
    return self._symtype

  @property
  def description(self):
    """
    Description of the function
    """
    return self._desc

  def checkType( self, elem, action ):
    """
    Check if the given elem
    """
    if action != self.name :
      # print( "one: " + self.name )
      return False

    if elem == None:
      # print( "two" )
      return False

    if self._symtype != None and not isinstance( elem, self._symtype ): # pylint: disable=isinstance-second-argument-not-valid-type
      # print( "two a: " + str(  self._symtype) )
      # print(" two b: " + str( type(elem) ))
      return False

    return True # correct call

  @abstractmethod
  def optimize( self, elem, action ):
    """
    Optimization method, give the optimize elem back, do not change the elem
    """
    return None
