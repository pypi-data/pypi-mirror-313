The English version of the README.md file was created by a translator. Therefore, the translation may not be accurate. If you can use Korean, we recommend that you view the Korean document.
[한국어 문서 바로가기(korean)](https://github.com/yhg4908/ranpick.py/blob/main/README_KR.md)

# Ranpick



Ranpick complements the shortcomings of the existing PRNG method and generates random numbers with nanoseconds and hash-based systems.


---



## Installation



1. Use 'pip' to install the ranpick:

   ```bash
   pip install ranpick
   ```
2. Add the import statement below to the code (.py) to import the ranpick:

   ```python
   import ranpick
   ```



## Modules and Use Guides


As of `2024.12.3 (KST)`, the modules currently available are as follows.

- rannumber: `Produces a random number in the form of a number`
- ranrandom: Select a random value from the list. (Applicable starting from 2.1.0)



### number - Generating a numeric random number


`Number` generates a random number in the form of a normal number.

You can generate numbers up to 100000000.



#### The basics



The number module can be used in the following ways.
```python
random_number = ranpick.rannumber()  # random_number variable, store the random number (~100000000) that is selected as the random number module.

print(random_number) # print_number The value of the variable random_number.
print(ranpick.rannumber()) #rampicknumber Outputs the value of the random number drawn by the module.
```
This is the basic method of using the number module. You can generate random numbers with `ranpick.number()`.


#### Limiting the Number of Random Numbers



You can also limit the number of random numbers. The example code below limits random numbers to between 5 and 10.
```python
limit_number = ranpick.rannumber(5, 10)

print(limit_number)
print(ranpick.rannumber(5, 10))
```
`ranpick.number(5, 10)` is a code that limits the number of random numbers to between 5 and 10. You can complete it by adding `starting numbers, arriving numbers` in `()`.

Calculations such as ' `2+3,10/2` can also be used to limit the number of random numbers and can be used in all the contents to be described later.


#### Set decimal place



By default, a generated random number can only be generated with integers. However, if you refer to the example below, you can output a small number of outputs.
```python
decimal_number = ranpick.rannumber(0, 1, "d3")

print(decimal_number)
print(ranpick.number(0,1, "d3"))
```
This example code is a code that outputs numbers between 0 and 1 up to three decimal places. `"d3"` means that it outputs up to three decimal places.

If `"d4"` is used, it can be output up to four decimal places.

It can be up to 10 digits.


#### Application



The codes below are created by applying this module, other libraries, and modules. In addition to the examples used here, a variety of other libraries and applications are possible.

##### DataTime Library Application
Below is the code applied using the datetime library.
```python
import ranpick
from datetime import datetime

date_number = int(datetime.now().strftime("%Y%m%d%H%M%S"))

print(ranpick.rannumber(date_number, date_number × 10))
```
This code was made to output random numbers by leveraging the time output from the datetime library.

##### Ramdom Module Application
Below is the code applied using the random module.
```python
import ranpick
import random

random_number = random.randint(1,10)

print(random_number, 100)
```
This code generates another random number by using the random number output from the random module. It can be applied to produce almost unpredictable random numbers.

However, using this type of code is not recommended because it requires a lot of resources on your computer.

### ranrandom - Random Value Selection
`ranrandom` selects and outputs a random value from a list.

#### Basic Usage
You can use the `ranrandom` module as shown below:
```python
random = ranpick.ranrandom("left", "right", "center", "miss")

print(random)
print("left", "right", "center", "miss")
```
You can use `ranpick.ranrandom()`. Inside the parentheses, you can input items in a format such as `("win", "miss")`.
One of the items listed here will be randomly selected.
At least two items must be provided.

#### Setting Probabilities
You can set the probabilities for each item. Please refer to the example code below:
```python
random = ranpick.ranrandom(("left", 33), ("right", 33), ("center", 33), ("miss", 1))

print(random)
print(("left", 33), ("right", 33), ("center", 33), ("miss", 1))
```
You can add another pair of parentheses `()` inside the main `()`.
Within this added `()`, you can specify items in the format `("item_name", probability[%])`.
The total sum of all probabilities must equal 100, otherwise an error will occur.
```python
print("left", ("right", 50), "center", "miss")
```
If some probabilities are omitted as shown above, the remaining probabilities will be automatically redistributed among the unspecified items.

## Bug report


Please report bugs on the site below (github).

<https://github.com/yhg4908/ranpick.py/issues>
