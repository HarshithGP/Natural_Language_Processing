# French Number Speller

Project description
- Designed a Finte State Automata to spell out French Numbers from 0 - 999 from it's equivalent Arabic numeric. 
- Implemented the design using Python NLTK library (FST module) to build a transducer comprising of 29 states ( 2 non terminal and 27 terminal ).
- The French Language uses a mixture of decimal(base 10) and vegesimal(base 20) system which adds to the complexity of the design process.
- Successfully implemented the design and accurately generated the French spellings for numbers from 0 - 999 using Natural Language Processing principles.

# Soundex Code Generator using Finite State Transducers

Project description
- Designed a Finite State Automata to generate the Soundex Code for a person's name and developed 3 transducers using the fst module of the python's nltk library to implement the design. 
- A soundex code comprises of the first letter of a given name followed by 3 digits based on the phonetic soundex algorithm commonly used by the Census Bureau to represent names as pronounced in English.
- The automata consists of 8 states ( 1 non terminal and 7 terminal ) and is designed to handle both truncation( in the event the no of digits exceed 3) as well as padding( in the event there are fewer than 3 digits ) operations.
