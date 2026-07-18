#### How to create Dictionaries

**dict()** is a data type in python pl, and hence can be used directly to store data values in key : value pairs. Dictionaries can also be created in a traditional way by using the ``var_name { }`` method 

1. Traditional Method **``var_name { }``**
```
thisdict = {
		'brand' : 'Ford',
		'model' : 'Mustang',
		'year' : '2021'
	}
print(thisdict)
```

2. Using the **`dict( )`** data type method
```
thisdict = dict (
		name = "John",
		age = 36,
		country = "Norway"
		
	)  
print(thisdict)
```

#### When to use either
In everyday Python programming:
-  Use **`{}`** most of the time. It's shorter, more flexible, and is the standard style.
-  Use **`dict()`** when:
    -  you're converting another data structure into a dictionary,
    -  or you prefer the keyword-argument syntax for simple keys.
- Generally just use **`{}`** ~ Similar to creating sets

#### Python Collections (Arrays)
There are four collection data types in the Python programming language:

- **[List](https://www.w3schools.com/python/python_lists.asp)** is a collection which is ordered and changeable. Allows duplicate members.
- **[Tuple](https://www.w3schools.com/python/python_tuples.asp)** is a collection which is ordered and unchangeable. Allows duplicate members.
- **[Set](https://www.w3schools.com/python/python_sets.asp)** is a collection which is unordered, unchangeable*, and unindexed. No duplicate members.
- **Dictionary** is a collection which is ordered** and changeable. No duplicate members

#### Accessing Items
You can access the items of a dictionary by referring to its key name, inside square brackets:
```
thisdict ={  
    "brand": "Ford",  
    "model": "Mustang",  
    "year": 1964  
}  
x = thisdict["model"]  
print (x)  
#OR  
print (thisdict["model"]) # without creating a var "x"

```

Also by using the method `.get`
```
thisdict =	{
	"brand": "Ford",
	"model": "Mustang",
	"year": 1964
}

x = thisdict.get("model")

print(x)

```

##### Using the `.keys()` method to list (display) all keys in the dictionary.
Remember an item in a dictionary has two attributes `keys : value ` think of it like identifiers.  Example ;
```
key : value =  firstname : " John "
<!-- firstname is the key, john is the value -->
```

A dictionary stores data as `key : value` pairs.
- The **key** is like a label or identifier.
- The **value** is the information associated with that key.

- - - 

```
thisdict = {
	  "brand": "Ford",
	  "model": "Mustang",
	  "year": 1964
}

x = thisdict.keys()

print(x)

>> dict_keys(['brand', 'model', 'year'])

```


##### Using the `.values()` method to list (display) all keys in the dictionary.
Just  like the `` .keys`` method display  the keys of a dictionary, ``.values`` method displays the value

##### Using the `.items()` method to list (display) all items "grouped" in the dictionary.
The `items()` method will return each item in a dictionary, as tuples in a list.

Example: 
```
thisdict = {
	  "brand": "Ford",
	  "model": "Mustang",
	  "year": 1964
}

x = thisdict.items()

print(x)

>> dict_items([('brand', 'Ford'), ('model', 'Mustang'), ('year', 1964)])

```

#### Changing Values
You can replace the value of an item by using two  methods ;

1.  Referring to it's key name
```
thisdict = {  
	  "brand": "Ford",  
	  "model": "Mustang",  
	  "year": 1964  
}  
  
x = thisdict["year"] = 2022  
  
print(x) 
>> 2022

```

2.  By Using the .update() method
```
thisdict = {
	  "brand": "Ford",
	  "model": "Mustang",
	  "year": 1964
}
thisdict.update({"year": 2020})

print(thisdict)

```

#### Adding Item
You can add new item to a dictionary by using two methods ;

1.  Adding a new index key and assigning a value to it
```
thisdict =	{
	  "brand": "Ford",
	  "model": "Mustang",
	  "year": 1964
}
thisdict["color"] = "red"

print(thisdict)
```

2.  Using the ``.update ()`` method
```
thisdict = {
	  "brand": "Ford",
	  "model": "Mustang",
	  "year": 1964
}
thisdict.update({"color": "red"})

print(thisdict)

```

#### Removing an Item
There are about 3 ways to remove an item

1. The `pop()` method removes the item with the specified key name:
```
thisdict =	{
	  "brand": "Ford",
	  "model": "Mustang",
	  "year": 1964
}
thisdict.pop("model")

print(thisdict)

>> {'brand': 'Ford', 'year': 1964}
# Removes the entire model item
```

2. The `popitem()` method removes the last inserted item
```
thisdict =	{
	  "brand": "Ford",
	  "model": "Mustang",
	  "year": 1964
}
thisdict.popitem()

print(thisdict)

>> {'brand': 'Ford', 'model': 'Mustang'}
# Removes the last added item - year : 1964
```

3. The `del()` keyword removes the item with the specified key name
```
thisdict =	{
	  "brand": "Ford",
	  "model": "Mustang",
	  	"year": 1964
}
del thisdict["model"]

print(thisdict)

>> {'brand': 'Ford', 'year': 1964}
# Deletes the entire model item from the var thisdict dictionary

also .clear clears the entire dictionary
thisdict.clear()
```
