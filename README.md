[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Build Status](https://travis-ci.org/gvannest/expert_system.svg?branch=master)](https://travis-ci.org/gvannest/expert_system)


# Expert System

Expert System is a project as part of the 42 algorithmic curriculum.
The aim of this project is to build an expert system. It consists of a set of logical rules given as inputs,
as well as initial facts (line starting with the `=` sign) which are considered to be true.
Finally, the input file also contains a set of queries (line starting with the `?` sign) which are the element to be proved using the set of rules and initial facts.

The subject include some constraints such as using a backward chaining inference method.

## Input

The input is a .txt file containing the rules, initial facts and queries.
It has to be passed to the program as an argument (see the *Usage* section below).

Example of an input file :

```
#You can also add comment

    #Wherever you want in the file

C => E
A + B + C => D
A | B => C
A + !B => F
V ^ W => X              #And it would still work as expected
C | !G => H
C | G => X + V
E + F => !V
A + B => C
#A + B => !C

=ABG
#Add also one here if it pleases you!

?GVXC
```


## Usage

You need to have python 3 installed on your machine.

``` python3 expert_system.py [-i] [-u] [-v] filename```

**Positional arguments (= required):**

Argument         | Description              
:----------------|:-----------------------
filename         | Path to the text file with the rule set, facts and queries to be solved|
  

**Optional arguments :**

Short flag       | Long flag              | Description
:----------------|:-----------------------| :---------------------------|
  -h             | --help                 |    Show help message
  -i             | --interactive          |    Interactive facts mode, where the user can change facts or add new facts
  -u             | --undetermined         |    Undetermined mode, where the user can clarify undetermined facts
  -v             | --verbose              |    Verbose mode. Outputs the rules leading to a particular conclusion


## Results

Program will output the status (i.e. `true`, `false` or `undetermined`) of each element in the query list.
For example, if the query is `?ABC`, we may have an output of this kind:

```
A is true
B is true
C is false
```

## Unit tests

Running `pytest xs_tests.py` will launch a set of unit tests. You can fin the different tests inputs and outputs in the `tests` folder.
These tests are also used for CI.