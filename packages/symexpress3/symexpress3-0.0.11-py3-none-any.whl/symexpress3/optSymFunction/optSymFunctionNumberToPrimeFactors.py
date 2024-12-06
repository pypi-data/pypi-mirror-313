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

class OptSymFunctionNumberToPrimeFactors( optFunctionBase.OptFunctionBase ):
  """
  Convert a given number into prime factors
  """
  def __init__( self ):
    super().__init__()
    self._name         = "numberToPrimeFactors"
    self._desc         = "Convert a given number to prime factors"
    self._funcName     = "numberToPrimeFactors"   # name of the function
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
      factCount = primefactor.FactorizationDict( elemParam.factCounter )

    if elemParam.factDenominator != 1:
      factDenom = primefactor.FactorizationDict( elemParam.factDenominator )

    elemSym = symexpress3.SymExpress( '*' )

    if elemParam.factSign == -1:
      symNew = symexpress3.SymNumber( -1, 1, 1, 1, 1, 1, 1)
      elemSym.add( symNew )

    if factCount != None:
      for key, value in factCount.items():
        symNew = symexpress3.SymNumber( 1, key, 1, 1, value, 1, 1)
        elemSym.add( symNew )

    if factDenom != None:
      for key, value in factDenom.items():
        symNew = symexpress3.SymNumber( 1, key, 1, -1, value, 1, 1)
        elemSym.add( symNew )

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


  symTest = symexpress3.SymFormulaParser( "numberToPrimeFactors( 12 )" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]

  testClass = OptSymFunctionNumberToPrimeFactors()
  symNew    = testClass.optimize( symTest, "numberToPrimeFactors" )

  _Check( testClass, symTest, symNew, "2^^2 * 3" )


  symTest = symexpress3.SymFormulaParser( "numberToPrimeFactors( 1 / 309 )^^(1/2)" )
  symTest.optimize()
  symTest.optimize( "multiply")
  symTest.optimize()
  symTest = symTest.elements[ 0 ]

  testClass = OptSymFunctionNumberToPrimeFactors()
  symNew    = testClass.optimize( symTest, "numberToPrimeFactors" )

  _Check( testClass, symTest, symNew, "(3^^-1 * 103^^-1)^^(1/2)" )


  symTest = symexpress3.SymFormulaParser( "numberToPrimeFactors( 25 / 309 )" )
  symTest.optimize()
  symTest.optimize( "multiply")
  symTest.optimize()
  symTest = symTest.elements[ 0 ]

  testClass = OptSymFunctionNumberToPrimeFactors()
  symNew    = testClass.optimize( symTest, "numberToPrimeFactors" )

  _Check( testClass, symTest, symNew, "5^^2 * 3^^-1 * 103^^-1" )


if __name__ == '__main__':
  Test( True )
