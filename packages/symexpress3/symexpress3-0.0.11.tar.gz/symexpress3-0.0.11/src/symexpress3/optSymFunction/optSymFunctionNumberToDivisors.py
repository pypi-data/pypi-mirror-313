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
from symexpress3 import primefactor

class OptSymFunctionNumberToDivisors( optFunctionBase.OptFunctionBase ):
  """
  Convert a given number into all his divisors as an add sum
  """
  def __init__( self ):
    super().__init__()
    self._name         = "numberToDivisors"
    self._desc         = "Convert a given number to all his divisors as an add sum"
    self._funcName     = "numberToDivisors"       # name of the function
    self._minparams    = 1                        # minimum number of parameters
    self._maxparams    = 1                        # maximum number of parameters


  def optimize( self, elem, action ):
    if self.checkType( elem, action ) != True:
      return None

    elemParam = elem.elements[ 0 ]
    if not isinstance( elemParam, symexpress3.SymNumber ):
      return None

    if elemParam.factCounter == 1 and elemParam.factDenominator == 1:
      return None

    if not elemParam.power in (1, -1):
      return None

    factCount = None
    factDenom = None

    if elemParam.factCounter != 1:
      factCount = primefactor.FactorAllInt( elemParam.factCounter )

    if elemParam.factDenominator != 1:
      factDenom = primefactor.FactorAllInt( elemParam.factDenominator )


    elemSym = symexpress3.SymExpress( '+' )

    signNumber = 1
    if elemParam.factSign == -1:
      signNumber = -1

    if factCount != None:
      for value in factCount :
        symNew = symexpress3.SymNumber( signNumber, value, 1, 1, 1, 1, 1)
        elemSym.add( symNew )

    if factDenom != None:
      symExtra = None
      if factCount != None:
        symExtra = elemSym.copy()
        elemSym.elements = []

      for value in factDenom:
        symNew = symexpress3.SymNumber( signNumber, value, 1, -1, 1, 1, 1)
        elemSym.add( symNew )

      if symExtra != None:
        symExtra2 = elemSym.copy()
        elemSym = symexpress3.SymExpress( '*' )
        elemSym.add( symExtra  )
        elemSym.add( symExtra2 )

    elemSym.powerCounter     = elem.powerCounter
    elemSym.powerDenominator = elem.powerDenominator
    elemSym.powerSign        = elem.powerSign  * elemParam.power
    elemSym.onlyOneRoot      = elem.onlyOneRoot

    return elemSym

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """

  def _Check( testClass, symOrg, symTest, wanted ):
    if display == True :
      print( f"naam      : {testClass.name}" )
      print( f"orginal   : {str( symOrg  )}" )
      print( f"optimized : {str( symTest )}" )

    if str( symTest ).strip() != wanted:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'SymFunction optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symOrg )}' )


  symTest = symexpress3.SymFormulaParser( "numberToDivisors( -12 )" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]

  testClass = OptSymFunctionNumberToDivisors()
  symNew    = testClass.optimize( symTest, "numberToDivisors" )

  _Check( testClass, symTest, symNew, "(-1) + (-2) + (-3) + (-4) + (-6) + (-12)" )


  symTest = symexpress3.SymFormulaParser( "numberToDivisors( 1/309 )^^(1/2)" )
  symTest.optimize()
  symTest.optimize( "multiply")
  symTest.optimize()
  symTest = symTest.elements[ 0 ]

  testClass = OptSymFunctionNumberToDivisors()
  symNew    = testClass.optimize( symTest, "numberToDivisors" )

  _Check( testClass, symTest, symNew, "(1^^-1 + 3^^-1 + 103^^-1 + 309^^-1)^^(1/2)" )


  symTest = symexpress3.SymFormulaParser( "numberToDivisors( 25/309 )" )
  symTest.optimize()
  symTest.optimize( "multiply")
  symTest.optimize()
  symTest = symTest.elements[ 0 ]

  testClass = OptSymFunctionNumberToDivisors()
  symNew    = testClass.optimize( symTest, "numberToDivisors" )

  _Check( testClass, symTest, symNew, "(1 + 5 + 25) * (1^^-1 + 3^^-1 + 103^^-1 + 309^^-1)" )


if __name__ == '__main__':
  Test( True )
