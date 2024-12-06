#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Add elements for Sym Express 3

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

class OptimizeAdd( optimizeBase.OptimizeBase ):
  """
  Add elements
  """
  def __init__( self ):
    super().__init__()
    self._name         = "add"
    self._symtype      = "+"
    self._desc         = "Add elements"


  def optimize( self, symExpr, action ):
    """
    Adding up elements in this expression and his sub-expression.
    \n x + 2x becomes 3x
    """
    result = False
    if self.checkExpression( symExpr, action ) != True:
      # print( "Afgekeurd: " + symExpr.symType )
      return result

    if symExpr.symType != '+' :
      return result

    if symExpr.numElements() <= 1 :
      return result

    # print('add element start type: {}: {}'.format( symExpr.symType, str( symExpr )))
    # return

    # add the same elements (SymVariables) together

    # addBefore = str( symExpr )

    lFound = True
    while lFound == True :
      lFound = False
      for iCnt in range( 0, len( symExpr.elements ) - 1) :

        elem1 = symExpr.elements[ iCnt ]

        # print( 'add start: {}'.format( str( elem1 )))

        # search next elements that is the same
        for iCnt2 in range( iCnt + 1, len( symExpr.elements )) :
          if iCnt2 >= len( symExpr.elements ):
            continue

          elem2 = symExpr.elements[ iCnt2 ]

          # print( 'elem2: {}'.format( str( elem2 )))

          # do not check the factors ( = numbers with power of 1)
          if elem1.isEqual( elem2, False ) != True :
            continue

          # print( "symExpr.getValue: {}".format( symExpr.getValue() ))
          # print( "elem1: {}, type: {}".format( str( elem1 ), type( symExpr.elements[ iCnt  ] )))
          # print( "elem2: {}, type: {}".format( str( elem2 ), type( symExpr.elements[ iCnt2 ] )))

          # same name, same power, found one
          # add factors and delete cnt2
          if ( isinstance( elem1, symexpress3.SymNumber ) and isinstance( elem2, symexpress3.SymNumber )):
            if ( elem1.power != 1 and elem1.power != -1 ): # pylint: disable=consider-using-in

              if elem1.factor != elem2.factor :
                continue

              elemnew = symexpress3.SymExpress( '*' )
              elemnum = symexpress3.SymNumber( 1, 2, 1, 1, 1, 1)
              elemnew.add( elemnum )
              elemnew.add( elem1   )
              symExpr.elements[ iCnt ] = elemnew
            else:
              elem3 = symexpress3.SymNumber()
              elem3.factSign        = elem1.factSign
              elem3.factCounter     = elem1.factCounter
              elem3.factDenominator = elem1.factDenominator
              elem3.onlyOneRoot     = elem1.onlyOneRoot

              # elem1.factSign *= elem2.factSign
              elem1.factCounter     *= elem2.factDenominator
              elem1.factDenominator *= elem2.factDenominator

              elem2.factCounter     *= elem3.factDenominator
              elem2.factDenominator *= elem3.factDenominator

              elem1factor = elem1.factSign * elem1.factCounter
              elem2factor = elem2.factSign * elem2.factCounter

              elem1.factSign    = 1
              elem1.factCounter = elem1factor + elem2factor
              # elem1.onlyOneRoot = max( elem3.onlyOneRoot, elem2.onlyOneRoot )
              elem1.onlyOneRoot = min( elem3.onlyOneRoot, elem2.onlyOneRoot )

            # print( "elem1 new: {}".format( str( elem1 )))
            del symExpr.elements[ iCnt2 ]
            lFound = True
            result = True
            break

          if ( not isinstance( elem1, symexpress3.SymExpress ) and not isinstance( elem2, symexpress3.SymExpress ) ):
            elemnew = symexpress3.SymExpress( '*' )
            elemnum = symexpress3.SymNumber( 1, 2, 1, 1, 1, 1)
            elemnew.add( elemnum )
            elemnew.add( elem1   )
            symExpr.elements[ iCnt ] = elemnew

            del symExpr.elements[ iCnt2 ]
            lFound = True
            result = True
            break

          if ( not isinstance( elem1, symexpress3.SymExpress ) or not isinstance( elem2, symexpress3.SymExpress ) ):

            # print( 'special, elem1: {}, elem2: {}'.format( str( elem1 ), str( elem2 )))

            # 2 different types, 1 is an expression
            elemnew = symexpress3.SymExpress( '*' )
            elemnum = symexpress3.SymNumber( 1, 1, 1, 1, 1, 1)
            if isinstance( elem1, symexpress3.SymExpress ):
              elemexp = elem1
            else:
              elemexp = elem2
            elemnew.onlyOneRoot      = elemexp.onlyOneRoot
            elemnew.powerSign        = elemexp.powerSign
            elemnew.powerCounter     = elemexp.powerCounter
            elemnew.powerDenominator = elemexp.powerDenominator

            # print( "elemnew stap 1: {}".format( elemnew ))

            # elemexp is now the symexpress
            lOnlyOne = True
            for iCnt3 in range( 0, elemexp.numElements()):
              elemsub = elemexp.elements[ iCnt3 ]
              if ( lOnlyOne == True and isinstance( elemsub, symexpress3.SymNumber ) and elemsub.power == 1 ):
                lOnlyOne = False
                # print( 'elemsub start: {}, power: {}'.format( str( elemsub ), elemsub.power ))
                # print( 'elemnum start: {}'.format( str( elemnum )))

                elem3 = symexpress3.SymNumber()
                elem3.factSign        = elemnum.factSign
                elem3.factCounter     = elemnum.factCounter
                elem3.factDenominator = elemnum.factDenominator
                elem3.onlyOneRoot     = elemnum.onlyOneRoot

                # elem1.factSign *= elem2.factSign
                elemnum.factCounter     *= elemsub.factDenominator
                elemnum.factDenominator *= elemsub.factDenominator

                elemsub.factCounter     *= elem3.factDenominator
                elemsub.factDenominator *= elem3.factDenominator

                elem1factor = elemnum.factSign * elemnum.factCounter
                elem2factor = elemsub.factSign * elemsub.factCounter

                # print( 'elem1factor: {}'.format( elem1factor ))
                # print( 'elem2factor: {}'.format( elem2factor ))

                # print( 'elemnum.factDenominator: {}'.format( elemnum.factDenominator ))
                # print( 'elemsub.factDenominator: {}'.format( elemsub.factDenominator ))

                elemnum.factSign    = 1
                elemnum.factCounter = elem1factor + elem2factor
                # elemnum.onlyOneRoot = max( elem3.onlyOneRoot, elemsub.onlyOneRoot )
                elemnum.onlyOneRoot = min( elem3.onlyOneRoot, elemsub.onlyOneRoot )

                # print( "elemnum end: {}".format( elemnum ))
              else:
                elemnew.add( elemsub )

            # print( "elemnum add: {}".format( elemnum ))

            elemnew.add( elemnum )
            symExpr.elements[ iCnt ] = elemnew

            # print( 'special, elemnew : {}'.format( str( elemnew  )))

            del symExpr.elements[ iCnt2 ]
            lFound = True
            result = True
            break

          if ( elem1.power != 1 and elem2.power != 1 ):
            # 2 expression with powers
            elemnew = symexpress3.SymExpress( '*' )
            elemnew.add( symexpress3.SymNumber( 1, 2, 1, 1,1,1 ))
            elemnew.add( elem1 )

            symExpr.elements[ iCnt ] = elemnew

            del symExpr.elements[ iCnt2 ]
            lFound = True
            result = True
          elif ( elem1.power != 1 or elem2.power != 1 ):
            # 2 expression, 1 with power and 1 without
            if elem1.power == 1 :
              elemnew = elem1
            else:
              elemnew = elem2
            # search number in elemnew and increase it with 1
            for iCnt3 in range( elemnew.numElements()):
              elemsub = elemnew.elements[ iCnt3 ]
              if not isinstance( elemsub, symexpress3.SymNumber ):
                continue
              iNumAdd = elemsub.factDenominator

              iFactCount          = elemsub.factCounter * elemsub.factSign + iNumAdd
              elemsub.factSign    = 1
              elemsub.factCounter = iFactCount
              break

            symExpr.elements[ iCnt ] = elemnew

            del symExpr.elements[ iCnt2 ]
            lFound = True
            result = True
            break

          else:
            # 2 expression , same
            elemnew = symexpress3.SymExpress( '*' )
            elemnum = None

            # dVal1 = elem1.getValue()
            # dVal2 = elem2.getValue()

            # cElem1 = str( elem1 )
            # cElem2 = str( elem2 )

            # print( 'elem1: {} = {}'.format( str( elem1 ), dVal1 ))
            # print( 'elem2: {} = {}'.format( str( elem2 ), dVal2 ))
            # print( 'totaal: {}'.format( dVal1 + dVal2 ))

            elemexp = elem1
            # take all the numbers form elem2
            for iCnt3 in range( 0, elem2.numElements()):
              elemsub = elem2.elements[ iCnt3 ]
              if (isinstance( elemsub, symexpress3.SymNumber ) and elemsub.power == 1 ):
                if elemnum == None :
                  elemnum = elemsub
                  continue

                # print( 'elemnum: {}'.format( str( elemnum )))
                # print( 'elemsub: {}'.format( str( elemsub )))

                elem3 = symexpress3.SymNumber()
                elem3.factSign        = elemnum.factSign
                elem3.factCounter     = elemnum.factCounter
                elem3.factDenominator = elemnum.factDenominator
                elem3.onlyOneRoot     = elemnum.onlyOneRoot

                elemnum.factCounter     = elemnum.factCounter     * elemsub.factCounter
                elemnum.factDenominator = elemnum.factDenominator * elemsub.factDenominator

                elemnum.factSign = elem3.factSign * elemsub.factSign
                # elemnum.onlyOneRoot = max( elem3.onlyOneRoot, elemsub.onlyOneRoot )
                elemnum.onlyOneRoot = min( elem3.onlyOneRoot, elemsub.onlyOneRoot )

                # print( 'elemnnum new: {}'.format( str( elemnum )))

            # first expression had no number so it is 1
            if elemnum == None :
              elemnum = symexpress3.SymNumber( 1, 1, 1, 1, 1, 1)

            elemnew.onlyOneRoot      = elemexp.onlyOneRoot
            elemnew.powerSign        = elemexp.powerSign
            elemnew.powerCounter     = elemexp.powerCounter
            elemnew.powerDenominator = elemexp.powerDenominator

            # lFoundNum = False
            elemnum2  = None
            # elemexp is now the symexpress
            for iCnt3 in range( 0, elemexp.numElements()):
              elemsub = elemexp.elements[ iCnt3 ]

              if ( isinstance( elemsub, symexpress3.SymNumber ) and elemsub.power == 1 ):
                if elemnum2 == None :
                  elemnum2 = elemsub
                  continue

                elem3 = symexpress3.SymNumber()
                elem3.factSign        = elemnum2.factSign
                elem3.factCounter     = elemnum2.factCounter
                elem3.factDenominator = elemnum2.factDenominator
                elem3.onlyOneRoot     = elemnum2.onlyOneRoot

                elemnum2.factCounter     = elemnum2.factCounter     * elemsub.factCounter
                elemnum2.factDenominator = elemnum2.factDenominator * elemsub.factDenominator

                elemnum2.factSign    = elem3.factSign * elemsub.factSign
                # elemnum2.onlyOneRoot = max( elem3.onlyOneRoot, elemsub.onlyOneRoot )
                elemnum2.onlyOneRoot = min( elem3.onlyOneRoot, elemsub.onlyOneRoot )

              else:
                elemnew.add( elemsub )

            # second had no number so it is 1
            if elemnum2 == None:
              elemnum2 = symexpress3.SymNumber( 1, 1, 1, 1, 1, 1)

            elem3 = symexpress3.SymNumber()
            elem3.factSign        = elemnum.factSign
            elem3.factCounter     = elemnum.factCounter
            elem3.factDenominator = elemnum.factDenominator
            elem3.onlyOneRoot     = elemnum.onlyOneRoot

            elemnum.factCounter     *= elemnum2.factDenominator
            elemnum.factDenominator *= elemnum2.factDenominator

            elemnum2.factCounter     *= elem3.factDenominator
            elemnum2.factDenominator *= elem3.factDenominator

            elem1factor = elemnum.factSign  * elemnum.factCounter
            elem2factor = elemnum2.factSign * elemnum2.factCounter

            elemnum.factSign    = 1
            elemnum.factCounter = elem1factor + elem2factor
            # elemnum.onlyOneRoot = max( elem3.onlyOneRoot, elemsub.onlyOneRoot )
            elemnum.onlyOneRoot = min( elem3.onlyOneRoot, elemsub.onlyOneRoot )

            elemnew.add( elemnum )

            # if ( (dVal1 + dVal2) != elemnew.getValue() ):
            #   print( 'result: {} = {} = {} = {}  +  {}'.format( elemnew.getValue(), dVal1 + dVal2, str( elemnew ), cElem1, cElem2 ))

            symExpr.elements[ iCnt ] = elemnew

            del symExpr.elements[ iCnt2 ]
            lFound = True
            result = True
            break

        if lFound == True:
          break
    # print( 'add element end: {}'.format( str( symExpr )))
    # addAfter = str( symExpr )
    # if ( addBefore != addAfter ):
    #   dBefore = SymFormulaParser( addBefore ).getValue()
    #   dAfter  = SymFormulaParser( addAfter  ).getValue()
    #   if ( True or dAfter != dBefore ):
    #      print( "Before: {}, {}".format( dBefore, addBefore ))
    #      print( "After : {}, {}".format( dAfter , addAfter  ))
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


  symTest = symexpress3.SymFormulaParser( '2 + 3' )
  symTest.optimize()
  symOrg = symTest.copy()

  testClass = OptimizeAdd()
  testClass.optimize( symTest, "add" )

  _Check( testClass, symOrg, symTest, "5" )


  symTest = symexpress3.SymFormulaParser( 'a + a' )
  symTest.optimize()

  symOrg = symTest.copy()

  testClass = OptimizeAdd()
  testClass.optimize( symTest, "add" )

  _Check( testClass, symOrg, symTest, "2 * a" )


  symTest = symexpress3.SymFormulaParser( '(a * b) + (a * b)' )
  symTest.optimize()
  symOrg = symTest.copy()

  testClass = OptimizeAdd()
  testClass.optimize( symTest, "add" )

  _Check( testClass, symOrg, symTest, "a * b * 2" )


  symTest = symexpress3.SymFormulaParser( '1/5 + 1/3' )
  symTest.optimize()
  symOrg = symTest.copy()

  testClass = OptimizeAdd()
  testClass.optimize( symTest, "add" )

  _Check( testClass, symOrg, symTest, "(8/15)" )


  symTest = symexpress3.SymFormulaParser( '3^(1/2) + 3^^(1/2)' )
  symTest.optimize()
  symOrg = symTest.copy()

  testClass = OptimizeAdd()
  testClass.optimize( symTest, "add" )

  _Check( testClass, symOrg, symTest, "2 * 3^(1/2)" )


  symTest = symexpress3.SymFormulaParser( '2 a^^2 + 3 a^^2' )
  symTest.optimize()
  symOrg = symTest.copy()

  testClass = OptimizeAdd()
  testClass.optimize( symTest, "add" )

  _Check( testClass, symOrg, symTest, "a^^2 * 5" )


  symTest = symexpress3.SymFormulaParser( '2 - 3' )
  symTest.optimize()
  symTest.optimize( "multiply")
  symTest.optimize()

  symOrg = symTest.copy()

  testClass = OptimizeAdd()
  testClass.optimize( symTest, "add" )

  _Check( testClass, symOrg, symTest, "(-1)" )


  symTest = symexpress3.SymFormulaParser( '2 a - 3 a' )
  symTest.optimize()
  # symTest.optimize( "multiply")
  # symTest.optimize()
  symOrg = symTest.copy()

  testClass = OptimizeAdd()
  testClass.optimize( symTest, "add" )

  _Check( testClass, symOrg, symTest, "a * (-1)" )


if __name__ == '__main__':
  Test( True )
