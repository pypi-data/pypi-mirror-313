#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Exp function voor Sym Express 3

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


    https://en.wikipedia.org/wiki/Exponential_function

"""

import math

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncBase

class SymFuncExp( symFuncBase.SymFuncBase ):
  """
  Exp function, exponent, exp( x, y ) = y^x
  Default for y = e
  """
  def __init__( self ):
    super().__init__()
    self._name      = "exp"
    self._desc      = "Exponent, y^^x, default is e (e^^x)"
    self._minparams = 1    # minimum number of parameters
    self._maxparams = 2    # maximum number of parameters
    self._syntax    = "exp(<x> [,<y>])"
    self._synExplain= "exp(<x> [,<y>]) = y^^x, default is e (e^^x)"

  def mathMl( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return [], None

    output = ""

    output += '<msup>'

    if elem.numElements() == 2:

      isExtraClose = True
      if (     isinstance( elem.elements[ 1 ], symexpress3.SymNumber )
         and elem.elements[ 1 ].power           == 1
         and elem.elements[ 1 ].factDenominator == 1
         and elem.elements[ 1 ].factSign        == 1 ):
        isExtraClose = False

      if (     isinstance( elem.elements[ 1 ], symexpress3.SymVariable )
         and elem.elements[ 1 ].power           == 1         ):
        isExtraClose = False

      if isExtraClose == True:
        output += "<mfenced separators=''>"

      output += elem.elements[ 1 ].mathMl()

      if isExtraClose == True:
        output += "</mfenced>"
    else:
      output += '<mi>'
      output += 'e'
      output += '</mi>'

    output += elem.elements[ 0 ].mathMl()

    output += '</msup>'

    return ['()'], output


  def functionToValue( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return None
    #
    # x^y
    # elem1 = y
    # elem2 = x if not provided, e is used
    #
    elem1 = elem.elements[ 0 ]

    if not isinstance ( elem1, symexpress3.SymNumber ):
      return None

    if elem1.power != 1:
      return None

    if elem.numElements() < 2:
      elemBase = "e"
    else:
      # array not supported, use expandArray
      if isinstance ( elem.elements[ 1 ], symexpress3.SymArray ):
        return None
      elemBase = str( elem.elements[ 1 ] )

    # print("_convertFuncExp elem1: {}".format(elem1) )
    if str( elem1 ) == "0":
      elemStr = "1"
    else:
      elemStr = "(" + elemBase + ")^^(" + str( elem1 ) + ")"
    # print( "_convertFuncExp: {}".format( elemStr ))

    elemnew = symexpress3.SymFormulaParser( elemStr )

    elemnew.powerSign        = elem.powerSign
    elemnew.powerCounter     = elem.powerCounter
    elemnew.powerDenominator = elem.powerDenominator

    return elemnew


  def _getValueSingle( self, dValue, dValue2 = math.e ):
    dResult = dValue2 ** dValue
    return dResult


#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  def _Check( testClass, symTest, value, dValue, valueCalc, dValueCalc ):
    dValue     = round( dValue    , 10 )
    if dValueCalc != None:
      dValueCalc = round( dValueCalc, 10 )
    if display == True :
      print( f"naam    : {testClass.name}" )
      print( f"function: {str( symTest )}" )
      print( f"Value   : {str( value   )}" )
      print( f"DValue  : {str( dValue  )}" )

    if str( value ).strip() != valueCalc or (dValueCalc != None and dValue != dValueCalc) : # pylint: disable=consider-using-in
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, value: {value} <> {valueCalc}, dValue:{dValue} <> {dValueCalc}' )

  symTest = symexpress3.SymFormulaParser( 'exp( 2 ,10 )' )
  symTest.optimize()
  exp    = SymFuncExp()
  value  = exp.functionToValue( symTest.elements[ 0 ] )
  dValue = exp.getValue(        symTest.elements[ 0 ] )

  _Check( exp, symTest, value, dValue, "(10)^^2", 100 )


  symTest = symexpress3.SymFormulaParser( 'exp( 2 )' )
  symTest.optimize()
  exp    = SymFuncExp()
  value  = exp.functionToValue( symTest.elements[ 0 ] )
  dValue = exp.getValue(        symTest.elements[ 0 ] )

  _Check( exp, symTest, value, dValue, "(e)^^2", 7.3890560989 )

if __name__ == '__main__':
  Test( True )
