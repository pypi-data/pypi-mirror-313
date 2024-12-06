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

from symexpress3          import symexpress3
from symexpress3.optimize import optimizeBase


class OptimizeRootOfImagNumToCosISin( optimizeBase.OptimizeBase ):
  """
  Root of imaginaire number  to cos + i sin
  """
  def __init__( self ):
    super().__init__()
    self._name         = "rootOfImagNumToCosISin"
    self._symtype      = "all"
    self._desc         = "Root of imaginaire number  to cos + i sin"


  def optimize( self, symExpr, action ):

    def _checkExpressType( symTest ):
      # check type of symTest
      #  0 = mixed
      #  1 = real
      # -1 = imag

      if symTest.symType == '+' and symTest.numElements() > 1:
        return 0

      result = 1 # start with all is a number
      for elemTest in symTest.elements :
        # only principal root elements supported
        if elemTest.onlyOneRoot != 1:
          return 0

        if isinstance( elemTest, symexpress3.SymNumber ):
          continue

        if isinstance( elemTest, symexpress3.SymArray ): # array not supported
          result = 0
          break

        if isinstance( elemTest, symexpress3.SymExpress ): # symexpress in symexpress not supported
          # print( "check symepxress afgekeurd" )
          result = 0
          break

        if isinstance( elemTest, symexpress3.SymVariable ):
          if elemTest.name == "pi":
            continue
          if elemTest.name == "e":
            continue
          if elemTest.name == "i":
            if elemTest.power != 1:
              # print( f"check variable afgekeurd: {str(elemTest)}" )
              result = 0
              break
            result = -1
            continue
          # print( f"check variable afgekeurd: {str(elemTest)}" )
          result = 0  # variables not supported
          break

        if isinstance( elemTest, symexpress3.SymFunction ):
          dVars = elemTest.getVariables()
          for dVar in dVars :
            # function with variables not supported, only predefined variables are ok
            if not dVar in ( 'e', 'pi' ):
              result = 0
              break
          if result == 0:
            break
          continue

        # cannot come here, if so then an unknown element type
        # print( f"Onbekend type: {str(elemTest)}" )
        result = 0
        break

      return result

    # print( "Help: " + str( symExpr ) )
    # print( symExpr.onlyOneRoot  )
    # print( symExpr.powerDenominator  )
    result = False

    if symExpr.onlyOneRoot != 1:
      return result

    if symExpr.powerDenominator == 1:
      return result

    # First expands the array(s)
    if symExpr.existArray():
      return result

    symImag = []
    symReal = []

    # print( "Start optimizeRootOfImageNumToCosISin" )

    # wanted (a + b i)^^(1/n)
    if symExpr.symType == '*':
      # search for imag number

      checkType = _checkExpressType( symExpr )
      if checkType == 0:
        return result

      if checkType == 1:
        return result

      elemCopy = symExpr.copy()
      elemCopy.powerCounter      = 1
      elemCopy.powerDenominator  = 1
      elemCopy.powerSign         = 1

      symImag.append( elemCopy )
    else:
      # split it in imag and real part
      for elemplus in symExpr.elements:
        # only principal root elements supported
        if elemplus.onlyOneRoot != 1:
          return result

        # print( f"check element {str(elemplus)}")

        # symarray not supported, expand first
        if isinstance( elemplus, symexpress3.SymArray ):
          return result

        if isinstance( elemplus, symexpress3.SymNumber ):
          symReal.append( elemplus )
          continue

        if isinstance( elemplus, symexpress3.SymFunction ):
          dVars = elemplus.getVariables()
          for dVar in dVars :
            # function with variables not supported, only predefined variables are ok
            if dVar != 'e' or dVar != 'pi':
              return result
          symReal.append( elemplus )
          continue

        if isinstance( elemplus, symexpress3.SymVariable ):
          if elemplus.name in ( 'e', 'pi' ):
            symReal.append( elemplus )
            continue
          if elemplus.name != 'i':
            return result
          if elemplus.power != 1:
            return result

          # append 1 for the i variable
          symImag.append( symexpress3.SymNumber() )
          continue

        if isinstance( elemplus, symexpress3.SymExpress ):
          checkType = _checkExpressType( elemplus )
          # print( f"_checkExpressType: {checkType}")
          if checkType == 0:
            return result

          if checkType == -1:
            if elemplus.power != 1: # write out power of i first
              return result

          if checkType == 1:
            symReal.append( elemplus )
          else:
            symImag.append( elemplus )
          continue

        # cannot come here, if so then unknown object type
        # print( "Unknown type: " + str( elemplus ))
        return result

      # print( "End check elements" )

    # print( "Number imag: " + str( len( symImag )))
    # print( "Number real: " + str( len( symReal )))

    if len( symReal ) == 0:
      symReal.append( symexpress3.SymNumber( 1, 0 )) # append 0

    # remove the i variable
    dDict = {}
    dDict[ 'i' ] = "1"
    for iCnt, elem in enumerate( symImag ):
      if isinstance( elem, symexpress3.SymVariable ): # change i into 1
        symImag[ iCnt ] = symexpress3.SymNumber()
      elif isinstance( elem, symexpress3.SymFunction ):
        elemNew = elem.copy()
        elemNew.replaceVariable( dDict )
        symImag[ iCnt ] = elemNew
      elif isinstance( elem, symexpress3.SymExpress ):
        elemNew = elem.copy()
        elemNew.replaceVariable( dDict )
        symImag[ iCnt ] = elemNew


    # on this point
    # 2 arrays
    # - symReal = real parts
    # - symImag = imag parts

    symRealExpress = symexpress3.SymExpress( '+' )
    for elem in symReal:
      symRealExpress.add( elem )

    # if not imag part but the real part is negative then it is a imag number also
    if len( symImag ) == 0:
      try:
        calcReal = symRealExpress.getValue()
      except: # pylint: disable=bare-except
        return False

      if isinstance( calcReal, list ):
        return False

      if isinstance( calcReal, complex ):
        return False

      if calcReal >= 0:
        return False

    symImagExpress = symexpress3.SymExpress( '+' )
    for elem in symImag:
      symImagExpress.add( elem )

    # print( f"Real: {str(symRealExpress)}" )
    # print( f"Imag: {str(symImagExpress)}" )


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
    real = "( " + str( symRealExpress  ) + " )"
    img  = "( " + str( symImagExpress  ) + " )"
    x    = "atan2( " + img + " , " + real + " )"
    n    = str( symExpr.powerDenominator )
    r    = "abs((" + real + "^^2 + " + img + "^^2" + ")^^(1/2))"

    # print( "real: {}".format( real ))
    # print( "img : {}".format( img  ))
    # print( "x   : {}".format( x    ))
    # print( "n   : {}".format( n    ))
    # print( "r   : {}".format( r    ))

    arrSolutions = []
    for iCnt2 in range( 0, symExpr.powerDenominator ):
      angle   = " ( " + x + " + 2 pi " + str( iCnt2 ) + " ) /" + n
      result  = r + "^^(1/"+ n + ") * ( cos( " + angle + " ) + i sin( " + angle + "))"

      # print( "Result: {}".format( result ))

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
        return False

      # there should be no array but a function can give an array back, so check it
      if isinstance( iCalc, list ):
        return False

      if isinstance( iCalc, symexpress3.SymArray ):
        return False

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

    symExpr.powerDenominator = 1
    symExpr.elements         = []
    symExpr.add( principal )

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
      raise NameError( f'optimize {testClass.name}, unit test error: {str( symTest )}, wanted: {wanted}, value: {str( symOrg )}' )

  result = False
  symTest = symexpress3.SymFormulaParser( '(1+i)^^(1/2)' )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeRootOfImagNumToCosISin()
  result |= testClass.optimize( symTest, "rootOfImagNumToCosISin" )

  _Check( testClass, symOrg, symTest, "abs( ((1)^^2 + (1)^^2)^^(1/2) )^^(1/2) * ( cos( ( atan2( 1,1 ) + 2 * pi * 0) * 2^^-1 ) + i *  sin( ( atan2( 1,1 ) + 2 * pi * 0) * 2^^-1 ))" )


  symTest = symexpress3.SymFormulaParser( '(1 + e + pi * sin( 3/4 ) + i * pi * cos( 3/4 ) )^^(1/3)' )
  symTest.optimize()
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeRootOfImagNumToCosISin()
  testClass.optimize( symTest, "rootOfImagNumToCosISin" )

  _Check( testClass, symOrg, symTest, "abs( ((1 + e + pi *  sin( 3 * 1 * 4^^-1 ))^^2 + (1 * pi *  cos( 3 * 1 * 4^^-1 ))^^2)^^(1/2) )^^(1/3) * ( cos( ( atan2( 1 * pi *  cos( 3 * 1 * 4^^-1 ),(1 + e + pi *  sin( 3 * 1 * 4^^-1 )) ) + 2 * pi * 0) * 3^^-1 ) + i *  sin( ( atan2( 1 * pi *  cos( 3 * 1 * 4^^-1 ),(1 + e + pi *  sin( 3 * 1 * 4^^-1 )) ) + 2 * pi * 0) * 3^^-1 ))" )


if __name__ == '__main__':
  Test( True )
