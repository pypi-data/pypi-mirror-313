#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    expandArrays for Sym Express 3

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


class OptimizeExpandArrays( optimizeBase.OptimizeBase ):
  """
  If the expression containts at least 1 array then make the hole expression an array element.
  \nExample: 2 + [a|b] -> [2+a|2+b]
  """
  def __init__( self ):
    super().__init__()
    self._name         = "expandArrays"
    self._symtype      = "all"
    self._desc         = "If the expression containts at least 1 array then make the hole expression an array element."

  def optimize( self, symExpr, action ):
    result = False

    if self.checkExpression( symExpr, action ) != True:
      return result

    if symExpr.numElements() <= 1 :
      return result

    iArray = -1
    # for iCnt in range( 0, len(symExpr.elements)):
    for iCnt, elemTest in enumerate( symExpr.elements ):
      # if isinstance( symExpr.elements[ iCnt ], symexpress3.SymArray ) :
      if isinstance( elemTest, symexpress3.SymArray ) and elemTest.power == 1 and elemTest.onlyOneRoot == 1:
        iArray = iCnt
        break

    if iArray == -1 :
      return result

    expr = symexpress3.SymExpress( symExpr.symType )
    # for iCnt in range( 0, len(symExpr.elements)):
    for iCnt, elemTest in enumerate( symExpr.elements ):
      if iCnt == iArray :
        continue
      # expr.add( symExpr.elements[ iCnt ] )
      expr.add( elemTest )

    elemarr     = symExpr.elements[ iArray ]

    elemarrfact = symexpress3.SymExpress( '*', elemarr.powerSign, elemarr.powerCounter, elemarr.powerDenominator
                                        , elemarr.onlyOneRoot
                                        )
    newarr  = symexpress3.SymArray()
    for iCnt in range( 0, elemarr.numElements()):
      elem     = elemarr.elements[ iCnt ]
      elemadd  = elemarrfact.copy()
      elemadd.add( elem )
      elemadd2 = expr.copy()
      elemadd2.add( elemadd )
      newarr.add( elemadd2 )
    symExpr.elements = []

    symExpr.add( newarr )
    result = True

    return result


#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Test unit
  """

  def _Check( testClass, symOrg, symTest, wanted ):
    if display == True :
      print( f"naam      : {testClass.name}" )
      print( f"orginal   : {str( symOrg  )}" )
      print( f"optimized : {str( symTest )}" )

    if str( symTest ).strip() != wanted:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symOrg )}' )

  symTest = symexpress3.SymFormulaParser( '2 + [a|b]' )
  symTest.optimize()
  symOrg = symTest.copy()

  testClass = OptimizeExpandArrays()
  testClass.optimize( symTest, "expandArrays" )

  _Check( testClass, symOrg, symTest, "[ 2 + a | 2 + b ]" )

if __name__ == '__main__':
  Test( True )
