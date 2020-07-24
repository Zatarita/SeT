# SeT
## Saber editing toolkit

SeT is a set of python scrips dedicated towards editing saber files for halo 1 aniversary. It is still under development. Not everything has been mapped out yet; however, the tools will still be useful to anyone who wants to make their own tools for saber files. 

**__If you use the toolkit during development, things may change with updates__**

Table of contents:  
[s3dpak](#s3dpaks)  
[ipak](#ipak)  
[imeta](#imeta)  
[fmeta](#fmeta)  
[SceneData](#scenedata)  
[TexturesInfo](#texturesinfo)

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
saber_pak.export_all("export/") #it will automatically name

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
to load a ipak import the module, and create the object.
You can pass the data at initialize, or you can create a blank object, and pass the data with the _load_ function.
```python
from Saber.ipak import ipak
...
with open(file, "rb") as file:
    content = file.read()
ipak_object = ipak(content)
#pass the data after initialize
ipak_object = ipak()
ipak_object.load(content)
```

## accessing ipak contents
__IPAK IS CURRENTLY INCOMPLETE, MAY NOT WORK AS INTENDED__
__Ipak requires 64 bit python. You wont have enough memory to decompress an ipak on 32 bit (will add failsafe to use file buffer in future)__

The ipak consists of a list of imetas, and their coorosponding texture data. The items variable in the ipak object holds the imeta information, and the and the items.data object holds the ipak data. The structure of an ipak is fairly large.

### item content
>imeta (see imeta for more information on the structure)
>
>data.width
>
>data.height
>
>data.unknown = 1
>
>data.face_count
>
>data.type
>
>data.mipmap_count
>

### accessing the information
accessing the information is similar to s3dpaks. You need to know the name of the data you wish to access. to do this you can use the _names()_ function to get a list of available names in the ipak. then you reference the item using one of those names. You can also access items by index by using _find(string)_, and _item_at_index(index)_.
```python
from Saber.ipak import ipak
...
ipak_names = ipak_object.names()
print(ipak_names[0])
index = ipak_object.find("xbox_rt_b")
if index = -1: print("Texture not found with that name")
else: print(ipak_object.item_at_index(index).data.type)
```
>in this example, we assume there is a texture named "xbox_rt_b", if it didnt exist, find would return -1

### Modifying the information
currently this part is what is under development. Adding textures to the imeta requires analyzing a dds header and extracting the information to populate the data. Not difficult, but to be done. You CAN currently delete data
```python
from Saber.ipak import ipak
...
ipak_object.delete("xbox_rt_b")
```

### Saving
There are a few ways to save ipak data. you can save the entire file with _save(path)_, you can save an individual item with _items[x].save(path)_, or you can save just the dds raw data without the header with _items[x].save_rawdata(path)_.
```python
from Saber.fmeta import ipak
...
index = ipak_object.find("xbox_rt_b")
if index = -1: print("Texture not found with that name")
ipak_object.item_at_index(index).save("path/to/file")             # save with saber header data
ipak_object.item_at_index(index).save_rawdata("path/to/file")     # save texture data without header
ipak_object.save("path/to/save.ipak")                             # save the entire ipak file
```

## Imeta
__IPAK IS CURRENTLY INCOMPLETE, MAY NOT WORK AS INTENDED__

to load a imeta import the module, and create the object.
You can pass the data at initialize, or you can create a blank object, and pass the data with the _load(data)_ function.
```python
from Saber.imeta import ipak
...
with open(file, "rb") as file:
    content = file.read()
imeta_object = imeta(content)
#pass the data after initialize
imeta_object = imeta()
imeta_object.load(content)
```

### accessing the information
The data in an imeta object is similiar to s3dpak, and ipak. you can reference the item by name, or you can reference by index. To find out the names you use the _names()_ function, or you can search for an index using _find(string)_ and refernce the item with that index using _item_at_index(index)_
```python
from Saber.imeta import imeta
...
imeta_names = imeta_object.names()
print(imeta_names[0])
index = imeta_names.find("xbox_rt_b")
if index = -1: print("Texture not found with that name")
else: print(imeta_object.item_at_index(index).offset)
```
>in this example, we assume there is a texture named "xbox_rt_b", if it didnt exist, find would return -1

### Modifying the information
currently, we can only delete data (see ipak for more information)

```python
from Saber.imeta import imeta
...
imeta_object.delete("xbox_rt_b")
```

### Saving
you can save the entire file with _save(path)_
```python
from Saber.imeta import imeta
...
imeta_object.save("path/to/file.imeta")             # save imeta
```

## Fmeta
To load a fmeta you simply import the module, and create the object.
to do this you can pass the data in the constructor, or you can create a blank object, and call the load function on it.
```python
from Saber.fmeta import fmeta
...
with open(file, "rb") as file:
    content = file.read()
fmeta_object = fmeta(content)
#pass the data after initialize
fmeta_object = fmeta()
fmeta_object.load(content)
```

### Accessing fmeta contents
the fmeta structure is fairly simple, it is just a list of files, and if it's a .map; it's decompressed size. The fmeta object has three variables. _string_ which holds the name, _decompressed_size_ which holds the decompressed size if the file is a .map, and _type_ which is either 0 for s3dpak, or 1 for .map
```python
from Saber.fmeta import fmeta
...
print(fmeta_object.items[0].decompressed_size)
print(fmeta_object.items[0].string)
print("map" if fmeta_object.items[0].type else "s3dpak")
```

### Modifying fmeta contents
To modify the contents of a fmeta object we have a few options. we can add and entry with _add_entry(file, size)_ and we can delete an entry with _delete(name)_.

>When adding an entry, if the size parameter is left blank, SeT will assume the file is a s3dpak. If the entry is a map file, we have to specify the decompressed map size. We can get that value with the _get_decompressed_size(path)_ function.
```python
from Saber.fmeta import fmeta
...
#adding to a fmeta
fmeta_object.add_entry("a10.s3dpak")
fmeta_object.add_entry("a30.s3dpak")
#adding a .map
filesize = fmeta.get_decompressed_size("location/to/a10.map")
fmeta_object.add_entry("a10.map", filesize)
...
#delete an entry
fmeta_object.delete("a30.s3dpak")
```
__Set does not look for duplicates yet when adding an entry__

### Saving the changes
After we have modified the data, we can save the new file to disk. We do this with the _save(path)_ function
```python
from Saber.fmeta import fmeta
...
fmeta_object.save("path/to/file.fmeta")
```

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

## TexturesInfo
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
