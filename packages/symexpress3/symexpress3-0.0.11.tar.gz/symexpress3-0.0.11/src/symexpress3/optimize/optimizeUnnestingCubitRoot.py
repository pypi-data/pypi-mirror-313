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
from symexpress3          import primefactor

globalCacheCubicRoot = {}

# import sys
# sys.stderr.write( f"Start cubic root\n" )


class OptimizeUnnestingCubitRoot( optimizeBase.OptimizeBase ):
  """
  Unnesting of cubic roots of format (a * b^^(1/2) + c)^^(1/3)
  \n a, b and c are numbers, a can also be an imaginair number (a * i)
  """
  def __init__( self ):
    super().__init__()
    self._name         = "unnestingCubicRoot"
    self._symtype      = "+"
    self._desc         = "Unnesting of cubic roots of format (a * b^^(1/2) + c)^^(1/3)"

  def optimize( self, symExpr, action ):
    result = False

    if self.checkExpression( symExpr, action ) != True:
      return result

    if symExpr.onlyOneRoot != 1:
      return result

    if symExpr.powerDenominator != 3:
      return result

    if symExpr.numElements() != 2:
      return result

    # return False

    # print( "Start 3" )

    # cubic root with only 2 elements
    # 1 must be a number
    # the other a sqrt root or an express with only a sqrt root
    # it can only have max 3 elements, number, variable (only i supported) and a sqrt root of a number
    #
    # (a+b)^^3
    # a^^3 + b * a^^2 * 3 + b^^2 * a * 3 + b^^3
    #
    # root part   = a^^3 + 3 * b^^2 * a
    # number part = 3 * a^^2 * b + b^^3 -> b ( 3 a^^2 + b^^2 ) -> b is always a factor of number part
    #
    elem1 = symExpr.elements[ 0 ]
    elem2 = symExpr.elements[ 1 ]

    numberPart = None
    rootPart   = None

    if isinstance( elem1, symexpress3.SymNumber ) and elem1.powerCounter == 1 and elem1.powerDenominator == 1:
      # ok found the number
      numberPart = elem1
      rootPart   = elem2
    elif isinstance( elem2, symexpress3.SymNumber ) and elem2.powerCounter == 1 and elem2.powerDenominator == 1:
      numberPart = elem2
      rootPart   = elem1
    else:
      return result

    # print( "Numberpart found: " + str( numberPart ))

    if isinstance( rootPart, symexpress3.SymNumber ) :
      if rootPart.powerDenominator != 2:
        return result
      if rootPart.onlyOneRoot != 1:
        return result
    elif isinstance( rootPart, symexpress3.SymExpress ):
      if rootPart.power != 1:
        return result

      if rootPart.onlyOneRoot != 1:
        return result

      foundSqrt     = False
      foundNumber   = False
      foundVariable = False
      # need:
      # - number       optional
      # - variable (i) optional
      # - sqrt         mandatory
      for elem in rootPart.elements:

        # print( "Check: " + str( elem ))

        if isinstance( elem, symexpress3.SymNumber ):
          if elem.powerDenominator == 2:
            if foundSqrt == True:
              return result # only 1 sqrt supported

            if elem.powerCounter != 1:
              return result # wanted a sqrt

            if elem.onlyOneRoot != 1:
              return result

            foundSqrt = True
          else:
            if elem.power != 1:
              return result # only 1 power supported

            if foundNumber == True:
              return result # only 1 number supported

            foundNumber = True
        elif isinstance( elem, symexpress3.SymVariable ):
          if foundVariable == True:
            return result # only 1 variable supported

          if elem.name != 'i':
            return result # only i supported

          foundVariable = True
        else:
          return result

      # need sqrt
      # print(" check sqrt: " + str(foundSqrt ) )
      if foundSqrt == False:
        return result
    else:
      return result

    # on this point
    # rootPart   = valid sqrt expression
    # numberPart = valid number

    # print( "Valid rootpart: " + str( rootPart ))

    keyCache = str( symExpr )
    if keyCache in globalCacheCubicRoot:
      keyData = globalCacheCubicRoot[ keyCache ]
      if keyData == None:
        return False

      symExpr.powerDenominator = 1
      symExpr.symType = "+"
      symExpr.elements = []

      symExpr.add( keyData[ 'symRotate' ] )

      # symExpr.add( keyData[ 'exprFndB' ] )
      # symExpr.add( keyData[ 'exprFndA' ] )

      return True

    # sys.stderr.write( f"cubic root: {keyCache}\n" )
    #
    # need al the factors
    factorCounter     = primefactor.FactorAllInt( numberPart.factCounter     )
    factorDenominator = primefactor.FactorAllInt( numberPart.factDenominator )

    # TODO check (reason) why 2 must always in the denominator
    # we can handle quations by whole numbers, work out how the handle it

    if not 2 in factorDenominator:
      factorDenominator.append( 2 )

    if not 3 in factorDenominator:
      factorDenominator.append( 3 )

    if not 6 in factorDenominator:
      factorDenominator.append( 6 )


    # print( f"factorCounter: {factorCounter}" )
    # print( f"factorDenominator: {factorDenominator}" )

    # factorCounter     cannot exceed numberPart^^(1/3)  -> not for imaginair numbers = negative number
    # factorDenominator cannot exceed numberPart^^(1/3)  -> not for imaginair numbers = negative number

    if foundVariable == False:
      # no i variable, so no negative a^^2
      # not ** (1. / 3) used, but /2 insteed. /3 give a to small number
      maxValue = int( round( numberPart.factCounter ** (1. / 2), 0 ))
      factorCounter = [ x for x in factorCounter if x <= maxValue]

      # maxValue = int( round( numberPart.factDenominator ** (1. / 3), 0 ))
      # factorDenominator = [ x for x in factorDenominator if x <= maxValue]


    # root part   = a^^3 + 3 * b^^2 * a
    # number part = 3 * a^^2 * b + b^^3 -> b ( 3 a^^2 + b^^2 ) -> b is always a factor of number part

    # root part = a^^2 * a + 3 b^^2 * a
    # a = x sqrt(y)
    # x^2 * y * x * sqrt(y) + 3 b^^2 * x sqrt(y)
    # root part = x^2 * y * x * sqrt(y) + 3 b^^2 * x sqrt(y)
    # root part hole = x^3 * y + 3  b^^2
    # root part hole = x^^3 * y + 3 b^^2


    # need expression for a
    # 3 * a^^2 * b + b^^3 = numberPart
    # numberPart - b^^3 = 3 a^^2 * b
    # (numberPart - b^^3) / ( 3 b ) = a^^2
    # a = ( (numberPart - b^^3) / ( 3 b ))^^(1/2)

    # rootPart   = a^^3 + 3 * b^^2 * a
    # 0 = a^^3 + 3 * b^^2 * a - rootPart
    # fill in a, b and rootPart and check on 0
    #
    strA     = "( ((" + str( numberPart ) + ") - (bs * b^^3)) / ( 3 * bs * b ))^^(1/2)"
    expressA = symexpress3.SymFormulaParser( strA )
    expressA.optimizeNormal()

    strCheck     = "a^^3 + 3 * b^^2 * a - " + str( rootPart )
    expressCheck = symexpress3.SymFormulaParser( strCheck )
    expressCheck.optimizeNormal()

    # strA = sqrt() it can be + and -
    strCheck2     = "a^^3 + 3 * b^^2 * a + " + str( rootPart )
    expressCheck2 = symexpress3.SymFormulaParser( strCheck2 )
    expressCheck2.optimizeNormal()


    # print( f"strA        : {strA}" )
    # print( f"expressA    : {expressA}" )
    # print( f"expressCheck: {expressCheck}" )


    # no walk all the factorCounter and factDenominator
    # check on + and - if theck gives 0 (zero)
    #
    exprFndA = None
    exprFndB = None

    # big numbers before small numbers
    factorDenominator.sort()           # smallest denominator first
    factorCounter.sort( reverse=True ) # greatest counter first

    # print( f"factorCounter    : {factorCounter}" )
    # print( f"factorDenominator: {factorDenominator}" )

    for facSign in range( 0, 2 ): # principal root, positive before negative
      for facDenom in factorDenominator:  # big numbers before small
        for facNum in factorCounter:

          # if facNum != 5:
          #    continue
          # if facDenom != 1:
          #   continue
          # if facSign == 1:
          #   continue

          factor = str( facNum ) + "/" + str( facDenom )
          fsign  = "1"
          if facSign == 1:
            fsign = "-1"
            # factor = '-' + factor

          # print( f"Check factor: {factor} sign: {fsign}" )

          copyA = expressA.copy()
          dictVar = {}
          dictVar[ 'b'  ] = factor
          dictVar[ 'bs' ] = fsign

          # print( f"before copyA: {copyA} " )

          copyA.replaceVariable( dictVar )
          # print( f"after copyA: {copyA} " )
          copyA.optimizeNormal()
          # print( f"optimized copyA: {copyA} " )

          # print( f"CopyA: {copyA} " )

          copyCheck = expressCheck.copy()
          # print( f"copyCheck: { str(copyCheck)}" )
          dictVar[ 'a' ] = str( copyA )
          copyCheck.replaceVariable( dictVar )

          # print( f"before copyCheck: {copyCheck} " )

          copyCheck.optimizeNormal()

          # print( f"after copyCheck: {copyCheck} " )
          # print( f"value copyCheck: {copyCheck.getValue()} " )

          if foundVariable == True and str( copyCheck ) != "0":
            # print( "Use negRootToI" )
            copyCheck.optimize( "negRootToI" )
            copyCheck.optimizeNormal()
            # print( f"After negRootToI: {copyCheck}" )

          # check the negative a
          if str( copyCheck ) != "0": # and foundVariable == False:
            # print( f"Neg check" )
            copyCheck = expressCheck2.copy()
            dictVar[ 'a' ] = str( copyA )
            copyCheck.replaceVariable( dictVar )
            copyCheck.optimizeNormal()
            # print( f"heg check copy: {copyCheck}" )
            if foundVariable == True and str( copyCheck ) != "0":
              copyCheck.optimize( "negRootToI" )
              copyCheck.optimizeNormal()
              # print( f"heg check 2 copy: {copyCheck}" )

            if str( copyCheck ) == "0":
              addNeg = symexpress3.SymExpress( '*' )
              addNeg.add( symexpress3.SymNumber( -1, 1, 1, 1, 1, 1, 1 ) )
              addNeg.add( copyA )
              copyA = addNeg


          if str( copyCheck ) == "0":
            # print( "Jippie found" )
            result = True

            exprFndA = copyA
            exprFndB = symexpress3.SymFormulaParser( fsign + ' * ' + factor )

          if result == True:
            break
        if result == True:
          break
      if result == True:
        break

    if result == True:
      # sometime the wrong root is determined (not principal)
      # safety check

      # add extra layer for rotate
      symCheck = symExpr.copy()
      symCheck.powerDenominator = 1
      symCheck.symType = "+"
      symCheck.elements = []

      symRotate = symexpress3.SymExpress( '*' )
      symPlus   = symexpress3.SymExpress( '+' )

      symPlus.add( exprFndB )
      symPlus.add( exprFndA )

      symRotate.add( symPlus )

      symCheck.elements = []
      symCheck.add( symRotate )

      valueCheck = symCheck.getValue()
      valueOrg   = symExpr.getValue()

      if isinstance( valueCheck, complex ):
        valueCheck = valueCheck.real

      if isinstance( valueOrg, complex ):
        valueOrg = valueOrg.real

      if round( valueCheck, 10 ) != round( valueOrg, 10 ):
        # ok, not the principal, take the next root
        # print( f"keyCache: {keyCache}" )
        # print( f"valueCheck: {valueCheck}, valueOrg: {valueOrg}" )

        # rotate: ( -1 + i (3)^^(1/2) ) / 2
        # rotate 2 times max to find the principal
        #

        # 1e rotate
        symRotate.add( symexpress3.SymFormulaParser( "(( -1 + i (3)^^(1/2) ) / 2)" ))

        symCheck.elements = []
        symCheck.add( symRotate )

        valueCheck = symCheck.getValue()
        # valueOrg   = symExpr.getValue()

        if isinstance( valueCheck, complex ):
          valueCheck = valueCheck.real

        # if isinstance( valueOrg, complex ):
        #   valueOrg = valueOrg.real

        if round( valueCheck, 10 ) != round( valueOrg, 10 ):

          # 2e rotate
          symRotate.add( symexpress3.SymFormulaParser( "(( -1 + i (3)^^(1/2) ) / 2)" ))

          symCheck.elements = []
          symCheck.add( symRotate )

          valueCheck = symCheck.getValue()
          # valueOrg   = symExpr.getValue()

          if isinstance( valueCheck, complex ):
            valueCheck = valueCheck.real

          # if isinstance( valueOrg, complex ):
          #   valueOrg = valueOrg.real

          if round( valueCheck, 10 ) != round( valueOrg, 10 ):

            globalCacheCubicRoot[ keyCache ] = None
            return False

      symExpr.powerDenominator = 1
      symExpr.symType = "+"
      symExpr.elements = []

      symExpr.add( symRotate )

      # symExpr.add( exprFndB )
      # symExpr.add( exprFndA )

      keyData = {}
      # keyData[ 'exprFndB'  ] = exprFndB
      # keyData[ 'exprFndA'  ] = exprFndA
      keyData[ 'symRotate' ] = symRotate

      globalCacheCubicRoot[ keyCache ] = keyData
    else:
      globalCacheCubicRoot[ keyCache ] = None

    # sys.stderr.write( f"cubic root END: {keyCache}\n" )

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
      raise NameError( f'optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symOrg )}, wanted: {wanted}' )

  # ((55/1369) * 37^^(1/2) + i * (126/1369) * 111^^(1/2))^^(1/3)
  # answer: (47/74 + (33 i 3^^(1/2))/74 )^^(1/2)

  # (1/9 + 1/11 17^^(1/2))^^3  = (1/3) * ((4252/3267) + (580/1331) * 17^^(1/2))^^(1/3)
  symTest = symexpress3.SymFormulaParser( '((4252/3267) + (580/1331) * 17^^(1/2))^^(1/3)' )
  symTest.optimizeNormal()
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeUnnestingCubitRoot()
  testClass.optimize( symTest, "unnestingCubicRoot" )

  _Check( testClass, symOrg, symTest, "(1 * 1 * 3^^-1 + (3/11) * 17^^(1/2))" )


  # ( 7 + 11 i 31^^(1/2))^^3 -> is not the principal root
  symTest = symexpress3.SymFormulaParser( '( -78428 + i * 31^^(1/2) * (-39644) )^^(1/3)' )
  symTest.optimizeNormal()
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeUnnestingCubitRoot()
  testClass.optimize( symTest, "unnestingCubicRoot" )

  _Check( testClass, symOrg, symTest, "(1 * 7 * 1^^-1 + 11 * 31^^(1/2) * i) * ((-1) + i * (3)^^(1/2)) * 2^^-1 * ((-1) + i * (3)^^(1/2)) * 2^^-1" )


  # ((-126) * i * 3^^(1/2) + (-55))^^(1/3)
  # answer is (principal)           : 5 - 2 i 3^^(1/2)
  # but other can be (not principal): (1/2) + i * (7/2) * 3^^(1/2)
  symTest = symexpress3.SymFormulaParser( '((-126) * i * 3^^(1/2) + (-55))^^(1/3)' )
  symTest.optimizeNormal()
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeUnnestingCubitRoot()
  testClass.optimize( symTest, "unnestingCubicRoot" )

  _Check( testClass, symOrg, symTest, "(1 * 5 * 1^^-1 + (-1) * 2 * 3^^(1/2) * i)" )


  #  (80960 + (-1499) * 2917^^(1/2))^^(1/3)
  # = 1/2 * (55 - 2917^^(1/2))
  symTest = symexpress3.SymFormulaParser( '(80960 + (-1499) * 2917^^(1/2))^^(1/3)' )
  symTest.optimizeNormal()
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeUnnestingCubitRoot()
  testClass.optimize( symTest, "unnestingCubicRoot" )

  _Check( testClass, symOrg, symTest, "(1 * 55 * 2^^-1 + (-1) * (1/2) * 2917^^(1/2))" )


  symTest = symexpress3.SymFormulaParser( '(6 * 3^^(1/2) - 10)^^(1/3)' )
  symTest.optimizeNormal()
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeUnnestingCubitRoot()
  testClass.optimize( symTest, "unnestingCubicRoot" )

  _Check( testClass, symOrg, symTest, "((-1) * 1 * 1^^-1 + 3^^(1/2))" )


  symTest = symexpress3.SymFormulaParser( '(170 + 78 * 3^^(1/2))^^(1/3)' )
  symTest.optimizeNormal()
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeUnnestingCubitRoot()
  testClass.optimize( symTest, "unnestingCubicRoot" )

  _Check( testClass, symOrg, symTest, "(1 * 5 * 1^^-1 + 3^^(1/2))" )


  # (3 + 2 i 5^^(1/2))^^3
  symTest = symexpress3.SymFormulaParser( '((-153) + i * 5^^(1/2) * 14 )^^(1/3)' )
  symTest.optimizeNormal()
  symTest = symTest.elements[ 0 ]
  symOrg = symTest.copy()

  testClass = OptimizeUnnestingCubitRoot()
  testClass.optimize( symTest, "unnestingCubicRoot" )

  _Check( testClass, symOrg, symTest, "(1 * 3 * 1^^-1 + 2 * 5^^(1/2) * i)" )





if __name__ == '__main__':
  Test( True )
