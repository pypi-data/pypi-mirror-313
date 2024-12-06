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

from symexpress3 import symexpress3
from symexpress3 import optTypeBase

class OptSymAnyRootToPrincipalRoot( optTypeBase.OptTypeBase ):
  """
  Put the power of an array into his elements
  """
  def __init__( self ):
    super().__init__()
    self._name         = "rootToPrincipalRoot"
    self._desc         = "Write out all roots into principal roots"

  def optimize( self, elem, action ):
    if self.checkType( elem, action ) != True:
      return None

    # symexpress and symarray use the routine from optimize directory

    if isinstance( elem, symexpress3.SymArray) :
      return None

    if elem.onlyOneRoot == 1 :
      return None

    if elem.powerDenominator == 1:
      elemNew = elem.copy()
      elemNew.onlyOneRoot = 1
      return elemNew

    elemNew = elem.copy()
    elemNew.onlyOneRoot  = 1
    elemNew.powerCounter = 1
    elemNew.powerSign    = 1

    #
    # https://en.wikipedia.org/wiki/Nth_root
    # https://en.wikipedia.org/wiki/De_Moivre%27s_formula
    # https://en.wikipedia.org/wiki/Imaginary_unit
    #
    # https://en.wikipedia.org/wiki/Atan2
    # https://en.wikipedia.org/wiki/Polar_coordinate_system
    #
    # r^(1/n) = ( cos( ( x  + 2 pi k ) /n) + i sin( ( x + 2 pi k ) / n) )
    # r = (real^2 + img^2)^1/2
    # x = atan2( img, real )

    symreal = 1
    symimg  = 0
    real    = "( " + str( symreal ) + " )"
    img     = "( " + str( symimg  ) + " )"
    x       = "atan2( " + img + " , " + real + " )"
    n       = str( elem.powerDenominator )
    # r    = "((" + real + "^^2 + " + img + "^^2" + ")^^(1/2))"

    symNew = symexpress3.SymArray()

    for iCnt in range( 0, elem.powerDenominator ):
      angle   = " ( " + x + " + 2 * pi * " + str( iCnt ) + " ) /" + n
      # result  = r + "^^(1/"+ n + ") * ( cos( " + angle + " ) + i sin( " + angle + "))"
      result  = "( cos( " + angle + " ) + i sin( " + angle + "))"

      # print( "Result: {}".format( result ))

      expfunc = symexpress3.SymFormulaParser( result )

      symFunc = symexpress3.SymExpress( '*' )
      symFunc.powerSign    = elem.powerSign
      symFunc.powerCounter = elem.powerCounter

      symFunc.add( elemNew )
      symFunc.add( expfunc )

      symNew.add( symFunc )

    return symNew

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  symTest = symexpress3.SymFormulaParser( "4^(1/2)" )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  testClass = OptSymAnyRootToPrincipalRoot()
  symNew    = testClass.optimize( symTest, "rootToPrincipalRoot" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "[ 4^^(1/2) * ( cos( ( atan2( 0,1 ) + 2 * pi * 0) * 2^^-1 ) + i *  sin( ( atan2( 0,1 ) + 2 * pi * 0) * 2^^-1 )) | 4^^(1/2) * ( cos( ( atan2( 0,1 ) + 2 * pi * 1) * 2^^-1 ) + i *  sin( ( atan2( 0,1 ) + 2 * pi * 1) * 2^^-1 )) ]":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymAny optimize {testClass.name}, unit test error: {str( symTest )}, value: {symNew}' )


if __name__ == '__main__':
  Test( True )
