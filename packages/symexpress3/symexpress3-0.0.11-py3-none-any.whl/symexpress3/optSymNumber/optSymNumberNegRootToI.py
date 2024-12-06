#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Negative root to i for Sym Express 3

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

from  symexpress3 import symexpress3
from  symexpress3 import optTypeBase

class OptSymNumberNegRootToI( optTypeBase.OptTypeBase ):
  """
  Negative root change to i
  """
  def __init__( self ):
    super().__init__()
    self._name         = "negRootToI"
    self._symtype      = symexpress3.SymNumber
    self._desc         = "Negative root change to i"

  def optimize( self, elem, action ):
    if self.checkType( elem, action ) != True:
      return None

    if elem.powerDenominator == 1:
      return None

    # it must be a negative number
    if elem.factSign != -1:
      return None

    if elem.onlyOneRoot != 1:
      return None

    # print( "negRootToI: " + str( elem ))

    # fast way for square's
    if elem.powerDenominator == 2:
      elemnew = symexpress3.SymExpress( '*' )
      elemnew.onlyOneRoot = elem.onlyOneRoot

      elemVar = symexpress3.SymVariable( 'i' )
      elemNum = elem.copy()
      elemNum.factSign = 1

      elemnew.powerSign    = elemNum.powerSign
      elemnew.powerCounter = elemNum.powerCounter

      elemNum.powerSign    = 1
      elemNum.powerCounter = 1

      elemnew.add( elemVar )
      elemnew.add( elemNum )
      return elemnew

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

    # TO DO "(-1)^^(1/3)" -> r wordt negative 1 getal, geeft probleem bij quadraat -> bij optellen eerst kwadraat dan pas root
    # current solution abs()...


    elemcopy = elem.copy()
    elemcopy.powerCounter     = 1
    elemcopy.powerDenominator = 1
    elemcopy.powerSign        = 1

    symreal = elemcopy
    symimg  = 0
    real    = "( " + str( symreal ) + " )"
    img     = "( " + str( symimg  ) + " )"
    x       = "atan2( " + img + " , " + real + " )"
    n       = str( elem.powerDenominator )
    # r       = "(abs(" + real + "^^2 + " + img + "^^2" + ")^^(1/2))"
    r       = "abs(" + real + ")"

    arrSolutions = []
    for iCnt in range( 0, elem.powerDenominator ):
      angle   = " ( " + x + " + 2 pi " + str( iCnt ) + " ) /" + n
      result  = r + "^^(1/"+ n + ") * ( cos( " + angle + " ) + i sin( " + angle + "))"
      expfunc = symexpress3.SymFormulaParser( result )

      arrSolutions.append( expfunc )

    # get the principal
    iMax = None
    iId  = 0
    for iCnt2, elem2 in enumerate( arrSolutions ):

      # print( "Get Value from: {}".format( elem2 ))

      iCalc = elem2.getValue()
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
  # (-2/3)^^(1/2)
  symTest = symexpress3.SymNumber( -1, 2, 3, 1, 1, 2, 1 )
  testClass = OptSymNumberNegRootToI()
  symNew    = testClass.optimize( symTest, "negRootToI" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

  if str( symNew ).strip() != "i * (2/3)^^(1/2)":
    print( f"Error unit test {testClass.name} number" )
    raise NameError( f'SymNumber optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symNew )}' )

  # (-2/3)^^(5/2)
  symTest = symexpress3.SymNumber( -1, 2, 3, 1, 5, 2, 1 )
  testClass = OptSymNumberNegRootToI()
  symNew    = testClass.optimize( symTest, "negRootToI" )

  if display == True :
    print( f"naam      : {testClass.name}" )
    print( f"orginal   : {str( symTest )}" )
    print( f"optimized : {str( symNew  )}" )

    print( f"Error unit test {testClass.name} number" )
    raise NameError( f'SymNumber optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symNew )}' )


if __name__ == '__main__':
  Test( True )
