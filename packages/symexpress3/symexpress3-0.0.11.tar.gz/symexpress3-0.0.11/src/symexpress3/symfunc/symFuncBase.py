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
class SymFuncBase( ABC ):
  """
  Base class for defining a function
  """
  def __init__( self ):
    self._name         = None  # must be set by in the real class
    self._desc         = ""    # description of the function
    self._minparams    = 1     # minimum number of parameters
    self._maxparams    = 1     # maximum number of parameters
    self._syntax       = None  # syntax of functions: sum(<variable>,<lower>,<upper>,<function>)
    self._synExplain   = None  # syntax explanation : sum function, from lower to upper, example: sum(n,0,100,exp(x,n)

  @property
  def name(self):
    """
    Name of the function
    """
    return self._name

  @property
  def description(self):
    """
    Description of the function
    """
    return self._desc

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

  @property
  def syntax(self):
    """
    Syntax of the function
    """
    return self._syntax

  @property
  def syntaxExplain(self):
    """
    More explanation of the syntax (not a description)
    """
    if self._synExplain != None:
      return self._synExplain

    return self._syntax

  @abstractmethod
  def functionToValue( self, elem ):
    """
    Convert a given function into a value/expression.
    Return None if it cannot convert
    """
    return None

  def _checkCorrectFunction( self, elem ):
    # check if the given element is a function and has the correct function name
    if not isinstance( elem, symexpress3.SymFunction ):
      return False
    if elem.name != self.name:
      return False

    numElem = elem.numElements()
    if  numElem < self._minparams :
      return False
    if numElem > self._maxparams :
      return False

    return True



  def mathMl( self, elem ):
    """
    Give the MathMl string back for the given function
    1e parameter indicate that the power must be done by the caller
    2e parameter is the string MathMl of the function, if None is given back then the caller must do it all
    See symexpress3.SymFunction.MathMl()
    """
    # pylint: disable=unused-argument
    return [], None


  # to be override
  def _getValueSingle( self, dValue, dValue2 = None ):
    # pylint: disable=unused-argument

    # Get a value from a single element
    # pyling do not like none as a return value
    # return None
    return 0

  def _getValueMultiple( self, listOrValue, listOrValue2 = None ):
    # get value from multiple elements

    listOne = []
    listTwo = []

    singleValue =  True

    if isinstance( listOrValue, list ):
      listOne     = listOrValue
      singleValue = False
    else:
      listOne.append( listOrValue )

    if isinstance( listOrValue2, list ):
      listTwo     = listOrValue2
      singleValue = False
    else:
      listTwo.append( listOrValue2 )

    # just to be sure
    if len( listOne ) == 0:
      listOne.append( None )

    if len( listTwo ) == 0:
      listTwo.append( None )

    result = []
    dValue = 0
    for valOne in listOne :
      for valTwo in listTwo :
        if valTwo == None:
          dValue = self._getValueSingle( valOne )
        else:
          dValue = self._getValueSingle( valOne, valTwo )
        result.append( dValue )

    if singleValue == False:
      dValue = result

    return dValue   # this is a list or a real/complex value

  def getValue( self, elemFunc, dDict = None ):
    """
    Convert the function into a real/complex value(s)
    """
    if self._checkCorrectFunction( elemFunc ) != True:
      return None

    numElem = elemFunc.numElements()
    if numElem < self.minimumNumberOfParameters :
      raise NameError( f'function {elemFunc.name} need {self.minimumNumberOfParameters} parameter found: {numElem}' )

    if numElem > self.maximumNumberOfParameters :
      raise NameError( f'function {elemFunc.name} need at most {self.maximumNumberOfParameters} parameters found: {numElem}' )

    if numElem > 2:
      raise NameError( 'function {elemFunc.name} more as 2 parameters no automatic supported at the moment' )

    if numElem >= 2:
      listOrValue1 = elemFunc.elements[ 0 ].getValue( dDict )
      listOrValue2 = elemFunc.elements[ 1 ].getValue( dDict )

      listOrValue = self._getValueMultiple( listOrValue1, listOrValue2 )
      listOrValue = elemFunc.valuePow( listOrValue )
    else:
      listOrValue = elemFunc.elements[ 0 ].getValue( dDict )
      listOrValue = self._getValueMultiple( listOrValue )
      listOrValue = elemFunc.valuePow( listOrValue )

    return listOrValue
