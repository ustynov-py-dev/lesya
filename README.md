# Lesya

Lesya is a simple Python package for declining Ukrainian personal names into Ukrainian grammatical cases (_відмінки_): NOMINATIVE, GENITIVE, DATIVE, ACCUSATIVE, INSTRUMENTAL, PREPOSITIONAL, and VOCATIVE (_називний, родовий, давальний, знахідний, орудний, місцевий, кличний_).

## Usage example

The most common usage is to convert a name into all cases:

```python
from lesya import Lesya

person = Lesya('Леся Українка')
print(person.nominative) # Леся Українка
print(person.genitive) # Лесі Українки
print(person.dative) # Лесі Українці
print(person.accusative) # Лесю Українку
print(person.instrumental) # Лесею Українкою
print(person.prepositional) # Лесі Українці
print(person.vocative) # Лесе Українко
```

When printing the `Lesya` object, you will get just nominative case:

```python
person = Lesya('Дмитро Андрійович Устинов')
print(person) # Дмитро Андрійович Устинов
```


You can also get a name in a specific case with square brackets:

```python
from lesya import Lesya
from lesya import CaseUA

person = Lesya('Тарас Григорович Шевченко')
print(person[CaseUA.DATIVE]) # Тарасу Григоровичу Шевченку
print(person[CaseUA.PREPOSITIONAL]) # Тарасові Григоровичу Шевченкові
print(person['орудний']) # Тарасом Григоровичем Шевченком
```

## Double names support

Lesya works well with double last names:
    
```python
from lesya import Lesya

person = Lesya('Іван Семенович Нечуй-Левицький')
print(person.forms)
# Output:
{
    'називний': 'Іван Семенович Нечуй-Левицький', 
    'родовий': 'Івана Семеновича Нечуя-Левицького', 
    'давальний': 'Івану Семеновичу Нечуєві-Левицькому', 
    'знахідний': 'Івана Семеновича Нечуя-Левицького', 
    'орудний': 'Іваном Семеновичем Нечуєм-Левицьким', 
    'місцевий': 'Іванові Семеновичу Нечуєві-Левицькому', 
    'кличний': 'Іване Семеновичу Нечую-Левицький'
}
```

## `forms` attribute

You can get all cases at once using the forms attribute. It returns a dictionary where the keys are case names (in lowercase Ukrainian), and the values are the corresponding declined names.

## Foreign names support

Lesya supports foreign names. However, since it does not use an ML model to automatically detect a person's gender, it works better if you explicitly provide the gender:

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
