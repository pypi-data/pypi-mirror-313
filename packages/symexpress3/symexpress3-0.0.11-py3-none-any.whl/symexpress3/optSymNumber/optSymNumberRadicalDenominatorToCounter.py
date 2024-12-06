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

from  symexpress3 import symexpress3
from  symexpress3 import optTypeBase

class OptSymNumberRadicalDenominatorToCounter( optTypeBase.OptTypeBase ):
  """
  Move the radical from the denominator to the counter (principal root only)
  """
  def __init__( self ):
    super().__init__()
    self._name         = "radicalDenominatorToCounter"
    self._symtype      = symexpress3.SymNumber
    self._desc         = "Move the radical from the denominator to the counter, principal root only"

  def optimize( self, elem, action ):
    if self.checkType( elem, action ) != True:
      return None

    if elem.powerSign != -1:
      return None

    if elem.powerDenominator == 1:
      return None

    if elem.onlyOneRoot != 1:
      return None

    if elem.factDenominator != 1: # is this realy needed -> yes, onlyOneRoot = OptimizeOnlyOneRoot()
      return None


    elemnew = elem.copy()

    # ok, found radicals in the denominator = 3^^(-1/3)
    # want 3^^(-1/3) * 3^^(2/3) / 3^^(2/3) = 3^^(-1/3) * 3^^(2/3) 3^^(-2/3) = 3^^(2/3) * 3^(-1) = 3^^(2/3) *  1 / 3
    symNew = symexpress3.SymExpress( '*' )

    elemnew.powerSign        = 1
    elemnew.powerCounter     = elem.powerDenominator - elem.powerCounter
    elemnew.powerDenominator = elem.powerDenominator

    elemnum = symexpress3.SymNumber( 1,elem.factCounter,1, -1,1,1 )

    symNew.add( elemnew )
    symNew.add( elemnum )

    # print( 'symNew: {}'.format( str( symNew )))

    return symNew

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  symTest = symexpress3.SymNumber( 1, 3, 1, -1, 1, 3, 1 )

  testClass = OptSymNumberRadicalDenominatorToCounter()
  symNew    = testClass.optimize( symTest, "radicalDenominatorToCounter" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "3^^(2/3) * 3^^-1":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymNumber optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symNew )}' )


if __name__ == '__main__':
  Test( True )
