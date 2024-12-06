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
from symexpress3 import optFunctionBase

class OptSymFunctionCosXplusYtoSinCos( optFunctionBase.OptFunctionBase ):
  """
  cos(x+y) = cos(x)cos(y) - sin(x)sin(y)
  """
  def __init__( self ):
    super().__init__()
    self._name         = "cosXplusYtoSinCos"
    self._desc         = "Convert cos(x+y) into cos(x)cos(y) - sin(x)sin(y)"
    self._funcName     = "cos"                    # name of the function
    self._minparams    = 1                        # minimum number of parameters
    self._maxparams    = 1                        # maximum number of parameters


  def optimize( self, elem, action ):
    if self.checkType( elem, action ) != True:
      return None

    # https://en.wikipedia.org/wiki/Trigonometric_functions
    # cos(x+y) into sin(x)cos(y) + cos(x)sin(y)
    elem1 = elem.elements[ 0 ]
    if not isinstance( elem1, symexpress3.SymExpress ):
      return None

    if elem1.symType != '+':
      return None

    if elem1.power != 1:
      return None

    if elem1.numElements() <= 1:
      return None

    elemCopy = elem1.copy()
    elemX    = elemCopy.elements[ 0 ]
    del elemCopy.elements[ 0 ]

    strX = str( elemX )
    strY = str( elemCopy )

    elemStr = '( cos(' + strX + ') * cos(' + strY + ') - sin(' + strX + ')* sin( ' + strY + ') )'

    elemSym = symexpress3.SymFormulaParser( elemStr )
    elemSym.powerSign        = elem.powerSign
    elemSym.powerCounter     = elem.powerCounter
    elemSym.powerDenominator = elem.powerDenominator

    return elemSym

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  symTest = symexpress3.SymFormulaParser( "cos(pi/4 + 5/2)" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]

  testClass = OptSymFunctionCosXplusYtoSinCos()
  symNew    = testClass.optimize( symTest, "cosXplusYtoSinCos" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "( cos( pi * 1 * 4^^-1 ) *  cos( 5 * 1 * 2^^-1 ) + (-1) *  sin( pi * 1 * 4^^-1 ) *  sin( 5 * 1 * 2^^-1 ))":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymFunction optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symNew )}' )


if __name__ == '__main__':
  Test( True )
