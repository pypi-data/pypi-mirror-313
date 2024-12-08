# This is RTS_Simpledatabase

a little module for Python to create databases.

### Update notes

- added Events
you can now add an @DatabaseEvent.<on_create, on_update, on_delete>(databasename) on a function and get the record being proccessed by one of these events

# How to use

For the "How to use" lets get some sample data:

| fieldname      | userid        | displayname   | balance  | joined     | note  
|----------------|---------------|---------------|----------|------------|-------
| example value  | 9783836285131 | randomtimetv  | 6.50     | 31.03.2024 |       
| format         | str           | str           | float    | str        | str   
| state          | unique        | modular       | modular  | locked     | loose 

# Initiate the database
```py
from RTSDataBase import DB
Database = DB('users') #creates or reads the users.rtsdb

# does not overwrite headers if there are headers already present
# all 3 (fields, format, states) are required and have to have the same length (in this case 5 entries)
Database.setHeaders({ 
    "fields": ["userid", "displayname", "balance", "joined", "note" ], 
    "format": ["str",    "str"        , "float"  , "str"   , "str"  ], 
    "states": ["unique", "modular"    , "modular", "locked", "loose"]
})
```



# Create a record
```py
Database.create({
    "userid": "9783836285131",
    "displayname": "randomtimetv",
    "balance": 6.50,
    "joined": "31.03.2024" # dd.mm.yyy
})
```
Note: As you can see the .create() does not set the "note" field, this is because of the state being "loose", more to that in the **States and Formats** section.

# Read a record
```py
# selectorFieldName is idealy a unique, locked or index field like in this case "userid"
# selectorFieldValue is the known full value of selectorFieldName in this case "9783836285131"
# specificFieldNameToRead can be specified to obtain the value of a single field of the specified record
# if no field is given it returns the full record

# Syntax: Database.read({<selectorFieldName>:<selectorFieldValue>, [field=specificFieldNameToRead]})

Database.read({"userid":"9783836285131"})
# Returns: {"userid": "9783836285131","displayname": "randomtimetv","balance": 6.50,"joined": "31.03.2024"}

Database.read({"userid":"9783836285131"},"displayname")
# Returns: "randomtimetv"

```
Does not return errors.

# Update a record
```py
# selectorFieldName is idealy a unique, locked or index field like in this case "userid"
# selectorFieldValue is the known full value of selectorFieldName in this case "9783836285131"
# targetField is the field you want to update, let's say "balance" needs to be updated
# newValue is the, you might have guessed it, new Value you want to set, lets say: 19.0

# Syntax: Database.update({<selectorFieldName>:<selectorFieldValue>}, <targetField>, <newValue>)

Database.update({"userid": "9783836285131"}, "balance", 19.0)
```
<br/>If something went wrong, like you tried to set the wrong type, you get:
```
 InvalidType: "balance" does not match typerule "float" in: {'balance': '19'}
```
More to these errors in **States and Formats**
<br/><br/>Trying to update locked fields results in:
```
 LockedField: "joined" can not be updated.
```


# Search records
```py
# Note: find is best used if you have a UserInterface with a search field
# query can be the full value or just a section of the actual value
# fieldname is by default __any and searches ALL fields except __id if they atleast partially contain query, specify to limit the search to a single field
# case_sensitive is by default True
# allow_typo is by default False

# Returns a list of all matching records

# Syntax: Database.find(<query type:string>, [fieldname=<fieldName>], [case_sensitive=<True|False>], [allow_typo=<True|False>])

Database.find("Random", fieldname="displayname")
# Returns: [] because "Random" is not contained in "displayname" ("random" would be contained)

Database.find("Random", fieldname="displayname", case_sensitive=False)
# Returns: [{"userid": "9783836285131","displayname": "randomtimetv","balance": 6.50,"joined": "31.03.2024"}]
# because this time case_sensitive is turned off
```
Does not throw errors.


# Test if a record exists
```py
# selectorFieldName is idealy a unique, locked or index field like in this case "userid"
# selectorFieldValue is the known full value of selectorFieldName in this case "9783836285131"

# Returns a boolean

# Syntax: Database.exists({<selectorFieldName>:<selectorFieldValue>})

Database.exists({"userid","9783836285131"})
# Returns: True
```
Does not throw errors.

# Delete a record
```py
# __id is the hidden and unique id of the record
# Syntax: Database.delete(<__id>)

Database.delete(1)
# Deletes the record with the __id 1

Database.delete(Database.read({"userid":"9783836285131"}, "__id"))
# Deletes the record 
```
Does not throw errors.

# Mass data output (dumping)
```py
Database.header
# Returns a list of all present headers

Database.dump_header()
# Returns the full header segment with the fieldnames, types and states

# suported formats: csv, plain  
Database.formated_dump(format)
# plain is default, it returns the data as it is saved 
# csv, returns the database formated in csv seperated by "|"
```

# States and Formats


The State of a field can have following values:
```
unique  = field can be changed but must contain a unique value among all records, only applies to the same field
locked  = field needs to be set in .create(), can not be changed afterwards
modular = field can be updated without restrictions
index   = locked and unique
loose   = field can remain unset or undefined and is modular
```
All fieldtypes, except "loose", need to be set by their rules in .create() otherwise it will throw an error like 
```
 MissingField: "displayname" is missing in: {"userid": "9783836285131","balance": 6.50,"joined": "31.03.2024"}
```

<br/>There are a few supported formats as of now:
```
__any = ignores type notations, aka can have any type. Is not recommended
str, list, dict, bool, float, int = only accepts its propper type as value
nostr, nolist, nodict, nobool, nofloat, noint = accepts it's propper type or None as value
```
If there is a Type mismatch you get:
```
 InvalidType: "userid" does not match typerule "str" in: {"userid":9783836285131,"displayname": "randomtimetv","balance": 6.50,"joined": "31.03.2024"}
```