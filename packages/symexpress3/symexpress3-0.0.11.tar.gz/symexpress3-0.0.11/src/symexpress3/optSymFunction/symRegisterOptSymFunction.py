#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Registration of function classes for symexpress3

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

from symexpress3                import symtables
from symexpress3.optSymFunction import optSymFunctionSinToSum
from symexpress3.optSymFunction import optSymFunctionCosToSum
from symexpress3.optSymFunction import optSymFunctionSinAtanDivNToSinICos
from symexpress3.optSymFunction import optSymFunctionCosAtanDivNToSinICos
from symexpress3.optSymFunction import optSymFunctionCosXplusYtoSinCos
from symexpress3.optSymFunction import optSymFunctionSinXplusYtoSinCos
from symexpress3.optSymFunction import optSymFunctionCosAtanDiv3
from symexpress3.optSymFunction import optSymFunctionCosToE
from symexpress3.optSymFunction import optSymFunctionSinToE
from symexpress3.optSymFunction import optSymFunctionEToCosSin
from symexpress3.optSymFunction import optSymFunctionEToSum
from symexpress3.optSymFunction import optSymFunctionNumberToPrimeFactors
from symexpress3.optSymFunction import optSymFunctionNumberToDivisors

#
# automatic called from symepxress3 too fill functionTable[]
#
def SymRegisterOptimize():
  """
  Register all the function optimize classes
  """

  symtables.RegisterTableEntry( 'optSymFunction', optSymFunctionSinToSum.OptSymFunctionSinToSum() )
  symtables.RegisterTableEntry( 'optSymFunction', optSymFunctionCosToSum.OptSymFunctionCosToSum() )
  symtables.RegisterTableEntry( 'optSymFunction', optSymFunctionSinAtanDivNToSinICos.OptSymFunctionSinAtanDivNToSinICos() )
  symtables.RegisterTableEntry( 'optSymFunction', optSymFunctionCosAtanDivNToSinICos.OptSymFunctionCosAtanDivNToSinICos() )
  symtables.RegisterTableEntry( 'optSymFunction', optSymFunctionCosXplusYtoSinCos.OptSymFunctionCosXplusYtoSinCos()       )
  symtables.RegisterTableEntry( 'optSymFunction', optSymFunctionSinXplusYtoSinCos.OptSymFunctionSinXplusYtoSinCos()       )
  symtables.RegisterTableEntry( 'optSymFunction', optSymFunctionCosAtanDiv3.OptSymFunctionCosAtanDiv3()                   )
  symtables.RegisterTableEntry( 'optSymFunction', optSymFunctionCosToE.OptSymFunctionCosToE()                             )
  symtables.RegisterTableEntry( 'optSymFunction', optSymFunctionSinToE.OptSymFunctionSinToE()                             )
  symtables.RegisterTableEntry( 'optSymFunction', optSymFunctionEToCosSin.OptSymFunctionEToCosSin()                       )
  symtables.RegisterTableEntry( 'optSymFunction', optSymFunctionEToSum.OptSymFunctionEToSum()                             )
  symtables.RegisterTableEntry( 'optSymFunction', optSymFunctionNumberToPrimeFactors.OptSymFunctionNumberToPrimeFactors() )
  symtables.RegisterTableEntry( 'optSymFunction', optSymFunctionNumberToDivisors.OptSymFunctionNumberToDivisors()         )

#
# Get all the modules from the optSymNumber, used in testsymexpress3.py
#
def SymRegisterGetModuleNames():
  """
  Get all the modules of the function optimizes
  """

  symModules = []

  symModules.append( optSymFunctionSinToSum             )
  symModules.append( optSymFunctionCosToSum             )
  symModules.append( optSymFunctionSinAtanDivNToSinICos )
  symModules.append( optSymFunctionCosAtanDivNToSinICos )
  symModules.append( optSymFunctionCosXplusYtoSinCos    )
  symModules.append( optSymFunctionSinXplusYtoSinCos    )
  symModules.append( optSymFunctionCosAtanDiv3          )
  symModules.append( optSymFunctionCosToE               )
  symModules.append( optSymFunctionSinToE               )
  symModules.append( optSymFunctionEToCosSin            )
  symModules.append( optSymFunctionEToSum               )
  symModules.append( optSymFunctionNumberToPrimeFactors )
  symModules.append( optSymFunctionNumberToDivisors     )


  return symModules

if __name__ == '__main__':
  SymRegisterOptimize()
  print( "Modules: " + str( ( SymRegisterGetModuleNames() )))
  # print( "globals: " + str( globals() ))
