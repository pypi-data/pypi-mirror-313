#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Write out number powers for Sym Express 3

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

class OptSymNumberPower( optTypeBase.OptTypeBase ):
  """
  Write out powers
  """
  def __init__( self ):
    super().__init__()
    self._name         = "power"
    self._symtype      = symexpress3.SymNumber
    self._desc         = "Write out powers"

  def optimize( self, elem, action ):
    if self.checkType( elem, action ) != True:
      return None

    if ( elem.power != 1 and elem.power != -1 and elem.powerCounter > 1 ):
      # can write out power
      pass
    else:
      return None

    if ( elem.powerDenominator > 1 and elem.factSign == -1 ):
      # first calc the roots
      return None

    # print( 'number _writeOutPowers: {} powerCounter: {}, power: {} deno: {}, value: {}'.format( str( elem  ), elem.powerCounter, elem.power, elem.powerDenominator, elem.getValue() ))

    elemnew = elem.copy()

    iFactC = elemnew.factCounter   * elemnew.factSign
    iFactD = elemnew.factDenominator
    for _ in range(1, elemnew.powerCounter ):
      iFactC *= elemnew.factCounter * elemnew.factSign
      iFactD *= elemnew.factDenominator
    elemnew.factSign        = 1
    elemnew.powerCounter    = 1
    elemnew.factCounter     = iFactC
    elemnew.factDenominator = iFactD

    # print( 'number _writeOutPowers after: {}, value: {}'.format( str( elemnew ), elemnew.getValue() ))

    return elemnew

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  symTest = symexpress3.SymNumber( 1, 2, 3, 1, 3, 1, 1 )

  testClass = OptSymNumberPower()
  symNew    = testClass.optimize( symTest, "power" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "(8/27)":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymNumber optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symNew )}' )


if __name__ == '__main__':
  Test( True )
