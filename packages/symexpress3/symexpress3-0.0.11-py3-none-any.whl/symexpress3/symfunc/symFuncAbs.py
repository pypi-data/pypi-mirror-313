#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Abs function for Sym Express 3

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


    https://en.wikipedia.org/wiki/Absolute_value
"""

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncBase

class SymFuncAbs( symFuncBase.SymFuncBase ):
  """
  Abs function, round to the highest integer
  """
  def __init__( self ):
    super().__init__()
    self._name      = "abs"
    self._desc      = "Absolute value"
    self._minparams = 1    # minimum number of parameters
    self._maxparams = 1    # maximum number of parameters
    self._syntax    = "abs(<x>)"


  def functionToValue( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return None

    # absolute value of x
    elem2 = elem.elements[ 0 ]
    if isinstance ( elem2, symexpress3.SymNumber ):
      # if elem2.power != 1 and elem2.power != -1 ):
      if not elem2.power in ( 1, -1 ):
        return None

      if elem2.factSign == -1:
        elemnew = elem2.copy()
        elemnew.factSign = 1

        elemnew.powerSign        = elem.powerSign
        elemnew.powerCounter     = elem.powerCounter
        elemnew.powerDenominator = elem.powerDenominator
        elemnew.onlyOneRoot      = elem.onlyOneRoot

        return elemnew

      elem2.powerSign        = elem.powerSign
      elem2.powerCounter     = elem.powerCounter
      elem2.powerDenominator = elem.powerDenominator

      return elem2

    if not isinstance( elem2, symexpress3.SymExpress ):
      return None

    # check if the number is positief
    dVars = elem2.getVariables()
    varsOk = True
    for dVar in dVars :
      # function with variables not supported, only predefined variables are ok
      if not dVar in ( 'e', 'pi' ):
        varsOk = False
        break
    if varsOk == True:
      # no arrays allowed
      if elem2.existArray() == False:
        try:
          calcValue = elem2.getValue()
        except: # pylint: disable=bare-except
          return None

        if isinstance( calcValue, list ): # just to be sure
          return None

        if not isinstance( calcValue, complex ):
          elemnew = symexpress3.SymExpress( '*' )
          elemnew.powerSign        = elem.powerSign
          elemnew.powerCounter     = elem.powerCounter
          elemnew.powerDenominator = elem.powerDenominator
          elemnew.onlyOneRoot      = elem.onlyOneRoot

          if calcValue < 0:
            elemnew.add( symexpress3.SymNumber( -1, 1, 1, 1, 1, 1, 1 ) ) # -1
          elemnew.add( elem2 )
          return elemnew

    # if ( elem2.power != 1 and elem2.power != -1 ):
    if not elem2.power in ( 1, -1 ):
      return None

    if elem2.symType != '*':
      return None

    # look if there are only numbers
    for iCnt in range( 0, elem2.numElements()):
      elemsub = elem2.elements[ iCnt ]
      if not isinstance( elemsub, symexpress3.SymNumber ):
        return None
      if not elemsub.power in ( 1, -1 ):
        return None

    elemnew = elem2.copy()
    for iCnt in range( 0, elemnew.numElements()):
      elemsub = elemnew.elements[ iCnt ]
      elemsub.factSign = 1

    elemnew.powerSign        = elem.powerSign
    elemnew.powerCounter     = elem.powerCounter
    elemnew.powerDenominator = elem.powerDenominator
    elemnew.onlyOneRoot      = elem.onlyOneRoot
    return elemnew

  def _getValueSingle( self, dValue, dValue2 = None ):
    return abs( dValue )


#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  def _Check(  testClass, symTest, value, dValue, valueCalc, dValueCalc ):
    if display == True :
      print( f"naam    : {testClass.name}" )
      print( f"function: {str( symTest )}" )
      print( f"Value   : {str( value   )}" )
      print( f"DValue  : {str( dValue  )}" )

    if str( value ) != valueCalc or dValue != dValueCalc:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, value: {value}' )


  symTest = symexpress3.SymFormulaParser( 'abs( 6 )' )
  symTest.optimize()
  testClass = SymFuncAbs()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, dValue, "6", 6 )


  symTest = symexpress3.SymFormulaParser( 'abs( -6 )' )
  symTest.optimize()
  testClass = SymFuncAbs()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, dValue, "6", 6 )


  symTest = symexpress3.SymFormulaParser( 'abs( -2 * 3 )' )
  symTest.optimize()
  testClass = SymFuncAbs()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, dValue, "(-1) * (-2) * 3", 6 )


if __name__ == '__main__':
  Test( True )
