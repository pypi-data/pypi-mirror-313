#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    sin(atan(x)/n) for Sym Express 3

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

class OptSymFunctionSinAtanDivNToSinICos( optFunctionBase.OptFunctionBase ):
  """
  sin(atan(x)/n) to sin i + cos
  """
  def __init__( self ):
    super().__init__()
    self._name         = "sinAtanDivNToSinICos"
    self._desc         = "Convert sin(atan(x)/n) to value"
    self._funcName     = "sin"                    # name of the function
    self._minparams    = 1                        # minimum number of parameters
    self._maxparams    = 1                        # maximum number of parameters


  def optimize( self, elem, action ):
    # sin(atan(x)/n) = ( (cos(atan(x)) + i sin(atan(x)))^(1/n) - (cos(atan(x)) - i sin(atan(x)))^(1/n) ) / (2 i)
    if self.checkType( elem, action ) != True:
      return None

    elem1 = elem.elements[0]
    if not isinstance( elem1, symexpress3.SymExpress ):
      return None

    if elem1.symType != '*':
      return None

    if elem1.numElements() != 2: # can be any number greater as 1 but for the moment only atan
      return None

    elemA = elem1.elements[0]
    elemB = elem1.elements[1]
    # one must be a function, second must be number

    if not isinstance( elemA, symexpress3.SymFunction):
      elemB = elem1.elements[0]
      elemA = elem1.elements[1]

    if not isinstance( elemA, symexpress3.SymFunction):
      return None

    if not isinstance( elemB, symexpress3.SymNumber):
      return None

    if elemA.name != "atan":  # can be anything but for the moment only atan
      return None

    # if elemB.power != 1 and elemB.power != -1:
    if not elemB.power in (1, -1):
      return None

    if elemB.factSign != 1:
      return None

    # if elem.name == "sin":
    convertFrm = "( (cos(atan(x)) + i * sin(atan(x)))^^(y) - (cos(atan(x)) - i * sin(atan(x)))^^(y) ) / (2 * i)"
    # else:
    #   convertFrm = "( (cos(atan(x)) + i * sin(atan(x)))^^(y) + (cos(atan(x)) - i * sin(atan(x)))^^(y) ) / 2"

    convertFrm = convertFrm.replace( "y"      , str( elemB ))
    convertFrm = convertFrm.replace( "atan(x)", str( elemA ))

    exprResult = symexpress3.SymFormulaParser( convertFrm  )
    exprResult.optimizeNormal()

    return exprResult

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  symTest = symexpress3.SymFormulaParser( "sin(atan(x)/5)" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]

  # print( "symTest: " + str( symTest ))

  testClass = OptSymFunctionSinAtanDivNToSinICos()
  symNew    = testClass.optimize( symTest, "sinAtanDivNToSinICos" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "(2 * i)^^-1 * ( cos(  atan( x ) ) + i *  sin(  atan( x ) ))^^(1/5) + (2 * i)^^-1 * (-1) * ( cos(  atan( x ) ) + (-1) * i *  sin(  atan( x ) ))^^(1/5)":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymFunction optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symNew )}' )


if __name__ == '__main__':
  Test( True )
