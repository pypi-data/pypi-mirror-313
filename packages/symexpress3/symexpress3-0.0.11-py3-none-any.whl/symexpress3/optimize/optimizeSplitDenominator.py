#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Splt denominator in there lowest form for Sym Express 3

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

class OptimizeSplitDenominator( optimizeBase.OptimizeBase ):
  """
  Write out roots in there lowest form
  \n 1 / ( a * b * c ) into 1/a * 1/b * 1/c
  """
  def __init__( self ):
    super().__init__()
    self._name         = "splitDenominator"
    self._symtype      = "*"
    self._desc         = "Split denominator"


  def optimize( self, symExpr, action ):
    result = False

    if self.checkExpression( symExpr, action ) != True:
      return result

    if symExpr.powerSign != -1:
      return result

    # get the imaginary and numbers out
    exprNew = symexpress3.SymExpress( '*' )
    for iCnt in range( len( symExpr.elements ) - 1, -1, -1 ):
      elem = symExpr.elements[ iCnt ]

      if isinstance( elem, symexpress3.SymNumber ):
        elem.powerSign = elem.powerSign * -1
        exprNew.add( elem )
        del symExpr.elements[ iCnt ]
        continue
      if ( isinstance( elem, symexpress3.SymVariable ) and elem.name == 'i' ):
        elem.powerSign = elem.powerSign * -1
        exprNew.add( elem )
        del symExpr.elements[ iCnt ]
        continue

    if exprNew.numElements() == 0 :
      return result

    result = True

    exprReplace = symexpress3.SymExpress( '*', -1, 1, 1 )
    exprReplace.elements = symExpr.elements

    symExpr.powerSign = 1
    symExpr.elements  = []

    if exprReplace.numElements() > 0:
      symExpr.add( exprReplace )

    for elemExpr in exprNew.elements:
      symExpr.add( elemExpr )

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

  symTest = symexpress3.SymFormulaParser( '1 / (a * i * 3)' )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  # symexpress3.SymExpressTree( symTest )
  symOrg = symTest.copy()

  testClass = OptimizeSplitDenominator()
  testClass.optimize( symTest, "splitDenominator" )

  _Check( testClass, symOrg, symTest, "(a)^^-1 * 3^^-1 * i^^-1" )

if __name__ == '__main__':
  Test( True )
