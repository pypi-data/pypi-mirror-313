#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Log function for Sym Express 3

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


    https://en.wikipedia.org/wiki/Logarithm

"""

import math
import cmath

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncBase
from symexpress3         import primefactor

class SymFuncLog( symFuncBase.SymFuncBase ):
  """
  Logarithm function, log( x, y ) = y^^answer = x
  Default for y = e
  """
  def __init__( self ):
    super().__init__()
    self._name      = "log"
    self._desc      = "Logarithm function, log( x, y ) = y^^answer = x"
    self._minparams = 1    # minimum number of parameters
    self._maxparams = 2    # maximum number of parameters
    self._syntax    = "log(<x> [,<y>])"
    self._synExplain= "log(<x> [,<y>]) => y^^answer = x, default is e (e^^answer = x)"

  def mathMl( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return [], None

    output = ""

    output += '<msub>'

    base = "<mi>e</mi>"
    if elem.numElements() == 2:
      base = elem.elements[1].mathMl()

    output += "<mi>log</mi>"
    output += base

    output += '</msub>'

    output += "<mfenced separators=''>"
    output += elem.elements[ 0 ].mathMl()
    output += "</mfenced>"


    return ['()'], output


  def functionToValue( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return None

    # answer = log(<x> [,<y>])
    elem1 = elem.elements[ 0 ]

    if elem1.onlyOneRoot != 1:
      return None

    # print( f"check 1: {elem1} {type(elem1)}" )

    # if there is a power the get it out
    if ( elem1.powerCounter     > 1 or
         elem1.powerDenominator > 1 or
         elem1.powerSign       != 1   ) :

      elemNew    = symexpress3.SymExpress( '*' )
      elemNew.powerSign        = elem.powerSign
      elemNew.powerCounter     = elem.powerCounter
      elemNew.powerDenominator = elem.powerDenominator

      elemNumber = symexpress3.SymNumber( elem1.powerSign, elem1.powerCounter, elem1.powerDenominator )

      elemLog    = elem.copy()
      elemLog.powerSign        = 1
      elemLog.powerCounter     = 1
      elemLog.powerDenominator = 1

      elemLog1 = elemLog.elements[ 0 ]
      elemLog1.powerSign        = 1
      elemLog1.powerCounter     = 1
      elemLog1.powerDenominator = 1

      elemNew.add( elemNumber )
      elemNew.add( elemLog    )

      # print( f"elemNew: {elemNew}" )

      return elemNew

    # this power, the first element always power 1

    if isinstance ( elem1, symexpress3.SymNumber ):

      # log( x / y ) = log( x ) - log(y)
      if elem1.factDenominator > 1 :
        elemNew    = symexpress3.SymExpress( '+' )
        elemNew.powerSign        = elem.powerSign
        elemNew.powerCounter     = elem.powerCounter
        elemNew.powerDenominator = elem.powerDenominator

        elemLog1 = elem.copy()
        elemLog1.powerSign        = 1
        elemLog1.powerCounter     = 1
        elemLog1.powerDenominator = 1

        elemLog2 = elemLog1.copy()

        elemLog1.elements[ 0 ].factDenominator = 1

        elemLog2.elements[ 0 ].factCounter     = elemLog2.elements[ 0 ].factDenominator
        elemLog2.elements[ 0 ].factDenominator =  1
        elemLog2.elements[ 0 ].factSign        =  1
        elemLog2.elements[ 0 ].powerSign       =  1

        elemNew.add( elemLog1 )

        elemNum = symexpress3.SymNumber( -1, 1, 1 )
        elem2   = symexpress3.SymExpress( '*' )
        elem2.add( elemNum )
        elem2.add( elemLog2 )

        elemNew.add( elem2 )

        return elemNew

      # log( 1 ) = 0
      if ( elem1.factCounter     == 1 and
           elem1.factDenominator == 1 and
           elem1.factSign        == 1     ) :

        elemNumber = symexpress3.SymNumber( 1, 0, 1 )

        return elemNumber

      # log( 2, 2 ) = 1
      if elem.numElements() > 1:
        if elem1.isEqual( elem.elements[1] ):
          return symexpress3.SymNumber( 1, 1, 1 )

      # log( -100 ) = log(100) + i * pi
      if elem1.factSign == -1:
        elemNew    = symexpress3.SymExpress( '+' )
        elemNew.powerSign        = elem.powerSign
        elemNew.powerCounter     = elem.powerCounter
        elemNew.powerDenominator = elem.powerDenominator

        elemLog = elem.copy()
        elemLog.powerSign        = 1
        elemLog.powerCounter     = 1
        elemLog.powerDenominator = 1

        elemLog.elements[ 0 ].factSign = 1

        elemNew.add( elemLog )

        elemIPi = symexpress3.SymExpress( '*' )
        elemIPi.add( symexpress3.SymVariable( 'i' ))
        elemIPi.add( symexpress3.SymVariable( 'pi' ))

        elemNew.add( elemIPi )

        return elemNew


      # split number in prime numbers to get the highest power
      if elem1.factDenominator == 1 and elem1.factSign == 1 and elem1.factCounter > 3:
        dictFactors = primefactor.FactorizationDict( elem1.factCounter )

        # TODO log - for the moment only 1 number, not splitting into prime numbers
        # log( 156279375 ) = 6 log(3) + 4 log(5) + 3 log(7)
        if len( dictFactors ) == 1:
          highestPower = None
          for iNumber, iPower in dictFactors.items():
            if highestPower == None:
              highestPower = iPower
            elif highestPower > iPower:
              highestPower = iPower

          if highestPower != None and highestPower > 1:
            elemNew    = symexpress3.SymExpress( '*' )
            elemNew.powerSign        = elem.powerSign
            elemNew.powerCounter     = elem.powerCounter
            elemNew.powerDenominator = elem.powerDenominator

            elemNew.add( symexpress3.SymNumber( 1, highestPower, 1 ) )

            elemLog = elem.copy()
            elemLog.powerSign        = 1
            elemLog.powerCounter     = 1
            elemLog.powerDenominator = 1

            elemParam1 = symexpress3.SymExpress( '*' )

            if elem1.factSign == -1:
              elemParam1.add( symexpress3.SymNumber( -1, 1, 1 ) )

            for iNumber, iPower in dictFactors.items():
              elemParam1.add( symexpress3.SymNumber( 1, iNumber, 1, 1, max( iPower - highestPower, 1), 1, 1 ) )

            elemLog.elements[ 0 ] = elemParam1
            elemNew.add( elemLog )

            return elemNew

    # log( exp( 2 )) = log( e^^2 ) = 2 log( e )
    if (     isinstance ( elem1, symexpress3.SymFunction )
         and elem1.name          == "exp"
         and elem1.numElements() >= 1
         and elem1.numElements() <= 2
       ):
      if elem1.power == 1:
        elemNew    = symexpress3.SymExpress( '*' )
        elemNew.powerSign        = elem.powerSign
        elemNew.powerCounter     = elem.powerCounter
        elemNew.powerDenominator = elem.powerDenominator

        elemNew.add( elem1.elements[ 0 ] )

        elemLog = symexpress3.SymFunction( 'log' )

        elemFunc = symexpress3.SymFunction( "exp" )
        elemFunc.add( symexpress3.SymNumber( 1,1,1 ))
        if elem1.numElements() >= 2:
          elemFunc.add( elem1.elements[ 1 ])

        elemLog.add( elemFunc )
        if elem.numElements() == 2:
          elemLog.add( elem.elements[ 1 ])

        elemNew.add( elemLog )

        return elemNew


    # log( a, a ) = 1
    if isinstance ( elem1, symexpress3.SymVariable ):
      if elem.numElements() == 1:
        if elem1.name == "e":
          return symexpress3.SymNumber( 1, 1, 1 )
      else:
        if elem1.isEqual( elem.elements[1] ):
          return symexpress3.SymNumber( 1, 1, 1 )


    # log( x * y ) = log(x) + log(y)
    if isinstance ( elem1, symexpress3.SymExpress ) and elem1.symType == '*' :
      elemNew    = symexpress3.SymExpress( '+' )
      elemNew.powerSign        = elem.powerSign
      elemNew.powerCounter     = elem.powerCounter
      elemNew.powerDenominator = elem.powerDenominator

      elemBase = None
      if elem.numElements() > 1:
        elemBase = elem.elements[ 1 ]
      for elemsub in elem1.elements:
        elemLog = symexpress3.SymFunction( self.name )
        elemLog.add( elemsub )
        if elemBase != None:
          elemLog.add( elemBase )

        elemNew.add( elemLog )

      return elemNew

    # nothing to optimize
    return None


  def _getValueSingle( self, dValue, dValue2 = math.e ):
    dResult = cmath.log( dValue, dValue2 )
    return dResult


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

    if str( value ).strip() != valueCalc or (dValueCalc != None and dValue != dValueCalc) : # pylint: disable=consider-using-in
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, value: {value} <> {valueCalc}, dValue:{dValue} <> {dValueCalc}' )

  symTest = symexpress3.SymFormulaParser( 'log( a^^2 )' )
  symTest.optimize()
  # symTest.elements[ 0 ].elements[ 0 ] = symTest.elements[ 0 ].elements[ 0 ].elements[ 0 ]
  # symexpress3.SymExpressTree( symTest )
  fncLog = SymFuncLog()
  value  = fncLog.functionToValue( symTest.elements[ 0 ] )
  dValue = None

  _Check( fncLog, symTest, value, dValue, "2 *  log( a )", None )


  symTest = symexpress3.SymFormulaParser( 'log( 1 )' )
  symTest.optimize()
  # symTest.elements[ 0 ].elements[ 0 ] = symTest.elements[ 0 ].elements[ 0 ].elements[ 0 ]
  fncLog = SymFuncLog()
  value  = fncLog.functionToValue( symTest.elements[ 0 ] )
  dValue = fncLog.getValue(        symTest.elements[ 0 ] )

  _Check( fncLog, symTest, value, dValue, "0", 0 )


  symTest = symexpress3.SymFormulaParser( 'log( 2 / 3 )' )
  symTest.optimizeNormal()
  # symTest.elements[ 0 ].elements[ 0 ] = symTest.elements[ 0 ].elements[ 0 ].elements[ 0 ]
  fncLog = SymFuncLog()
  value  = fncLog.functionToValue( symTest.elements[ 0 ] )
  dValue = fncLog.getValue(        symTest.elements[ 0 ] )

  _Check( fncLog, symTest, value, dValue, "log( 2 ) + (-1) *  log( 3 )", -0.4054651081 )


  symTest = symexpress3.SymFormulaParser( 'log( x * y * z * a, 2 )' )
  symTest.optimize()
  # symTest.elements[ 0 ].elements[ 0 ] = symTest.elements[ 0 ].elements[ 0 ].elements[ 0 ]
  fncLog = SymFuncLog()
  value  = fncLog.functionToValue( symTest.elements[ 0 ] )
  dValue = None # fncLog.getValue(        symTest.elements[ 0 ] )

  _Check( fncLog, symTest, value, dValue, "log( x,2 ) +  log( y,2 ) +  log( z,2 ) +  log( a,2 )", None )


  symTest = symexpress3.SymFormulaParser( 'log( e )' )
  symTest.optimize()
  # symTest.elements[ 0 ].elements[ 0 ] = symTest.elements[ 0 ].elements[ 0 ].elements[ 0 ]
  fncLog = SymFuncLog()
  value  = fncLog.functionToValue( symTest.elements[ 0 ] )
  dValue = fncLog.getValue(        symTest.elements[ 0 ] )

  _Check( fncLog, symTest, value, dValue, "1", 1 )


  symTest = symexpress3.SymFormulaParser( 'log( x, x )' )
  symTest.optimize()
  # symTest.elements[ 0 ].elements[ 0 ] = symTest.elements[ 0 ].elements[ 0 ].elements[ 0 ]
  fncLog = SymFuncLog()
  value  = fncLog.functionToValue( symTest.elements[ 0 ] )
  dValue = None # fncLog.getValue(        symTest.elements[ 0 ] )

  _Check( fncLog, symTest, value, dValue, "1", None )


  symTest = symexpress3.SymFormulaParser( 'log( 7, 7 )' )
  symTest.optimize()
  # symTest.elements[ 0 ].elements[ 0 ] = symTest.elements[ 0 ].elements[ 0 ].elements[ 0 ]
  fncLog = SymFuncLog()
  value  = fncLog.functionToValue( symTest.elements[ 0 ] )
  dValue = fncLog.getValue(        symTest.elements[ 0 ] )

  _Check( fncLog, symTest, value, dValue, "1", 1 )


  symTest = symexpress3.SymFormulaParser( 'log( exp( 7, 5 ) )' )
  symTest.optimize()
  # symTest.elements[ 0 ].elements[ 0 ] = symTest.elements[ 0 ].elements[ 0 ].elements[ 0 ]
  fncLog = SymFuncLog()
  value  = fncLog.functionToValue( symTest.elements[ 0 ] )
  dValue = fncLog.getValue(        symTest.elements[ 0 ] )

  _Check( fncLog, symTest, value, dValue, "7 *  log(  exp( 1,5 ) )", 11.266065387 )


  symTest = symexpress3.SymFormulaParser( 'log( 25 )' )
  symTest.optimize()
  # symTest.elements[ 0 ].elements[ 0 ] = symTest.elements[ 0 ].elements[ 0 ].elements[ 0 ]
  fncLog = SymFuncLog()
  value  = fncLog.functionToValue( symTest.elements[ 0 ] )
  dValue = fncLog.getValue(        symTest.elements[ 0 ] )

  _Check( fncLog, symTest, value, dValue, "2 *  log( 5 )", 3.2188758249  )


  symTest = symexpress3.SymFormulaParser( 'log( -100 )' )
  symTest.optimize()
  # symTest.elements[ 0 ].elements[ 0 ] = symTest.elements[ 0 ].elements[ 0 ].elements[ 0 ]
  fncLog = SymFuncLog()
  value  = fncLog.functionToValue( symTest.elements[ 0 ] )
  dValue = None # fncLog.getValue(        symTest.elements[ 0 ] )

  _Check( fncLog, symTest, value, dValue, "log( 100 ) + i * pi", None  )


if __name__ == '__main__':
  Test( True )
