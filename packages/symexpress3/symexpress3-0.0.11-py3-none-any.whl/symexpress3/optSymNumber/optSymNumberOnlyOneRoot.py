#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Sym Express 3

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

import math

from symexpress3 import symexpress3
from symexpress3 import optTypeBase
from symexpress3 import primefactor  as primefac



class OptSymNumberOnlyOneRoot( optTypeBase.OptTypeBase ):
  """
  Lower the power of radicals
  """
  def __init__( self ):
    super().__init__()
    self._name         = "onlyOneRoot"
    self._symtype      = symexpress3.SymNumber
    self._desc         = "Lower the power of radicals"

  def optimize( self, elem, action ):
    if self.checkType( elem, action ) != True:
      return None

    # 4^^(1/4) = 2^^(1/2)
    if elem.powerDenominator == 1:
      return None

    # only principal roots
    if elem.onlyOneRoot != 1:
      return None

    if elem.factCounter == 1 and elem.factDenominator == 1:
      if elem.factSign == 1:
        # (1)^^(x) = 1
        if elem.power != 1:
          newExp = elem.copy()
          newExp.powerCounter     = 1
          newExp.powerDenominator = 1
          newExp.powerSign        = 1

          return newExp

      if elem.factSign == -1 and elem.powerSign == 1 and elem.powerCounter == 1 and elem.powerDenominator == 2:
        # (-1)^^(1/2) => i (1)^^(1/2)

        newExpr = symexpress3.SymExpress( '*' )
        elemcopy = elem.copy()
        elemcopy.factSign = 1
        newExpr.add( elemcopy )
        newExpr.add( symexpress3.SymVariable( 'i' ))

        return newExpr

      return None

    # return None

    # counter
    dPrimeSet = primefac.factorint( elem.factCounter )
    # print( f"Counter: {elem.factCounter} Primeset counter: {dPrimeSet}" )
    dChange   = {}
    for iPrime, iCount in dPrimeSet.items():
      if iCount < elem.powerDenominator:
        divisor = math.gcd( iCount, elem.powerDenominator )
        if divisor <= 1:
          continue
      # print( f"iPrime: {iPrime}, iCount: {iCount}" )
      dChange[ iPrime ] = iCount

    # denominator
    dPrimeSet2 = primefac.factorint( elem.factDenominator )
    dChange2   = {}
    for iPrime, iCount in dPrimeSet2.items():
      if iCount < elem.powerDenominator:
        divisor = math.gcd( iCount, elem.powerDenominator )
        if divisor <= 1:
          continue
      dChange2[ iPrime ] = iCount

      # print( f"dChange: {dChange}" )

    if len( dChange ) == 0 and len( dChange2 ) == 0:
      # special case
      if elem.factCounter == 1 and elem.factDenominator != 1 and elem.powerSign == 1:
        # (1/3)^^(1/3) => 1/3 * 9^^(1/3) =
        newExpr = symexpress3.SymExpress( '*' )
        newExpr.powerSign    = elem.powerSign
        newExpr.powerCounter = elem.powerCounter

        outNum = symexpress3.SymNumber( 1, elem.factCounter, elem.factDenominator, 1, 1, 1 )
        newExpr.add( outNum )

        orgExpr  = symexpress3.SymExpress( '*' )
        orgExpr.powerDenominator = elem.powerDenominator
        elemcopy = elem.copy()
        elemcopy.powerSign        = 1
        elemcopy.powerCounter     = 1
        elemcopy.powerDenominator = 1
        orgExpr.add( elemcopy )

        inNum  = symexpress3.SymNumber( 1, elem.factDenominator, elem.factCounter, 1, elem.powerDenominator, 1 )
        orgExpr.add( inNum )

        newExpr.add( orgExpr )

        return newExpr

      if elem.powerSign == -1:
        # (1/3)^^(-1/2) = (3/1)^^(1/2)
        newExp = elem.copy()
        # swap sign and fact
        newExp.powerSign = 1
        newExp.factCounter, newExp.factDenominator = newExp.factDenominator, newExp.factCounter

        return newExp

      if elem.factSign == -1 and elem.powerSign == 1 and elem.powerCounter == 1 and elem.powerDenominator == 2:
        # (-1)^^(1/2) => i (1)^^(1/2)

        newExpr = symexpress3.SymExpress( '*' )
        elemcopy = elem.copy()
        elemcopy.factSign = 1
        newExpr.add( elemcopy )
        newExpr.add( symexpress3.SymVariable( 'i' ))

        return newExpr


      return None

    newExpr = symexpress3.SymExpress( '*' )
    newExpr.powerSign    = elem.powerSign
    newExpr.powerCounter = elem.powerCounter

    orgExpr  = symexpress3.SymExpress( '*' )
    orgExpr.powerDenominator = elem.powerDenominator
    elemcopy = elem.copy()
    elemcopy.powerSign        = 1
    elemcopy.powerCounter     = 1
    elemcopy.powerDenominator = 1
    orgExpr.add( elemcopy )

    # counter
    for iPrime, iCount in dChange.items():
      if iCount >= elem.powerDenominator:
        divisor = iCount - iCount % elem.powerDenominator
      else:
        divisor = math.gcd( iCount, elem.powerDenominator )

      # print( f"split: iPrime: {iPrime}, iCount: {iCount}, divisor: {divisor}" )

      outNum = symexpress3.SymNumber( 1, iPrime, 1,  1, divisor, elem.powerDenominator, 1 )
      inNum  = symexpress3.SymNumber( 1, iPrime, 1, -1, divisor, 1                    , 1 )

      orgExpr.add( inNum  )
      newExpr.add( outNum )

    # denominator
    for iPrime, iCount in dChange2.items():
      if iCount >= elem.powerDenominator:
        divisor = iCount - iCount % elem.powerDenominator
      else:
        divisor = math.gcd( iCount, elem.powerDenominator )

      outNum = symexpress3.SymNumber( 1, 1, iPrime,  1, divisor, elem.powerDenominator, 1 )
      inNum  = symexpress3.SymNumber( 1, 1, iPrime, -1, divisor, 1                    , 1 )

      orgExpr.add( inNum  )
      newExpr.add( outNum )

    newExpr.add( orgExpr )

    return newExpr


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

  # (-3)^^(1/2)
  symTest   = symexpress3.SymNumber( -1, 3, 1, 1, 1, 2, 1 )
  testClass = OptSymNumberOnlyOneRoot()
  symNew    = testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symTest, symNew, "3^^(1/2) * i" )

  # (1/3)^^(-1/3)
  symTest   = symexpress3.SymNumber( 1, 1, 3, 1, -1, 3, 1 )
  testClass = OptSymNumberOnlyOneRoot()
  symNew    = testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symTest, symNew, "3^^(1/3)" )


  # (1/3)^^(1/3)
  symTest   = symexpress3.SymNumber( 1, 1, 3, 1, 1, 3, 1 )
  testClass = OptSymNumberOnlyOneRoot()
  symNew    = testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symTest, symNew, "(1/3) * ((1/3) * 3^^3)^^(1/3)" )


  # 14348907^^(1/6)
  symTest   = symexpress3.SymNumber( 1, 14348907, 1, 1, 1, 6, 1 )
  testClass = OptSymNumberOnlyOneRoot()
  symNew    = testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symTest, symNew, "3^^(12/6) * (14348907 * 3^^-12)^^(1/6)" )


  # 4^^(1/4)
  symTest   = symexpress3.SymNumber( 1, 4, 1, 1, 1, 4, 1 )
  testClass = OptSymNumberOnlyOneRoot()
  symNew    = testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symTest, symNew, "2^^(2/4) * (4 * 2^^-2)^^(1/4)" )

  # 27^^(1/2)
  symTest   = symexpress3.SymNumber( 1, 27, 1, 1, 1, 2, 1 )
  testClass = OptSymNumberOnlyOneRoot()
  symNew    = testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symTest, symNew, "3 * (27 * 3^^-2)^^(1/2)" )

  # 841^^(1/2)
  symTest   = symexpress3.SymNumber( 1, 841, 1, 1, 1, 2, 1 )
  testClass = OptSymNumberOnlyOneRoot()
  symNew    = testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symTest, symNew, "29 * (841 * 29^^-2)^^(1/2)" )

  # 27^^(1/6)
  symTest   = symexpress3.SymNumber( 1, 27, 1, 1, 1, 6, 1 )
  testClass = OptSymNumberOnlyOneRoot()
  symNew    = testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symTest, symNew, "3^^(3/6) * (27 * 3^^-3)^^(1/6)" )

  # 4^^(1/2)
  symTest   = symexpress3.SymNumber( 1, 4, 1, 1, 1, 2, 1 )
  testClass = OptSymNumberOnlyOneRoot()
  symNew    = testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symTest, symNew, "2 * (4 * 2^^-2)^^(1/2)" )

  # (1/27)^^(1/6)
  symTest   = symexpress3.SymNumber( 1, 1, 27, 1, 1, 6, 1 )
  testClass = OptSymNumberOnlyOneRoot()
  symNew    = testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symTest, symNew, "(1/3)^^(3/6) * ((1/27) * (1/3)^^-3)^^(1/6)" )



if __name__ == '__main__':
  Test( True )
