#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    De-nest radicals (onlyOneRoot) for Sym Express 3

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

class OptimizeNestedRadicals( optimizeBase.OptimizeBase ):
  """
  de-nest radicals (onlyOneRoot)
  """
  def __init__( self ):
    super().__init__()
    self._name         = "nestedRadicals"
    self._symtype      = "all"
    self._desc         = "De-nest principal radicals"


  def optimize( self, symExpr, action ):
    result = False
    if self.checkExpression( symExpr, action ) != True:
      # print( "Afgekeurd: " + symExpr.symType )
      return result

    if ( symExpr.numElements() > 1 and symExpr.symType != '*' ):
      return result

    if symExpr.onlyOneRoot != 1:
      return result

    if symExpr.powerDenominator == 1:
      return result

    elemRadicals = []
    elemNormal   = []
    for elem in symExpr.elements :
      if ( elem.onlyOneRoot == 0 or symExpr.powerDenominator == 1 ):
        elemNormal.append( elem )
      else:
        elemRadicals.append( elem )
    if len(elemRadicals ) == 0:
      return result
    if len(elemNormal) == 0:
      elemNormal.append ( symexpress3.SymNumber( 1,1,1,1,1,1 ))

    # 2 list of elements
    # - normals
    # - radicals
    # Put the normals in a new expression
    exprNormal = symexpress3.SymExpress( '*' )
    exprNormal.powerSign        = symExpr.powerSign
    exprNormal.powerCounter     = symExpr.powerCounter
    exprNormal.powerDenominator = symExpr.powerDenominator
    exprNormal.onlyOneRoot      = symExpr.onlyOneRoot
    exprNormal.elements         = elemNormal

    symExpr.elements = []
    symExpr.elements.append( exprNormal )
    symExpr.powerSign       = 1
    symExpr.powerCounter    = 1
    symExpr.powerDenominator= 1
    # add the radicals
    for elem in elemRadicals :
      iCounter     = exprNormal.powerCounter * exprNormal.powerSign * elem.powerCounter * elem.powerSign
      iDenominator = exprNormal.powerDenominator * elem.powerDenominator

      elem.powerSign        = 1
      elem.powerCounter     = iCounter
      elem.powerDenominator = iDenominator

      symExpr.add( elem )
      result = True

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

  symTest = symexpress3.SymFormulaParser( '(2 * 5^^(1/3))^^(1/3)' )
  symTest.optimize()
  symTest.optimize( "multiple" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]

  # symexpress3.SymExpressTree( symTest )

  symOrg = symTest.copy()

  testClass = OptimizeNestedRadicals()
  testClass.optimize( symTest, "nestedRadicals" )

  _Check( testClass, symOrg, symTest, "(1)^^(1/3) * 2^^(1/3) * 5^^(1/9)" )


if __name__ == '__main__':
  Test( True )
