# t1
Тема 1. Обработка исключений

[Python Pet Orm](https://github.com/cyrillelamal/x3PORM)


# x3PORM
Python pet PostgreSQL ORM
## Getting started
The module functions like Django or SQLAlchemy ORM.
### Establish connection
To establish connection use method `set_connection` of `PORM` static class.
```python
import psycopg2
import PORM as p

settings = {'user': 'user_name', 'port': '5432', ... }
# Either
p.PORM.set_connection(**settings)
# Or

p.PORM.set_connection(psycopg2.connection(**settings))
```
To close the connection use method `close_connection` of `PORM` static class.
### Create models
A model is a class inherited from `Model` class.
Fields of the model are instances of abstract class `FieldType`. 
You must not use `FieldType` instances!  
Use classes like `Integer`, `Varchar`, `ForeignKey` instead.  
The primary key field can be omitted so you have to define it yourself.  
To define a ForeignKey pass parameter `references` as `str` or `Model` subclass
```python
class Book(p.Model):
    id = p.Integer(primary_key=True, serial=True)
    title = p.Varchar()
    author_id = p.ForeignKey('Author')
    year = p.Integer(not_null=True)

class Author(p.Model):
    id = p.Integer(primary_key=True, serial=True)
    name = p.Varchar()
    dob = p.Integer()

class Wrapper(p.Model):
    uid = p.Integer(primary_key=True)
    book = p.ForeignKey(Book)
```
#### About polymorphic Varchar
If you are looking for `Text`, use `Varchar` with parameter `length` equals None.
```python
class Post(p.Model):
    body = p.Varchar(length=None, not_null=True)
# body TEXT NOT NULL,
```
Are you looking for `Char`? Use `Varchar` with parameter `varchar` set to False.
```python
class Card(p.Model):
    number = p.Varchar(length=16, varchar=False, unique=True)
### number CHAR (16) UNIQUE,
```
You can create instances of model. Fields of instance are available before saving but not
entirely, e.g. serial values will be set only after saving
```python
class Author(p.Model):
    id = p.Integer(primary_key=True, serial=True)
    name = p.Varchar()
    dob = p.Integer()

paul = Author(name='Jean', dob=1337)
paul.name
# 'Jean'
```
If a field not described in model is passed so `AttributeError` is raised.
```python
paul = Author(undefined='lol')
# AttributeError: The model Author has no column undefined}
```
You can get or set primary key value of the model using its `pk` property 
without knowing its name.
```python
paul.pk = 100
paul.pk
# 100
paul.id
# 100
```
#### Save or update
Use the method `save` of instance.
```python
paul.save()
```
#### Delete
Use the method `delete` of instance.
```python
paul.delete()
```
### Create tables
Use the function `create_tables`. All models inherited from `Model` will be considered.
```python
import PORM as p

class Book(p.Model):
    id = p.Integer(primary_key=True, serial=True)
    title = p.Varchar()
    author_id = p.ForeignKey('Author')
    year = p.Integer(not_null=True)

class Author(p.Model):
    id = p.Integer(primary_key=True, serial=True)
    name = p.Varchar()
    dob = p.Integer()

class Wrapper(p.Model):
    uid = p.Integer(primary_key=True)
    book = p.ForeignKey(Book)

p.create_tables()
```
the function returns string with sql script.
### Queries
Use method `query()` of a `Model` subclass. It is a builder for chainable queries.  
There are statements: `limit`, `offset`, `order`, `group_by`, `filter`. The end of query
is indicated with the method `do`.  
By default all rows are chosen.
```python
author = Author.query().filter(id=10)
books = Book.query().filter(author=author).limit(100).group_by('year').do()
```
#### Filter
Pass key-word parameters matching pattern `{field_name}[__{token}][__...]={value}`. The
`token` is a django like statement, e.g. `iexact` matches case-insensitive strings.
```python
books = Book.query().filter(title__iexact='As Is? Or as is?')
```
### Extensions
#### Factories
The method `do` of query instances takes the parameter `factory`. You can set key - 
*factory name* and value - *name of the method-factory*. That method must get one
parameter **rows** returned by psycopg2.  
Query returns row with all values of the graph describing the model (DFS is used).
Model names (got with DFS) are in `model_names` attribute, row values (got with DFS)
are in `rows` parameter.  
The class method `column_by_name` of `Model` may be useful in this case. It returns `Column`
instance with column properties, name, etc.
#### Field types
Inherit from `FieldType`. Pass to the super constructor all not specific values as dict.
Then redefine `__str__`. It represents the described column while table creation. You
can get common representation with `.base_repr` method describing common properties
as `primary_key`, `unique`, etc.
