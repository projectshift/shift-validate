[![Build Status](https://api.travis-ci.org/projectshift/shift-schema.svg)](https://travis-ci.org/projectshift/shift-schema)

# shift-schema


Filtering and validation library for Python3. Can filter and validate data in 
model objects and simple dictionaries with flexible schemas. 

Because validation and filtering of data with form objects seems to be
the trend in web frameworks but it never felt right.

Main idea: decouple filtering and validation rules from web forms into
flexible schemas, then reuse those schemas in forms as well as apis and cli.

## model:

You can use any kind of object or a dictionary as your model.
If you use filtering model will be changed in-place by applying 
the filters you define. 

## schema:


Schema is a collection of rules to filter and validate properties of your
model (object or dictionary). There are several ways to create a schema
the simples being initialization from spec dictionary:

```python
from shiftschema.schema import Schema
from shiftschema import validators as validator

schema = Schema({
    'properties': {
        'name' = dict(
            required=True,
            validators = [validator.Length(min=3, max=100)]
        ),
        'email' = dict(
            validators = [validator.Email()]
        )    
    }
})
```

Alternatively you can create a schema by subclassing Schema object:

```python
from shiftschema.schema import Schema
from shiftschema import validators as validator

class MySchema(Schema):
    def schema(self):
        self.add_property('name')
        self.name.required=True
        self.name.add_validator(validator.Length(min=3, max=100))
        
        self.add_property('email')
        self.email.add_validator(validator.Email)

schema = MySchema()
```

## validation:

You can then use this schema to filter and validate your model data, or `process` it (filter and validate as single operation).
To validate a model pass it to your schema and get back `Result`:

```python
model = dict(name=None, email='BAD')
valid = schema.process(model)
print(valid == True) # False - validaation failed
print(valid.errors) # errors: name='Required', email='Invalid'
```

There is a number of common validators provided and you can easily plug your own.

## filtering:

You can attach filters to your schema. Those will be applied in turn and update model data in-place before doing any validations.

```
person = Person(name='   Morty   ', birthyear = 'born in 1900')
schema = Schema({
    'properties': {
        'name': dict(
            filters: [Strip()]
        ),
        'birthyear': dict(
            filters: [Digits(to_int=True)]
        )
    }
})

print(person.name) # 'Morty' (stripped of spaces)
print(person.birthyar) # 1900 (int)
```

As with validators there are some filters provided and you can easily plug your own.

## errors are objects:

Validation on a model gets you a `Result` objects that evaluates to boolean
`True` or `False` depending on if it was valid or not:

```python
valid = schema.validate(model)
valid # shiftschema.result.Result
bool(valid) # False, if has errors
```

All the errors the result contains are `Error` objects that 
simple validators (like `Length`)return. You can easily get those errors as string 
messages with:

```python
errors_dict = result.get_messages()
```

All errors are translated, so you can have them in any language supported
by passing a locale (defaults to 'en'):

```python
errors_dict = result.get_messages(locale='en') # translate to locale
```

## translation:

You can pass `translator` and `locale` to `Result` object manually but
the most easy way to use translations is through globally available
`Translator` that exists on the `Schema`. Schemas will inject this translator
and locale in to result objects they create. So you can simply:

```python
from shiftschema.schema import Schema

Schema.translator # preconfigured with default translations
Schema.translator.add_.location(path) # but you can add your own
Schema.locale # is 'en' by default
Schema.locale = 'ru' # but you can change that
```

After setting those you will get errors by default in Russian with
your custom translations loaded.

```python
valid = schema.validate(model)
if not valid:
    valid.get_messages() # in russian per global setting
    valid.get_messages(locale='en') # or whatever you specify
```

