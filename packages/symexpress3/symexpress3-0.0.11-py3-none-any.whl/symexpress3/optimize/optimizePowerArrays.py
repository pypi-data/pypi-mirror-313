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

from symexpress3          import symexpress3
from symexpress3.optimize import optimizeBase

class OptimizePowerArrays( optimizeBase.OptimizeBase ):
  """
  Put the power of the array into the elements
  """
  def __init__( self ):
    super().__init__()
    self._name         = "powerArrays"
    self._symtype      = "all"
    self._desc         = "Put the power of the array into the elements"

  def optimize( self, symExpr, action ):
    result = False

    if self.checkExpression( symExpr, action ) != True:
      # print( "Afgekeurd: " + symExpr.symType )
      return result

    for elem in symExpr.elements:
      if not isinstance( elem, symexpress3.SymArray ):
        continue
      if elem.power == 1:
        continue

      for iCnt2, elem2 in enumerate( elem.elements ):
        symNew                  = symexpress3.SymExpress( '*' )
        symNew.powerSign        = elem.powerSign
        symNew.powerCounter     = elem.powerCounter
        symNew.powerDenominator = elem.powerDenominator
        symNew.onlyOneRoot      = elem.onlyOneRoot
        symNew.add( elem2 )
        elem.elements[ iCnt2 ] = symNew

      elem.powerSign        = 1
      elem.powerCounter     = 1
      elem.powerDenominator = 1
      result                = True

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

  symTest = symexpress3.SymFormulaParser( '[ 2 | 4 ]^^2' )
  symTest.optimize()
  symOrg = symTest.copy()

  testClass = OptimizePowerArrays()
  testClass.optimize( symTest, "powerArrays" )

  _Check( testClass, symOrg, symTest, "[ (2)^^2 | (4)^^2 ]" )

if __name__ == '__main__':
  Test( True )
