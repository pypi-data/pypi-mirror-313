#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Abstract class for optimize variable type` implementation symexpress3

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

from symexpress3 import symexpress3
from symexpress3 import optTypeBase

#
# base class for a specific sym function type
#
class OptFunctionBase( optTypeBase.OptTypeBase ):
  """
  Base class for type function optimization
  """
  def __init__( self ):
    super().__init__()
    self._name         = None                     # must be set by in the real class
    self._symtype      = symexpress3.SymFunction  # symexpress3 type class, example symexpress3.SymNumber, symexpress3.SymVariable, symexpress3.SymFunction
    self._desc         = ""                       # description of the optimization
    self._funcName     = None                     # name of the function
    self._minparams    = 1                        # minimum number of parameters
    self._maxparams    = 1                        # maximum number of parameters


  @property
  def functionName(self):
    """
    Name of the function
    """
    return self._funcName

  @property
  def minimumNumberOfParameters(self):
    """
    Minimum number of parameters
    """
    return self._minparams

  @property
  def maximumNumberOfParameters(self):
    """
    Maximum number of parameters
    """
    return self._maxparams


  def checkType( self, elem, action ):
    """
    Check if the given elem
    """
    if super().checkType( elem, action ) != True:
      # print("Name: " + self.name )
      # print("Type: " + str( self._symtype ))
      # print( "test 1")
      return False

    if elem.name != self.functionName:
      return False

    numElem = elem.numElements()
    if  numElem < self._minparams :
      return False

    if numElem > self._maxparams :
      return False

    return True
