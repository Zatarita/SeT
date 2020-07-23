# SeT
## Saber editing toolkit

SeT is a set of python scrips dedicated towards editing saber files for halo 1 aniversary. It is still under development. Not everything has been mapped out yet; however, the tools will still be useful to anyone who wants to make their own tools for saber files. 

**__If you use the toolkit during development, things may change with updates__**

## s3dpaks
SeT will handle decompression for you; however, compression has still yet to be implimented.
To load a s3dpak you simply import the module, and create the object.
to do this you can pass the data in the constructor, or you can create a blank object, and call the load function on it. Optionally, you can pass hooks for the decompression status, and decompression percentage.

### s3dpak data passed on initialize
```python
from Saber.s3dpak import s3dpak
...
with open(file_path, "rb") as file:
    content = file.read()

saber_pak = s3dpak(content)
```

### s3dpak data passed after initialize
```python
from Saber.s3dpak import s3dpak
...
with open(file_path, "rb") as file:
    content = file.read()

saber_pak = s3dpak()
saber_pak.load(content)
```

### s3dpak data passed with hooks
```python
from Saber.s3dpak import s3dpak
...
with open(file_path, "rb") as file:
    content = file.read()

saber_pak = s3dpak(content, status_hook = print, percent_hook = print)
```

_When passing functions to the hooks, it's advised to use something more versitile than print. The percent hook returns a value between 0 and 1. If you want to get a percentage out of 100, it might be wise to create a function that multiplies the value by 100 and throws a % on the end._

## accessing the data inside of s3dpaks
There are a few different ways to access the data in the paks. You can reference them by index, or by name. 

If you want to access the data by name, it might be useful to know what names are available. To do this we can use the _names()_ function. This will return a list of available names in the s3dpak.


We can also reference data by index. We can find an index by name using the _find(name)_ function, and use the index as a parameter for _item_at_index(i)_ to get the item. We could also iterate through the items with the _item_count()_ function using _for i in range(saber_pak.item_count())_

### getting names
```python
from Saber.s3dpak import s3dpak
...
pak_names = saber_pak.names()
print(pak_names)
...
```

### referencing by name
```python
from Saber.s3dpak import s3dpak
...
print(saber_pak.items["SceneData"].data)
...
```

### finding an item and referencing by it's index
```python
from Saber.s3dpak import s3dpak
...
index = saber_pak.find("SceneData")
print(saber_pak.item_at_index(index).data)
...
```

### iterating through each item by index
```python
from Saber.s3dpak import s3dpak
...
for i in range(saber_pak.item_count()):
  print(saber_pak.item_at_index(i).data)
...
```
## editing the contents of the s3dpak
After accessing the items, we also need to be able to edit the items. At this level we can do a few different things. We can delete an item with _delete(name)_. we can import a file with _import_file(path, type)_. and we can export all of the items with _export_all(path)_.

We can also export data on the item level with _save(path)_

If we manually edit an item without using these functions. We'll need to update the file size and offsets with _recalculate_offsets()_

### deleting an item
```python
from Saber.s3dpak import s3dpak
...
#deleting by name
saber_pak.delete("SceneData")

#deleting by index
saber_pak.delete(saber_pak.item_at_index(0))

#if we manually delete the item, we adjust the offsets
del saber_pak.items["SceneData"]
saber_pak.recalculate_offsets()
...
```

### importing an item
```python
from Saber.s3dpak import s3dpak
...
saber_pak.import_file("File_location.extension", "Template")
...
```
_see item types below_

### exporting item(s)
```python
from Saber.s3dpak import s3dpak
...
#exporting the entire content of the s3dpak
saber_pak.export_all("export/") #it will automatically name it the name of the file

#exporting just one item
saber_pak.items["SceneData"].save("export/Scenedata") #must state the name of file
...
```

### Item types
>"Scene Data" : 0
>
>"Data" : 1
>
>"Single Player Lines" : 2
>
>"Shader" : 3
>
>"Textures Info" : 5
>
>"Sound Data" : 8
>
>"Memory" : 10
>
>"Skull Data" : 11
>
>"Template" : 12
>
>"String List" : 14
>
>"Game Logic" : 16
>
>"Breakable glass" : 17
>
>"Effects" : 18
>
>"(.grs)" : 22
>
>"Rain" : 25
>
>"(.cdt)" : 26
>
>"(.sm)" : 27
>
>"(.vis)" : 29
>

Each item has a numerical value that determines what type of file it is. When we import we must tell SeT what file type it is. We can either use the numerical value, or we can use the string name when using the import function. **Future versions of SeT will hopefully be able to determine file type based off content**


## Ipak
Set also supports the ipak format; however, it's not as flushed out as s3dpak yet. It has a similar structure as the s3dpak; however, until it's fully finished this will remain blank

**TODO - FILL THIS OUT**

## SceneData
SeT has the SceneData file mapped out. It's a fairly simple format. SceneData is just a collection of a list of strings.
To create a SceneData object just import the module, and pass the data. You can pass the data at initialize, or pass the data after with the _load(data)_ function

### Initializing a SceneData object
```python
from Saber.s3dpak import s3dpak
from Saber.Definitions.scene_data import scene_data
...
with open(file_path, "rb") as file:
    content = file.read()

saber_pak = s3dpak(content)
#initialize with data
SceneData = scene_data(saber_pak.items["SceneData"])
#initialize, then load data
SceneData2 = scene_data()
SceneData2.load(saber_pak.items["SceneData"])
```

### Manipulating the SceneData
Since the SceneData object is just a list of strings, you can simply edit them like any other python list. There is two special functions though and they are the _compile_data()_ function, and _save(path)_ function. compile_data will take the lists, and format them into the format saber needs, and save will compile the data, and save it to disk.

### Editing SceneData, reimporting the edit, and saving to disk
```python
from Saber.Definitions.scene_data import scene_data
...
#Put the edits back into the s3dpak
SceneData = scene_data(saber_pak.items["SceneData"].data)
SceneData.Templates.append("Example_item")
saber_pak.items["SceneData"].data = SceneData.compile_data()
#save the edits to disk
SceneData.save("file/location.extension")
```

### Content of SceneData
>SceneData[]
>
>CacheBlock[]
>
>Textures[]
>
>SoundData[]
>
>Templates[]
>
>VoiceSplines[]
>
>Scene[]
>
>Hkx[]
>
>TexturesDistanceFile[]
>
>CheckPointTexFile[]
>
>SceneRain[]
>
>SceneGrs[]
>
>SceneCDT[]
>
>SceneSM[]
>
>SceneVis[]
>

##TexturesInfo
Textures info is basically the same concept as SceneData. It is simply a list of strings. There is other data available in the TexturesInfo file; however, they seem to consistantly be the same. (0,0,0,1,1,1,0 if you're curious) 

To load the data it's basically the same as everything else. You load the data by creating a textures_info object and pass the data at initialize, or _load()_ it manually.

### Loading a TexturesInfo object
```python
from Saber.s3dpak import s3dpak
from Saber.Definitions.scene_data import textures_info
...
with open(file_path, "rb") as file:
    content = file.read()

saber_pak = s3dpak(content)
#initialize with data
TexturesInfo = textures_info(saber_pak.items["TexturesInfo"])
#initialize, then load data
SceneData2 = scene_data()
SceneData2.load(saber_pak.items["TexturesInfo"])
```

### Manipulating TexturesData
After loading the contents of the data, we have a few options. We can add an entry with _add_entry(string)_, we can add multiple entries with _add_entries([strings])_ and we can delete an entry with _delete(string)_

### Editing TexturesData
```python
from Saber.Definitions.scene_data import textures_info
...
#Put the edits back into the s3dpak
TexturesInfo = textures_info(saber_pak.items["TexturesInfo"])
TexturesInfo.add_entry("Example_item")
TexturesInfo.add_entries(["Example_item1", "Example_item2"])
TexturesInfo.delete("Example_item1")
```

### Saving the changes
After editing the data, we can either save the changes to disk, or we can reattach them to the s3dpak. Just like with SceneData, we can _compile_data()_ to get the data formatted correctly, or we can call _save(path)_ to save a copy to disk

### Storing the changes
```python
from Saber.Definitions.scene_data import scene_data
...
#Put the edits back into the s3dpak
TexturesInfo = textures_info(saber_pak.items["TexturesInfo"])
TexturesInfo.add_entry("Example_item")
saber_pak.items["TexturesInfo"].data = TexturesInfo.compile_data()
#save the edits to disk
TexturesInfo.save("file/location.extension")
```

currently this is all that has been developed. More to come
