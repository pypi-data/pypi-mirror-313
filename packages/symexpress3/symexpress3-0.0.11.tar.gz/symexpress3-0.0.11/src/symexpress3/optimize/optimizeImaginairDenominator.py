#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Set imaginair denominator too the counter for Sym Express 3

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

class OptimizeImaginairDenominator( optimizeBase.OptimizeBase ):
  """
  Set imaginair denominator too the counter, format ( 1 / ( a + bi ))
  """
  def __init__( self ):
    super().__init__()
    self._name         = "imaginairDenominator"
    self._symtype      = "+"
    self._desc         = "Set imaginair denominator too the counter, format ( 1 / ( a + bi ))"


  def optimize( self, symExpr, action ):
    result = False

    if self.checkExpression( symExpr, action ) != True:
      return result

    if symExpr.symType != '+' :
      return result

    # if symExpr.power != -1 :
    #  return result

    if symExpr.powerSign != -1:
      return result

    # search for real and imaginair parts
    elemReal = []
    elemImg  = []
    lOk      = True
    # for iCnt in range( 0, len( symExpr.elements )):
    # for iCnt, elem in enumerate( symExpr.elements ):
    for elem in symExpr.elements:
      # elem = symExpr.elements[ iCnt ]
      if isinstance( elem, symexpress3.SymVariable ):
        if elem.name == 'i' :
          if elem.power != 1 :
            lOk = False
            break
          elemImg.append( elem )
        else:
          elemReal.append( elem )

        continue

      if isinstance( elem, symexpress3.SymExpress ):
        if ( elem.symType != '*' and elem.numElements() != 1 ):
          lOk = False
          break

        lImg = False
        # for iCnt2 in range( 0, len( elem.elements )):
        # for iCnt2, elem2 in enumerate( elem.elements ):
        for elem2 in elem.elements:
          # elem2 = elem.elements[ iCnt2 ]
          if isinstance( elem2, symexpress3.SymVariable ):
            if elem2.name == 'i':
              if elem2.power != 1:
                lOk = False
                break
              if lImg == True:
                lOk = False
                break
              lImg = True
            elif isinstance( elem2, symexpress3.SymExpress ):
              # this SymExpress has already be writen out
              lOk = False
              break

        if lImg == True:
          elemImg.append( elem )
        else:
          elemReal.append( elem )
      else:
        # not an SymExpression, then always real
        elemReal.append( elem )

      if lOk == False:
        break


    # print( 'lOk: {}, symExpr: {}'.format( lOk, str( symExpr) ))

    if lOk == False:
      return result
    if len( elemImg ) == 0:
      return result

    # 2 arrays
    # elemReal = real elements
    # elemImg  = imaginair elements
    # ( a + b ) * ( a - b ) = a^2 - ab + ab - b^2 = a^2 - b^2
    symNeg = symexpress3.SymExpress( '+' )
    # for iCnt in range( 0, len ( elemImg )):
    # for iCnt, elem in enumerate( elemImg ):
    for elem in elemImg:
      # elem = elemImg[ iCnt ]
      exprNeg = symexpress3.SymExpress( '*' )
      exprNeg.add( symexpress3.SymNumber( -1, 1, 1, 1, 1,1  ))
      exprNeg.add( elem )
      symNeg.add( exprNeg )

    # for iCnt in range( 0, len ( elemReal )):
    # for iCnt, elem in enumerate( elemReal ):
    for elem in elemReal:
      # elem = elemReal[ iCnt ]
      symNeg.add( elem )

    # current expression = 1 / ( SymPos )
    # new expression = 1/ ( SymNeg ) * ( SymPos ) / ( SymNeg )
    # new expression = 1/ ( SymNeg ) * ( SymPos ) * ( SymNeg )^(-1)

    exprReal = symexpress3.SymExpress( '+' )
    exprImg  = symexpress3.SymExpress( '+' )

    exprReal.powerCounter = 2
    exprImg.powerCounter  = 2

    # for iCnt in range( 0, len ( elemReal )):
    # for iCnt, elem in enumerate( elemReal ):
    for elem in elemReal:
      # elem = elemReal[ iCnt ]
      exprReal.add( elem )

    # for iCnt in range( 0, len ( elemImg )):
    # for iCnt, elem in enumerate( elemImg ):
    for elem in elemImg:
      # elem = elemImg[ iCnt ]
      exprImg.add( elem )

    exprImgNeg = symexpress3.SymExpress( '*' )
    exprImgNeg.add( symexpress3.SymNumber( -1, 1, 1, 1, 1,1 ))
    exprImgNeg.add( exprImg )

    exprPlus = symexpress3.SymExpress( '+' )
    exprPlus.add( exprReal   )
    exprPlus.add( exprImgNeg )
    exprPlus.powerSign = -1


    # symExpr.powerCounter     = 1
    # symExpr.powerDenominator = 1
    symExpr.powerSign        = 1
    symExpr.elements         = []
    symExpr.symType          = '*'

    symExpr.add( symNeg   )
    symExpr.add( exprPlus )

    result = True

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
      raise NameError( f'optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symOrg )}' )

  symTest = symexpress3.SymFormulaParser( '1 / (3 + 4 i)' )
  symTest.optimize()
  symTest.optimize( "multiple" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]

  # symexpress3.SymExpressTree( symTest )

  symOrg = symTest.copy()

  testClass = OptimizeImaginairDenominator()
  testClass.optimize( symTest, "imaginairDenominator" )

  _Check( testClass, symOrg, symTest, "((-1) * 4 * i + 3) * ((3)^^2 + (-1) * (4 * i)^^2)^^-1" )


if __name__ == '__main__':
  Test( True )
