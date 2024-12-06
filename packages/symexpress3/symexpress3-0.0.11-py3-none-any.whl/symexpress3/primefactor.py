#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Prime Factorization

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


    Module primfac and clones give sometimes error by installation.
    This is a python only implementation. Not that fast but it is python only

    based on:
    https://stackoverflow.com/questions/32871539/integer-Factorization-in-python
    https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm

"""

from math      import gcd
from math      import sqrt
from threading import Thread
from queue     import Queue
from functools import reduce

import sympy   # use it for prime factorization and divisors
# TODO seek out, use sympy always and delete own implementation
# https://stackoverflow.com/questions/4643647/fast-prime-factorization-module


globalCachePrimeFactors = {}
globalCacheAllFactors   = {}

#
# only factor positive odd numbers
#
def FactorizationOddThread(n, resultQueue = None):
  """
  Factorization odd number with threads
  """
  factors = []

  def GetFactor( n, x, q ):
    xFixed    = 2
    cycleSize = 2
    # x = 2
    factor    = 1

    while factor == 1:
      for _ in range(cycleSize):
        if factor > 1:
          break
        x = (x * x + 1) % n
        factor = gcd(x - xFixed, n)

      cycleSize *= 2
      xFixed = x

    q.put( factor )
    return factor

  # change this into threads ??
  if n > 1:
    q1 = Queue()
    q2 = Queue()
    q3 = Queue()
    q4 = Queue()

    t1 = Thread(target=GetFactor, args=(n , 2 ,q1,))
    t2 = Thread(target=GetFactor, args=(n , 3 ,q2,))
    t3 = Thread(target=GetFactor, args=(n , 4 ,q3,))
    t4 = Thread(target=GetFactor, args=(n , 5 ,q4,))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    next1 = q1.get()
    next2 = q2.get()
    next3 = q3.get()
    next4 = q4.get()

    nextVal = min( next1, next2, next3, next4 )

    # next = GetFactor(n)
    if nextVal > 1:
      if nextVal == n :
        factors.append(nextVal)
      else:
        n //= nextVal

        q1 = Queue()
        q2 = Queue()

        t1 = Thread(target=FactorizationOddThread, args=(nextVal,q1,))
        t2 = Thread(target=FactorizationOddThread, args=(n      ,q2,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        factors += q1.get() + q2.get()

  if resultQueue != None:
    resultQueue.put(factors)

  return factors


#
# only factor positive odd numbers
#
def FactorizationOdd(n):
  """
  Factorization odd number (no threads)
  """

  factors = []

  def GetFactor(n):
    xFixed    = 2
    cycleSize = 2
    x         = 2
    factor    = 1
    startX    = 2

    # print( "get factor: " + str( n ))
    while factor == 1:
      for _ in range(cycleSize):
        if factor > 1:
          break
        x = (x * x + 1) % n
        factor = gcd(x - xFixed, n)

      if factor == n :
        if startX > 5:
          break
        # print( "factor: " + str( factor ) + " n: " + str( n ) + " startX: " + str( startX ))
        xFixed = 2
        startX += 1
        x = startX
        factor = 1
        continue

      cycleSize *= 2
      xFixed = x

    # print( "found factor: " + str( factor ))
    return factor

  # change this into threads ??
  while n > 1:
    nextVal = GetFactor(n)
    factors.append(nextVal)
    n //= nextVal

  numFactors = len( factors )
  if numFactors <= 1:
    # print( "found factor: " + str( factors ))
    return factors

  newFactors = []
  for numFact in factors:
    # threads ???
    # print( "Check factor: " + str( numFact ))
    newFactors += FactorizationOdd( numFact )

  return newFactors

#
# factor all (positive) numbers
# give back: array of integers (factors)
#
def Factorization(n):
  """
  Factorization of given number, give array of integer back
  """
  # print( f"Factorization: {n}" )
  if n <= 1 :
    return []

  factors = []

  # div by 2, 3 and 5 for speed start
  modRest = n % 2
  while modRest == 0:
    factors.append( 2 )
    n //= 2
    modRest = n % 2

  modRest = n % 3
  while modRest == 0:
    factors.append( 3 )
    n //= 3
    modRest = n % 3

  modRest = n % 5
  while modRest == 0:
    factors.append( 5 )
    n //= 5
    modRest = n % 5

  return factors + FactorizationOddThread( n )
  # return factors + FactorizationOdd( n )

#
# factor all positive numbers
# give back dictionary  { number: count }
def FactorizationDict(n):
  """
  Factorization given number, give dictionary back ( number: count )
  """
  # global globalCachePrimeFactors

  # print( f"FactorizationDict n: {n}")

  if n in globalCachePrimeFactors:
    # print( f"FactorizationDict cache used")
    return globalCachePrimeFactors[ n ].copy()
    # pass

  # print( f"FactorizationDict: {n}" )

  factorDict = sympy.ntheory.factorint( n )

  # pylint: disable=pointless-string-statement)
  """
  factors = Factorization( n )

  factorDict = {}
  for numFact in factors:
    if numFact in factorDict :
      factorDict[ numFact ] += 1
    else:
      factorDict[ numFact ] = 1
  """
  globalCachePrimeFactors[ n ] = factorDict.copy()

  # print( f"FactorizationDict done: {n}" )

  return factorDict

#
# Same function name as primefac used for Factorization
# Give back a dictionary { number: count }
#
def factorint(n):  # pylint: disable=invalid-name
  """
  Factorization of given number, give a dictionary back ( number: count )
  Is equal to primefac
  """
  return FactorizationDict(n)

# https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
def FactorsAll(n):
  """
  Get all the factors of a given n`
  """
  step = 2 if n%2 else 1
  return set(reduce(list.__add__, ([i, n//i] for i in range(1, int(sqrt(n))+1, step) if n % i == 0)))

# get all the factors of the given n`
def FactorAllInt( n ):
  """
  Get all the factors of a given n with caching
  """
  # global globalCacheAllFactors

  if n in globalCacheAllFactors:
    return globalCacheAllFactors[ n ].copy()

  # print( f"FactorAllInt: {n}" )

  factors = sympy.divisors( n )

  # print( "factors: {factors}" )

  # factors = FactorsAll( n )

  globalCacheAllFactors[ n ] = factors.copy()

  # print( f"FactorAllInt done: {n}" )

  return factors




# print(Factorization(41612032092113))
# print(FactorizationOddThread(4161203209211377777))
# print(FactorizationOdd(4161203209211377777))
# print(FactorizationOddThread(416120320921137777799999))
# 169 = 13 * 13
# print(Factorization(          78125 ))
# print(FactorizationOddThread( 78125 ))
# print(Factorization(169))
# print(Factorization(125))


# print( FactorizationDict( 845))
# print( FactorizationDict( 75))
