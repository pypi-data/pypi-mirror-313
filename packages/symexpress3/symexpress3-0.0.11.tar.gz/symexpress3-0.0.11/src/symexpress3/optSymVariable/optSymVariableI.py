#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Simplify I for Sym Express 3

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

from symexpress3 import symexpress3
from symexpress3 import optTypeBase

class OptSymVariableI( optTypeBase.OptTypeBase ):
  """
  Simplify i
  """
  def __init__( self ):
    super().__init__()
    self._name         = "i"
    self._symtype      = symexpress3.SymVariable
    self._desc         = "Simplify i"

  def optimize( self, elem, action ):
    if self.checkType( elem, action ) != True:
      return None

    if elem.name != 'i' :
      return None

    if elem.powerDenominator != 1 :
      return None

    if elem.powerCounter == 0 :
      # i^0 = 1
      elemnew = symexpress3.SymNumber( 1, 1, 1, 1, 1,1 )
      return elemnew

    if elem.powerCounter == 2 :
      # i^2 = -1
      # 1/-1 = -1
      elemnew = symexpress3.SymNumber( -1, 1, 1, 1, 1,1 )
      return elemnew

    if elem.powerCounter == 3 :
      # i^3 = -i
      elemnew   = symexpress3.SymNumber( -1, 1, 1, 1, 1,1 )
      elemExtra = elem.copy()
      elemExtra.powerCounter = 1
      elemExp = symexpress3.SymExpress( '*' )
      elemExp.add( elemnew    )
      elemExp.add( elemExtra  )
      return elemExp

    if ( elem.powerSign == -1 and elem.powerCounter == 1 and elem.powerDenominator == 1 ):
      # 1/i = i / (i*i) = i / (-1) = - i
      elemnew   = symexpress3.SymNumber( -1, 1, 1, 1, 1,1 )
      elemExtra = elem.copy()
      elemExtra.powerCounter = 1
      elemExtra.powerSign    = 1
      elemExp = symexpress3.SymExpress( '*' )
      elemExp.add( elemnew   )
      elemExp.add( elemExtra )
      return elemExp

    # i^2 = -1
    # i^3 = -i
    # i^4 = i^2 * i^2        = -1 * -1 = 1
    # i^5 = i^2 * i^2 * i    = i
    # i^6 = i^2 * i^2 * i^2  = i^2     = -1
    # power = power modulo 4

    #
    # problem:
    # i^4 = 1
    # (i^4)^(1/3) = 1^(1/3)    = 1
    # i^(4/3)     = (-1)^(2/3) = -0.5 + 0.866025i
    # but it is the same ???
    #
    if ( elem.powerDenominator == 1 ) and (elem.powerCounter >= 4 ):
      elemNew = elem.copy()
      elemNew.powerCounter %= 4

      if elemNew.powerCounter == 0 :
        elemNew = symexpress3.SymNumber( 1, 1, 1, 1, 1,1 )
      elif elemNew.powerCounter == 2 :
        # value is -1
        elemNew = symexpress3.SymNumber( -1, 1, 1, 1, 1,1 )
      elif elemNew.powerCounter == 3 :
        # value is -i
        elemNew   = symexpress3.SymNumber( -1, 1, 1, 1, 1,1 )
        elemExtra = elem.copy()
        elemExtra.powerCounter = 1
        elemExtra.powerSign    = 1
        elemExp = symexpress3.SymExpress( '*' )
        elemExp.add( elemNew   )
        elemExp.add( elemExtra )

        elemNew = elemExp

      # 1/i => 1/i * i/i = i / (i^2) = i / -1 = -i
      # if ( elemNew.name == 'i' and elemNew.powerSign == -1 ):
      #   # power will be 1, sign will be -1
      #   # self.factSign  *= -1
      #   # self.powerSign  = 1
      #   pass
      return elemNew

    return None

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  symTest = symexpress3.SymVariable( 'i', 1, 2, 1, 1 )

  testClass = OptSymVariableI()
  symNew    = testClass.optimize( symTest, "i" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "(-1)":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymVariable optimize {testClass.name}, unit test error: {str( symTest )}, value: {symNew}' )


  symTest = symexpress3.SymVariable( 'i', 1, 3, 1, 1 )

  testClass = OptSymVariableI()
  symNew    = testClass.optimize( symTest, "i" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "(-1) * i":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymVariable optimize {testClass.name}, unit test error: {str( symTest )}, value: {symNew}' )


  symTest = symexpress3.SymVariable( 'i', 1, 4, 1, 1 )

  testClass = OptSymVariableI()
  symNew    = testClass.optimize( symTest, "i" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "1":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymVariable optimize {testClass.name}, unit test error: {str( symTest )}, value: {symNew}' )



  symTest = symexpress3.SymVariable( 'i', 1, 5, 1, 1 )

  testClass = OptSymVariableI()
  symNew    = testClass.optimize( symTest, "i" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "i":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymVariable optimize {testClass.name}, unit test error: {str( symTest )}, value: {symNew}' )


  symTest = symexpress3.SymVariable( 'i', -1, 1, 1, 1 )

  testClass = OptSymVariableI()
  symNew    = testClass.optimize( symTest, "i" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "(-1) * i":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymVariable optimize {testClass.name}, unit test error: {str( symTest )}, value: {symNew}' )


  symTest = symexpress3.SymVariable( 'i', -1, 2, 1, 1 )

  testClass = OptSymVariableI()
  symNew    = testClass.optimize( symTest, "i" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "(-1)":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymVariable optimize {testClass.name}, unit test error: {str( symTest )}, value: {symNew}' )


if __name__ == '__main__':
  Test( True )
