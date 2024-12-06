#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Rising Factorial function for Sym Express 3

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


    https://en.wikipedia.org/wiki/Falling_and_rising_factorials

"""

from symexpress3          import symexpress3
from symexpress3.symfunc  import symFuncBase
from symexpress3          import symtools


class SymFuncRisingFactorial( symFuncBase.SymFuncBase ):
  """
  Rising Factorial function, product( k, 1, n, x + k - 1 )
  """
  def __init__( self ):
    super().__init__()
    self._name        = "risingfactorial"
    self._desc        = "Rising Factorial product( k, 1, n, x + k - 1 )"
    self._minparams   = 2    # minimum number of parameters
    self._maxparams   = 2    # maximum number of parameters
    self._syntax      = "risingfactorial(<fnc>,<n>)"
    self._synExplain  = "risingfactorial(<fnc>,<n>) = product(k, 1, n, <fnc> + k - 1)"

  def functionToValue( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return None

    elemFunc  = elem.elements[ 0 ]
    elemEnd   = elem.elements[ 1 ]

    if not isinstance( elemEnd, symexpress3.SymNumber):
      dVars = elemEnd.getVariables()
      if len( dVars ) != 0:
        return None
    else:
      if elemEnd.power != 1:
        return None
      if elemEnd.factDenominator != 1:
        return None

    try:
      endVal   = elemEnd.getValue()
    except: # pylint: disable=bare-except
      return None

    if not isinstance(endVal, int):
      return None

    if endVal < 0 :
      return None

    if endVal == 0:
      elemSym = symexpress3.SymFormulaParser( "1" )
    else:
      # if function is a hole number then special case
      if ( isinstance( elemFunc, symexpress3.SymNumber ) and
           elemFunc.factSign         == 1 and
           elemFunc.factDenominator  == 1 and
           elemFunc.powerSign        == 1 and
           elemFunc.powerCounter     == 1 and
           elemFunc.powerDenominator == 1      ) :

        elemStr = "factorial( xRisingFactorial + nRisingFactorial - 1 ) / factorial( xRisingFactorial - 1 )"
        elemSym = symexpress3.SymFormulaParser( elemStr )

        dDict = {}
        dDict[ 'xRisingFactorial' ] = str( elemFunc )
        dDict[ 'nRisingFactorial' ] = str( elemEnd  )

        elemSym.replaceVariable( dDict )
      else:

        varName = symtools.VariableGenerateGet()
        elemStr = "product(" + varName + ", 1, nRisingFactorial, xRisingFactorial + " + varName + " - 1)"
        elemSym = symexpress3.SymFormulaParser( elemStr )

        dDict = {}
        dDict[ 'xRisingFactorial' ] = str( elemFunc )
        dDict[ 'nRisingFactorial' ] = str( elemEnd  )

        elemSym.replaceVariable( dDict )

    elemSym.powerCounter     = elem.powerCounter
    elemSym.powerDenominator = elem.powerDenominator
    elemSym.powerSign        = elem.powerSign
    elemSym.onlyOneRoot      = elem.onlyOneRoot

    return elemSym

  def _getValueSingle( self, dValue, dValue2 = None ):
    # product(k, 1, n, <fnc> + k - 1)"

    result = 1
    for k in range( 1, dValue2 + 1):
      result *= (dValue + k - 1)

    return result

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  def _Check( testClass, symTest, value, dValue, valueCalc, dValueCalc ):
    if dValue != None:
      dValue = round( dValue, 10 )
    if dValueCalc != None:
      dValueCalc = round( dValueCalc, 10 )
    if display == True :
      print( f"naam    : {testClass.name}" )
      print( f"function: {str( symTest )}" )
      print( f"Value   : {str( value   )}" )
      print( f"DValue  : {str( dValue  )}" )

    if str( value ).strip() != valueCalc.strip() or (dValueCalc != None and dValue != dValueCalc) : # pylint: disable=consider-using-in
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, value: {value} <> {valueCalc}, dValue:{dValue} <> {dValueCalc}' )

  symtools.VariableGenerateReset()

  symTest = symexpress3.SymFormulaParser( 'risingfactorial( 5, 4 )' )
  symTest.optimize()
  testClass = SymFuncRisingFactorial()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check( testClass, symTest, value, dValue, "factorial( 5 + 4 + (-1) * 1 ) *  factorial( 5 + (-1) * 1 )^^-1", 1680 )


  symtools.VariableGenerateReset()

  symTest = symexpress3.SymFormulaParser( 'risingfactorial( x, 4 )' )
  symTest.optimize()
  testClass = SymFuncRisingFactorial()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = None # testClass.getValue(        symTest.elements[ 0 ] )

  _Check( testClass, symTest, value, dValue, "product( n1,1,4,x + n1 + (-1) * 1 )", None )



if __name__ == '__main__':
  Test( True )
