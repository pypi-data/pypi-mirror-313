#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Command line interface for Symbolic expression 3

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

import sys
import symexpress3

def OptimzeFunction( cExpress, outputFormat, optimizeActions ):
  """
  Optimize the given expression according the optimize actions
  Output the result for the given output types`
  """
  # convert string expression into object
  try:
    oExpress = symexpress3.SymFormulaParser( cExpress )
  except NameError as exceptInfo:
    print( "Error in expression: " + cExpress )
    print( exceptInfo )
    return
  except:  # pylint: disable=bare-except
    print( "Error in expression: " + cExpress )
    print( str( sys.exc_info()[0] ))
    return

  # optimize expression
  if len( optimizeActions ) < 1:
    oExpress.optimizeExtended()
  else:
    oExpress.optimize()
    for optKey in optimizeActions:
      if optKey == "optimizeNormal":
        oExpress.optimizeNormal()
        continue
      if optKey == "optimizeExtended":
        oExpress.optimizeExtended()
        continue
      oExpress.optimize( optKey )
      oExpress.optimize()

  # output expression
  if outputFormat == "":
    print( str( oExpress ))
  else:
    for outputType in outputFormat:
      if outputType == "c":
        try:
          dValue = oExpress.getValue()
          print( dValue )
        except NameError as exceptInfo:
          print( "Error in getting the value of expression: " + cExpress )
          print( exceptInfo )
          return

      elif outputType == "s":
        print( str( oExpress ))

      elif outputType == "m":
        print( oExpress.mathMl() )

      elif outputType == "h":
        output = symexpress3.SymToHtml( None, "SymExpress 3" )
        # try:
        output.writeSymExpress( oExpress )
        output.writeLine( str( oExpress ))

        # except:
        #  pass

        output.closeFile()
        output = None

      elif outputType == "t":
        symexpress3.SymExpressTree( oExpress )

      else:
        print( "Unknown output (-o) : {outputType}" )
        return # stop by unknown output`



def CheckOptimizeActions( cList ):
  """
  Check of the given optimize actions are valid
  """
  optDict = symexpress3.GetAllOptimizeActions()

  actions = cList.split(",")
  actions = [s.strip() for s in actions]
  for optKey in actions:
    if optKey == "optimizeNormal":
      continue
    if optKey == "optimizeExtended":
      continue
    if optKey in optDict:
      continue

    print( f"Unknown optimize action (-a) : {optKey}" )
  return actions


def DisplayList( listTypes ):
  """
  Display list of the given type
  f = functions
  a = optimize actions
  v = fixed variables
  """
  for listType in listTypes:
    if listType == "f" :
      print( "Functions:" )
      funcTable = symexpress3.GetAllFunctions()
      funcTable = dict(sorted(funcTable.items()))

      for optKey, optValue in funcTable.items():
        print( f"  {optKey: <30} - {optValue}" )

    elif listType == "a" :
      print( "Optimize actions:")
      optDict = symexpress3.GetAllOptimizeActions()
      optDict = dict(sorted(optDict.items()))

      optDict[ "optimizeNormal"  ] = "Normal optimization"
      optDict[ "optimizeExtended" ] = "Extended optimization"

      for optKey, optValue in optDict.items():
        print( f"  {optKey: <30} - {optValue}" )

    elif listType == "v" :
      print( "Predefined variables:" )
      varDict = symexpress3.GetFixedVariables()
      for varKey, varValue in varDict.items():
        print( f"  {varKey: <8} - {varValue}" )

    else:
      print( f"Unknown -list options: {listType}" )

def DisplayVersion():
  """
  Display version information
  """
  # print( "symexp3cmd.py - symexpress3 command line interface" )
  print( "Version    : " + symexpress3.__version__    )
  # print( "Build number: " + symexpress3.symexpress3.__buildnumber__ )

  print( "Author     : " + symexpress3.__author__     )
  print( "Copyright  : " + symexpress3.__copyright__  )
  print( "License    : " + symexpress3.__license__    )
  print( "Maintainer : " + symexpress3.__maintainer__ )
  print( "Email      : " + symexpress3.__email__      )
  print( "Status     : " + symexpress3.__status__     )


def DisplayHelp():
  """
  Display help
  """
  # print( "symexp3cmd.py - symexpress3 command line interface" )
  # print( "usage: symexp3cmd [options] [arg] " )
  print( "usage: python -m symexpress3 [options] [arg]" )
  print( "options: " )
  print( "  -h           : Help" )
  print( "  -v           : Version information" )
  print( "  -a <actions> : Comma separated list of actions" )
  print( "  -l <types>   : List of types" )
  print( "                 f = defined functions" )
  print( "                 a = optimize actions" )
  print( "                 v = fixed variables" )
  print( "  -o <format>  : output format" )
  print( "                 s - string format (default)" )
  print( "                 m - MathML (xml) format" )
  print( "                 c - Calculated value " )
  print( "                 t - tree view" )
  print( "                 h - html, formula in string and MathMl format" )
  print( "arg:" )
  print( "<formula>" )
  print( " " )
  print( "Example: " )
  print( 'python -m symexpress3 -v -l fav -o sc "cos( pi / 4 )^^(1/3)"' )

def CommandLine( argv ):
  """
  Process the symexpres3 command line parameters
  """
  outputFormat    = ""
  optimizeActions = []

  nrarg = len( argv )

  # nothing given, then display help
  if nrarg <= 1:
    DisplayHelp()

  mode        = ""
  expressions = []
  for iCnt in range( 1, nrarg ) :
    cArg = argv[ iCnt ]

    if mode == "list":
      DisplayList( cArg )
      mode = ""
      continue

    if mode == "output":
      outputFormat = cArg
      mode = ""
      continue

    if mode == "optimize":
      optimizeActions = CheckOptimizeActions(cArg)
      mode = ""
      continue



    if cArg == "-h" :
      DisplayHelp()

    elif cArg == "-v" :
      DisplayVersion()

    elif cArg == "-l" :
      mode = "list"

    elif cArg == "-o":
      mode = "output"

    elif cArg == "-a":
      mode = "optimize"

    else:
      if cArg.startswith( "-" ):
        print( f"Unknown option: {cArg}, use -h for help")
      else:
        # collect the given expression, process after all the options are read
        expressions.append( cArg )

  # process all the given expressions
  for key in expressions:
    OptimzeFunction( key, outputFormat, optimizeActions )


# ---------------------------
# The end
# ---------------------------
