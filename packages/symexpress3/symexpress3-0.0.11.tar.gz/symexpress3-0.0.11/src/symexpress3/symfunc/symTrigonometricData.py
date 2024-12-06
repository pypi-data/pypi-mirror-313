#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    trigonometric data for Sym Express 3

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


    https://en.wikipedia.org/wiki/Trigonometric_functions
    https://en.wikipedia.org/wiki/Inverse_trigonometric_functions
    https://en.wikipedia.org/wiki/Exact_trigonometric_values
    https://en.wikipedia.org/wiki/Sine

"""

# sin 0 -> PI/2 equal to PI -> PI/2 (inverse),  PI -> 2PI/3 ( * -1)
# cos ( x ) = sin( pi / 2 - x )
# only needed is sin from  0 -> pi/2
#
#               trio-name[0], sign[1], counter[2], denominator[3], expression[4]    , SymExpress[5]
trigonometricdata = [ [ "sin",    1    ,0      ,  1         , "0"                               , None]
                    , [ "sin",    1    ,1      , 12         , "( 6^^(1/2) - 2^^(1/2) ) / 4"     , None]
                    , [ "sin",    1    ,1      , 10         , "(5^^(1/2) - 1) / 4"              , None]
                    , [ "sin",    1    ,1      ,  8         , "(2 - 2^^(1/2))^^(1/2) / 2"       , None]
                    , [ "sin",    1    ,1      ,  6         , "1 / 2"                           , None]
                    , [ "sin",    1    ,1      ,  5         , "(10 - 2 * 5^^(1/2))^^(1/2) / 4"  , None]
                    , [ "sin",    1    ,1      ,  4         , "2^^(1/2) / 2"                    , None]
                    , [ "sin",    1    ,3      , 10         , "( 1 + 5^^(1/2)) / 4"             , None]
                    , [ "sin",    1    ,1      ,  3         , "3^^(1/2) / 2"                    , None]
                    , [ "sin",    1    ,3      ,  8         , "( 2 + 2^^(1/2) )^^(1/2) / 2"     , None]
                    , [ "sin",    1    ,2      ,  5         , "(10 + 2 * 5^^(1/2))^^(1/2) / 4"  , None]
                    , [ "sin",    1    ,5      , 12         , "(6^^(1/2) + 2^^(1/2)) / 4"       , None]
                    , [ "sin",    1    ,1      ,  2         , "1"                               , None]

                    , [ "sin",    1    ,2      , 15         , "(-1/8) * (10 + (-2) * 5^^(1/2))^^(1/2) + 3^^(1/2) * (1/8) + (1/8) * 15^^(1/2)", None ]
                    , [ "sin",    1    ,1      , 15         , "((7/16) + 5^^(1/2) * (-1/16) + ((15/32768) + 5^^(1/2) * (-3/32768))^^(1/2) * (-16))^^(1/2)" , None ]

                    , [ "cos",    1    ,0      ,  1         , "1"                               , None]
                    , [ "cos",    1    ,1      , 12         , "(6^^(1/2) + 2^^(1/2))/4"         , None]
                    , [ "cos",    1    ,1      , 10         , "( (10 + 2 * 5^^(1/2))^^(1/2))/4" , None]
                    , [ "cos",    1    ,1      ,  8         , "( ( 2 + 2^^(1/2))^^(1/2))/2"     , None]
                    , [ "cos",    1    ,1      ,  6         , "(3^^(1/2))/2"                    , None]
                    , [ "cos",    1    ,1      ,  5         , "(1 + 5^^(1/2))/4"                , None]
                    , [ "cos",    1    ,1      ,  4         , "(2^^(1/2))/2"                    , None]
                    , [ "cos",    1    ,3      , 10         , "(( 10 - 2 * 5^^(1/2))^^(1/2))/4" , None]
                    , [ "cos",    1    ,1      ,  3         , "1/2"                             , None]
                    , [ "cos",    1    ,3      ,  8         , "((2 - 2^^(1/2))^^(1/2))/2"       , None]
                    , [ "cos",    1    ,2      ,  5         , "( 5^^(1/2)-1)/4"                 , None]
                    , [ "cos",    1    ,5      , 12         , "( 6^^(1/2) - 2^^(1/2))/4"        , None]
                    , [ "cos",    1    ,1      ,  2         , "0"                               , None]

                    , [ "cos",    1    ,2      , 15         , "(1/8) * (30 + (-6) * 5^^(1/2))^^(1/2) + (1/8) + (1/8) * 5^^(1/2)" , None ]
                    , [ "cos",    1    ,1      , 15         , "((9/16) + (1/16) * 5^^(1/2) + ((15/32768) + 5^^(1/2) * (-3/32768))^^(1/2) * 16)^^(1/2)", None ]

                    , [ "tan",    1    ,0      ,   1        , "0"                                  , None]
                    , [ "tan",    1    ,1      ,  12        , "(2 - 3^^(1/2))"                     , None]
                    , [ "tan",    1    ,1      ,  10        , "((25 - 10 * 4^^(1/2) )^^(1/2) / 5)" , None]
                    , [ "tan",    1    ,1      ,   8        , "(2^^(1/2) - 1)"                     , None]
                    , [ "tan",    1    ,1      ,   6        , "(3^^(1/2) / 3)"                     , None]
                    , [ "tan",    1    ,1      ,   5        , "(5 - 2 * 5^^(1/2))^^(1/2) / 5"      , None]
                    , [ "tan",    1    ,1      ,   4        , "1"                                  , None]
                    , [ "tan",    1    ,3      ,  10        , "( 25 + 10 * 5^^(1/2))^^(1/2) / 5"   , None]
                    , [ "tan",    1    ,1      ,   3        , "3^^(1/2)"                           , None]
                    , [ "tan",    1    ,3      ,   8        , "(2^^(1/2) + 1)"                     , None]
                    , [ "tan",    1    ,2      ,   5        , "(5 + 2 * 5^^(1/2))^^(1/2)"          , None]
                    , [ "tan",    1    ,5      ,  12        , "(2 + 3^^(1/2))"                     , None]

                    ]
