#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Cos to sum for Sym Express 3

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

class OptSymFunctionCosToE( optFunctionBase.OptFunctionBase ):
  """
  Convert cos to e
  """
  def __init__( self ):
    super().__init__()
    self._name         = "cosToE"
    self._desc         = "Convert cos to e power"
    self._funcName     = "cos"                    # name of the function
    self._minparams    = 1                        # minimum number of parameters
    self._maxparams    = 1                        # maximum number of parameters


  def optimize( self, elem, action ):
    if self.checkType( elem, action ) != True:
      return None

    elemParam = elem.elements[ 0 ]

    # https://en.wikipedia.org/wiki/Sine_and_cosine
    elemSym = symexpress3.SymFormulaParser( "(exp( i * x ) + exp( -i * x )) / 2" )

    dDict = {}
    dDict[ 'x' ] = str( elemParam )

    elemSym.replaceVariable( dDict )

    elemSym.powerCounter     = elem.powerCounter
    elemSym.powerDenominator = elem.powerDenominator
    elemSym.powerSign        = elem.powerSign
    elemSym.onlyOneRoot      = elem.onlyOneRoot

    return elemSym

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  symTest = symexpress3.SymFormulaParser( "cos(1/3)" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]

  # print( "symTest: " + str( symTest ))

  testClass = OptSymFunctionCosToE()
  symNew    = testClass.optimize( symTest, "cosToE" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "( exp( i * 1 * 3^^-1 ) +  exp( (-1) * i * 1 * 3^^-1 )) * 2^^-1":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymFunction optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symNew )}' )

if __name__ == '__main__':
  Test( True )
