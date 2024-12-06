#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    unnestingRadicals for Sym Express 3

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

from symexpress3          import symexpress3
from symexpress3.optimize import optimizeBase

class OptimizeUnnestingRadicals( optimizeBase.OptimizeBase ):
  """
  UnnestingRadicals
  /nhttps://en.wikipedia.org/wiki/Nested_radical
  """
  def __init__( self ):
    super().__init__()
    self._name         = "unnestingRadicals"
    self._symtype      = "+"
    self._desc         = "UnnestingRadicals"

  def optimize( self, symExpr, action ):
    result = False

    if self.checkExpression( symExpr, action ) != True:
      # print( "Afgekeurd: " + symExpr.symType )
      return result

    def _nextSquare():
      #
      # https://en.wikipedia.org/wiki/Nested_radical
      # https://math.stackexchange.com/questions/196155/strategies-to-denest-nested-radicals-sqrtab-sqrtc
      #
      # if ( symExpr.numElements() > 1 and symExpr.symType != '+' ):
      if symExpr.symType != '+':
        return False

      if symExpr.onlyOneRoot != 1:
        return False

      # only denest sqrt roots
      # ( a + b * c^^(1/2) )^^(1/2)
      if symExpr.powerCounter != 1:
        return False
      # if symExpr.powerDenominator != 2:
      if symExpr.powerDenominator % 2 != 0:
        return False
      if symExpr.numElements() != 2:
        return False

      #
      # ( a + b * c^^(1/2) )^^(1/2) =
      # b > 0 ( ( a + (a^2 - b^2 * c)^^(1/2) ) / 2 )^^(1/2)  + ( ( a - (a^2 - b^2 * c)^^(1/2) ) / 2 )^^(1/2)
      # b < 0 ( ( a + (a^2 - b^2 * c)^^(1/2) ) / 2 )^^(1/2)  - ( ( a - (a^2 - b^2 * c)^^(1/2) ) / 2 )^^(1/2)
      #
      # ( ( a + (a^2 - b^2 * c)^^(1/2) ) / 2 )^^(1/2)  + sign( b ) * ( ( a - (a^2 - b^2 * c)^^(1/2) ) / 2 )^^(1/2)
      #

      #
      # need 1 number with power 1/-1
      # need 1 expression or number with power 1/2
      #        by expression = 1 number power 1/-1 and 1 number power 1/2
      #
      elem1 = symExpr.elements[ 0 ]
      elem2 = symExpr.elements[ 1 ]

      elemA = None
      elemB = None

      if isinstance( elem1, symexpress3.SymNumber ):
        if (elem1.power == 1 or elem1.power == -1): # pylint: disable=consider-using-in
          elemA = elem1
          elemB = elem2

      if elemA == None:
        if isinstance( elem2, symexpress3.SymNumber ):
          if (elem2.power == 1 or elem2.power == -1): # pylint: disable=consider-using-in
            elemA = elem2
            elemB = elem1

      if elemA == None:
        return False

      if isinstance( elemB, symexpress3.SymNumber) :
        if elemB.powerCounter != 1:
          return False
        if elemB.powerDenominator != 2:
          return False
        if elemB.onlyOneRoot != 1:
          return False
        # ok, found elemB^^(1/2)
        elemB1 = symexpress3.SymNumber( 1, 1, 1,  1, 1, 1,  1 )
        elemB2 = elemB
      else:
        if not isinstance( elemB, symexpress3.SymExpress):
          return False
        if elemB.symType != '*':
          return False
        if elemB.numElements() != 2:
          return False
        if elemB.power != 1:
          return False
        # this place 2 elements  e1 and e2
        elemB1 = elemB.elements[ 0 ]
        elemB2 = elemB.elements[ 1 ]

        if not isinstance( elemB1, symexpress3.SymNumber ):
          return False
        if not isinstance( elemB1, symexpress3.SymNumber ):
          return False

        if (elemB1.power != 1 and elemB1.power != -1): # pylint: disable=consider-using-in
          elemB1 = elemB.elements[ 1 ]
          elemB2 = elemB.elements[ 0 ]

        if (elemB1.power != 1 and elemB1.power != -1): # pylint: disable=consider-using-in
          return False

        if elemB2.powerCounter != 1:
          return False

        if elemB2.powerDenominator != 2:
          return False

      # elemA  = a
      # elemB1 = b
      # elemB2 = c

      elemA  = elemA.copy()
      elemB1 = elemB1.copy()
      elemB2 = elemB2.copy()

      elemB2.powerCounter     = 1
      elemB2.powerDenominator = 1

      # print( "Unnesting: " + str( symExpr ))
      # print( "A : " + str( elemA ))
      # print( "B : " + str( elemB1 ))
      # print( "C : " + str( elemB2 ))

      # (a^2 - b^2 * c)^^(1/2)
      formulaRoot = "(a^^2 - b^^2 * c)^^(1/2)"
      dVars = {}
      dVars[ 'a' ] = str( elemA  )
      dVars[ 'b' ] = str( elemB1 )
      dVars[ 'c' ] = str( elemB2 )

      oFormulaRoot = symexpress3.SymFormulaParser( formulaRoot )

      # print( "power form: " + str( oFormulaRoot ) )

      oFormulaRoot.replaceVariable( dVars )

      # print( "power form: " + str( oFormulaRoot ) )

      oFormulaRoot.optimizeNormal()
      oFormulaRoot.optimize( "power" )
      oFormulaRoot.optimizeNormal()

      # print( f"dVars: {dVars}" )
      # print( "power form: " + str( oFormulaRoot ) )
      # print( "oFormulaRoot.powerCounter     " + str( oFormulaRoot.powerCounter ) )
      # print( "oFormulaRoot.powerDenominator " + str( oFormulaRoot.powerDenominator ) )
      # print( f"Num elements {oFormulaRoot.numElements()}" )
      # print( f"Type {oFormulaRoot.symType}" )

      if oFormulaRoot.powerCounter != 1:
        return False
      if oFormulaRoot.powerDenominator != 1:
        return False
      if oFormulaRoot.numElements() != 1:
        return False

      elemRoot = oFormulaRoot.elements[ 0 ]
      if not isinstance( elemRoot, symexpress3.SymNumber):
        return False

      if elemRoot.powerCounter != 1:
        return False
      if elemRoot.powerDenominator != 1:
        return False

      # Ok, can be denested

      sign = " 1 "
      if elemB1.factor < 0:
        sign = " -1 "

      # ( ( a + (a^2 - b^2 * c)^^(1/2) ) / 2 )^^(1/2)  + sign( b ) * ( ( a - (a^2 - b^2 * c)^^(1/2) ) / 2 )^^(1/2)
      formulaRoot = "( ( a + (a^^2 - b^^2 * c)^^(1/2) ) / 2 )^^(1/2)  + " + sign + " * ( ( a - (a^^2 - b^^2 * c)^^(1/2) ) / 2 )^^(1/2)"
      oFormulaRoot = symexpress3.SymFormulaParser( formulaRoot )
      oFormulaRoot.replaceVariable( dVars )

      # print( "Formula: " + str( oFormulaRoot ))

      oFormulaRoot.optimizeNormal()

      symExpr.powerCounter     = oFormulaRoot.powerCounter
      symExpr.powerDenominator = oFormulaRoot.powerDenominator * (symExpr.powerDenominator // 2)
      symExpr.powerSign        = symExpr.powerSign * oFormulaRoot.powerSign

      symExpr.elements = oFormulaRoot.elements

      return True

    def _reprocipals():
      if ( symExpr.numElements() > 1 and symExpr.symType != '+' ):
        return False

      # if ( symExpr.onlyOneRoot != 1 ):
      #   return False

      # only reprocipals
      # ( a + b * c^^(1/2) )^^(-1/x)
      if symExpr.powerCounter != 1:
        return False
      # if ( symExpr.powerDenominator <= 1 ):
      #   return False
      if symExpr.powerSign != -1:
        return False
      if symExpr.numElements() != 2:
        return False

      elem1 = symExpr.elements[ 0 ]
      elem2 = symExpr.elements[ 1 ]

      squareFound = 0
      if isinstance( elem1, symexpress3.SymNumber) :
        if elem1.powerCounter != 1:
          return False
        if elem1.powerDenominator > 2:
          return False
        if elem1.powerDenominator == 2:
          squareFound += 1

      elif isinstance( elem1, symexpress3.SymExpress ):
        if elem1.symType != '*':
          return False

        # for iCnt in range( 0, len( elem1.elements )):
        for elem1a in elem1.elements:
          # elem1a = elem1.elements[ iCnt ]
          if not isinstance( elem1a, symexpress3.SymNumber ):
            return False
          if elem1a.powerDenominator > 2:
            return False
          if elem1a.powerDenominator == 2:
            squareFound += 1
      else:
        return False


      if isinstance( elem2, symexpress3.SymNumber) :
        if elem2.powerCounter != 1:
          return False
        if elem2.powerDenominator > 2:
          return False
        if elem2.powerDenominator == 2:
          squareFound += 1

      elif isinstance( elem2, symexpress3.SymExpress ):
        if elem2.symType != '*':
          return False

        # for iCnt in range( 0, len( elem2.elements )):
        for elem2a in elem2.elements:
          # elem2a = elem2.elements[ iCnt ]
          if not isinstance( elem2a, symexpress3.SymNumber ):
            return False
          if elem2a.powerDenominator > 2:
            return False
          if elem2a.powerDenominator == 2:
            squareFound += 1
      else:
        return False

      if squareFound <= 0:
        return False

      # have: ( elem1 + elem2 )^^(-1/x)
      # elem1 are both number and at least one is a square
      #
      # multiple with: ( elem1 - elem2 ) / ( elem1 - elem2 )
      # so the ^^(-1/x)  become( ^^(1/x)
      #

      str1     = str( elem1 )
      str2     = "( -1 * ( " + str( elem2 ) + "))"
      # TO DO: it is going wrong with principal roots and imaginair numbers i^2=-1

      strMulti = "(" + str1 + " + " + str2 + ")"

      oCopy = symExpr.copy()
      oCopy.powerCounter     =  1
      oCopy.powerDenominator =  1
      oCopy.powerSign        =  1

      strNew =  "( (" + str( oCopy ) + ') * ' + strMulti + " / " + strMulti + ")^^-1"

      oNew = symexpress3.SymFormulaParser( strNew )

      if oNew.power != 1:
        return False

      symExpr.powerSign = 1
      symExpr.symType   = oNew.symType
      symExpr.elements  = oNew.elements

      return True

    # try square first
    result |= _nextSquare()
    if result != False:
      return result

    # try reciprocals
    # 1/a * a = 1
    result |= _reprocipals()
    if result != False:
      return result

    return result


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
      raise NameError( f'optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symOrg )}, wanted: {wanted}' )

  symTest = symexpress3.SymFormulaParser( '((15/32768) + 5^^(1/2) * (-3/32768))^^(1/2)' )
  symTest.optimize()
  symTest.optimize( "multiply" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  # symexpress3.SymExpressTree( symTest )
  symOrg = symTest.copy()

  testClass = OptimizeUnnestingRadicals()
  testClass.optimize( symTest, "unnestingRadicals" )

  # print( str( symTest ))
  _Check( testClass, symOrg, symTest, "((15/32768) + 5^^(1/2) * (-3/32768))^^(1/2)" )


  # return

  symTest = symexpress3.SymFormulaParser( '(61 - 24 * 5^^(1/2))^^(1/2)' )
  symTest.optimize()
  symTest.optimize( "multiply" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  # symexpress3.SymExpressTree( symTest )
  symOrg = symTest.copy()

  testClass = OptimizeUnnestingRadicals()
  testClass.optimize( symTest, "unnestingRadicals" )

  _Check( testClass, symOrg, symTest, "3 * 5^^(1/2) + (-4)" )


  symTest = symexpress3.SymFormulaParser( '( 3 + 3 * 5^^(1/2) )^^(-1/5)' )
  symTest.optimize()
  symTest.optimize( "multiply" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  # symexpress3.SymExpressTree( symTest )
  symOrg = symTest.copy()

  testClass = OptimizeUnnestingRadicals()
  testClass.optimize( symTest, "unnestingRadicals" )

  _Check( testClass, symOrg, symTest, "(((3 + 3 * 5^^(1/2)) * (3 + (-1) * 3 * 5^^(1/2)) * (3 + (-1) * 3 * 5^^(1/2))^^-1)^^-1)^^(1/5)" )

if __name__ == '__main__':
  Test( True )
