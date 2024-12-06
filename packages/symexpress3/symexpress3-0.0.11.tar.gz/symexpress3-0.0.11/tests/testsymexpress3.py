#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Test Symbolic expression 3

    Copyright (C) 2021 Gien van den Enden - swvandenenden@gmail.com

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

import sys

from datetime import datetime

# pylint: disable=consider-using-from-import
import symexpress3
import symexpress3.symfunc.symRegisterFunctions             as symRegisterFunctions
import symexpress3.optimize.symRegisterOptimize             as symRegisterOptimize
import symexpress3.optSymNumber.symRegisterOptSymNumber     as symRegisterOptSymNumber
import symexpress3.optSymVariable.symRegisterOptSymVariable as symRegisterOptSymVariable
import symexpress3.optSymFunction.symRegisterOptSymFunction as symRegisterOptSymFunction
import symexpress3.optSymAny.symRegisterOptSymAny           as symRegisterOptSymAny

testData = [ # 1
             { 'expression' : 'x x'
             , 'result'     : 'x^2'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 2
             { 'expression' : 'x^2 * 3 + 2'
             , 'result'     : '3x^2 + 2'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 3
             { 'expression' : '(4+2^4 + (2/3)^3) + y ( 1 + 3 i x)^2'
             , 'result'     : '548/27 + y + 6y i x - 9 y x^2'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 4
             { 'expression' : '(x + 1)^-3'
             , 'result'     : '(x^3+3x^2+3x+ 1)^-1'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 5
             { 'expression' : '(x + i)^7'
             , 'result'     : 'x^7 + 7i x^6 - 21 x^5 - 35 i x^4 + 35 x^3 + 21 i x^2 - 7 x - i'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 6
             { 'expression' : '( 1 / x + 1)^7'
             , 'result'     : 'x^-7 + 7 x^-6 + 21 x^-5 + 35 x^-4 + 35 x^-3 + 21 x^-2  + 7 x^-1 + 1'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 7
             { 'expression' : '2(x+2)^3+2^5'
             , 'result'     : '2 (x^3 + 6x^2 + 12x + 8) + 32'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 8
             { 'expression' : '2 x^2 * x i + 2 x * x i * x + 4 x * x i * x i'
             , 'result'     : '4 i x^3 -4x^3'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 9
             { 'expression' : '(a + b i )^(1/3) * (a + b i )^3 + 1 / ( (a + b i )^3 )'
             , 'result'     : '(a + b i)^(1/3) (a^3 + 3 a^2 b i - 3 a b^2 - b^3 i) + (a^3 + 3 a^2 b i - 3 a b^2 - b^3 i)^-1'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 10
             { 'expression' : 'x + 2x + 3^-1 + y + y + 3y + 3 + 4'
             , 'result'     : '3x+22/3+5y'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 11
             { 'expression' : '(a+b)^(1/2) + (b+a)^(1/2)'
             , 'result'     : '2(a + b)^(1/2)'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 12
             { 'expression' : '(a+b)^(1/2) + 2(b+a)^(1/2)'
             , 'result'     : '3(a + b)^(1/2)'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 13
             { 'expression' : '3(a+b)^(1/2) + (b+a)^(1/2)'
             , 'result'     : '4(a + b)^(1/2)'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 14
             { 'expression' : '3/5(a+b)^(1/2) + 2(b+a)^(1/2)'
             , 'result'     : '13/5(a + b)^(1/2)'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 15
             { 'expression' : '(a+b)^(1/2) + (b+a+1)^(1/2)'
             , 'result'     : '(a+b)^(1/2) + (b+a+1)^(1/2)'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 16
             { 'expression' : '(b+a+1)^(1/2) + (a+b)^(1/2)'
             , 'result'     : '(a+b)^(1/2) + (b+a+1)^(1/2)'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 17
             { 'expression' : '3 + a + a + b + 2'
             , 'result'     : '2a+b+5'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 18
             { 'expression' : '(2x+3i)^3'
             , 'result'     : '8x^3 + 36 i x^2 -54x-27i'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 19
             { 'expression' : '1 / ( (a + b i )^3 )'
             , 'result'     : '1/(a^3 + 3 i a^2 b - 3 a b^2 - b^3 * i)'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 20
             { 'expression' : '10(a + 2b)'
             , 'result'     : '10a+20b'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 21
             { 'expression' : '10 + 2 5^^(1/2)'
             , 'result'     : '2 5^^(1/2) + 10'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 22
             { 'expression' : '5^^(1/2)+5^^(1/2)'
             , 'result'     : '2 5^^(1/2)'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 23
             { 'expression' : '5^^(1/2)+2 * 5^^(1/2)'
             , 'result'     : '3 5^^(1/2)'
             , 'actions'    : [ 'optimizeNormal' ]
             }

           , # 24
             { 'expression' : '3^(1/2)'
             # , 'result'     : '3^^(1/2)[-1|1]'
             , 'result'     : '[ 3^^(1/2) | 3^^(1/2) * (-1) ]'
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 25
             { 'expression' : '(25 * 5 * 5 * 5 )^(1/5)'
             # , 'result'     : '[ (5/4) * i * (10 + 2 * 5^^(1/2))^^(1/2) + (5/4) * 5^^(1/2) + (-5/4) | (5/4) * i * (10 + (-2) * 5^^(1/2))^^(1/2) + (-5/4) + (-5/4) * 5^^(1/2) | (-5/4) * i * (10 + (-2) * 5^^(1/2))^^(1/2) + (-5/4) + (-5/4) * 5^^(1/2) | (-5/4) * i * (10 + 2 * 5^^(1/2))^^(1/2) + (5/4) * 5^^(1/2) + (-5/4) | 5 ]'
             # , 'result'     : '[ (5/4) * 5^^(1/2) + (-5/4) + (5/4) * i * (5 + 2 * 5^^(1/2))^^(1/2) + (5/4) * i * (5 + (-2) * 5^^(1/2))^^(1/2) | (-5/4) + (-5/4) * 5^^(1/2) + (5/4) * i * (5 + 2 * 5^^(1/2))^^(1/2) + (-5/4) * i * (5 + (-2) * 5^^(1/2))^^(1/2) | (-5/4) + (-5/4) * 5^^(1/2) + (-5/4) * i * (5 + 2 * 5^^(1/2))^^(1/2) + (5/4) * i * (5 + (-2) * 5^^(1/2))^^(1/2) | (5/4) * 5^^(1/2) + (-5/4) + (-5/4) * i * (5 + 2 * 5^^(1/2))^^(1/2) + (-5/4) * i * (5 + (-2) * 5^^(1/2))^^(1/2) | 5 ]'
             # , 'result'     : '[ (5/4) * i * (10 + 2 * 5^^(1/2))^^(1/2) + (5/4) * 5^^(1/2) + (-5/4) | (5/4) * i * (10 + (-2) * 5^^(1/2))^^(1/2) + (-5/4) + (-5/4) * 5^^(1/2) | (-5/4) * i * (10 + (-2) * 5^^(1/2))^^(1/2) + (-5/4) + (-5/4) * 5^^(1/2) | (-5/4) * i * (10 + 2 * 5^^(1/2))^^(1/2) + (5/4) * 5^^(1/2) + (-5/4) | 5 ] '
             # , 'result'     : '[ (5/4) * 5^^(1/2) + (-5/4) + (5/4) * i * (5 + 2 * 5^^(1/2))^^(1/2) + (5/4) * i * (5 + (-2) * 5^^(1/2))^^(1/2) | (-5/4) + (-5/4) * 5^^(1/2) + (5/4) * i * (5 + 2 * 5^^(1/2))^^(1/2) + (-5/4) * i * (5 + (-2) * 5^^(1/2))^^(1/2) | (-5/4) + (-5/4) * 5^^(1/2) + (-5/4) * i * (5 + 2 * 5^^(1/2))^^(1/2) + (5/4) * i * (5 + (-2) * 5^^(1/2))^^(1/2) | (5/4) * 5^^(1/2) + (-5/4) + (-5/4) * i * (5 + 2 * 5^^(1/2))^^(1/2) + (-5/4) * i * (5 + (-2) * 5^^(1/2))^^(1/2) | 5 ] '
             , 'result'     : '[ 5 | (5/4) * i * (10 + 2 * 5^^(1/2))^^(1/2) + (5/4) * 5^^(1/2) + (-5/4) | (5/4) * i * (10 + (-2) * 5^^(1/2))^^(1/2) + (-5/4) + (-5/4) * 5^^(1/2) | (-5/4) * i * (10 + (-2) * 5^^(1/2))^^(1/2) + (-5/4) + (-5/4) * 5^^(1/2) | (-5/4) * i * (10 + 2 * 5^^(1/2))^^(1/2) + (5/4) * 5^^(1/2) + (-5/4) ]'
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 26
             { 'expression' : '(-25 * 3 )^(1/2) + (3)^(1/2)'
             # , 'result'     : '3^^(1/2) * [ -5 i | 5 i ] + 3^^(1/2) * [ -1 | 1 ]'
             # , 'result'     : 'i * 3^^(1/2) * [ (-5) | 5 ] + 3^^(1/2) * [ (-1) | 1 ] '
             # , 'result'       : '[ i * 5 * 3^^(1/2) | (-5) * i * 3^^(1/2) ] + [ 3^^(1/2) | 3^^(1/2) * (-1) ]'
             # , 'result'     : '[ [ i * 5 * 3^^(1/2) + 3^^(1/2) | i * 5 * 3^^(1/2) + 3^^(1/2) * (-1) ] | [ (-5) * i * 3^^(1/2) + 3^^(1/2) | (-5) * i * 3^^(1/2) + 3^^(1/2) * (-1) ] ]'
             , 'result'     : '[ i * 5 * 3^^(1/2) + 3^^(1/2) | i * 5 * 3^^(1/2) + 3^^(1/2) * (-1) | (-5) * i * 3^^(1/2) + 3^^(1/2) | (-5) * i * 3^^(1/2) + 3^^(1/2) * (-1) ]'
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 27 test TODO
             # { 'expression' : '(-16)^(1/2) + (-27)^(1/3) + (-16)^(1/4) + (-1 * 5^5)^(1/5) + (-1 * 5^6)^(1/6)+ (5^7)^(1/7) + (5^8)^(1/8) + (5^9)^(1/9) + (3)^(1/2)'
             { 'expression' : '1'
             # , 'result'     : '[ -4 i | 4 i ] + [ -3 | 3/2 -3/2 i 3^^(1/2) | 3/2 + 3/2 i 3^^(1/2) ] + [ -1 2^^(1/2) + i * 2^^(1/2) | (-1) * 2^^(1/2) + (-1) * i * 2^^(1/2) | 2^^(1/2) + (-1) * i * 2^^(1/2) | 2^^(1/2) + i * 2^^(1/2) ] + [ (-5/4) * 5^^(1/2) + (5/4) * i * (10 + 2 * 5^^(1/2))^^(1/2) | (-5) | (-5/4) * 5^^(1/2) + (-5/4) * i * (10 + 2 * 5^^(1/2))^^(1/2) | (-5/4) * i * (10 + (-2) * 5^^(1/2))^^(1/2) + (5/4) + (5/4) * 5^^(1/2) | (5/4) * i * (10 + (-2) * 5^^(1/2))^^(1/2) + (5/4) + (5/4) * 5^^(1/2) ] + [ 5 * i | (-5/2) * 3^^(1/2) + (5/2) * i | (-5/2) * 3^^(1/2) + (-5/2) * i | (-5) * i | (5/2) * 3^^(1/2) + (-5/2) * i | (5/2) * 3^^(1/2) + (5/2) * i ] + [ 5 *  cos( (2/7) * pi ) + 5 * i *  sin( (2/7) * pi ) | 5 *  cos( pi * (4/7) ) + 5 * i *  sin( pi * (4/7) ) | 5 *  cos( pi * (6/7) ) + 5 * i *  sin( pi * (6/7) ) | 5 *  cos( pi * (8/7) ) + 5 * i *  sin( pi * (8/7) ) | 5 *  cos( pi * (10/7) ) + 5 * i *  sin( pi * (10/7) ) | 5 *  cos( pi * (12/7) ) + 5 * i *  sin( pi * (12/7) ) | 5 ] + [ (5/2) * 2^^(1/2) + (5/2) * i * 2^^(1/2) | 5 * i | (-5/2) * 2^^(1/2) + (5/2) * i * 2^^(1/2) | (-5) | (-5/2) * 2^^(1/2) + (-5/2) * i * 2^^(1/2) | (-5) * i | (5/2) * 2^^(1/2) + (-5/2) * i * 2^^(1/2) | 5 ] + [ 5 *  cos( (2/9) * pi ) + 5 * i *  sin( (2/9) * pi ) | 5 *  cos( pi * (4/9) ) + 5 * i *  sin( pi * (4/9) ) | (-5/2) + (5/2) * i * 3^^(1/2) | 5 *  cos( pi * (8/9) ) + 5 * i *  sin( pi * (8/9) ) | 5 *  cos( pi * (10/9) ) + 5 * i *  sin( pi * (10/9) ) | (-5/2) + (-5/2) * i * 3^^(1/2) | 5 *  cos( pi * (14/9) ) + 5 * i *  sin( pi * (14/9) ) | 5 *  cos( pi * (16/9) ) + 5 * i *  sin( pi * (16/9) ) | 5 ] + 3^^(1/2) * [ (-1) | 1 ]'
             # , 'result'     : '[ (-4) * i | 4 * i ] + [ (-3) | (3/2) + (-3/2) * i * 3^^(1/2) | (3/2) + (3/2) * i * 3^^(1/2) ] + [ (-1) * 2^^(1/2) + i * 2^^(1/2) | (-1) * 2^^(1/2) + (-1) * i * 2^^(1/2) | 2^^(1/2) + (-1) * i * 2^^(1/2) | 2^^(1/2) + i * 2^^(1/2) ] + [ (5/4) * i * (10 + 2 * 5^^(1/2))^^(1/2) + (-5/4) * 5^^(1/2) + (5/4) | (-5) | (-5/4) * i * (10 + 2 * 5^^(1/2))^^(1/2) + (-5/4) * 5^^(1/2) + (5/4) | (-5/4) * i * (10 + (-2) * 5^^(1/2))^^(1/2) + (5/4) + (5/4) * 5^^(1/2) | (5/4) * i * (10 + (-2) * 5^^(1/2))^^(1/2) + (5/4) + (5/4) * 5^^(1/2) ] + [ 5 * i | (-5/2) * 3^^(1/2) + (5/2) * i | (-5/2) * 3^^(1/2) + (-5/2) * i | (-5) * i | (5/2) * 3^^(1/2) + (-5/2) * i | (5/2) * 3^^(1/2) + (5/2) * i ] + [ 5 * cos( (2/7) * pi ) + 5 * i * sin( (2/7) * pi ) | 5 * cos( pi * (4/7) ) + 5 * i * sin( pi * (4/7) ) | 5 * cos( pi * (6/7) ) + 5 * i * sin( pi * (6/7) ) | 5 * cos( pi * (8/7) ) + 5 * i * sin( pi * (8/7) ) | 5 * cos( pi * (10/7) ) + 5 * i * sin( pi * (10/7) ) | 5 * cos( pi * (12/7) ) + 5 * i * sin( pi * (12/7) ) | 5 ] + [ (5/2) * 2^^(1/2) + (5/2) * i * 2^^(1/2) | 5 * i | (-5/2) * 2^^(1/2) + (5/2) * i * 2^^(1/2) | (-5) | (-5/2) * 2^^(1/2) + (-5/2) * i * 2^^(1/2) | (-5) * i | (5/2) * 2^^(1/2) + (-5/2) * i * 2^^(1/2) | 5 ] + [ 5 * cos( (2/9) * pi ) + 5 * i * sin( (2/9) * pi ) | 5 * cos( pi * (4/9) ) + 5 * i * sin( pi * (4/9) ) | (-5/2) + (5/2) * i * 3^^(1/2) | 5 * cos( pi * (8/9) ) + 5 * i * sin( pi * (8/9) ) | 5 * cos( pi * (10/9) ) + 5 * i * sin( pi * (10/9) ) | (-5/2) + (-5/2) * i * 3^^(1/2) | 5 * cos( pi * (14/9) ) + 5 * i * sin( pi * (14/9) ) | 5 * cos( pi * (16/9) ) + 5 * i * sin( pi * (16/9) ) | 5 ] + 3^^(1/2) * [ (-1) | 1 ]'
             # , 'result'     : 'i * [ (-4) | 4 ] + [ (-3) | (3/2) + (-3/2) * i * 3^^(1/2) | (3/2) + (3/2) * i * 3^^(1/2) ] + [ (-1) * 2^^(1/2) + i * 2^^(1/2) | (-1) * 2^^(1/2) + (-1) * i * 2^^(1/2) | 2^^(1/2) + (-1) * i * 2^^(1/2) | 2^^(1/2) + i * 2^^(1/2) ] + [ (-5/4) * 5^^(1/2) + (5/4) + (5/4) * i * (5 + 2 * 5^^(1/2))^^(1/2) + (5/4) * i * (5 + (-2) * 5^^(1/2))^^(1/2) | (-5) | (-5/4) * 5^^(1/2) + (5/4) + (-5/4) * i * (5 + 2 * 5^^(1/2))^^(1/2) + (-5/4) * i * (5 + (-2) * 5^^(1/2))^^(1/2) | (5/4) + (5/4) * 5^^(1/2) + (-5/4) * i * (5 + 2 * 5^^(1/2))^^(1/2) + (5/4) * i * (5 + (-2) * 5^^(1/2))^^(1/2) | (5/4) + (5/4) * 5^^(1/2) + (5/4) * i * (5 + 2 * 5^^(1/2))^^(1/2) + (-5/4) * i * (5 + (-2) * 5^^(1/2))^^(1/2) ] + [ 5 * i | (-5/2) * 3^^(1/2) + (5/2) * i | (-5/2) * 3^^(1/2) + (-5/2) * i | (-5) * i | (5/2) * 3^^(1/2) + (-5/2) * i | (5/2) * 3^^(1/2) + (5/2) * i ] + [ 5 * cos( (2/7) * pi ) + 5 * i * sin( (2/7) * pi ) | 5 * cos( pi * (4/7) ) + 5 * i * sin( pi * (4/7) ) | 5 * cos( pi * (6/7) ) + 5 * i * sin( pi * (6/7) ) | 5 * cos( pi * (8/7) ) + 5 * i * sin( pi * (8/7) ) | 5 * cos( pi * (10/7) ) + 5 * i * sin( pi * (10/7) ) | 5 * cos( pi * (12/7) ) + 5 * i * sin( pi * (12/7) ) | 5 ] + [ (5/2) * 2^^(1/2) + (5/2) * i * 2^^(1/2) | 5 * i | (-5/2) * 2^^(1/2) + (5/2) * i * 2^^(1/2) | (-5) | (-5/2) * 2^^(1/2) + (-5/2) * i * 2^^(1/2) | (-5) * i | (5/2) * 2^^(1/2) + (-5/2) * i * 2^^(1/2) | 5 ] + [ 5 * cos( (2/9) * pi ) + 5 * i * sin( (2/9) * pi ) | 5 * cos( pi * (4/9) ) + 5 * i * sin( pi * (4/9) ) | (-5/2) + (5/2) * i * 3^^(1/2) | 5 * cos( pi * (8/9) ) + 5 * i * sin( pi * (8/9) ) | 5 * cos( pi * (10/9) ) + 5 * i * sin( pi * (10/9) ) | (-5/2) + (-5/2) * i * 3^^(1/2) | 5 * cos( pi * (14/9) ) + 5 * i * sin( pi * (14/9) ) | 5 * cos( pi * (16/9) ) + 5 * i * sin( pi * (16/9) ) | 5 ] + 3^^(1/2) * [ (-1) | 1 ] '
             # , 'result'       : '[ i * 4 | (-4) * i ] + [ (3/2) + (3/2) * i * 3^^(1/2) | (-3) | (3/2) + i * 3^^(1/2) * (-3/2) ] + [ 2^^(1/2) + i * 2^^(1/2) | i * 2^^(1/2) + (-1) * 2^^(1/2) | (-1) * 2^^(1/2) + (-1) * i * 2^^(1/2) | (-1) * i * 2^^(1/2) + 2^^(1/2) ] + [ (5/4) + 5^^(1/2) * (5/4) + (5/4) * i * (5 + 2 * 5^^(1/2))^^(1/2) + (-5/4) * i * (5 + (-2) * 5^^(1/2))^^(1/2) | (-5/4) * 5^^(1/2) + (5/4) + i * (5 + (-2) * 5^^(1/2))^^(1/2) * (5/8) + i * ((25/64) + (5/32) * 5^^(1/2))^^(1/2) * 5 | (-5) | (5/4) + 5^^(1/2) * (-5/4) + (-5/8) * i * (5 + 2 * 5^^(1/2))^^(1/2) + (5/8) * i * (5 + (-2) * 5^^(1/2))^^(1/2) + (-5) * i * ((25/64) + (5/32) * 5^^(1/2))^^(1/2) + 5 * i * ((25/64) + (-5/32) * 5^^(1/2))^^(1/2) | (5/4) * 5^^(1/2) + (5/4) + i * (5 + 2 * 5^^(1/2))^^(1/2) * (-5/8) + i * ((25/64) + (-5/32) * 5^^(1/2))^^(1/2) * (-5) ] + [ (5/2) * 3^^(1/2) + (5/2) * i | i * 5 | 3^^(1/2) * (-5/2) + i * (5/2) | (-5/2) * 3^^(1/2) + (-5/2) * i | i * (-5) | 3^^(1/2) * (5/2) + i * (-5/2) ] + [ 5 | 5 * cos( (2/7) * pi ) + 5 * i * sin( (2/7) * pi ) | 5 * cos( (4/7) * pi ) + 5 * i * sin( (4/7) * pi ) | 5 * cos( (6/7) * pi ) + 5 * i * sin( (6/7) * pi ) | 5 * cos( (8/7) * pi ) + 5 * i * sin( (8/7) * pi ) | 5 * cos( (10/7) * pi ) + 5 * i * sin( (10/7) * pi ) | 5 * cos( (12/7) * pi ) + 5 * i * sin( (12/7) * pi ) ] + [ 5 | (5/2) * 2^^(1/2) + (5/2) * i * 2^^(1/2) | 5 * i | (-5/2) * 2^^(1/2) + (5/2) * i * 2^^(1/2) | (-5) | (-5/2) * 2^^(1/2) + (-5/2) * i * 2^^(1/2) | (-5) * i | (5/2) * 2^^(1/2) + (-5/2) * i * 2^^(1/2) ] + [ 5 | 5 * cos( (2/9) * pi ) + 5 * i * sin( (2/9) * pi ) | 5 * cos( (4/9) * pi ) + 5 * i * sin( (4/9) * pi ) | (-5/2) + (5/2) * i * 3^^(1/2) | 5 * cos( (8/9) * pi ) + 5 * i * sin( (8/9) * pi ) | 5 * cos( (10/9) * pi ) + 5 * i * sin( (10/9) * pi ) | (-5/2) + (-5/2) * i * 3^^(1/2) | 5 * cos( (14/9) * pi ) + 5 * i * sin( (14/9) * pi ) | 5 * cos( (16/9) * pi ) + 5 * i * sin( (16/9) * pi ) ] + [ 3^^(1/2) | 3^^(1/2) * (-1) ]'
             , 'result'       : '1'
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 28
             { 'expression' : '5 cos( pi ) + 5 i sin( pi )'
             , 'result'     : '-5'
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 29
             { 'expression' : '(1 + i)^^(1/2)'
             , 'result'     : '2^^(1/4) * (2 + 2^^(1/2))^^(1/2) * (1/2) + 2^^(1/4) * i * (2 + (-1) * 2^^(1/2))^^(1/2) * (1/2)'
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 30
             { 'expression' : 'atan2(2,0)'
             , 'result'     : 'pi/2'
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 31
             { 'expression' : 'i^(1/2)'
             # , 'result'     : '[ -1/2 2^^(1/2) -1/2 i 2^^(1/2) | 1/2 2^^(1/2) + 1/2 i 2^^(1/2) ]'
             # , 'result'     : '[ (2^^(1/2) * (1/2) + i * 2^^(1/2) * (1/2)) | ((-1/2) * 2^^(1/2) + (-1/2) * i * 2^^(1/2)) ]'
             , 'result'     : '[ 2^^(1/2) * (1/2) + i * 2^^(1/2) * (1/2) | 2^^(1/2) * (-1/2) + i * 2^^(1/2) * (-1/2) ]'
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 32
             { 'expression' : '(1 + i)^(1/2) '
             , 'result'     : '[ 2^^(1/4) * (2 + 2^^(1/2))^^(1/2) * (1/2) + 2^^(1/4) * i * (2 + (-1) * 2^^(1/2))^^(1/2) * (1/2) | 2^^(1/4) * (-1/2) * (2 + 2^^(1/2))^^(1/2) + 2^^(1/4) * i * (-1/2) * (2 + (-1) * 2^^(1/2))^^(1/2) ]'
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 33
             { 'expression' : '(-1) * (3 * 1)^-1 * ((-6) + ((1/2) * (((-6))^^3 * (1)^2 * (-6) * 108 + (1)^2 * ((-6))^2 * (11)^2 * (-27) + (1)^3 * (-6) * 11 * (-6) * (-486) + 729 * (1)^4 * ((-6))^2 + 108 * (1)^3 * (11)^3)^^(1/2) + ((-6))^^3 + 1 * (-6) * 11 * (-9/2) + (1)^2 * (-6) * (27/2))^^(1/3) + (((-6))^^2 + (-3) * 1 * 11) * ((1/2) * (((-6))^^3 * (1)^2 * (-6) * 108 + (1)^2 * ((-6))^2 * (11)^2 * (-27) + (1)^3 * (-6) * 11 * (-6) * (-486) + 729 * (1)^4 * ((-6))^2 + 108 * (1)^3 * (11)^3)^^(1/2) + ((-6))^^3 + 1 * (-6) * 11 * (-9/2) + (1)^2 * (-6) * (27/2))^^(-1/3))'
             # , 'result'     : '2 + (-1/3) * ((1/2) * (-108)^^(1/2))^^(1/3) + (-1) * ((1/2) * (-108)^^(1/2))^^(-1/3)'
             , 'result'     : '1'
             # , 'actions'    : [ 'optimizeNormal' ]
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 34
             { 'expression' : '3^^(1/2) 3^^(1/2) 3^^(1/2) 3^^(1/2) 3^^(1/2)'
             , 'result'     : '9 * 3^^(1/2)'
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 35
             { 'expression' : '3^^(1/2) * 3^^(1/5)'
             , 'result'     : '2187^^(1/10)'
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 36
             { 'expression' : '3^^(1/2) * 3^^(2/5)'
             , 'result'     : '19683^^(1/10) '
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 37
             { 'expression' : '2^^(1/2) * 3^^(1/2)'
             , 'result'     : '6^^(1/2)'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 38
             { 'expression' : '((1/2) * 108^^(1/2))^^(1/3)'
             , 'result'     : '3^^(1/2)'
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 39
             { 'expression' : '3^^(-1/3) * 3^^(1/2)'
             , 'result'     : '3^^(1/6)'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 40
             { 'expression' : 'i^^(1/3)'
             , 'result'     : '3^^(1/2) * (1/2) + i * (1/2)'
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 41
             { 'expression' : '((-1) * i * (1/2) + 3^^(1/2) * (1/2)) * ((3^^(1/2) * (1/2))^2 + (-1) * (i * (1/2))^2)^-1'
             , 'result'     : '(-1/2) * i + 3^^(1/2) * (1/2)'
             , 'actions'    : [ 'optimizeNormal' ]
             }
           , # 42
             { 'expression' : '2 + ((1/2) * (-108)^^(1/2))^^(1/3) * (-1/3) + ((1/2) * (-108)^^(1/2))^^(-1/3) * (-1)'
             , 'result'     : '1'
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 43
             { 'expression' : '2 + (3 * i * 3^^(1/2))^^(1/3) * (-1) * 3^-1 + (3 * i * 3^^(1/2))^^(-1/3) * (-1)'
             , 'result'     : '1'
             , 'actions'    : [ 'optimizeExtended' ]
             }
           , # 44
             { 'expression' : '2 + (1/6) * ((1/2) * (-108)^^(1/2))^^(1/3) + (-1/6) * ((1/2) * (-108)^^(1/2))^^(1/3) * i * 3^^(1/2) + (((1/2) * (-108)^^(1/2))^^(1/3) * (-1/2) + ((1/2) * (-108)^^(1/2))^^(1/3) * (1/2) * i * 3^^(1/2))^-1 * (-1)'
             , 'result'     : '3'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 45
             { 'expression' : '(-16)^^(1/2)'
             , 'result'     : '4 i'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 46
             { 'expression' : '(5^7)^(1/7)'
             , 'result'     : '[ 5 *  cos( (2/7) * pi ) + 5 * i *  sin( (2/7) * pi ) | 5 *  cos( pi * (4/7) ) + 5 * i *  sin( pi * (4/7) ) | 5 *  cos( pi * (6/7) ) + 5 * i *  sin( pi * (6/7) ) | 5 *  cos( pi * (8/7) ) + 5 * i *  sin( pi * (8/7) ) | 5 *  cos( pi * (10/7) ) + 5 * i *  sin( pi * (10/7) ) | 5 *  cos( pi * (12/7) ) + 5 * i *  sin( pi * (12/7) ) | 5 ]'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 47
             { 'expression' : '2 + (1/6) * ((1/2) * (-108)^^(1/2))^^(1/3) + (1/6) * ((1/2) * (-108)^^(1/2))^^(1/3) * i * 3^^(1/2) + (((1/2) * (-108)^^(1/2))^^(1/3) * (-1/2) + ((1/2) * (-108)^^(1/2))^^(1/3) * i * 3^^(1/2) * (-1/2))^-1 * (-1)'
             , 'result'     : '2'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 48
             { 'expression' : "cos(3)^2 + sin(3)^2"
             , 'result'     : '1'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 49
             { 'expression' : "2 cos(3)^2 + 2 sin(3)^2"
             , 'result'     : '2'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 50
             { 'expression' : "sin( atan( 2/13 )) + cos( atan( 2/13 ))"
             # , 'result'     : '(173/169)^(-1/2) * (2/13) + (173/169)^(-1/2)'
               , 'result'     : '(15/173) * 173^^(1/2)'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 51
             { 'expression' : "(-1)^^(1/3)"
             , 'result'     : '(1/2) + i * 3^^(1/2) * (1/2)'  # '-1' principal root is not -1
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 52
             { 'expression' : "(-256/9)^^(1/2)"
             , 'result'     : '16/3 * i'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 53
             { 'expression' : "1 + i * (-256/9)^^(1/2) * (-3/8) + (-9/32) * (-256/27)^^(1/2) + (3/32) * (-256/3)^^(1/2)"
             , 'result'     : '3'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 54
             { 'expression' : "i^^(4/3) * 27^^(1/3)"
             , 'result'     : '(-3/2) + i * 3^^(1/2) * (3/2)'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 55
             { 'expression' : "(-1)^^(2/3)"
             , 'result'     : '-1/2 + 1/2 * i * 3^^(1/2)'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 56
             { 'expression' : "((7/4) + (3/4) * (-1)^^(2/3) + (-1)^^(1/3) * (3/4))^-1 * i * 3^^(1/2) * (-1)^^(1/3) * (1/2) + ((7/4) + (3/4) * (-1)^^(2/3) + (-1)^^(1/3) * (3/4))^-1 * i * 3^^(1/2) * (-3/8) + ((7/4) + (3/4) * (-1)^^(2/3) + (-1)^^(1/3) * (3/4))^-1 * (-1/4) + (3/4) * (-1)^^(2/3) * ((7/4) + (3/4) * (-1)^^(2/3) + (-1)^^(1/3) * (3/4))^-1 + (-1)^^(1/3) * ((7/4) + (3/4) * (-1)^^(2/3) + (-1)^^(1/3) * (3/4))^-1 * (-3/4) + (-15/8) * (1/3)^^(1/2) * ((7/4) + (3/4) * (-1)^^(2/3) + (-1)^^(1/3) * (3/4))^-1 * i"
             , 'result'     : '-1'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 57
             { 'expression' : "(5 * 169^^-1)^^(-1/2)"
             , 'result'     : '(13/5) * 5^^(1/2)'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 58
             { 'expression' : "(2 * 3^^-1)^^(-1/3)"
             # , 'result'     : '(1/2) * 12^^(1/3)'
             , 'result'     : '(3/2)^^(1/3)'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 59
             { 'expression' : "(((-1 * ( -1 * ( (-8/3))) + ( ( -1 * ( (-8/3)))^^2 - 4 * ( (-4/3)) * ((-28/9)) )^^(1/2) ) / ( 2 * ((-4/3))) - ( -1 * -3 / 3 )) / ( (-1 * ( -1 * ( (-8/3))) - ( ( -1 * ( (-8/3)))^^2 - 4 * ( (-4/3)) * ((-28/9)) )^^(1/2) ) / ( 2 * ((-4/3))) - ( -1 * -3 / 3 )))^^(1/3)* (-1/2 - (1/2) * i * 3^^(1/2))"
             , 'result'     : '(1/2) + i * 3^^(1/2) * (-1/2)'
             # , 'result'     : '(1/2) + (-1/4) * i * 3^^(1/2) + (-1/4) * 27^^(1/6) * i '
             # , 'result'     : '(1/2) + i * 3^^(1/2) * (-1/4) + 27^^(1/6) * i * (-1/4)'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 60
             { 'expression' : "sum( n, 1, 5 , 1 / (n^2) )"
             , 'result'     : '1^-2 + 2^-2 + 3^-2 + 4^-2 + 5^-2'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 61
             { 'expression' : "binomial( 20,10 )^^2 + floor( 1 * 5^-1 )^^2 + ceil( 7 * 5^-1 )^^2 + factorial( 7 )^^2 + exp( 2, sin( pi * 3^^-1 ) ) + exp( 3 ) "
             , 'result'     : '(136640724563/4) + e^^3'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 62
             { 'expression' : "(1 * 2^^-1 * ((-729) * 64^^-1)^^(1/2) + 27 * 16^^-1 * 3^^(1/2))^^(1/3) * (-1) * 3^^-1 + (1 * 2^^-1 * ((-729) * 64^^-1)^^(1/2) + 27 * 16^^-1 * 3^^(1/2))^^(-1/3) * (-3) * 4^^-1"
             , 'result'     : '- cos( pi / 18 )'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 63
             { 'expression' : "(1 * 2^^-1 * ((-729) * 64^^-1)^^(1/2) + 27 * 16^^-1 * 3^^(1/2))^^(1/3) * i * 3^^(1/2) * 1 * 6^^-1"
             , 'result'     : '3^^(1/2) * (1/4) * i * cos( (1/18) * pi ) + 3^^(1/2) * (-1/4) * sin( (1/18) * pi )'
             , 'actions'    : [ 'optimizeExtended' ]
             }
             , # 64 - by principal root, first the 1/3 power and then the 2 power
             { 'expression' : '( ((1/2) * (-190512)^^(1/2) + (-55))^^(1/3)  + ((-1/101306) * (-190512)^^(1/2) + (-55/50653))^^(1/3) )^^2'
             # , 'result'     : '((-55) + 126 * 3^^(1/2) * i)^^(2/3) + 2 + ((-55/50653) + (-126/50653) * 3^^(1/2) * i)^^(2/3)'
             # ,  'result'    : '2 + cos( (1/6) * pi + (1/3) * atan( (55/378) * 3^^(1/2) ) )^2 * 37 + cos( (1/6) * pi + (1/3) * atan( (55/378) * 3^^(1/2) ) ) * i * sin( (1/6) * pi + (1/3) * atan( (55/378) * 3^^(1/2) ) ) * 74 + (-37) * sin( (1/6) * pi + (1/3) * atan( (55/378) * 3^^(1/2) ) )^2 + cos( (-1/6) * pi + (-1/3) * atan( (55/378) * 3^^(1/2) ) )^2 * (1/37) + cos( (-1/6) * pi + (-1/3) * atan( (55/378) * 3^^(1/2) ) ) * i * sin( (-1/6) * pi + (-1/3) * atan( (55/378) * 3^^(1/2) ) ) * (2/37) + (-1/37) * sin( (-1/6) * pi + (-1/3) * atan( (55/378) * 3^^(1/2) ) )^2 '
             # , 'result'     : "2 + cos( (1/3) * atan( (55/378) * 3^^(1/2) ) )^2 * (1371/74) + cos( (1/3) * atan( (55/378) * 3^^(1/2) ) ) * sin( (1/3) * atan( (55/378) * 3^^(1/2) ) ) * 3^^(1/2) * (-1370/37) + sin( (1/3) * atan( (55/378) * 3^^(1/2) ) )^2 * (-1367/74) + cos( (1/3) * atan( (55/378) * 3^^(1/2) ) )^2 * i * 3^^(1/2) * (684/37) + cos( (1/3) * atan( (55/378) * 3^^(1/2) ) ) * i * sin( (1/3) * atan( (55/378) * 3^^(1/2) ) ) * (1367/37) + sin( (1/3) * atan( (55/378) * 3^^(1/2) ) )^2 * i * 3^^(1/2) * (-685/37)"
             # , 'result'     : "(556/37) + i * 3^^(1/2) * (1479/74) + cos( (1/3) * atan( (55/378) * 3^^(1/2) ) ) * (-1/37) * 3^^(1/2) * sin( (1/3) * atan( (55/378) * 3^^(1/2) ) ) + cos( (1/3) * atan( (55/378) * 3^^(1/2) ) ) * i * sin( (1/3) * atan( (55/378) * 3^^(1/2) ) ) * (-2/37)"
             , 'result'     : '(20548/1369) + (27360/1369) * i * 3^^(1/2) '
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 65
             { 'expression' : 'atan2( pi * cos( (3/4) ),1 + e + pi * sin( (3/4) ) ) * (1/3)'
             , 'result'     : 'atan( (1 + e + pi *  sin( (3/4) ))^^-1 * pi *  cos( (3/4) ) ) * (1/3)'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 66
             { 'expression' : '(6 * 3^^(1/2) + (-30))^^(1/3)'
             # , 'result'     : '((-6) * 3^^(1/2) + 30)^^(1/3) * 1 * 2^^-1 + ((-6) * 3^^(1/2) + 30)^^(1/3) * i * 3^^(1/2) * 2^^-1'
             # , 'result'     : '(1008 + 3^^(1/2) * (-360))^^(1/6) * 1 * 2^^-1 + (1008 + 3^^(1/2) * (-360))^^(1/6) * i * 3^^(1/2) * 2^^-1'
             # , 'result'     : '(1008 + 3^^(1/2) * (-360))^^(1/6) * (1/2) + (1008 + 3^^(1/2) * (-360))^^(1/6) * (-1/2) * 0 * 3^^(1/2) + (1008 + 3^^(1/2) * (-360))^^(1/6) * (1/2) * 0 + (1008 + 3^^(1/2) * (-360))^^(1/6) * i * 3^^(1/2) * (1/2)' 
             # , 'result'     : '(1/2) * (7 + (-5/2) * 3^^(1/2))^^(1/6) * 12^^(1/3) + i * 3^^(1/2) * (1/2) * (7 + (-5/2) * 3^^(1/2))^^(1/6) * 12^^(1/3)'
             # , 'result'     : '(1/2) * (28 + (-10) * 3^^(1/2))^^(1/6) * 6^^(1/3) + i * 3^^(1/2) * (1/2) * (28 + (-10) * 3^^(1/2))^^(1/6) * 6^^(1/3)'
             , 'result'     : '(1/2) * (30 + (-6) * 3^^(1/2))^^(1/3) + i * 3^^(1/2) * (1/2) * (30 + (-6) * 3^^(1/2))^^(1/3)'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 67
             { 'expression' : '[2 | 4 ]^(1/2)'
             # , 'result'     : '[ 2^^(1/2) | 4^^(1/2) | (-1) * 2^^(1/2) | (-2) ]'
             , 'result'     : '[ 2^^(1/2) | 2^^(1/2) * (-1) | 2 | (-2) ]'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 68
             { 'expression' : '( (-27)^2 )^^(1/3)'
             , 'result'     : '9'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 69
             { 'expression' : '( (-27)^^2 )^^(1/3)'
             , 'result'     : '9'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 70
             { 'expression' : '(-27)^^(2/3)'
             , 'result'     : '(-9/2) + (9/2) * i * 3^^(1/2)'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 71
             { 'expression' : 'abs( -1 + i  + test(1)) + cos( 1 + test(1)) + atan2( test(1), 0 ) * sin( test(1) ) + ( 1 + i + test(1))^^(1/3)'
             , 'result'     : 'abs( (-1) + i + test( 1 ) ) + ( cos( 1 ) * cos( test( 1 ) ) + (-1) * sin( 1 ) * sin( test( 1 ) )) + atan2( test( 1 ),0 ) * sin( test( 1 ) ) + (1 + i + test( 1 ))^^(1/3)'
             , 'actions'    : [ 'optimizeExtended' ]
             }
            , # 72
             { 'expression' : 'cos( 7 pi / 30 )'
             #, 'result'     : '3^^(1/2) * (-1/8) + 15^^(1/2) * (1/8) + (1/2) * ((45/128) + (-9/128) * 5^^(1/2))^^(1/2) + (1/2) * ((225/128) + (-45/128) * 5^^(1/2))^^(1/2) + (-1/32) * (5 + 2 * 5^^(1/2))^^(1/2) + (-1/32) * (25 + 10 * 5^^(1/2))^^(1/2) + (1/32) * (5 + (-2) * 5^^(1/2))^^(1/2) + (1/32) * (25 + (-10) * 5^^(1/2))^^(1/2)'
             , 'result'     : '(-1/32) * (10 + (-2) * 5^^(1/2))^^(1/2) + (-1/32) * (50 + (-10) * 5^^(1/2))^^(1/2) + (1/32) * (90 + (-18) * 5^^(1/2))^^(1/2) + 3^^(1/2) * (-1/8) + 15^^(1/2) * (1/8) + (1/32) * (450 + (-90) * 5^^(1/2))^^(1/2)'
             , 'actions'    : [ 'optimizeExtended' ]
             }

           ]

def TestModule( modules ):
  """
  Unit test given module
  """
  iTotalTest = 0
  iGoodTest  = 0
  for module in modules:
    # print( "Module: " + str( module ))
    try:
      iTotalTest += 1
      module.Test()
      iGoodTest  += 1
    except NameError as exceptInfo:
      print( exceptInfo)

  return iTotalTest, iGoodTest

# commandline options
lOptShow      = False
lOptResult    = False
lOptShowCheck = False
lOptShowOpt   = False

startTime = datetime.now()

print( "Test: Start", end='\r')

#
# always do the unit tests of the functions
# this may never give an error
#
# symRegisterFunctions.SymRegisterFunctions()

iTotUnitFunc, iGoodUnitFunc = TestModule( symRegisterFunctions.SymRegisterGetModuleNames()      )
iTotUnitOpt , iGoodUnitOpt  = TestModule( symRegisterOptimize.SymRegisterGetModuleNames()       )
iTotUnitNum , iGoodUnitNum  = TestModule( symRegisterOptSymNumber.SymRegisterGetModuleNames()   )
iTotUnitVar , iGoodUnitVar  = TestModule( symRegisterOptSymVariable.SymRegisterGetModuleNames() )
iTotUnitFnc , iGoodUnitFnc  = TestModule( symRegisterOptSymFunction.SymRegisterGetModuleNames() )
iTotUnitAny , iGoodUnitAny  = TestModule( symRegisterOptSymAny.SymRegisterGetModuleNames()      )

iTotModTest = iTotUnitFunc  + iTotUnitOpt  + iTotUnitNum  + iTotUnitVar  + iTotUnitFnc  + iTotUnitAny
iTotModGood = iGoodUnitFunc + iGoodUnitOpt + iGoodUnitNum + iGoodUnitVar + iGoodUnitFnc + iGoodUnitAny

print( "Test:      ", end='\r')

#
# walk the test formulas
#
if len( sys.argv ) > 0 :
  for iCnt in range( 1, len( sys.argv )):
    cOpt = sys.argv[ iCnt ]
    if cOpt == '--help' :
      print( 'testsymexpress3.py [options]' )
      print( '' )
      print( 'Options:' )
      print( '--help          Show help and exit' )
      print( '--show          Show expressions'   )
      print( '--showcheck     Show check expressions' )
      print( '--showoptimized Show optimized expressions' )
      print( '--showall       Show all'   )
      sys.exit()
    elif cOpt == '--show' :
      lOptShow = True
    elif cOpt == '--showcheck' :
      lOptShowCheck = True
    elif cOpt == '--showoptimized' :
      lOptShowOpt = True
    elif cOpt == '--showall' :
      lOptShow      = True
      lOptShowCheck = True
      lOptShowOpt   = True
    else:
      print( 'Unknown option: ' + cOpt )
      print( '' )
      print( 'use testsymexpress3.py --help' )
      sys.exit()

# test expressions
iTests = 0
iGood  = 0
iBad   = 0
# for iCntTestData in range( 0, len( testData )):
for dData in testData :
  iTests += 1
  # if iTests != 26:
  #   continue
  # print( "Test: " + str( iCntTestData ), end='\r')
  print( f"Test: {iTests}", end='\r')

  # dData    = testData[ iCntTestData ]
  cExpress = dData.get( 'expression' )
  cResult  = dData.get( 'result'     )
  cActions = dData.get( 'actions'    )

  oExpress = symexpress3.SymFormulaParser( cExpress )
  oResult  = symexpress3.SymFormulaParser( cResult  )

  if cActions[ 0 ] == 'optimize_writeOutSum' :
    oResult.optimize()
  else:
    oResult.optimizeNormal()

  # for iActions in range( 0, len( cActions )):
  for cAction in cActions :
    # cAction = cActions[ iActions ]
    if cAction == 'optimizeNormal' :
      oExpress.optimizeNormal()
    elif cAction == 'optimizeExtended' :
      oExpress.optimizeExtended()
    else:
      print( f'Unknown action "{cAction}" entry {iTests}' )

  if not oResult.isEqual( oExpress ) :
    iBad += 1
    print( f'Entry {iTests} not equal'  )
    print( f'  org expr  : {cExpress}'      )
    print( f'  expression: {str(oExpress)}' )
    print( f'  org result: {cResult}'       )
    print( f'  result    : {str(oResult)}'  )
  else:
    iGood += 1
    if lOptShow == True :
      print( f'{iTests} - Expr : {cExpress}' )
    if lOptShowOpt == True :
      print( f'{iTests} - Optim: {str( oExpress )}' )
    if lOptShowCheck == True :
      print( f'{iTests} - Check: {cResult}' )


endTime   = datetime.now()
timeInSec = ( endTime - startTime ).total_seconds()

print( f"Number of module test: {iTotModTest}, passed: {iTotModGood}" )
print( f"Number of tests      : {iTests}, passed: {iGood}, failed; {iBad}, total time: {timeInSec} (sec)" )
