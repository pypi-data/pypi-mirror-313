#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Product function for Sym Express 3

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


    https://en.wikipedia.org/wiki/Infinite_product
    https://en.wikipedia.org/wiki/Infinite_expression

"""

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncBase

class SymFuncProduct( symFuncBase.SymFuncBase ):
  """
  Product function, product(<variable>,<lower>,<upper>,<function>)
  """
  def __init__( self ):
    super().__init__()
    self._name        = "product"
    self._desc        = "product function, from lower to upper, example: product(n,0,100,exp(x,n))"
    self._minparams   = 4    # minimum number of parameters
    self._maxparams   = 4    # maximum number of parameters
    self._syntax      = "product(<variable>,<lower>,<upper>,<function>)"
    self._synExplain  = "product function, from lower to upper, example: product(n,0,100,exp(x,n))"


  def mathMl( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return [], None

    output = ""

    output += "<munderover>"
    output += '<mn>&#x220F;</mn>'  # this give a product with above and lower the range
    # output += '<mo>&#x220F;</mo>'  # this give a product with next to it the lower the range

    output += '<mrow>'
    output += elem.elements[ 0 ].mathMl()
    output += '<mo>=</mo>'
    output += elem.elements[ 1 ].mathMl()
    output += '</mrow>'

    output += elem.elements[ 2 ].mathMl()

    output += '</munderover>'

    output += "<mfenced separators=''>"
    output += elem.elements[ 3 ].mathMl()
    output += "</mfenced>"

    return [ '()' ], output


  def functionToValue( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return None

    elemVar   = elem.elements[ 0 ]
    elemStart = elem.elements[ 1 ]
    elemEnd   = elem.elements[ 2 ]
    elemFunc  = elem.elements[ 3 ]

    if not isinstance( elemVar, symexpress3.SymVariable ):
      return None
    if elemVar.power != 1:
      return None

    if not isinstance( elemStart, symexpress3.SymNumber ):
      dVars = elemStart.getVariables()
      if len( dVars ) != 0:
        return None
    else:
      if elemStart.power != 1:
        return None
      if elemStart.factDenominator != 1:
        return None

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
      startVal = elemStart.getValue()
      endVal   = elemEnd.getValue()
      varName  = elemVar.name
    except: # pylint: disable=bare-except
      return None

    if not isinstance(startVal, int):
      return None
    if not isinstance(endVal, int):
      return None

    if startVal > endVal:
      return None

    # Arrays (multiple values) are depended
    # So first take the array out of the product and after that expand the product
    # See expandArrays (optimizeExpandArrays.py & optSymAnyExpandArray.py)
    if elem.existArray():
      return None

    elemList = symexpress3.SymExpress( '*' )
    elemList.powerSign        = elem.powerSign
    elemList.powerCounter     = elem.powerCounter
    elemList.powerDenominator = elem.powerDenominator

    for iCntVal in range( startVal, endVal + 1 ):
      if isinstance( elemFunc, symexpress3.SymVariable ):
        if elemFunc.name == varName:
          elemNew = symexpress3.SymNumber( 1, iCntVal, 1, elemFunc.powerSign, elemFunc.powerCounter, elemFunc.powerDenominator, 1 )
        else:
          elemNew = elemFunc
      else:
        dDict = {}
        dDict[ varName ] = str( iCntVal )

        elemNew = elemFunc.copy()
        elemNew.replaceVariable( dDict )

      elemList.add( elemNew )

    # self.elements[ iCnt ] = elemList
    return elemList


  def getValue( self, elemFunc, dDict = None ):
    if self._checkCorrectFunction( elemFunc ) != True:
      return None

    if dDict == None:
      dDictProduct = {}
    else:
      dDictProduct = dDict.copy()

    listStart  = []
    listEnd    = []
    # listExpres = []

    # first must always be a single variable
    elemVar = elemFunc.elements[0]
    while elemVar != None and not isinstance( elemVar, symexpress3.SymVariable):
      elemVar = elemVar.elements[0]

    cVar = elemVar.name

    startVal = elemFunc.elements[1].getValue( dDict )
    if isinstance( startVal, list ):
      listStart = startVal
    else:
      listStart.append( startVal )

    endVal = elemFunc.elements[2].getValue( dDict )
    if isinstance( endVal, list ):
      listEnd = endVal
    else:
      listEnd.append( endVal )

    elemExpress = elemFunc.elements[3]

    result = []
    for startVal in listStart:
      for endVal in listEnd:
        dStart = int( startVal )
        dEnd   = int( endVal   )
        dValue = 1
        for iCnt in range( dStart, dEnd + 1 ):
          dDictProduct[ cVar ] = iCnt
          # if multiple values are given back, only the first will be used
          # see above by functionToValue()
          value = elemExpress.getValue( dDictProduct )
          if isinstance( value, list ):
            dValue *= value[ 0 ]
          else:
            dValue *= value
        result.append( dValue )

    if len( result ) == 1:
      dValue = result[ 0 ]
    else:
      dValue = result

    return dValue


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


  symTest = symexpress3.SymFormulaParser( 'product( n, 1, 4, n^2 )' )
  symTest.optimize()
  testClass = SymFuncProduct()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check( testClass, symTest, value, dValue, "1^^2 * 2^^2 * 3^^2 * 4^^2", 576 )

if __name__ == '__main__':
  Test( True )
