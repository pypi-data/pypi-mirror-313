# pandas-shredder
Пакет, предоставляющий интерфейс для нарезки Pandas.DataFrame на отдельные файлы с заданным количеством строк в каждом из них.  

## Оглавление
- [Установка](#install)  
- [Пример использованния](#example)  
- [Пример использования с пояснениями](#full_example)  
- [Возможные исключения](#exeptions)

## Установка <a name="install"></a>
Выполните в терминале команду:
```commandline
pip install pandas-shredder
```
В вашем коде выполните импорт:
```python
from pandas_shredder import Shredder
```
Ссылка на пакет `pandas-shredder` в **[PyPI](https://pypi.org/project/pandas-shredder/)**

## Пример использования <a name="example"></a>
```python
import pandas as pd
from pandas_shredder import Shredder

# Считываем большой файл формата CSV
df = pd.read_csv("C:\\Documents\\big_data.csv")

# Настраиваем измельчитель на сохранение xslx файлов по 500 000 строк в каталог C:\\Documents\\big_data.csv
shredder = Shredder(
    directory="C:\\Documents\\result",
    extension="xlsx",
    lines_per_serving=500_000
)
# Нарезаем большой файл на файлы по 500 000 строк с именем по маске {номер}_small_data.xlsx в каталог C:\\Documents\\result
# Исключаем из результата столбец с индексами pandas, исключаем строку с заголовком, присваиваем листу имя data
shredder.run(
    dataframe=df,
    file_name="small_data",
    index=False,
    header=False,
    sheet_name="data"
)
```

## Пример использования с пояснениями <a name="full_example"></a>
Предположим у вас есть файл _**big_data.csv**_ на **7 000 000** строк, расположенный в _**C:\\Documents**_.  
И у вас существует потребность сделать из него несколько файлов формата **xlsx** на **500 000** строк каждый.

_**Shredder**_ поможет Вам реализовать эту задумку в несколько строк кода.

Создайте DataFrame на основе данных из вашего файла _**C:\\Documents\\big_data.csv**_

```python
import pandas as pd

df = pd.read_csv("C:\\Documents\\big_data.csv")
```
Импортируйте `Shredder` из пакета `pandas-shredder` и инициализируйте его экзмепляр.
```python
from pandas_shredder import Shredder

shredder = Shredder(
    directory="C:\\Documents\\result",
    extension="xlsx",
    lines_per_serving=500_000
)
```
- `directory` - путь к каталогу, в который будут сохранены выходные файлы.
- `extension` - расширение / формат выходных файлов. Доступно: `xlsx`, `csv`, `json`, `html`, `xml`
- `lines_per_serving` - максимальное количество строк в одном выходном файле.

Запустите измельчитель вызовом метода `run()`, передав в него набор данных и имя для выходных файлов.
```python
shredder.run(
    dataframe=df,
    file_name="small_data"
)
```
- `dataframe` - экземпляр pandas.DataFrame, который нарезается на файлы заданного размера
- `filename` - имя, для файлов с результатом. К имени каждого файла будет добавлен префикс с номером файла.
- `**kwarg` - опционально. Произвольные именованные аргументы, которые поддерживаются методами DataFrame: `to_excel()`, `to_csv()`, `to_html()`, `to_xml()`, `to_json()`. Набор доступных аргументов зависит от выбранного на этапе инициализации экземпляра `Shredder` значения в свойстве `extension`.

В результате выполнения кода, в каталоге _**C:\\Documents\\result**_ вас будут ожидать файлы:
- 1_small_data.xlsx
- 2_small_data.xlsx
- 3_small_data.xlsx
- ...

Для сохранения данных в файлы, используются стандартные методы **pandas**. Вы можете сконфигурировать процесс сохранения через именованные аргументы переданные в `run()` вместо `**kwargs`.  
Например:
```python
shredder.run(
    dataframe=df,
    file_name="small_data",
    index=False,
    header=False,
    sheet_name="data"
)
```
Возможные именованные аргументы зависят от выбранного в `extension` расширения. Ознакомьтесь с таблицей ниже, что бы узнать больше.

| **extension** | **pandas method**                                                                                       |
|---------------|---------------------------------------------------------------------------------------------------------|
| csv           | [to_csv()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html)     |
| xlsx          | [to_excel()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html) |
| html          | [to_html()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_html.html)   |
| json          | [to_json()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html)   |
| xml           | [to_xml()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_xml.html)                                                                                            |


## Возможные исключения <a name="exeptions"></a>
### UnsupportedFileFormatError
Будет брошено в ситуации, когда указанное в `extension` значение не является одним из: `xlsx`, `csv`, `json`, `html`, `xml`
```commandline
    raise UnsupportedFileFormatError(value, self.allowed_formats)
pandas_shredder.component.error.UnsupportedFileFormatError: Не поддерживаемый формат файла «txt»! Доступные варианты: «xlsx», «csv», «json», «xml», «html»
```
### DirectoryDoesNotExistError
Будет брошено в ситуации, когда указанное в `directory` значение не является существующим в системе каталогом (папкой).
```commandline
    raise DirectoryDoesNotExistError(value)
pandas_shredder.component.error.DirectoryDoesNotExistError: Путь «C:\result» не существует или не является директорией!
```
### NegativeNumberOfRowsError
Будет брошено в ситуации, когда указанное в `lines_per_serving` значение меньше или равно 0.
```commandline
    raise NegativeNumberOfRowsError(value)
pandas_shredder.component.error.NegativeNumberOfRowsError: Количество строк не может быть отрицательным или равно 0. Задано значение -10
```
### LineLimitHasBeenExceededError
Будет брошено в ситуации, когда количество строк в `dataframe` меньше значения, заданного в `lines_per_serving`.
```commandline
    raise LineLimitHasBeenExceededError(lines_per_serving, dataframe_length)
pandas_shredder.component.error.LineLimitHasBeenExceededError: Количество строк в выходном файле не может быть больше количества строк в исходном наборе данных. Был задан размер 1000 строк, в наборе данных 573 строк
```