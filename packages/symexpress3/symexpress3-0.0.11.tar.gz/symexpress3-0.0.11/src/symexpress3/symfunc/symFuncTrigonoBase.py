#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
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


    https://en.wikipedia.org/wiki/Sine_and_cosine
    https://en.wikipedia.org/wiki/Trigonometric_functions
    https://en.wikipedia.org/wiki/Inverse_trigonometric_functions

"""

import math
import uuid

from symexpress3         import symexpress3
from symexpress3.symfunc import symTrigonometricData
from symexpress3.symfunc import symFuncBase
from symexpress3         import primefactor


class SymFuncTrigonoBase( symFuncBase.SymFuncBase ):
  """
  Base class for trigonometry functions
  """

  # sin/cos/tan are all in radius, between 0 and 2 pi
  def _optimizeSinCosTan( self, elemFunc ):
    elem = elemFunc.elements[ 0 ]
    if not isinstance( elem, symexpress3.SymExpress ):
      return None

    if elem.numElements() != 2:
      return None

    if elem.symType != '*':
      return None

    elemNum = None
    elemVar = None

    result = elemFunc.copy()
    elem   = result.elements[ 0 ]

    if isinstance( elem.elements[0], symexpress3.SymNumber ):
      elemNum = elem.elements[0]
    elif isinstance( elem.elements[1], symexpress3.SymNumber ):
      elemNum = elem.elements[1]
    if elemNum == None:
      return None

    if isinstance( elem.elements[0], symexpress3.SymVariable):
      elemVar = elem.elements[0]
    elif isinstance( elem.elements[1], symexpress3.SymVariable ):
      elemVar = elem.elements[1]
    if elemVar == None:
      return None

    if elemVar.name != 'pi':
      return None
    if elemVar.power != 1:
      return None

    if elemNum.power != 1:
      return None

    if elemNum.factor < 0:
      imore = elemNum.factDenominator * 2
      icurr = elemNum.factCounter * elemNum.factSign
      while icurr < 0:
        icurr += imore
      elemNum.factSign    = 1
      elemNum.factCounter = icurr
    elif elemNum.factor > 2:
      imore = elemNum.factDenominator * 2
      icurr = elemNum.factCounter * elemNum.factSign
      while icurr >  2 * elemNum.factDenominator:
        icurr -= imore
      elemNum.factSign    = 1
      elemNum.factCounter = icurr
    else:
      result = None

    return result

  # convert sin() and cos()
  def _convertFuncSinCosTan( self, elem ):

    # https://www.rapidtables.com/math/trigonometry/arctan.html

    # print( "_convertFuncSinCosTan: {}".format( str( elem )))

    elem2 = elem.elements[ 0 ]
    elemNum = None
    elemVar = None
    if isinstance ( elem2, symexpress3.SymNumber ):
      if elem2.factCounter == 0:
        elemNum = elem2
      else:
        return None

    if isinstance ( elem2, symexpress3.SymVariable ):
      if elem2.name != 'pi':
        return None
      if elem2.power != 1:
        return None
      # just one (1)
      elemNum = symexpress3.SymNumber()

    if elemNum == None:
      if not isinstance( elem2, symexpress3.SymExpress ):
        return None
      if elem2.symType != '*':
        return None
      if elem2.numElements() != 2:
        return None

      if isinstance( elem2.elements[ 0 ], symexpress3.SymNumber ):
        elemNum = elem2.elements[ 0 ]
      elif isinstance( elem2.elements[ 1 ], symexpress3.SymNumber ):
        elemNum = elem2.elements[ 1 ]
      if elemNum == None:
        return None

      if isinstance( elem2.elements[ 0 ], symexpress3.SymVariable ):
        elemVar = elem2.elements[ 0 ]
      elif isinstance( elem2.elements[ 1 ], symexpress3.SymVariable ):
        elemVar = elem2.elements[ 1 ]
      if elemVar == None:
        return None

      if elemVar.power != 1:
        return None
      if elemVar.name != 'pi':
        return None

    # check for optimize values
    if ( elemNum.power != 1 or elemNum.factor < 0 or elemNum.factor > 2 ):
      return None

    iSign        = elemNum.factSign
    iCounter     = elemNum.factCounter
    iDenominator = elemNum.factDenominator

    funcname = elem.name

    # print( "search trio: {}".format( str( elem )))
    # if (iDenominator == 20):
    #   print( "search trio: {}".format( str( elem )))

    # search direct in table
    elemnew = None
    for tri in symTrigonometricData.trigonometricdata:
      if tri[ 0 ] != funcname:
        continue
      if (  tri[ 1 ] != iSign
         or tri[ 2 ] != iCounter
         or tri[ 3 ] != iDenominator
         ):
        continue

      elemnew = symexpress3.SymFormulaParser( tri[ 4 ] )
      # this radicals can only have one (positive) solution (in the trigonometricdata all the radicals are onlyone)

      # print( "elemnew: " + str(elemnew))

      elemnew.powerSign        = elem.powerSign
      elemnew.powerCounter     = elem.powerCounter
      elemnew.powerDenominator = elem.powerDenominator

      # print( "found trip: {}".format( str(elemnew) ))

      return elemnew

    # converse the sin/cos/tan between 0 and pi/4
    # sin( x ) = cos(  pi/2 - x)
    if elem.name == 'cos':
      funcname      = 'sin'
      iCounter2     = 1
      iDenominator2 = 2

      iDenominator  *= iDenominator2
      iCounter      *= iDenominator2
      iDenominator2 *= elemNum.factDenominator
      iCounter2     *= elemNum.factDenominator

      # between 0 and 2
      iCounter = iCounter2 - iCounter
      while iCounter < 0:
        iCounter += iDenominator * 2

      # lowest form
      iGcd = math.gcd( iCounter, iDenominator )
      if iGcd != 1:
        iCounter     //= iGcd
        iDenominator //= iGcd

      # print( "cos counter:{}, denominator: {}, orginal: {}".format( iCounter, iDenominator , str( elem2)))

    cMultiple = ''
    dFactor   = iCounter / iDenominator


    iCountOrg = iCounter
    iDenomOrg = iDenominator

    # pylint: disable=chained-comparison
    if funcname == 'sin':
      if ( dFactor >= 0 and dFactor <= 0.5 ):
        # iCounter     = iCounter
        # iDenominator = iDenominator
        pass
      elif ( dFactor >= 0.5 and dFactor <= 1 ):
        iCounter     = 1 * iDenominator - iCounter
        # iDenominator = iDenominator
      elif ( dFactor >= 1 and dFactor <= 1.5 ):
        # iCounter     = ( 1 * iDenominator - iCounter ) + 1 * iDenominator
        iCounter     = iCounter - iDenominator
        # iDenominator = iDenominator
        cMultiple    = '-1 * '
      elif ( dFactor >= 1.5 and dFactor <= 2 ):
        iCounter     = 2 * iDenominator - iCounter
        # iDenominator = iDenominator
        cMultiple    = '-1 * '
    elif funcname == 'tan':
      if ( dFactor >= 0 and dFactor <= 0.5 ):
        # iCounter     = iCounter
        # iDenominator = iDenominator
        pass
      elif ( dFactor >= 0.5 and dFactor <= 1 ):
        iCounter     = 1 * iDenominator - iCounter
        # iDenominator = iDenominator
        cMultiple    = '-1 * '
      elif ( dFactor >= 1 and dFactor <= 1.5 ):
        # iCounter     = ( 1 * iDenominator - iCounter ) + 1 * iDenominator
        iCounter     = iCounter - iDenominator
        # iDenominator = iDenominator
      elif ( dFactor >= 1.5 and dFactor <= 2 ):
        iCounter     = 2 * iDenominator - iCounter
        # iDenominator = iDenominator
        cMultiple    = '-1 * '


    # print( "cos counter:{}, denominator: {}, dFactor: {}, orginal: {}".format( iCounter, iDenominator , dFactor, str( elem2)))
    elemnew = None
    for tri in symTrigonometricData.trigonometricdata:
      if tri[ 0 ] != funcname:
        continue
      if (  tri[ 1 ] != iSign
         or tri[ 2 ] != iCounter
         or tri[ 3 ] != iDenominator
         ):
        continue

      elemnew = symexpress3.SymFormulaParser( cMultiple + tri[ 4 ] )
      # this radicals can only have one (positive) solution (in the trigonometricdata all the radicals are onlyone)

      # print( "elemnew: " + str(elemnew))

      elemnew.powerSign        = elem.powerSign
      elemnew.powerCounter     = elem.powerCounter
      elemnew.powerDenominator = elem.powerDenominator

      break
    # print( "elemnew: " + str(elemnew))

    if elemnew == None:
      # try to create the sin/cos formula
      formualSinCos = self._getSinCos( funcname, iCountOrg, iDenomOrg)
      if formualSinCos != None:
        elemnew = symexpress3.SymFormulaParser( formualSinCos )
        elemnew.powerSign        = elem.powerSign
        elemnew.powerCounter     = elem.powerCounter
        elemnew.powerDenominator = elem.powerDenominator

    return elemnew


  #
  # get the sin/cos from the given counter/denominator
  # if not exist try to create one (with only real radicals, no complex)
  #
  def _getSinCos( self, cType, iCounter, iDenominator ):

    # search trigonometricdata to the given base
    def _getBaseFormula( cTp, iCount, iDenom ):
      for tri in symTrigonometricData.trigonometricdata:
        if tri[ 0 ] != cTp:
          continue
        if tri[ 1 ] != 1:  # type
          continue
        if tri[ 2 ] != iCount:
          continue
        if tri[ 3 ] != iDenom:
          continue

        return tri[ 4 ] # symexpress string formula

      return None

    def _createSinCosHalf( iDenom ):
      # sin( x / 2 ) = sign( sin( x/2 ) ) ( (1 - cos(x) ) / 2 )^^(1/2)
      # cos( x / 2 ) = sign( cos( x/2 ) ) ( (1 + cos(x) ) / 2 )^^(1/2)

      baseNum = iDenom // 2

      # it always in  first quarter, no sign needed
      formulaSin = f"( (1 - cos( pi / {baseNum}) ) / 2 )^^(1/2)"
      formulaCos = f"( (1 + cos( pi / {baseNum}) ) / 2 )^^(1/2)"

      oFormulaSin = symexpress3.SymFormulaParser( formulaSin )
      oFormulaCos = symexpress3.SymFormulaParser( formulaCos )

      oFormulaSin.optimizeNormal()
      oFormulaCos.optimizeNormal()

      triRec = []
      triRec.append( "sin" )
      triRec.append( 1 )
      triRec.append( 1 )
      triRec.append( iDenom )
      triRec.append( str( oFormulaSin ) )
      triRec.append( None )

      symTrigonometricData.trigonometricdata.append( triRec )

      # print( f"Add sin: { triRec[ 4 ]}" )

      triRec = []
      triRec.append( "cos" )
      triRec.append( 1 )
      triRec.append( 1 )
      triRec.append( iDenom )
      triRec.append( str( oFormulaCos ) )
      triRec.append( None )

      symTrigonometricData.trigonometricdata.append( triRec )

      # print( f"Add cos: { triRec[ 4 ]}" )

    def _createSinCosDouble( iCount, iDenom ):
      # sin( 2x ) = 2 sin(x) cos(x)
      # cos( 2x ) = 2 cos(x)^^2 - 1

      baseCount = iCount // 2

      formulaSin = f"2 sin( pi {baseCount} / {iDenom}) cos(pi {baseCount} / {iDenom})"
      formulaCos = f"2 cos(pi {baseCount} / {iDenom})^^2 - 1"

      oFormulaSin = symexpress3.SymFormulaParser( formulaSin )
      oFormulaCos = symexpress3.SymFormulaParser( formulaCos )

      oFormulaSin.optimizeNormal()
      oFormulaCos.optimizeNormal()

      triRec = []
      triRec.append( "sin" )
      triRec.append( 1 )
      triRec.append( iCount )
      triRec.append( iDenom )
      triRec.append( str( oFormulaSin ) )
      triRec.append( None )

      symTrigonometricData.trigonometricdata.append( triRec )

      # print( f"Add sin: { triRec[ 4 ]}" )

      triRec = []
      triRec.append( "cos" )
      triRec.append( 1 )
      triRec.append( iCount )
      triRec.append( iDenom )
      triRec.append( str( oFormulaCos ) )
      triRec.append( None )

      symTrigonometricData.trigonometricdata.append( triRec )

      # print( f"Add cos: { triRec[ 4 ]}" )

    def _createSinCosPlusOne( iCount, iDenom ):
      # sin( x + y ) = sin(x) cos(y) + cos(x) sin(y)
      # cos( x + y ) = cos(x) cos(y) - sin(x) sin(y)
      # sin( x - y ) = sin(x) cos(y) - cos(x) sin(y)
      # cos( x - y ) = cos(x) cos(y) - sin(x) sin(y)

      baseCount = iCount - 1
      # x = baseCount
      # y = 1
      formulaSin = f"sin( pi {baseCount} / {iDenom} ) cos( pi / {iDenom} ) + cos( pi {baseCount} / {iDenom} ) sin( pi / {iDenom} )"
      formulaCos = f"cos(pi {baseCount} / {iDenom}  ) cos( pi / {iDenom} ) - sin( pi {baseCount} / {iDenom} ) sin( pi / {iDenom} )"

      # print( f"formulaSin: {formulaSin}" )
      # print( f"formulaCos: {formulaSin}" )

      oFormulaSin = symexpress3.SymFormulaParser( formulaSin )
      oFormulaCos = symexpress3.SymFormulaParser( formulaCos )

      oFormulaSin.optimizeNormal()
      oFormulaCos.optimizeNormal()

      triRec = []
      triRec.append( "sin" )
      triRec.append( 1 )
      triRec.append( iCount )
      triRec.append( iDenom )
      triRec.append( str( oFormulaSin ) )
      triRec.append( None )

      symTrigonometricData.trigonometricdata.append( triRec )

      # print( f"Add sin: { triRec[ 4 ]}" )

      triRec = []
      triRec.append( "cos" )
      triRec.append( 1 )
      triRec.append( iCount )
      triRec.append( iDenom )
      triRec.append( str( oFormulaCos ) )
      triRec.append( None )

      symTrigonometricData.trigonometricdata.append( triRec )

      # print( f"Add cos: { triRec[ 4 ]}" )


    # only positive hooks
    if iCounter <= 0:
      return None

    if iDenominator <= 0:
      return None

    # 2 pi is max
    if iCounter >= iDenominator * 2 :
      return None

    # only sin and cos supported
    if not cType in ("sin", "cos" ):
      return None

    dictFactors = primefactor.FactorizationDict( iDenominator )

    # print( dictFactors );

    # only support 2, 3 and 5
    # other numbers will give complex radicals
    baseNumber = 1
    for key, value in dictFactors.items():
      if key == 2:
        baseNumber *= key
      elif key == 3:
        if value != 1:
          return None
        baseNumber *= key
      elif key == 5 :
        if value != 1:
          return None
        baseNumber *= key
      else:
        return None

    if baseNumber % 2 == 0:
      baseNumber //= 2

    if baseNumber == 1:
      return None

    # print( f"BaseNumber: {baseNumber}" )

    baseFormula = _getBaseFormula( cType, 1, baseNumber )
    if baseFormula == None:
      return None


    # get all the half numbers
    while baseNumber < iDenominator:
      baseNumber *= 2

      baseForm2 = _getBaseFormula( cType, 1, baseNumber )
      if baseForm2 == None:
        # print( f"Create new {baseNumber}" )
        # create new base formula
        _createSinCosHalf( baseNumber )

    # get the counter of the base
    baseFormula = _getBaseFormula( cType, iCounter, baseNumber )
    iCount = 1
    while baseFormula == None and iCount <= iCounter :
      iCount *= 2
      if iCount <= iCounter:
        # print( f"Add double {iCount} / {baseNumber}" )
        _createSinCosDouble( iCount, baseNumber )
      else:
        baseFormula = None
        break
      baseFormula = _getBaseFormula( cType, iCounter, baseNumber )

    if baseFormula == None:
      iCount //= 2
      while baseFormula == None and iCount <= iCounter:
        # add one
        iCount += 1
        # print( f"Add one {iCount} / {baseNumber}" )
        _createSinCosPlusOne( iCount, baseNumber )
        baseFormula = _getBaseFormula( cType, iCounter, baseNumber )

    # print( baseFormula );
    return baseFormula


  def _convertSinCosAtan( self, elem ):
    #
    # https://math.stackexchange.com/questions/1894265/how-do-i-show-this-cos2-arctanx-frac11x2/2121833#2121833
    # cos( atan( 11/3 ) / 2 )
    # sqrt( 1/4 (  ((i−11/3)/(i+11/3))^(1/2) + 2 + ((i+11/3)/(i−11/3))^(1/2) ))
    #
    # y is a number with power of 1
    # cos( atan( x ) * y ) = ( 1/4 ( ((i−x)/(i+x))^^(y) + 2 + ((i+x)/(i−x))^^(y) ))^^(1/2)
    # But this give an another cos( atan( ... )) -> imaginair number in a sqrt

    if elem.numElements() != 1:
      return None

    if isinstance( elem.elements[ 0 ], symexpress3.SymFunction ):
      elemfunc = elem.elements[ 0 ]
      if not elemfunc.name == 'atan':
        return None

      # sin( arctan(x)) = x / sqrt( 1+x^2 )
      # cos( arctan(x)) = 1 / sqrt( 1+x^2)
      strFunc   = '(' + str( elemfunc.elements[ 0 ] ) + ')'
      strSqrt   = '( 1 + ' + strFunc + '^^2)^^(1/2)'
      strResult = ''
      if elem.name == 'sin':
        strResult = strFunc + '/' + strSqrt
      else:
        # cos
        strResult = '1 /' + strSqrt

      # print( 'strResult: {}'.format( strResult ))

      exprResult = symexpress3.SymFormulaParser( '(' + strResult + ')' )
      exprResult.powerSign        = elem.powerSign
      exprResult.powerCounter     = elem.powerCounter
      exprResult.powerDenominator = elem.powerDenominator
      exprResult.optimizeNormal()

      # print( 'exprResult: {}'.format( str( exprResult ) ))

      return exprResult

    if ( isinstance( elem.elements[ 0 ], symexpress3.SymExpress) and elem.name == 'cos' ):
      #
      # https://de.wikipedia.org/wiki/Formelsammlung_Trigonometrie
      #
      # n = oneven
      # cos(x)^n = "1/exp(n-1,2) * sum( k, 0, (n-1)/2, binomial( n, k ) * cos( (n - 2k ) * x ))"
      #
      # n = even
      # cos(x)^n = "1/exp(n,2) * binomial( n, n / 2 )  +  1/exp(n-1,2) * sum( k, 0, n/2 - 1, binomial( n, k ) * cos( (n - 2k ) * x ))"
      #
      # format cos( ... )
      #
      # never ending loop -> give another cos( atan(...))

      # TODO sort out, solve others = disconnect...
      return None
      # pylint: disable=unreachable

      # global debugonlyonce

      # if ( debugonlyonce != 0  ):
      #    return None

      # debugonlyonce = 1

      elemexpress = elem.elements[ 0 ]
      if elemexpress.symType != '*':
        return None
      if elemexpress.numElements() != 2:
        return None
      if elemexpress.power != 1:
        return None

      # need a arctan(x) and a number with power of 1
      elemfunc = None
      elemnum  = None

      if isinstance( elemexpress.elements[ 0 ], symexpress3.SymFunction ):
        elemfunc = elemexpress.elements[ 0 ]
        elemnum  = elemexpress.elements[ 1 ]
      elif isinstance( elemexpress.elements[ 1 ], symexpress3.SymFunction ):
        elemfunc = elemexpress.elements[ 1 ]
        elemnum  = elemexpress.elements[ 0 ]

      if elemfunc == None:
        return None
      if elemfunc.name != 'atan':
        return None
      if elemfunc.numElements() != 1:
        return None

      if not isinstance( elemnum, symexpress3.SymNumber ):
        return None
      if elemnum.power != 1:
        return None


      if elemnum.factSign != 1:
        return None
      if elemnum.factDenominator == 1:
        return None


      # cos(x)^^3 = 3/4 cos(x) + cos(3x)
      # cos(3x) = 4 cos(x)^^3 - 3 cos(x)

      # strFunc = "4 cos( replace_x )^^3 - 3 cos( replace_x )"

      if elemnum.factDenominator % 2 == 1:
        # oneven
        strFunc = "1/exp( replace_n - 1,2) * sum( replace_k, 0, (replace_n - 1)/2, binomial( replace_n, replace_k ) * cos( (replace_n - 2 * replace_k ) * replace_x ))"
      else:
        # even
        strFunc = "1/exp(replace_n,2) * binomial( replace_n, replace_n / 2 )  +  1/exp(replace_n - 1,2) * sum( replace_k, 0, replace_n / 2 - 1, binomial( replace_n, replace_k ) * cos( (replace_n - 2 * replace_k ) * replace_x ))"

      print( f"strFunc: {strFunc}" )

      elemStr = "(" + str( elemexpress ) + ")"
      # elemStr = "(" + str( elemfunc ) + ")"
      strFunc = strFunc.replace( "replace_n", str( elemnum.factDenominator ) )
      strFunc = strFunc.replace( "replace_k", "k" + str( uuid.uuid4().int ) + "k" )
      strFunc = strFunc.replace( "replace_x", elemStr )

      strFunc = "(" + strFunc + ")^^( 1/" + str( elemnum.factDenominator ) + ")"

      print( f"strFunc filled in: {strFunc}" )

      exprResult = symexpress3.SymFormulaParser( strFunc )

      return exprResult

      # old solution below
      strNum  = '(' + str( elemnum )  + ')'
      strFunc = '(' + str( elemfunc.elements[ 0 ] ) + ')'

      # cos(x/3) = ((cos(x) + i sin(x))^(1/3) + (cos(x) - i sin(x))^(1/3) ) / 2
      # cos(x/y) = ((cos(x) + i sin(x))^(1/y) + (cos(x) - i sin(x))^(1/y) ) / 2

      # cos(atan(x)) = '(1 / ( (1+(x)^2)^(1/2)))'
      # sin(atan(x)) = '((x) / ( (1+(x)^2)^(1/2)))'

      # cos(atan(x)/y) = (( (1 / ( (1+(x)^2)^(1/2))) + i ((x) / ( (1+(x)^2)^(1/2))) )^(1/y) + ( (1 / ( (1+(x)^2)^(1/2))) - i ((x) / ( (1+(x)^2)^(1/2))) )^(1/y) ) / 2

      print( f'strNum : {strNum}'  )
      print( f'strFunc: {strFunc}' )


      strResult  = '(( (1 / ( (1+('+strFunc+')^^2)^^(1/2))) + i (('+strFunc+') / ( (1+('+strFunc+')^^2)^^(1/2))) )^^('+strNum+') + ( (1 / ( (1+('+strFunc+')^^2)^^(1/2))) - i (('+strFunc+') / ( (1+('+strFunc+')^^2)^^(1/2))) )^^('+strNum+') ) / 2'

      # y is a number with power of 1
      # cos( atan( x ) * y ) = ( 1/4 ( ((i−x)/(i+x))^^(y) + 2 + ((i+x)/(i−x))^^(y) ))^^(1/2)

      print( f'strNum : {strNum}'  )
      print( f'strFunc: {strFunc}' )


      # # strResult = '(1/4((( i - ' + strFunc + ')/(i + ' + strFunc + '))^^(' + strNum + ') + 2 + ((i + ' + strFunc + ')/(i - ' + strFunc + '))^^(' + strNum + ') ))^^(1/2)'
      # # (  (( ( 1 + 2iy - y^^2 ) / (1+y^^2) )^^z + 2 + ( ( 1 - 2iy - y^^2 ) / ( 1 + y^^2 ) )^^z ) / 4  )^^(1/2)
      # strResult = '(  (( ( 1 + 2 i ' + strFunc + ' - ' + strFunc + '^^2 ) / (1 + ' + strFunc + '^^2) )^^' + strNum + ' + 2 + ( ( 1 - 2 i ' + strFunc + ' - ' + strFunc + '^^2 ) / ( 1 + ' + strFunc + '^^2 ) )^^' + strNum + ' ) / 4  )^^(1/2)'

      print( f'strResult: {strResult}' )

      exprResult = symexpress3.SymFormulaParser( strResult )
      exprResult.optimizeNormal()

      print( f'strResult normalized: {str( exprResult )}' )

      return exprResult

    return None

  def _convertSinCosTanAtanSign( self, elem ):
    #  sin( -x ) = - sin(  x )
    #  cos( -x ) = + cos(  x )
    #  tan( -x ) = - tan(  x )
    # atan( -x ) = - atan( x )
    # asin( -x ) = - asin( x )
    # acos( -x ) = pi - acos( x )

    if elem.numElements() != 1:
      return None

    elem1 = elem.elements[ 0 ]
    if isinstance( elem1, symexpress3.SymNumber ):
      if (elem1.power != 1 or elem1.factSign == 1 ):
        return None

      elemExpress    = elem.copy()
      elem1          = elemExpress.elements[ 0 ]
      elem1.factSign = 1

      if elemExpress.name == "cos":
        elemResult = elemExpress

      elif elemExpress.name == "acos":
        elemResult = symexpress3.SymExpress( '+' )
        elemResult.add( symexpress3.SymVariable( 'pi' ))

        elemExtra = symexpress3.SymExpress('*')
        elemExtra.add( symexpress3.SymNumber( -1, 1, 1 ) )
        elemExtra.add( elemExpress )

        elemResult.add( elemExtra )
      else:
        elemResult = symexpress3.SymExpress('*')
        elemResult.add( symexpress3.SymNumber( -1, 1, 1, 1, 1, 1, 1) )
        elemResult.add( elemExpress )

      return elemResult

    if not isinstance( elem1, symexpress3.SymExpress ):
      return None

    if elem1.symType != '*':
      return None

    # search for a negative number
    foundNo = -1
    for iCnt, elemTest in enumerate( elem1.elements ):
      if not isinstance( elemTest, symexpress3.SymNumber ):
        continue
      if (elemTest.power != 1) or (elemTest.factSign == 1):
        continue
      # ok, found one
      foundNo = iCnt
      break

    if foundNo == -1:
      return None

    elemExpress    = elem.copy()
    elem1          = elemExpress.elements[ 0 ].elements[ foundNo ]
    elem1.factSign = 1

    if elemExpress.name == "cos":
      elemResult = elemExpress

    elif elemExpress.name == "acos":
      elemResult = symexpress3.SymExpress( '+' )
      elemResult.add( symexpress3.SymVariable( 'pi' ))

      elemExtra = symexpress3.SymExpress('*')
      elemExtra.add( symexpress3.SymNumber( -1, 1, 1 ) )
      elemExtra.add( elemExpress )

      elemResult.add( elemExtra )
    else:
      elemResult = symexpress3.SymExpress('*')
      elemResult.add( symexpress3.SymNumber( -1, 1, 1, 1, 1, 1, 1) )
      elemResult.add( elemExpress )

    return elemResult

  def _conversTableToArc( self, elem ):
    funcname = None
    if elem.name == 'atan':
      funcname = 'tan'
    elif elem.name == 'asin':
      funcname = "sin"
    elif elem.name == "acos":
      funcname = "cos"

    if funcname == None:
      return None

    exp = elem.elements[ 0 ]

    # print( "funcname: {}, exp: {}, type: {}".format( funcname, str( exp ), type( exp ) ))

    for tri in symTrigonometricData.trigonometricdata:

      if tri[ 0 ] != funcname:
        continue

      # convert string to expression
      if tri[ 5 ] == None:
        tri[ 5 ] = symexpress3.SymFormulaParser( tri[ 4 ] )
        tri[ 5 ].optimizeNormal()
        if tri[ 5 ].numElements() == 1:
          tri[ 5 ] = tri[ 5 ].elements[ 0 ]

      # print( "found {}, expr: {}, type: {}".format( tri[ 0 ], str( tri[ 5 ] ), type( tri[5] ) ) )

      if not exp.isEqual( tri[ 5 ] ):
        continue

      # found one
      angle = ''
      if tri [ 1 ] == -1:
        angle += '-1 '

      angle += str( tri[ 2 ] ) + ' / ' + str( tri[ 3 ] ) + ' * pi '

      newelem = symexpress3.SymFormulaParser( angle )
      newelem.powerSign        = elem.powerSign
      newelem.powerCounter     = elem.powerCounter
      newelem.powerDenominator = elem.powerDenominator

      return newelem

    return None
