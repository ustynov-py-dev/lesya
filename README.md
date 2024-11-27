# Lesya

This is a simple Python oackage convertin Ukrainian personal names to Ukrainian cases ( _відмінки_ ): NOMINATIVE, GENITIVE, DATIVE, ACCUSATIVE, INSTRUMENTAL, PREPOSITIONAL,VOCATIVE_ ('називний', 'родовий', 'давальний', 'знахідний', 'орудний', 'місцевий', 'кличний'_)

## Usage example

Most common usage is to convert a name to all cases:

```python
from lesya import Lesya

person = Lesya('Іван Сидоренко')
print(person.nominative) # Іван Сидоренко
print(person.genitive) # Івана Сидоренка
print(person.dative) # Івану Сидоренку
print(person.accusative) # Івана Сидоренка
print(person.instrumental) # Іваном Сидоренком
print(person.prepositional) # Івані Сидоренку
print(person.vocative) # Іване Сидоренко
```

Also you may want to get a name in a specific case :

```python
from lesya import Lesya
from lesya import CaseUA

person = Lesya('Тарас Григорович Шевченко')
print(person[CaseUA.DATIVE]) # Тарасу Григоровичу Шевченку
print(person[CaseUA.PREPOSITIONAL]) # Тарасові Григоровичу Шевченкові
print(person['орудний']) # Тарасом Григоровичем Шевченком
```

## Double names support

Lesya works well with doubled lastnames:
    
```python
from lesya import Lesya

person = Lesya('Іван Семенович Нечуй-Левицький')
print(person.forms)
{'називний': 'Іван Семенович Нечуй-Левицький', 
 'родовий': 'Івана Семеновича Нечуя-Левицького',
 'давальний': 'Івану Семеновичу Нечуєві-Левицькому', 
 'знахідний': 'Івана Семеновича Нечуя-Левицького',
 'орудний': 'Іваном Семеновичем Нечуєм-Левицьким', 
 'місцевий': 'Іванові Семеновичу Нечуєві-Левицькому',
 'кличний': 'Іване Семеновичу Нечую-Левицький'}
```

## forms attribute

You can get all cases at once using `forms` attribute. It will return a dictionary with all cases, where keys are case names (ukrainian in lower case) and values are names in corresponding cases.



## Foreign names support

Lesya supports foreign names, but since it has no ML model to automatically detect the person gender, it will work better if you provide gender explicitly:

```python
from lesya import Lesya
from lesya import CaseUA
from lesya import Gender

person = Lesya('Джозеф Байден', gender='male')  
print(person[CaseUA.DATIVE]) # Джозефу Байдену
print(person[CaseUA.PREPOSITIONAL]) # Джозефові Байденові

person = Lesya('Камала Гаріс', gender=Gender.FEMALE)
print(person[CaseUA.DATIVE]) # Камалі Гаріс
print(person[CaseUA.PREPOSITIONAL]) # Камалі Гаріс
```
