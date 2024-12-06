#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Atan2 function for Sym Express 3

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


    https://en.wikipedia.org/wiki/Atan2

"""

import math

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncBase


class SymFuncAtan2( symFuncBase.SymFuncBase ):
  """
  Atan2 function
  """
  def __init__( self ):
    super().__init__()
    self._name      = "atan2"
    self._desc      = "atan2"
    self._minparams = 2    # minimum number of parameters
    self._maxparams = 2    # maximum number of parameters
    self._syntax    = "atan2(<x>,<y>)"


  def functionToValue( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return None

    elem1 = elem.elements[ 0 ]
    elem2 = elem.elements[ 1 ]

    # print( "atan2: {}, type1: {}, typ2: {}".format( str( elem), str( type( elem1)), str(type( elem2))  ))

    dVars = elem1.getVariables()
    if ( dVars != None and len( dVars ) > 0 ):
      for dVar in dVars:
        if not dVar in ('e', 'pi' ):
          return None
      # return None

    dVars = elem2.getVariables()
    if ( dVars != None and len( dVars ) > 0 ):
      for dVar in dVars:
        if not dVar in ('e', 'pi' ):
          return None
      # return None

    # https://en.wikipedia.org/wiki/Atan2
    # 2 numbers
    try:
      valy = elem1.getValue()
      valx = elem2.getValue()
    except: # pylint: disable=bare-except
      return None

    if ( isinstance( elem1, ( list, complex, symexpress3.SymArray ) ) or
         isinstance( elem2, ( list, complex, symexpress3.SymArray ) )   ) :
      return None

    newelem = symexpress3.SymExpress( '*' )
    newelem.powerSign        = elem.powerSign
    newelem.powerCounter     = elem.powerCounter
    newelem.powerDenominator = elem.powerDenominator

    y = "( " + str( elem1 ) + " )"
    x = "( " + str( elem2 ) + " )"
    result = None

    # print ("atan2, x:{}, y:{}".format( x, y ))

    if valx > 0:
      # atan(y/x) ) if x > 0
      result = "atan( " + y + " / " + x + ")"
    elif valy > 0:
      # pi /2 - atan( x/y ) if ( y > 0 )
      result = "pi / 2 - atan( " + x + " / " + y + ")"
    elif valy < 0:
      # - pi / 2 - atan( x /y )  if y < 0
      result = " -pi / 2 - atan( " + x + " / " + y + ")"
    elif valx < 0:
      # atan( y/x + pi  if x < 0
      result = "atan( " + y + " / " + x + ") + pi"
    else:
      # undefined if x = 0 and y = 0
      result = None

    if result != None:
      # print( "elem: {}".format( str( elem )))
      # print( "result atan2: {}".format( result ))
      expfunc = symexpress3.SymFormulaParser( result )
      newelem.add( expfunc )

      return newelem

    return None

  def _getValueSingle( self, dValue, dValue2 = None):
    return math.atan2( dValue, dValue2 )



#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  def _Check(  testClass, symTest, value, dValue, valueCalc, dValueCalc ):
    dValue     = round( dValue    , 10 )
    dValueCalc = round( dValueCalc, 10 )
    if display == True :
      print( f"naam    : {testClass.name}" )
      print( f"function: {str( symTest )}" )
      print( f"Value   : {str( value   )}" )
      print( f"DValue  : {str( dValue  )}" )

    if str( value ).strip() != valueCalc or dValue != dValueCalc :
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, value: {value} <> {valueCalc}, dValue:{dValue} <> {dValueCalc}' )

  symTest = symexpress3.SymFormulaParser( 'atan2( 1 , 2)' )
  symTest.optimize()
  testClass = SymFuncAtan2()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, dValue, "atan( 1 * (2)^^-1 )", 0.4636476090008061 )


  symTest = symexpress3.SymFormulaParser( 'atan2( -1 , 2)' )
  symTest.optimize()
  testClass = SymFuncAtan2()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, dValue, "atan( (-1) * (2)^^-1 )", -0.4636476090008061 )


  symTest = symexpress3.SymFormulaParser( 'atan2( 1 , -2)' )
  symTest.optimize()
  testClass = SymFuncAtan2()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, dValue, "(pi * 2^^-1 + (-1) *  atan( (-2) * (1)^^-1 ))", 2.677945044588987 )


  symTest = symexpress3.SymFormulaParser( 'atan2( -1 , -2)' )
  symTest.optimize()
  testClass = SymFuncAtan2()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, dValue, "((-1) * pi * 2^^-1 + (-1) *  atan( (-2) * ((-1))^^-1 ))", -2.677945044588987 )


if __name__ == '__main__':
  Test( True )
