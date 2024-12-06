#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Sym Express 3

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

class OptSymAnyExpandArray( optTypeBase.OptTypeBase ):
  """
  If the expression contains at least 1 array then make the hole expression an array element.
  """
  def __init__( self ):
    super().__init__()
    self._name         = "expandArrays"
    self._desc         = "If the expression contains at least 1 array then make the hole expression an array element."

  def optimize( self, elem, action ):

    def _subExpandSymArray( elem ):
      if elem.power != 1 or elem.onlyOneRoot != 1 : # use arrayPower first
        return None

      result = None
      for elemsub in elem.elements:
        if isinstance( elemsub, symexpress3.SymArray ):
          if elemsub.power != 1 or elemsub.onlyOneRoot != 1:
            continue
          result = symexpress3.SymArray()
          break
      if result != None:
        # power is always 1 on this point
        for iCnt, elemsub in enumerate( elem.elements ):
          if isinstance( elemsub, symexpress3.SymArray ) and elemsub.power == 1 and elemsub.onlyOneRoot == 1:
            # get the sub elements
            for elemsub2 in elemsub.elements :
              result.add( elemsub2 )
          else:
            result.add( elemsub )

      return result

    def _subExpandSymFunction( elem ):
      result  = None
      iArrPos = -1
      for iCnt, elemsub in enumerate( elem.elements ):
        if isinstance( elemsub, symexpress3.SymArray ):
          if elemsub.power != 1 or elemsub.onlyOneRoot != 1:
            continue
          iArrPos = iCnt
      if iArrPos == -1:
        return None

      result    = symexpress3.SymArray()
      arrElem   = elem.elements[ iArrPos ].copy()
      iNumArray = arrElem.numElements()
      elem.elements[ iArrPos ] = symexpress3.SymNumber() # place holder

      for iCnt in range( 0, iNumArray ):
        elemSub = elem.copy()
        elemSub.elements[ iArrPos ] = arrElem.elements[ iCnt ]
        result.add( elemSub )

      return result

    def _subExpandSymSymExpress( elem ):
      return _subExpandSymFunction( elem )


    if self.checkType( elem, action ) != True:
      return None

    if not isinstance( elem, ( symexpress3.SymArray, symexpress3.SymFunction)) :
      return None

    result = None
    if isinstance( elem, symexpress3.SymArray ):
      result = _subExpandSymArray( elem )
    elif isinstance( elem, symexpress3.SymFunction ):
      result = _subExpandSymFunction( elem )
    return result


#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  symTest = symexpress3.SymFormulaParser( "[ 4 | [ a | b ] | 4 ]" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  testClass = OptSymAnyExpandArray()
  symNew    = testClass.optimize( symTest, "expandArrays" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "[ 4 | a | b | 4 ]":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymAny optimize {testClass.name}, unit test error: {str( symTest )}, value: {symNew}' )


  symTest = symexpress3.SymFormulaParser( "cos( 1, [ 2 | 3 ], 4)" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  testClass = OptSymAnyExpandArray()
  symNew    = testClass.optimize( symTest, "expandArrays" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "[  cos( 1,2,4 ) |  cos( 1,3,4 ) ]":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymAny optimize {testClass.name}, unit test error: {str( symTest )}, value: {symNew}' )

if __name__ == '__main__':
  Test( True )
