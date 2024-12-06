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

class OptSymVariableRootIToSinCos( optTypeBase.OptTypeBase ):
  """
  Root i to cos + i sin
  """
  def __init__( self ):
    super().__init__()
    self._name         = "rootIToSinCos"
    self._symtype      = symexpress3.SymVariable
    self._desc         = "Root i to cos + i sin"

  def optimize( self, elem, action ):
    if self.checkType( elem, action ) != True:
      return None

    if elem.name != 'i' :
      return None

    if elem.powerDenominator == 1 :
      return None

    if elem.onlyOneRoot != 1 : # only principal roots
      return None

    # i^^(1/3)
    #

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
    symreal = 0
    symimg  = 1
    real    = "( " + str( symreal ) + " )"
    img     = "( " + str( symimg  ) + " )"
    x       = "atan2( " + img + " , " + real + " )"
    n       = str( elem.powerDenominator )
    # r       = "((" + real + "^^2 + " + img + "^^2" + ")^^(1/2))"

    # print( "real: {}".format( real ))
    # print( "img : {}".format( img  ))
    # print( "x   : {}".format( x    ))
    # print( "n   : {}".format( n    ))
    # print( "r   : {}".format( r    ))

    arrSolutions = []
    for iCnt in range( 0, elem.powerDenominator ):
      angle   = " ( " + x + " + 2 pi " + str( iCnt ) + " ) /" + n
      # result  = r + "^^(1/"+ n + ") * ( cos( " + angle + " ) + i sin( " + angle + "))"
      result  = "( cos( " + angle + " ) + i sin( " + angle + "))"
      expfunc = symexpress3.SymFormulaParser( result )

      arrSolutions.append( expfunc )

    # get the principal
    iMax = None
    iId  = 0
    for iCnt2, elem2 in enumerate( arrSolutions ):

      # print( "Get Value from: {}".format( elem2 ))
      try:
        iCalc = elem2.getValue()
      except: # pylint: disable=bare-except
        return None

      if isinstance( iCalc, list ):
        return None

      if iMax == None:
        iMax = iCalc
        iId  = iCnt2
        if not isinstance( iMax, complex ):
          iMax = complex( iMax, 0 )
      else:
        if not isinstance( iCalc, complex ):
          iCalc = complex( iCalc, 0 )

        if iCalc.real > iMax.real :
          iMax = iCalc
          iId  = iCnt2
        elif ( iCalc.real == iMax.real and iCalc.imag > iMax.imag ):
          iMax = iCalc
          iId  = iCnt2

    principal = arrSolutions[ iId ]

    principal.powerCounter = elem.powerCounter
    principal.powerSign    = elem.powerSign
    principal.onlyOneRoot  = elem.onlyOneRoot

    return principal

#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  symTest   = symexpress3.SymVariable( 'i', 1, 2, 3, 1 )  # i^^(2/3)
  testClass = OptSymVariableRootIToSinCos()
  symNew    = testClass.optimize( symTest, "rootIToSinCos" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "(( cos( ( atan2( 1,0 ) + 2 * pi * 0) * 3^^-1 ) + i *  sin( ( atan2( 1,0 ) + 2 * pi * 0) * 3^^-1 )))^^2":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymVariable optimize {testClass.name}, unit test error: {str( symTest )}, value: {symNew}' )


  symTest   = symexpress3.SymVariable( 'i', -1, 2, 3, 1 ) # i^^(-2/3)
  testClass = OptSymVariableRootIToSinCos()
  symNew    = testClass.optimize( symTest, "rootIToSinCos" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "(( cos( ( atan2( 1,0 ) + 2 * pi * 0) * 3^^-1 ) + i *  sin( ( atan2( 1,0 ) + 2 * pi * 0) * 3^^-1 )))^^-2":
    print( f"Error unit test {testClass.name} function" )
    raise NameError( f'SymVariable optimize {testClass.name}, unit test error: {str( symTest )}, value: {symNew}' )


if __name__ == '__main__':
  Test( True )
