# Python Symbolic Expression 3

A Python module for symbolic calculations

## Usage

### Optimize expression
```py
>>> import symexpress3
>>> objExpress = symexpress3.SymFormulaParser( '(x+1) * (x+2)' )
>>> objExpress.optimizeExtended()
>>> print( objExpress )
x^2 + x * 3 + 2
```

### Supported operators
\+&nbsp;&nbsp; \-&nbsp;&nbsp; \*&nbsp;&nbsp; \/&nbsp;&nbsp; \(&nbsp;&nbsp; \)&nbsp;&nbsp; \^&nbsp;&nbsp; \^\^
<br>
^ gives root values by fractions
^^ gives principal root values by fractions
```py
>>> import symexpress3
>>> objExpress = symexpress3.SymFormulaParser( '(4)^(1/2)' )
>>> objExpress.optimizeExtended()
>>> print( objExpress )
[ (-2) | 2 ]
>>> objExpress = symexpress3.SymFormulaParser( '(4)^^(1/2)' )
>>> objExpress.optimizeExtended()
>>> print( objExpress )
2
```
### Numeric values
Only integers are supported. For fractions use /
```py
>>> import symexpress3
>>> objExpress = symexpress3.SymFormulaParser( '7/10 + 3/11' )
>>> objExpress.optimizeExtended()
>>> print( objExpress )
(107/110)
```

### Get the real value
If there is more the one value, it gives an array back
```py
>>> import symexpress3
>>> objExpress = symexpress3.SymFormulaParser( '7/10 + 3/11' )
>>> objExpress.optimizeExtended()
>>> print( objExpress.getValue() )
0.9727272727272728
>>> objExpress = symexpress3.SymFormulaParser( '(4)^(1/2)' )
>>> objExpress.optimizeExtended()
>>> print( objExpress.getValue() )
[-2, 2]
```

### Get all defined functions
Get a dictionary of all the defined functions. Key is the functions syntax, value is the description
```py
>>> import symexpress3
>>> print( symexpress3.GetAllFunctions() )
```

### Get all defined optimize actions
Get a dictionary of all the optimize actions. Key is the optimize action, value is the description
```py
>>> import symexpress3
>>> print( symexpress3.GetAllOptimizeActions() )
```

### Get all fixed variables
Get a dictionary of all the fixed variables. Key is the variable name, value is the description
```py
>>> import symexpress3
>>> print( symexpress3.GetFixedVariables() )
```

### Predefined optimization methods
The *optimizeNormal* method use the *multiply*, *onlyOneRoot*, *i*, *power* and *add* optimize actions
The *power* action do not optimize roots. *onlyOneRoot* get radicals in it lowest form.
```py
>>> import symexpress3
>>> objExpress = symexpress3.SymFormulaParser( '5 * 2^2 + i * i + (4)^(1/2)' )
>>> objExpress.optimizeNormal()
>>> print( objExpress )
19 + 4^(1/2)
```
The *optimizeExtended* method use the *optimizeNormal* method and the following optimize actions:
*rootToPrincipalRoot*, *powerArrays*,*arrayPower*, *functionToValues*, *negRootToI*,
*functionToValues*, *unnestingRadicals*, *functionToValues*, *radicalDenominatorToCounter*,
*rootIToSinCos*, *functionToValues*, *rootOfImagNumToCosISin*, *functionToValues*,
*nestedRadicals*, *imaginairDenominator*, *sinTwoCosTwo*, *cosXplusYtoSinCos*,
*sinXplusYtoSinCos*, *splitDenominator* and *expandArrays*
```py
>>> import symexpress3
>>> objExpress = symexpress3.SymFormulaParser( '5 * 2^2 + i * i + (4)^(1/2)' )
>>> objExpress.optimizeExtended()
>>> print( objExpress )
19 + [ (-2) | 2 ]
>>> print( objExpress.getValue() )
[17, 21]
```

### Optimize expression
Use the *optimize* method for optimization

Remove unnecessary () and optimize the internal structure
```py
>>> import symexpress3
>>> objExpress = symexpress3.SymFormulaParser( '((2) + (3))' )
>>> objExpress.optimize( None )
>>> print( objExpress )
2 + 3
```
Use of the optimize actions.
Use after *SymFormulaParser* and each *optimize(<action>)* an *optimize( None )*
Most of the time use *optimizeNormal()* instead of *optimize( None )*
```py
>>> import symexpress3
>>> objExpress = symexpress3.SymFormulaParser( 'cos( pi/4 )' )
>>> objExpress.optimize( None )
>>> objExpress.optimize( 'functionToValues' )
>>> objExpress.optimize( None )
>>> print( objExpress )
2^^(1/2) * (1/2)
```

### Output formats
MathMl output
```py
>>> import symexpress3
>>> objExpress = symexpress3.SymFormulaParser( 'cos( pi/4 )' )
>>> objExpress.optimize( None )
>>> print( objExpress.mathMl() )
```
Html output with expression in MathMl and string format.
It create the symexpress3_demo.html file in the current directory.
```py
>>> import symexpress3
>>> objExpress = symexpress3.SymFormulaParser( 'cos( pi/4 )' )
>>> objExpress.optimize( None )
>>> objOutput = symexpress3.SymToHtml( "symexpress3_demo.html", "SymExpress 3 demo" )
>>> objOutput.writeSymExpress( objExpress )
>>> objOutput.writeLine( str( objExpress ))
>>> objOutput.closeFile()
```

### Calculate value with variables
Define a dictionary for the variables. The key is the variable name and de value is a number.
```py
>>> import symexpress3
>>> objExpress = symexpress3.SymFormulaParser( '(x+1) (y+2)' )
>>> dictVar = {}
>>> dictVar[ 'x' ] = 0.33333
>>> dictVar[ 'y' ] = 3
>>> valueExpression = objExpress.getValue( dictVar )
>>> print( valueExpression )
6.66665
```

### Command line
python -m symexpress3

- *Help*: python -m symexpress3  -h
- *Direct optimize*: python -m symexpress3 "cos( pi / 4 )^^(1/3)"

### Graphical user interface
https://github.com/SWVandenEnden/websym3
