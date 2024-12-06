#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Multiply for Sym Express 3

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
from symexpress3          import primefactor  as primefac

class OptimizeMultiply( optimizeBase.OptimizeBase ):
  """
  Multiply the elements of this expressions and his sub-expressions
  \n(x+1)(x+1) becomes x^2 + 2x + 1
  """
  def __init__( self ):
    super().__init__()
    self._name         = "multiply"
    self._symtype      = "*"
    self._desc         = "Multiply elements"


  def optimize( self, symExpr, action ):
    result = False
    if self.checkExpression( symExpr, action ) != True:
      # print( "Afgekeurd: " + symExpr.symType )
      return result

    # multiply symNumbers
    def _multiplyNumbers():
      result = False
      if symExpr.symType != '*':
        return result

      elem = None
      iCnt = 0
      for iCnt, elem in enumerate( symExpr.elements ) :
        if not isinstance( elem, symexpress3.SymNumber ):
          continue
        if elem.powerDenominator != 1:
          continue
        break

      if elem == None:
        return result

      # print( "_multiplyNumbers start: {}".format( symExpr ) )

      for iCnt2 in range( len( symExpr.elements ) -1 , -1, -1 ) :
        if iCnt2 <= iCnt:
          break
        elem2 = symExpr.elements[ iCnt2 ]
        if not isinstance( elem2, symexpress3.SymNumber ):
          continue

        if elem2.powerDenominator > 1:
          continue

        if elem2.powerCounter > 1:
          elem2.factCounter     = pow( elem2.factCounter * elem2.factSign, elem2.powerCounter )
          elem2.factDenominator = pow( elem2.factDenominator             , elem2.powerCounter )

        if elem.powerCounter > 1:
          elem.factCounter     = pow( elem.factCounter * elem.factSign, elem.powerCounter )
          elem.factDenominator = pow( elem.factDenominator            , elem.powerCounter )
          elem.powerCounter    = 1

        if elem2.powerSign != elem.powerSign:
          elem.factDenominator *= elem2.factCounter
          elem.factCounter     *= elem2.factDenominator
        else:
          elem.factCounter     *= elem2.factCounter
          elem.factDenominator *= elem2.factDenominator

        elem.factSign    *= elem2.factSign
        # elem.onlyOneRoot  = max( elem.onlyOneRoot, elem2.onlyOneRoot )
        elem.onlyOneRoot  = min( elem.onlyOneRoot, elem2.onlyOneRoot )

        del symExpr.elements[ iCnt2 ]
        result = True

      return result

    # get all sub expressions with power op 1
    def _multiplyElemGetSubPowerOne():
      result = False
      if symExpr.symType != '*':
        return result

      lFound = True
      while lFound == True :
        lFound = False
        iCnt   = 0
        for iCnt, elem1 in enumerate( symExpr.elements ) :
          if not isinstance( elem1 , symexpress3.SymExpress ):
            continue
          if elem1.symType != '*':
            continue
          if elem1.power != 1:
            continue
          lFound = True
          for elem2 in elem1.elements :
            symExpr.add( elem2 )
          del symExpr.elements[ iCnt ]
          result = True
          break

      return result

    # multiply SymVariable with expression of type +
    def _multiplyElemUnitExpress():
      result = False
      if symExpr.symType != '*':
        return result

      lFound = True
      while( lFound == True and len( symExpr.elements ) > 1 ):
        lFound = False
        iCnt   = 0
        for iCnt, elem1 in enumerate( symExpr.elements ) :

          if not isinstance( elem1 , symexpress3.SymVariable ):
            continue

          # a root have multiple solutions, cannot multiply with + expressions
          if (elem1.powerDenominator > 1 and elem1.onlyOneRoot == 0 ):
            continue

          iCnt2 = 0
          while( lFound == False and iCnt2 < len( symExpr.elements )):
            if iCnt == iCnt2:
              iCnt2 += 1
              continue
            elem2 = symExpr.elements[ iCnt2 ]
            iCnt2 += 1

            if not isinstance( elem2 , symexpress3.SymExpress ):
              continue

            # only multiply no + expressions
            if elem2.symType != '+' :
              continue

            # only power of 1 is supported or same powers (numbers of roots must be the same)
            if (elem2.power == 1 or ( elem2.power == elem1.power and ( elem1.powerDenominator == 1 or elem1.onlyOneRoot == elem2.onlyOneRoot ) ) ):
              pass
            else:
              continue

            # found one
            # delete elements from current expression
            if iCnt < iCnt2:
              del symExpr.elements[ iCnt2 - 1 ] # already has done +1
              del symExpr.elements[ iCnt      ]
            else:
              del symExpr.elements[ iCnt      ]
              del symExpr.elements[ iCnt2 - 1 ] # already has done +1

            lFound = True
            result = True

            elemnew = symexpress3.SymExpress( '+' )
            if elem1.power == elem2.power:
              elemnew.powerSign        = elem1.powerSign
              elemnew.powerCounter     = elem1.powerCounter
              elemnew.powerDenominator = elem1.powerDenominator
              elemnew.onlyOneRoot      = elem1.onlyOneRoot

              elem1.powerSign        = 1
              elem1.powerCounter     = 1
              elem1.powerDenominator = 1

            for iCntSub1 in range( 0, elem2.numElements() ) :
              elem3 = elem2.elements[ iCntSub1 ]
              elemnew2 = symexpress3.SymExpress( '*' )
              elemnew2.add( elem1 )
              elemnew2.add( elem3 )
              elemnew.add ( elemnew2 )

            symExpr.add( elemnew )

          if lFound == True:
            break

      return result

    # multiply 2 expressions
    def _multiplyElemExpressExpress():
      result = False
      if symExpr.symType != '*':
        return result

      lFound = True
      while( lFound == True and len( symExpr.elements ) > 1 ):
        lFound  = False

        # print ('num elements: {}'.format(  len( symExpr.elements )))

        for iCnt in range( 0, len( symExpr.elements ) - 1 ) :
          elem1 = symExpr.elements[ iCnt     ]

          # only multiple expressions
          if not isinstance( elem1 , symexpress3.SymExpress ):
            continue
          # only multiply with power of 1
          if ( elem1.power != 1 and elem1.power != -1):  # pylint: disable=consider-using-in
            continue
          # only + expressions
          if elem1.symType != '+':
            continue

          iCnt2 = iCnt + 1
          while( lFound == False and iCnt2 < len( symExpr.elements )):
            elem2 = symExpr.elements[ iCnt2 ]
            iCnt2 += 1

            # only multiply expressions
            if not isinstance( elem2 , symexpress3.SymExpress ):
              continue
            # only multiply with power of 1
            if elem2.power != elem1.power:
              continue
            # only + expressions
            if elem2.symType != '+':
              continue

            # 2 plus expression with power of 1
            # the factors are already one, see loops above
            elemnew = symexpress3.SymExpress( '+' )
            elemnew.powerSign = elem2.powerSign
            for elemSub1 in elem1.elements:

              for elemSub2 in elem2.elements:
                elem12 = symexpress3.SymExpress( '*' )
                elem12.add( elemSub1 )
                elem12.add( elemSub2 )
                elemnew.add( elem12 )

            symExpr.elements[ iCnt ] = elemnew
            del symExpr.elements[ iCnt2 - 1 ] # already has done +1
            lFound = True
            result = True

          if lFound == True:
            break
      return result

    # multiply 2 variables
    def _multiplyElemVarVar():
      result = False
      if symExpr.symType != '*':
        return result

      # multiple all units with same name
      lFound = True
      while( lFound == True and len( symExpr.elements ) > 1 ):
        lFound = False
        for iCnt in range( 0, len( symExpr.elements ) - 1 ) :
          elem1 = symExpr.elements[ iCnt     ]

          # only SymVariable
          if not isinstance( elem1 , symexpress3.SymVariable ):
            continue

          iCnt2 = iCnt + 1
          while iCnt2 < len( symExpr.elements ):
            elem2 = symExpr.elements[ iCnt2 ]
            iCnt2 += 1

            if not isinstance( elem2 , symexpress3.SymVariable ):
              continue

            # it must have the same name
            if elem2.name != elem1.name:
              continue

            elemnew = elem1.copy()

            # if it is a fraction, make the denominator equal
            elem1.powerCounter     *= elem2.powerDenominator
            elem1.powerDenominator *= elem2.powerDenominator

            elem2.powerCounter     *= elemnew.powerDenominator
            elem2.powerDenominator *= elemnew.powerDenominator

            iCounter = elem1.powerCounter * elem1.powerSign + elem2.powerCounter * elem2.powerSign

            elem1.powerSign    = 1
            elem1.powerCounter = iCounter
            elem1.onlyOneRoot  = min( elem1.onlyOneRoot, elem2.onlyOneRoot )

            del symExpr.elements[ iCnt2 - 1 ] # already has done +1
            lFound = True
            result = True
            break

          if lFound == True:
            break
      return result

    # multiply number with multiple-plus-expression
    def _multiplyNumberExpress():
      result = False
      if symExpr.symType != '*':
        return result

      if symExpr.numElements() != 2:
        return result

      elem1 = symExpr.elements[ 0 ]
      elem2 = symExpr.elements[ 1 ]

      elemNum  = None
      elemExpr = None

      if isinstance( elem1, symexpress3.SymNumber ):
        elemNum = elem1
      elif isinstance( elem2, symexpress3.SymNumber ):
        elemNum = elem2
      if elemNum == None:
        return result

      if isinstance( elem1, symexpress3.SymExpress ):
        elemExpr = elem1
      elif isinstance( elem2, symexpress3.SymExpress ):
        elemExpr = elem2
      if elemExpr == None:
        return result

      if elemExpr.symType != '+':
        return result
      if elemExpr.power != 1:
        return result

      symExpr.elements = []
      symExpr.symType  = '+'
      for elemsub in elemExpr.elements :
        elemnew = symexpress3.SymExpress( '*' )
        elemnew.add( elemNum )
        elemnew.add( elemsub )
        symExpr.add( elemnew )
        result = True

      return result

    # multiply plus-expression with multiply-expression
    def _multplyPlusExpressMultiply():
      result = False
      if symExpr.symType != '*':
        return result

      if symExpr.numElements() <= 1:
        return result

      for iCnt, elem in enumerate( symExpr.elements ) :
        elem = symExpr.elements[ iCnt ]
        if not isinstance( elem, symexpress3.SymExpress ):
          continue
        if elem.power != 1:
          continue
        if elem.symType != '+':
          continue
        if elem.numElements() <= 1:
          continue
        # found a plus expression within a multiply express
        # make it a plus expression
        symMulti = symexpress3.SymExpress( '*' )
        for iCnt2, elemSub2 in enumerate( symExpr.elements ):
          if iCnt2 == iCnt:
            continue
          symMulti.add( elemSub2 )

        # print( 'SymMulti: {}'.format( str( SymMulti )))

        if symMulti.numElements() == 0:
          continue

        symExpr.symType  = '+'
        symExpr.elements = []
        result           = True
        for elemSub2 in elem.elements :
          symNew = symexpress3.SymExpress( '*' )
          symNew.add( symMulti )
          symNew.add( elemSub2 )
          symExpr.add( symNew )

        # SymExpress is now a plus expression
        return result

      return result

    # multiply radicals with the same base (onlyOneRoot only)
    def _multplyPlusMultiplyOnlyRoots():
      result = False
      if symExpr.symType != '*':
        return result

      lFound = True
      while lFound == True:
        lFound = False
        for iCnt, elem in enumerate( symExpr.elements ) :
          if elem.powerDenominator == 1:
            continue
          if elem.onlyOneRoot == 0:
            continue

          elemcheck1 = None

          # print( "_multplyPlusMultiplyOnlyRoots elem1: {}".format( str( elem )) )

          # search for the next element with the same base
          for iCnt2 in range( iCnt + 1 , len( symExpr.elements )):
            elem2 = symExpr.elements[ iCnt2 ]
            if elem2.onlyOneRoot != 1:
              continue
            if elem2.powerDenominator == 1:
              continue

            if elemcheck1 == None:
              elemcheck1 = elem.copy()
              elemcheck1.powerSign        = 1
              elemcheck1.powerDenominator = 1
              elemcheck1.powerCounter     = 1

            elemcheck2 = elem2.copy()
            elemcheck2.powerSign        = 1
            elemcheck2.powerDenominator = 1
            elemcheck2.powerCounter     = 1

            # print( "_multplyPlusMultiplyOnlyRoots elem1: {} == {}".format( str( elemcheck1 ), str( elem ) ) )
            # print( "_multplyPlusMultiplyOnlyRoots elem2: {} == {}".format( str( elemcheck2 ), str( elem2) ) )

            if not elemcheck1.isEqual( elemcheck2 ):
              lOk = False

              # needed this 4 variable to initialize, but the initialize value is never used (pylint)
              rem1FactCounter   = 1
              rem2FactCounter   = 1
              rem1PowerCounter  = 1
              rem2PowerCounter  = 1

              if ( isinstance( elem, symexpress3.SymNumber ) and isinstance( elem2, symexpress3.SymNumber )):
                dPrimeSet1 = primefac.factorint( elem.factCounter  )
                dPrimeSet2 = primefac.factorint( elem2.factCounter )

                # print ( "dPrimeSet1: {}".format( dPrimeSet1 ))
                # print ( "dPrimeSet2: {}".format( dPrimeSet2 ))

                if ( len( dPrimeSet1 ) == 1 and len( dPrimeSet2 ) == 1 ):
                  if list( dPrimeSet1.keys() )[0] == list( dPrimeSet2.keys() )[0] :
                    # 2 elements with the same base
                    # put the numbers in the counters of the power
                    # print( "list( dPrimeSet1)[ 0 ]: {}".format( list( dPrimeSet1.values())[ 0 ] ))
                    # print( "list( dPrimeSet2)[ 0 ]: {}".format( list( dPrimeSet2.values() )[ 0 ] ))

                    # TODO, not a nice solution but for the moment
                    elemcheck1 = elem.copy()
                    elemcheck1.powerSign        = 1
                    elemcheck1.powerDenominator = 1
                    elemcheck1.powerCounter     = 1

                    elemcheck2 = elem2.copy()
                    elemcheck2.powerSign        = 1
                    elemcheck2.powerDenominator = 1
                    elemcheck2.powerCounter     = 1

                    rem1FactCounter    = list( dPrimeSet1.keys()  )[ 0 ]
                    rem2FactCounter    = list( dPrimeSet2.keys()  )[ 0 ]
                    rem1PowerCounter  = elem.powerCounter  * list( dPrimeSet1.values())[ 0 ]
                    rem2PowerCounter  = elem2.powerCounter * list( dPrimeSet2.values())[ 0 ]

                    lOk = True

              if lOk == False:
                continue

              elemcheck1.factCounter   = rem1FactCounter
              elemcheck2.factCounter   = rem2FactCounter
              elemcheck1.powerCounter  = rem1PowerCounter
              elemcheck2.powerCounter  = rem2PowerCounter

              elemcheck1.powerSign        = 1
              elemcheck1.powerDenominator = 1
              elemcheck1.powerCounter     = 1

              elemcheck2.powerSign        = 1
              elemcheck2.powerDenominator = 1
              elemcheck2.powerCounter     = 1

              if not elemcheck1.isEqual( elemcheck2 ):
                # print( "afgekeurd" )
                continue

              elem.factCounter    = rem1FactCounter
              elem2.factCounter   = rem2FactCounter
              elem.powerCounter   = rem1PowerCounter
              elem2.powerCounter  = rem2PowerCounter

            # print( "_multplyPlusMultiplyOnlyRoots elem1: {} == {}".format( str( elemcheck1 ), str( elem ) ) )
            # print( "_multplyPlusMultiplyOnlyRoots elem2: {} == {}".format( str( elemcheck2 ), str( elem2) ) )

            # print( "_multplyPlusMultiplyOnlyRoots 2 elem1: {}".format( str( elem ) ) )
            # print( "_multplyPlusMultiplyOnlyRoots 2 elem2: {}".format( str( elem2) ) )

            elemcheck1 = None

            # print( "elem1: {}".format( str( elem  )))
            # print( "elem2: {}".format( str( elem2 )))

            # print( "_multplyPlusMultiplyOnlyRoots 0 elem1.powerCounter    : {}".format( elem.powerCounter      ) )
            # print( "_multplyPlusMultiplyOnlyRoots 0 elem2.powerCounter    : {}".format( elem2.powerCounter     ) )

            # print( "_multplyPlusMultiplyOnlyRoots 0 elem1.factCounter    : {}".format( elem.factCounter      ) )
            # print( "_multplyPlusMultiplyOnlyRoots 0 elem2.factCounter    : {}".format( elem2.factCounter     ) )

            # 2 radicals with the same denominator
            # add the powers
            if elem.powerDenominator != elem2.powerDenominator:
              # print( "_multplyPlusMultiplyOnlyRoots 1 elem1.powerDenominator: {}".format( elem.powerDenominator  ) )
              # print( "_multplyPlusMultiplyOnlyRoots 1 elem2.powerDenominator: {}".format( elem2.powerDenominator ) )

              # iPowerCounter1       = elem.powerCounter
              iPowerDenominator1   = elem.powerDenominator

              elem.powerDenominator  *= elem2.powerDenominator
              elem.powerCounter      *= elem2.powerDenominator

              elem2.powerCounter     *= iPowerDenominator1
              elem2.powerDenominator *= iPowerDenominator1

               # print( "_multplyPlusMultiplyOnlyRoots 2 elem1.powerCounter    : {}".format( elem.powerCounter      ) )
               # print( "_multplyPlusMultiplyOnlyRoots 2 elem1.powerDenominator: {}".format( elem.powerDenominator  ) )
               # print( "_multplyPlusMultiplyOnlyRoots 2 elem2.powerCounter    : {}".format( elem2.powerCounter     ) )
               # print( "_multplyPlusMultiplyOnlyRoots 2 elem2.powerDenominator: {}".format( elem2.powerDenominator ) )

            iCounter = elem.powerCounter * elem.powerSign + elem2.powerCounter * elem2.powerSign

            # print( "_multplyPlusMultiplyOnlyRoots 3 elem1.factCounter    : {}".format( elem.factCounter      ) )
            # print( "_multplyPlusMultiplyOnlyRoots 3 elem2.factCounter    : {}".format( elem2.factCounter     ) )

            # print( "_multplyPlusMultiplyOnlyRoots 3 elem1.powerCounter    : {}".format( elem.powerCounter      ) )
            # print( "_multplyPlusMultiplyOnlyRoots 3 elem2.powerCounter    : {}".format( elem2.powerCounter     ) )

            # print( "_multplyPlusMultiplyOnlyRoots iCounter: {}".format( iCounter ) )

            # print( "_multplyPlusMultiplyOnlyRoots last elem1: {}".format( str( elem ) ) )
            # print( "_multplyPlusMultiplyOnlyRoots last elem2: {}".format( str( elem2) ) )

            elem.powerSign     = 1
            elem.powerCounter  = iCounter

            # print( "elem new: {}".format( str( elem  )))

            del symExpr.elements[ iCnt2 ]
            lFound = True
            result = True
            break
          if lFound == True:
            break

      return result

    # multiply radicals with the same power
    def _multplyRadicalsSamePowerOnlyRoots():
      result = False

      if symExpr.symType != '*':
        return result

      lFound = True
      while lFound == True:
        lFound = False
        oExpr  = None
        for iCnt, elem in enumerate( symExpr.elements ) :
          if elem.powerDenominator == 1:
            continue
          if elem.onlyOneRoot == 0 :
            continue

          iCnt2 = iCnt + 1
          while iCnt2 < len( symExpr.elements ):
            elem2 = symExpr.elements[ iCnt2 ]
            iCnt2 += 1
            if elem2.onlyOneRoot == 0:
              continue
            if elem2.power != elem.power:
              continue
            lFound = True
            if oExpr == None:
              oExpr = symexpress3.SymExpress( '*' )
              oExpr.powerSign        = elem.powerSign
              oExpr.powerCounter     = elem.powerCounter
              oExpr.powerDenominator = elem.powerDenominator
              oExpr.onlyOneRoot      = 1

            elem2.powerSign        = 1
            elem2.powerCounter     = 1
            elem2.powerDenominator = 1

            oExpr.add( elem2 )

            iCnt2 -= 1
            del symExpr.elements[ iCnt2 ]
            result = True

          if lFound == True:
            elem.powerSign        = 1
            elem.powerCounter     = 1
            elem.powerDenominator = 1

            oExpr.add( elem )
            del symExpr.elements[ iCnt ]
            symExpr.add( oExpr )
            result = True
            break

      # print( "symExpr: {}".format( str( symExpr )) )
      return result

    def _multiplyFunctionFunction():
      result = False

      if symExpr.symType != '*':
        return result
      if symExpr.numElements() <= 1:
        return result

      lFound = True
      while lFound == True:

        lFound = False
        for iCnt, elem in enumerate( symExpr.elements ):

          # print( 'iCnt: {}'.format( iCnt ))

          if not isinstance( elem, symexpress3.SymFunction ):
            continue

          # print( '_multiplyFunctionFunction: {} {}'.format( iCnt, str( elem )))

          for iCnt2 in range( iCnt + 1, len( symExpr.elements ) ):
            elem2 = symExpr.elements[ iCnt2 ]

            if elem2.isEqual( elem, True, False ) != True:
              continue

            # 2 same function add powers
            iPowerCounter1     = elem.powerCounter  * elem.powerSign
            iPowerCounter2     = elem2.powerCounter * elem2.powerSign

            iPowerDenominator1 = elem.powerDenominator
            iPowerDenominator2 = elem2.powerDenominator

            # 2/3 + 3/5 = 2 * 5 / 3 * 5 + 3 * 3 / 5 * 3
            iPowerCounter     = iPowerCounter1 * iPowerDenominator2 + iPowerCounter2 * iPowerDenominator1
            iPowerDenominator = iPowerDenominator1 * iPowerDenominator2

            lFound = True
            result = True

            elem.powerSign        = 1
            elem.powerCounter     = iPowerCounter
            elem.powerDenominator = iPowerDenominator

            del symExpr.elements[ iCnt2 ]
            break

          if lFound == True:
            break
      return result

    #
    # Main part multplyElements
    # .........................

    # return
    # check for symType but every routine must check it to because the simType can be changed
    if symExpr.symType != '*':
      return result
    if symExpr.numElements() <= 1:
      return result

    # multiply SymNumbers
    result |= _multiplyNumbers()

    # get all sub expressons with power op 1
    result |= _multiplyElemGetSubPowerOne()

    # multiply SymVariable with sympexression of type +
    result |= _multiplyElemUnitExpress()

    # multiply 2 symexpressions (type plus)
    result |= _multiplyElemExpressExpress()

    # multiple all SymVariable
    result |= _multiplyElemVarVar()

    # multiply number with plus expression
    result |= _multiplyNumberExpress()

    # multiply radicals with onylroots
    result |= _multplyPlusMultiplyOnlyRoots()

    # multiply radicals with onlyroots with same power
    result |= _multplyRadicalsSamePowerOnlyRoots()

    # multiply plus with multiply
    result |= _multplyPlusExpressMultiply()

    # multiply same function = power + 1
    result |= _multiplyFunctionFunction()

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


  # multiply SymNumbers
  symTest = symexpress3.SymFormulaParser( '2 * 3' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "6" )


  # get all sub expressie with power op 1
  symTest = symexpress3.SymFormulaParser( '2 * 3 * (( 2 * 5 ))' )
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]

  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "6 * 2 * 5" )


  # multiply SymVariable with sympexression of type +
  symTest = symexpress3.SymFormulaParser( 'a * ( 2 + 3)' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "(a * 2 + a * 3)" )


  # multiply 2 symexpressions (type plus)
  symTest = symexpress3.SymFormulaParser( '( a + b ) * ( c + 3)' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "(a * c + a * 3 + b * c + b * 3)" )


  # multiple all SymVariable
  symTest = symexpress3.SymFormulaParser( 'a * a^2' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "a^3" )


  # multiply 2 symexpressions (type plus)
  symTest = symexpress3.SymFormulaParser( '( a + b ) * ( c + 3)' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "(a * c + a * 3 + b * c + b * 3)" )


  # multiply number with plus expression
  symTest = symexpress3.SymFormulaParser( '3 * ( a + 4)' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "3 * a + 3 * 4" )


  # multiply radicals with onylroots
  symTest = symexpress3.SymFormulaParser( '3^^(1/2) * 3^^(1/3)' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "3^^(5/6)" )


  # multiply radicals with onlyroots with same power
  symTest = symexpress3.SymFormulaParser( '3^^(1/3) * 5^^(1/3)' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "(5 * 3)^^(1/3)" )


  # multiply plus with multiply
  symTest = symexpress3.SymFormulaParser( '3 * a * ( c + d ) * e' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "3 * e * a * c + 3 * e * a * d" )


  # multiply same function = power + 1
  symTest = symexpress3.SymFormulaParser( 'cos(x) * cos(x)' )
  symTest.optimize()
  # the upper is a + expression, the inner is a * expression
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeMultiply()
  testClass.optimize( symTest, "multiply" )

  _Check( testClass, symOrg, symTest, "cos( x )^^2" )

if __name__ == '__main__':
  Test( True )
