# WAVE
> # Workflow Automation and Versatile Engine


<div align="center">
<img src="RDM_components/img/wave.jpeg" alt="WAVE" width="450px"/>
</div>

> Owned by Lucas Lourenço

> Maintained by Lucas Lourenço

> Translation to [Portuguese](/RDM_components/PT_README.md)
----

# Getting Started on WAVE
To use WAVE, execute the following command in your terminal

##### ```pip install -U wave-flow```



# Examples

<details open>
<summary>
Practical Examples
</summary>

<p>

 - [Simple Example](e.g/simple/simpleExample.py)
 
 - [Complex Example](e.g/complex/complexExample.py)

 - [Complex Example With Classes](e.g/complexWithClass/complexExample2.py)

</p>
</details>


<details open>
<summary>
Class Use Case Example
</summary>

<p>

 - [DataHandler](#-datahandler)

 - [Builder](#-builder)
 
 - [To](#-to)
 
 - [Transmitter](#-transmitter)


</p>
</details>


---

# How To Use


## | **DataHandler**
The `DataHandler` class is the first step when you're using WAVE. Using it, you become able to use several features, including the unique way to reach `Archive` class (as shown in the next topic). Below are the methods and it's explication.


* #### **DType**
>As [Pandas](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dtypes.html), you can pass a _DType_ as parameter. The _KEYS_ on this dict must have to be one of the Headers at the column that you want to perform the read as the _VALUE_ data.

e.g.:
```python
handler = DataHandler(r'example.xlsx')
handler.getArchive().setDelimiter('==') # important part of the code that will be shown below.
handler.setDtype({"ID":str, "DATE":str})
```

* #### **Acess Archive**
>To acess the class [Archive](#-archive), the unique way to reach it is using the code below.

e.g.:
```python
handler = DataHandler(r'example.xlsx')
handler.getArchive() # and it's methods as shown
```


* #### **Read File**
>After informate the [Delimiter](#-delimiter), and if you think it's necessary, inform the [Dtype](#dtype), you have to read the file.

e.g.:
```python
from WaveFlow import (PreRequisitesWave, To, DataHandler, Builder, Transmitter)

handler = DataHandler(r'example.xlsx')
handler.getArchive().setDelimiter('==')
handler.setDtype({"ID":str, "DATE":str})
handler.readFile()

print(handler.getArchive().getData()) # -> dict
```

## | **Archive**
After being accessed by the method in [DataHandler (Acess Archive)](#acess-archive), you can manage a lot of data informations. Which them gonna be expressed below.

* ### **Delimiter**
One of the most important part of the orchestra. It's necessary and primordial to identify where the placeholders are.

e.g.:
```python
from WaveFlow import (PreRequisitesWave, To, DataHandler, Builder, Transmitter)

handler = DataHandler(r'example.xlsx')
handler.getArchive().setDelimiter('==')

[...]

```


* ### **Transform Data**
This method cooperate with [To](#-to) class. To handle data, `To` has a lot of management about it. You can read more about it [clicking here](#-to).
Following the harmony of the structure, it is appropriate that you use this method to process any type of data.

e.g.:
```python
handler.getArchive().transformData("HOUR", To.Hour().to_hh_mm)
handler.getArchive().transformData("DATE", To.Date().to_dd_mm_yyyy)
handler.getArchive().transformData("FINALDATE", lambda x: To.Date().to_personalizedFormat(x, '%d de %B de %Y'))
```



* ### **Additional Parameter**
Using this method, you can personalize formatting configurations to each info which will be placed.
Assuming those obrigatory parameters `keyColumn`, `parameterToChange`, `newValueToParameter`, pay attention to the required data below.

| **possibilities**           | **appropriate data type**    | 
|-----------------------------|------------------------------|
| bold                        | bool                         |
| italic                      | bool                         |
| font                        | string                       |
| size                        | int                          |


`keyColumn`: Place here the header which you want to operate.

`parameterToChange`: Select one of the four possibility.

`newValueToParameter`: place the proper data to what you wanna format.

e.g.:
```python
from WaveFlow import (PreRequisitesWave, To, DataHandler, Builder, Transmitter)

    handler = DataHandler(r'example.xlsx')
    
    handler.getArchive().setDelimiter('==')
    handler.readFile()
    
    handler.getArchive().setAdditionalParameters("NAME", "size", 12)
    handler.getArchive().setAdditionalParameters("NAME", "bold", True)
    handler.getArchive().setAdditionalParameters("COUNTRY", 'italic', True)
    handler.getArchive().setAdditionalParameters("DATE", "font", 'Times New Roman')
    
    [...]

```

<!-- 
   def setAdditionalParameters(self, keyColumn:str, parameterToChange:Literal["font", "size", "italic", "bold"], newValueToParameter):
        self.__DictWithData[keyColumn]['additional_parameters'][parameterToChange] = newValueToParameter -->


* ### **Getters**

| **Method Name**              | **Return Type**         | **Description**                                                                 |
|------------------------------|-------------------------|---------------------------------------------------------------------------------|
| `getData()`                  | `dict`                 | Returns the data dictionary, raises `ReferenceError` if no data is available. **(maybe it's what you're looking for)**|
| `getFileType()`              | `str`                  | Returns the file type of the archive.                                          |
| `getMetaData()`              | `list[str]`            | Returns a list of metadata associated with the file.                           |
| `getFilename()`              | `str`                  | Returns the name of the file.                                                |
| `getDesignatedFile()`        | `docx.Document`        | Returns the designated file object.                                            |
| `getDataFrame()`             | `pd.DataFrame`         | Returns the data as a DataFrame, raises `ReferenceError` if no DataFrame exists.|
| `getDelimiter()`             | `str`                  | Returns the current delimiter used for key formatting.                         |
| `getFilesGenerated()`        | `list[docx.Document]`  | Returns a list of files generated by the system.                               |


---
## | **Builder**
The `Builder` class requires only two obrigatory parameters. Are them the _instance_ of Archive, it means you **HAVE** to informate "handler.getArchive()" as first parameter(archive parameter). As second, you have to informate the base document(baseDocx parameter) which you want to deal.

e.g.:
```python
from WaveFlow import (PreRequisitesWave, To, DataHandler, Builder, Transmitter)


handler = DataHandler(r'example.xlsx')
handler.getArchive().setDelimiter('==')
handler.readFile()

build = Builder(handler.getArchive(), r'example.docx')

[...]
```


* ### **Generation**
`.generate()`

Method used to generate the documents. There's no parameters, just need to run it.

e.g.:
```python
from WaveFlow import (PreRequisitesWave, To, DataHandler, Builder, Transmitter)


handler = DataHandler(r'example.xlsx')
handler.getArchive().setDelimiter('==')
handler.readFile()

build = Builder(handler.getArchive(), r'example.docx')
build.generate()

[...]

```


* ### **Saving Generated Files**
`.saveAs()`

To save in a zip file or locally, first you have to generate as shown above.

This method has a lot of personalization ways to do. Below you gonna find informations.


| Parameter     | Type Needed             |
|---------------|-------------------------|
| `textAtFile`  | str                     |
| `keyColumn`   | list[str]               |
| `ZipFile`     | bool -> False as default|
| `saveLocally` | bool -> True as default |

### Explication

- **textAtFile**

>That's the pattern name of the file that will be generated. <p>
As e.g.: " {} - Document Generated - {}". <p>
The "{}" in string is present because you can personalize the output with the next paramenter — keyColumn


- **keyColumn**

> With the Headers (Keys) which you informate in this list as string, you can provide the current

- **ZipFile & saveLocally**

> It'll build a ZipFile content (in case of ZipFile receives True) and create locally files (in case of saveLocally receives True)


e.g.:
```python
from WaveFlow import (PreRequisitesWave, To, DataHandler, Builder, Transmitter)


handler = DataHandler(r'example.xlsx')
handler.getArchive().setDelimiter('==')
handler.readFile()

build = Builder(handler.getArchive(), r'example.docx')
build.generate()

build.saveAs(textAtFile="DOCS/{}/{} - Document",
                    keyColumn=['Date', 'Name'], 
                    ZipFile=True, 
                    saveLocally=True)
```


* ### **Getters**
| Method                  | Output                                      |
|-------------------------|---------------------------------------------|
| `getTimeToGenerate`     | _the current time neeeded to generate_      |
| `getIndexSequence`      | _the actual sequence of all documents_      |

---
## | **To**

The `To` class provides multiple utilities for transforming dates, times, and monetary values into different formats. Below are the available methods and their usage examples.

---


> ### **1. Language Configuration**
***Before*** using the `Date`, `Hour`, or `Money` utilities, you can set the language using the `To.languageTo()` method.

#### **Languages Supported**
- `'pt_BR'` - Portuguese (Brazil)
- `'es_ES'` - Spanish
- `'en_US'` - English
- `'fr_FR'` - French
- You can use another language which `locale` can handle.

#### **Example**
```python
from WaveFlow import (PreRequisitesWave, To, DataHandler, Builder, Transmitter)

[...]

To.languageTo('pt_BR')  # Set language to Portuguese
handler.getArchive().transformData("HOUR", To.Hour().to_hh_mm)

[...]
```


---

> ### **2. Date Manipulation**
The `To.Date()` provides various methods to handle and transform date objects.

#### **Available Methods**
| Method                          | Output Format       | Example Input                | Example Output                |
|---------------------------------|---------------------|------------------------------|-------------------------------|
| `to_dd_mm`                      | `dd/m`             | `Timestamp('2024-01-01')`   | `01/1`                        |
| `to_dd_MM`                      | `dd/M`             | `Timestamp('2024-01-01')`   | `01/January`                  |
| `to_MM_yy`                      | `MM/y`             | `Timestamp('2024-01-01')`   | `January/24`                  |
| `to_MM_yyyy`                    | `MM/Y`             | `Timestamp('2024-01-01')`   | `January/2024`                |
| `to_dd_mm_yy`                   | `dd/mm/yy`         | `Timestamp('2024-01-01')`   | `01/01/24`                    |
| `to_dd_mm_yy_periodSep`         | `dd.mm.yy`         | `Timestamp('2024-01-01')`   | `01.01.24`                    |
| `to_dd_MM_yyyy`                 | `dd/MM/yyyy`       | `Timestamp('2024-01-01')`   | `01/January/2024`             |
| `to_dd_mm_yyyy`                 | `dd/mm/yyyy`       | `Timestamp('2024-01-01')`   | `01/01/2024`                  |
| `to_mm_dd_yyyy`                 | `mm/dd/yyyy`       | `Timestamp('2024-01-01')`   | `01/01/2024`                  |
| `to_yyyy_mm_dd`                 | `yyyy-mm-dd`       | `Timestamp('2024-01-01')`   | `2024-01-01`                  |
| `to_full_date`                  | Full Date String   | `Timestamp('2024-01-01')`   | `Monday, 01 January 2024`     |
| `to_dd_MM_yyyy_in_full`         | Full Date String   | `Timestamp('2024-01-01')`   | `01 January 2024`             |
| `to_personalizedFormat`         | Custom Format      | `Timestamp('2024-01-01')`   | Based on format provided      |

> Input type must be ***Timestamp class***
#### **Example**
* **pattern method use**:
```python
[...]

handler.getArchive().transformData("DATE", To.Date().to_dd_mm_yy_periodSep)

[...]
```
* **to_personalizedFormat**:

    It's an exclusive method in < To > class that provides a personalization about data been treated. You can use the same `.strftime()` as [used on pandas](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.strftime.html).
```python
[...]

handler.getArchive().transformData("DATE",lambda x:To.Date().to_personalizedFormat(x,'%d de %B de %Y'))

[...]
```


---

> ### **3. Time Manipulation**
The `To.Hour()` provides methods for transforming time objects into desired formats.

#### **Available Methods**
| Method               | Output Format       | Example Input          | Example Output     |
|----------------------|---------------------|------------------------|--------------------|
| `to_hh_mm_ss`        | `HH:MM:SS`         | `datetime(11, 30)`     | `11:30:00`         |
| `to_hh_mm`           | `HH:MM`            | `datetime(11, 30)`     | `11:30`            |
| `to_12_hour_format`  | `HH:MM AM/PM`      | `datetime(23, 30)`     | `11:30 PM`         |
| `to_24_hour_format`  | `HH:MM`            | `datetime(23, 30)`     | `23:30`            |

> Input type must be ***datetime class***

#### **Example**
* **pattern method use**:
```python
[...]

To.languageTo('pt_BR')
handler.getArchive().transformData("HOUR", To.Hour().to_hh_mm)

[...]
```

---



> ### **4. Money Formatting Manipulation**
The `To.Money()` provides methods for formatting monetary values into various currencies.

#### **Available Methods**
| Method           | Output Format            | Example Input  | Example Output         |
|------------------|--------------------------|----------------|------------------------|
| `to_dollars`     | `$ {value}`             | `1234.56`      | `$ 1,234.56`          |
| `to_euros`       | `€ {value}`             | `1234.56`      | `€ 1.234,56`          |
| `to_pounds`      | `£ {value}`             | `1234.56`      | `£ 1,234.56`          |
| `to_brl`         | `R$ {value}`            | `1234.56`      | `R$ 1.234,56`         |

> Input type must be ***float*** or ***int***

#### **Example**
* **pattern method use**:
```python
[...]

To.languageTo('pt_BR')
handler.getArchive().transformData("VALUE", To.Money().to_brl)

[...]
```

---

## | **Transmitter**
This class could be the first step for your usage on WAVE, because it can analyse a .docx and return a .xlsx file with all headers which where defined at docx.

Everything you need to do is informate the document (it **must have** to be a list) and pass the delimiter. After that, just use the method `export`.
Follow the example:

```python
from WaveFlow import Transmitter

transmitter = Transmitter(['example.xlsx'], '==')
transmitter.export("exampleExport.xlsx")

```

