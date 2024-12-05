The English version of the README.md file was created by a translator. Therefore, the translation may not be accurate. If you can use Korean, we recommend that you view the Korean document.
[한국어 문서 바로가기(korean)](https://github.com/yhg4908/ranpick.py/blob/main/README_KR.md)

# Ranpick



Ranpick complements the shortcomings of the existing PRNG method and generates random numbers with nanoseconds and hash-based systems.

A system using text is also currently being developed.

---



## Installation



1. Use 'pip' to install the lanpick:

   ```bash
   pip install ranpick
   ```
2. Add the import statement below to the code (.py) to import the ranpick:

   ```python
   from Rankick import
   ```
3. The import statement below allows you to import all modules:
   
   ```python
   from ranpick import *
   ```



## Modules and Use Guides


As of `2024.12.3 (KST)`, the modules currently available are as follows.

- number: `Produces a random number in the form of a number`


### number - Generating a numeric random number


`Number` generates a random number in the form of a normal number.

You can generate numbers up to 100000000.

The number module can be imported into the import statement below.
```python
from ranpick import number
```


#### The basics



The number module can be used in the following ways.
```python
random_number = ranpick.number()  # random_number variable, store the random number (~100000000) that is selected as the random number module.

print(random_number) # print_number The value of the variable random_number.
print(ranpick.number()) #rampicknumber Outputs the value of the random number drawn by the module.
```
This is the basic method of using the number module. You can generate random numbers with `ranpick.number()`.


#### Limiting the Number of Random Numbers



You can also limit the number of random numbers. The example code below limits random numbers to between 5 and 10.
```python
limit_number = ranpick.number(5, 10)

print(limit_number)
print(ranpick.number(5, 10))
```
`ranpick.number(5, 10)` is a code that limits the number of random numbers to between 5 and 10. You can complete it by adding `starting numbers, arriving numbers` in `()`.

Calculations such as ' `2+3,10/2` can also be used to limit the number of random numbers and can be used in all the contents to be described later.


#### Set decimal place



By default, a generated random number can only be generated with integers. However, if you refer to the example below, you can output a small number of outputs.
```python
decimal_number = ranpick.number(0, 1, d3)

print(decimal_number)
print(ranpick.number(0,1(d3))
```
This example code is a code that outputs numbers between 0 and 1 up to three decimal places. `(d3)` means that it outputs up to three decimal places.

If `(d4)` is used, it can be output up to four decimal places.

It can be up to 10 digits.


#### Application



The codes below are created by applying this module, other libraries, and modules. In addition to the examples used here, a variety of other libraries and applications are possible.

##### DataTime Library Application
Below is the code applied using the datetime library.
```python
from ranpick import number
from datetime import datetime

date_number = int(datetime.now().strftime("%Y%m%d%H%M%S"))

print(ranpick.number(date_number, date_number × 10))
```
This code was made to output random numbers by leveraging the time output from the datetime library.

##### Ramdom Module Application
Below is the code applied using the random module.
```python
from ranpick import number
import random

random_number = random.randint(1,10)

print(random_number, 100)
```
This code generates another random number by using the random number output from the random module. It can be applied to produce almost unpredictable random numbers.

However, using this type of code is not recommended because it requires a lot of resources on your computer.


## Bug report


Please report bugs on the site below (github).

<https://github.com/yhg4908/ranpick.py/issues>
