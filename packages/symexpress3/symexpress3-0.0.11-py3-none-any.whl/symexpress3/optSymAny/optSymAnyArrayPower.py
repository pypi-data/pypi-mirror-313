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

class OptSymAnyArrayPower( optTypeBase.OptTypeBase ):
  """
  Put the power of an array into his elements
  """
  def __init__( self ):
    super().__init__()
    self._name         = "arrayPower"
    self._desc         = "Put the power of an array into his elements"

  def optimize( self, elem, action ):
    if self.checkType( elem, action ) != True:
      return None

    if not isinstance( elem, symexpress3.SymArray) :
      return None

    if elem.power == 1 and elem.onlyOneRoot == 1 :
      return None

    # print( "Array start: " + str( elem ))  
      
    newArray = symexpress3.SymArray()
    
    for iCnt, elemsub in enumerate( elem.elements ):
      symSub = symexpress3.SymExpress( '*' )
      symSub.powerCounter     = elem.powerCounter
      symSub.powerDenominator = elem.powerDenominator
      symSub.powerSign        = elem.powerSign
      symSub.onlyOneRoot      = elem.onlyOneRoot
      symSub.add( elemsub )
      newArray.add( symSub )
      
    # print( "Array end: " + str( newArray ))
    
    return newArray

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  symTest = symexpress3.SymFormulaParser( "[ 4 | 2 ]^^2" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  testClass = OptSymAnyArrayPower()
  symNew    = testClass.optimize( symTest, "arrayPower" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "[ (4)^^2 | (2)^^2 ]":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymAny optimize {testClass.name}, unit test error: {str( symTest )}, value: {symNew}' )


if __name__ == '__main__':
  Test( True )
