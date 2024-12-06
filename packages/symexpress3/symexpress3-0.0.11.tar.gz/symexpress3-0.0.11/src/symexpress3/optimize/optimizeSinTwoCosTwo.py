#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Optimize sin^2 + cos^2 = 1 for Sym Express 3

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

class OptimizeSinTwoCosTwo( optimizeBase.OptimizeBase ):
  """
  Cos^2 + sin^2 = 1 optimization
  """
  def __init__( self ):
    super().__init__()
    self._name         = "sinTwoCosTwo"
    self._symtype      = "+"
    self._desc         = "sin(x)^2 + cos(x)^2 = 1"


  def optimize( self, symExpr, action ):
    result = False

    if self.checkExpression( symExpr, action ) != True:
      return result

    if symExpr.numElements() <= 1:
      return result

    # first check of sin & cos exist with power of 2 = sin^^2 + cos^^2
    for iCnt, elem in enumerate( symExpr.elements ):
      if iCnt >= len( symExpr.elements ):
        break
      if not isinstance( elem, symexpress3.SymFunction ):
        continue
      if elem.name != 'sin':
        continue
      if elem.power != 2:
        continue

      for iCnt2, elem2 in enumerate( symExpr.elements ):
        if iCnt2 == iCnt:
          continue
        if not isinstance( elem2, symexpress3.SymFunction ):
          continue
        if elem2.name != 'cos':
          continue
        if elem2.power != 2:
          continue
        elemcheck  = elem2.copy()
        elemcheck.name = 'sin'
        if not elem.isEqual( elemcheck ):
          continue

        symExpr.elements[ iCnt ] = symexpress3.SymNumber()  # replace sin with 1 and delete cos
        del symExpr.elements[ iCnt2 ]
        iCnt   = 0
        result = True
        break

    if result == True:
      return result

    # check 2 symexpress with sin & cos = a sin^^2 + a cos^^2
    for iCnt, elem in enumerate( symExpr.elements ):
      if not isinstance( elem, symexpress3.SymExpress ):
        continue
      if elem.power != 1:
        continue
      if elem.symType != '*':
        continue

      elemsin = None
      iCntSin = -1

      for iCntSin, elemcheck in enumerate( elem.elements):
        if not isinstance( elemcheck, symexpress3.SymFunction ):
          continue
        if elemcheck.name != 'sin':
          continue
        if elemcheck.power != 2:
          continue
        # ok, found a sin
        elemsin = elemcheck
        break

      if elemsin == None:
        continue

      # print( 'sin found: {}'.format( str( elemsin )))

      # search for a cos
      for iCnt2, elem2 in enumerate( symExpr.elements ):
        if iCnt2 == iCnt:
          continue
        if not isinstance( elem2, symexpress3.SymExpress ):
          continue
        if elem2.power != 1:
          continue
        if elem2.symType != '*':
          continue

        for iCntCos, elemcheck in enumerate( elem2.elements):
          # print( 'elemcheck cos: {}'.format( str( elemcheck )))
          if not isinstance( elemcheck, symexpress3.SymFunction ):
            continue
          if elemcheck.name != 'cos':
            continue
          if elemcheck.power != 2:
            continue
          # ok, found a cos

          # print( 'cos found: {}'.format( str( elemcheck )))

          # check if this is
          elemequal = elem2.copy()
          elemequal.elements[ iCntCos ].name = 'sin'
          if not elemequal.isEqual( elem ):
            continue

          # ok, found sin^2 + cos^2
          elem.elements[ iCntSin ] = symexpress3.SymNumber()
          del symExpr.elements[ iCnt2 ]
          result = True

          return result # is easier
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

  symTest = symexpress3.SymFormulaParser( 'cos( x )^2 + sin( x )^2' )
  symTest.optimize()
  symOrg = symTest.copy()

  testClass = OptimizeSinTwoCosTwo()
  testClass.optimize( symTest, "sinTwoCosTwo" )

  _Check( testClass, symOrg, symTest, "1" )

if __name__ == '__main__':
  Test( True )
