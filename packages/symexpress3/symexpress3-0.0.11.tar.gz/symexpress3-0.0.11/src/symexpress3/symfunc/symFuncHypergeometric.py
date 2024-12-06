#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Hypergeometric function for Sym Express 3

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


    https://en.wikipedia.org/wiki/Generalized_hypergeometric_function

    https://docs.sympy.org/latest/modules/simplify/hyperexpand.html
    https://github.com/sympy/sympy/blob/master/sympy/simplify/hyperexpand.py

    https://mathoverflow.net/questions/424518/does-any-hyper-geometric-function-can-be-analytically-continuated-to-the-whole-c
    https://dlmf.nist.gov/15.2
    https://encyclopediaofmath.org/wiki/Hypergeometric_function
    https://fa.ewi.tudelft.nl/~koekoek/documents/wi4006/hyper.pdf

    analytic continuation of 2F1
    https://www.sciencedirect.com/science/article/pii/S0377042700002673



    _2F_1(a, b; c; z) = (1-z)^{-a} {}_2F_1(c-a, b; c; 1-z).

    Kummer's transformation

"""

from symexpress3         import symexpress3
from symexpress3.symfunc import symFuncBase
from symexpress3         import symtools

class SymFuncHypergeometric( symFuncBase.SymFuncBase ):
  """
  Hypergeometric function, hypergeometric( p, q, a1,..,ap, b1,..,bq, z )
  """
  def __init__( self ):
    super().__init__()
    self._name        = "hypergeometric"
    self._desc        = "Hypergeometric function"
    self._minparams   = 3      # minimum number of parameters
    self._maxparams   = 100    # maximum number of parameters
    self._syntax      = "hypergeometric( p, q, a1,..,ap, b1,..,bq, z )"
    self._synExplain  = "hypergeometric( p, q, a1,..,ap, b1,..,bq, z ) Example: hypergeometric( 2, 1, a1, a2, b1, z )"

  def mathMl( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return None, None

    elemP   = elem.elements[ 0 ]
    elemQ   = elem.elements[ 1 ]

    elemTot = len( elem.elements )
    elemZ   = elem.elements[ elemTot - 1 ]

    if not isinstance( elemP, symexpress3.SymNumber ):
      dVars = elemP.getVariables()
      if len( dVars ) != 0:
        return None, None
    else:
      if elemP.power != 1:
        return None, None
      if elemP.factDenominator != 1:
        return None, None

    if not isinstance( elemQ, symexpress3.SymNumber):
      dVars = elemQ.getVariables()
      if len( dVars ) != 0:
        return None, None
    else:
      if elemQ.power != 1:
        return None, None
      if elemQ.factDenominator != 1:
        return None, None

    try:
      valP = elemP.getValue()
      valQ = elemQ.getValue()
    except: # pylint: disable=bare-except
      return None, None

    if not isinstance(valP, int):
      return None, None
    if not isinstance(valQ, int):
      return None, None

    if valP + valQ + 3 != elemTot:
      return None, None


    output = ""

    # https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mmultiscripts
    output += '<mmultiscripts>'
    output += '<mi>F</mi>'                           # <!-- base expression -->
    output += '<mi>' + elemQ.mathMl() + '</mi>'      # <!-- post-sub-script -->
    output += '<mrow></mrow>'                        # <!-- post-sup-script -->
    output += '<mprescripts />'                      #
    output += '<mi>' + elemP.mathMl() + '</mi>'      # <!-- pre-sub-script -->
    output += '<mrow></mrow>'                        # <!-- pre-sup-script -->
    output += '</mmultiscripts>'

    output += "<mfenced separators=''>"

    # print( f"valP {valP}" )
    # print( f"valQ {valQ}" )
    # print( f"elemTot {elemTot}" )

    output += elem.mathMlParameters( False, 2, valP + 1 )

    output += '<mspace width="4px"></mspace>'
    output += '<mi>;</mi>'
    output += '<mspace width="8px"></mspace>'

    output += elem.mathMlParameters( False, valP + 2, elemTot - 2 )

    output += '<mspace width="4px"></mspace>'
    output += '<mi>;</mi>'
    output += '<mspace width="8px"></mspace>'

    output += elemZ.mathMl()

    output += "</mfenced>"

    return [ '()' ], output


  def functionToValue( self, elem ):
    if self._checkCorrectFunction( elem ) != True:
      return None

    elemP   = elem.elements[ 0 ]
    elemQ   = elem.elements[ 1 ]

    elemTot = len( elem.elements )
    elemZ   = elem.elements[ elemTot - 1 ]

    #
    # TODO The below transformation is only valid if abs( elemZ ) < 1
    #

    if not isinstance( elemP, symexpress3.SymNumber ):
      dVars = elemP.getVariables()
      if len( dVars ) != 0:
        return None
    else:
      if elemP.power != 1:
        return None
      if elemP.factDenominator != 1:
        return None

    if not isinstance( elemQ, symexpress3.SymNumber):
      dVars = elemQ.getVariables()
      if len( dVars ) != 0:
        return None
    else:
      if elemQ.power != 1:
        return None
      if elemQ.factDenominator != 1:
        return None

    try:
      valP = elemP.getValue()
      valQ = elemQ.getValue()
    except: # pylint: disable=bare-except
      return None

    if not isinstance(valP, int):
      return None
    if not isinstance(valQ, int):
      return None

    if valP + valQ + 3 != elemTot:
      return None

    elemPQ  = symexpress3.SymExpress( '*' )
    varName = symtools.VariableGenerateGet()
    symVarN = symexpress3.SymVariable( varName )

    for iCntVal in range( 2, valP + 2):
      elemA    = elem.elements[ iCntVal ]
      elemFunc = symexpress3.SymFunction( "risingfactorial" )
      elemFunc.add( elemA   )
      elemFunc.add( symVarN )

      elemPQ.add( elemFunc )

    for iCntVal in range( valP + 2, valP + valQ + 2):
      elemB    = elem.elements[ iCntVal ]
      elemFunc = symexpress3.SymFunction( "risingfactorial", -1, 1, 1 )
      elemFunc.add( elemB   )
      elemFunc.add( symVarN )

      elemPQ.add( elemFunc )

    elemZExp = symexpress3.SymFunction( "exp" )
    elemZExp.add( symVarN )
    elemZExp.add( elemZ   ) # z^^n

    elemNFact = symexpress3.SymFunction( 'factorial', -1, 1, 1 )
    elemNFact.add( symVarN )

    elemParam = symexpress3.SymExpress( '*' )
    elemParam.add( elemPQ    )
    elemParam.add( elemZExp  )
    elemParam.add( elemNFact )

    elemProduct = symexpress3.SymFunction( 'sum' )
    elemProduct.add( symVarN )
    elemProduct.add( symexpress3.SymNumber( 1, 0, 1, 1, 1, 1, 1 ) )
    elemProduct.add( symexpress3.SymVariable( 'infinity' ))
    elemProduct.add( elemParam )

    elemProduct.powerSign        = elem.powerSign
    elemProduct.powerCounter     = elem.powerCounter
    elemProduct.powerDenominator = elem.powerDenominator

    return elemProduct


  def getValue( self, elemFunc, dDict = None ):
    #
    # convert to an optimize function with functionToValue()
    # and use that for calculation the value
    #
    elemNew = self.functionToValue( elemFunc )
    if elemNew == None:
      return None

    dValue = elemNew.getValue( dDict )

    return dValue


#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  def _Check( testClass, symTest, value, dValue, valueCalc, dValueCalc ):
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

  # https://reference.wolfram.com/language/ref/Hypergeometric2F1.html
  # 0.156542+0.150796i
  symTest = symexpress3.SymFormulaParser( 'hypergeometric( 2, 1, 2, 3, 4, 1/2 )' )
  symTest.optimize()
  testClass = SymFuncHypergeometric()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check( testClass, symTest, value, dValue, "sum( n2,0,infinity, risingfactorial( 2,n2 ) *  risingfactorial( 3,n2 ) *  risingfactorial( 4,n2 )^^-1 *  exp( n2,(1/2) ) *  factorial( n2 )^^-1 )", 2.7289327016   )

if __name__ == '__main__':
  Test( True )
