#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Write out powers for Sym Express 3

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

from symexpress3          import symexpress3
from symexpress3.optimize import optimizeBase

class OptimizePower( optimizeBase.OptimizeBase ):
  """
  Write out all the powers greater then one so that they become one.
  \n (x+1)^2 becomes (x+1)(x+1)
  """
  def __init__( self ):
    super().__init__()
    self._name         = "power"
    self._symtype      = "all"
    self._desc         = "Write out all the powers greater then one"


  def optimize( self, symExpr, action ):
    result = False

    if self.checkExpression( symExpr, action ) != True:
      # print( "Afgekeurd: " + symExpr.symType )
      return result

    if symExpr.powerCounter > 1 :
      if (symExpr.powerDenominator > 1 and symExpr.onlyOneRoot == 1):
        # (x+2)^^(2/3)
        # first calc the 1/3 principal root then the power
        # if number >= 0 you can do the power
        try:
          calcReal = symExpr.getValue()
        except: # pylint: disable=bare-except
          return False

        if isinstance( calcReal, list ):
          return False

        if isinstance( calcReal, complex ):
          return False

        if calcReal < 0:
          return False

      copysymExpr = symExpr.copy()
      copysymExpr.powerSign        = 1
      copysymExpr.powerCounter     = 1
      copysymExpr.powerDenominator = 1

      elemClone = []
      for _ in range( 0, symExpr.powerCounter ) :
        elemClone.append( copysymExpr.copy() )

      symExpr.symType      = '*'
      symExpr.elements     = elemClone
      symExpr.powerCounter = 1
      result               = True

    return result

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
      raise NameError( f'optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symOrg )}' )

  result = False
  symTest = symexpress3.SymFormulaParser( '(a + b)^2' )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  # symexpress3.SymExpressTree( symTest )
  symOrg = symTest.copy()

  testClass = OptimizePower()
  result |= testClass.optimize( symTest, "power" )

  _Check( testClass, symOrg, symTest, "(a + b) * (a + b)" )


  symTest = symexpress3.SymFormulaParser( '(a * b)^2' )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  # symexpress3.SymExpressTree( symTest )
  symOrg = symTest.copy()

  testClass = OptimizePower()
  testClass.optimize( symTest, "power" )

  _Check( testClass, symOrg, symTest, "a * b * a * b" )


if __name__ == '__main__':
  Test( True )
