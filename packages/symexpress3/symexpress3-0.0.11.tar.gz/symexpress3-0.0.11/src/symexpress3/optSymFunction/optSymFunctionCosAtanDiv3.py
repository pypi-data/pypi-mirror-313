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

class OptSymFunctionCosAtanDiv3( optFunctionBase.OptFunctionBase ):
  """
  cos(atan(x)/n) to sin i + cos
  """
  def __init__( self ):
    super().__init__()
    self._name         = "cosAtanDiv3"
    self._desc         = "Convert cos(atan(x)/3) to value"
    self._funcName     = "cos"                    # name of the function
    self._minparams    = 1                        # minimum number of parameters
    self._maxparams    = 1                        # maximum number of parameters


  def optimize( self, elem, action ):
    # https://www.quora.com/Is-there-a-method-to-calculate-cos-%CF%80-7-and-sin-%CF%80-7
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

    if elemB.power != 1:
      return None

    if elemB.factSign != 1:
      return None

    if elemB.factCounter != 1:
      return None

    if elemB.factDenominator != 3:
      return None

    # elemA = atan(x)
    # elemB = 1/3

    # "(( ((cos(x)^^2 - 1)^^(1/2) + cos(x))^^(1/3) + ( ((cos(x)^^2 - 1)^^(1/2) + cos(x))^^(1/3) )^^(-1))) * 1/2"

    convertFrm = "(( ((cos(" + str( elemA ) + ")^^2 - 1)^^(1/2) + cos(" + str(elemA) + "))^^(1/3) + (( ((cos(" + str( elemA ) + ")^^2 - 1)^^(1/2) + cos(" + str(elemA) + "))^^(1/3) )^^(-1))) * 1/2"

    exprResult = symexpress3.SymFormulaParser( convertFrm  )

    return exprResult
    # https://www.quora.com/What-is-the-formula-for-sin-x-3-one-third-angle-formula
    # sin(x/3) =
    # (
    #  ( -1 * sin( x ) + (sin(x)^^2 - 1)^^(1/2) ) / 8
    # )^^(1/3)
    #  +
    # (
    #  ( -1 * sin( x ) - (sin(x)^^2 - 1)^^(1/2) ) / 8
    # )^^(1/3)
    #
    # wrong answers on the following conditions :
    # x = pi / 2 - 1/10     -> wrong answer, same as pi / 2 + 1/10
    # x = pi / 2 + 1/10     -> correct answer
    # x = pi / 2            -> correct answer -> Looks like a mirror
    #                                            Everything below is wrong, above is correct

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  symTest = symexpress3.SymFormulaParser( "cos(atan(x)/3)" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]

  # print( "symTest: " + str( symTest ))

  testClass = OptSymFunctionCosAtanDiv3()
  symNew    = testClass.optimize( symTest, "cosAtanDiv3" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "((( cos(  atan( x ) )^^2 + (-1) * 1)^^(1/2) +  cos(  atan( x ) ))^^(1/3) + ((( cos(  atan( x ) )^^2 + (-1) * 1)^^(1/2) +  cos(  atan( x ) ))^^(1/3))^^-1) * 1 * 2^^-1":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymFunction optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symNew )}' )


if __name__ == '__main__':
  Test( True )
