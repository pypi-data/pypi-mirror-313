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

from symexpress3 import symexpress3
from symexpress3 import optFunctionBase

class OptSymFunctionEToCosSin( optFunctionBase.OptFunctionBase ):
  """
  Convert e power to cos + i sin
  """
  def __init__( self ):
    super().__init__()
    self._name         = "eToCosSin"
    self._desc         = "Convert e power to cos + i sin"
    self._funcName     = "exp"                    # name of the function
    self._minparams    = 1                        # minimum number of parameters
    self._maxparams    = 2                        # maximum number of parameters


  def optimize( self, elem, action ):
    if self.checkType( elem, action ) != True:
      return None

    if elem.numElements() > 1:
      # only e powers supported
      elemPower = elem.elements[ 1 ]
      if not isinstance( elemPower, symexpress3.SymVariable ):
        return None
      if elemPower.power != 1:
        return None
      if elemPower.name != 'e':
        return None

    elemParam = elem.elements[ 0 ]

    # https://en.wikipedia.org/wiki/Sine_and_cosine
    elemSym = symexpress3.SymFormulaParser( "cos( -i * (x) ) + i sin( -i * (x) )" )

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
  def _Check( testClass, symOrg, symTest, wanted ):
    if display == True :
      print( f"naam      : {testClass.name}" )
      print( f"orginal   : {str( symOrg  )}" )
      print( f"optimized : {str( symTest )}" )

    if str( symTest ).strip() != wanted:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symOrg )}' )

  symTest = symexpress3.SymFormulaParser( 'exp( 3 i )' )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  symOrg  = symTest.copy()

  testClass = OptSymFunctionEToCosSin()
  symTest   = testClass.optimize( symTest, "eToCosSin" )

  _Check( testClass, symOrg, symTest, "cos( (-1) * i * 3 * i ) + i *  sin( (-1) * i * 3 * i )" )


  symTest = symexpress3.SymFormulaParser( 'exp( -3 i, e )' )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  symOrg  = symTest.copy()

  testClass = OptSymFunctionEToCosSin()
  symTest   = testClass.optimize( symTest, "eToCosSin" )

  _Check( testClass, symOrg, symTest, "cos( (-1) * i * (-3) * i ) + i *  sin( (-1) * i * (-3) * i )" )


if __name__ == '__main__':
  Test( True )
