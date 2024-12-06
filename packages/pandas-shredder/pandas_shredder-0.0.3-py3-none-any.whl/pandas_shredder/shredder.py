import math
import os.path
from datetime import datetime
from typing import Literal, Optional

import pandas

from .component.validator import FileFormatValidator, DirectoryPathValidator, LinesPerServingValidator, NegativeLinesPerServingValidator


Extensions = Literal["xlsx", "csv", "json", "xml", "html"]


class Shredder:
    """
    Измельчитель для объектов типа DataFrame из pandas.

    Предоставляет возможность "нарезать" на N файлов c фиксированным количество строк произвольный набор данных.

    Поддерживает следующие форматы выходных файлов: ``xlsx``, ``html``, ``csv``, ``json``, ``html``.
    """
    extension = FileFormatValidator(allowed_formats=["xlsx", "csv", "json", "xml", "html"])
    directory = DirectoryPathValidator()
    lines_per_serving = NegativeLinesPerServingValidator()

    def __init__(
            self,
            directory: str,
            extension: Extensions = "csv",
            lines_per_serving: int = 1000
    ):
        """
        Измельчитель для объектов типа DataFrame из pandas.

        Пример
        --------
        Сформируйте DataFrame, который необходимо разделить на файлы с фиксированным количеством строк.

        >>> import pandas as pd
        >>> df = pd.read_excel("C:\\Documents\\big_data.xlsx")

        Создайте экземпляр измельчителя, указав путь до каталога для сохранения результата, формат выходных файлов и количество строк в одном файле.

        >>> shredder = Shredder(directory="C:\\Documents", extension="xlsx", lines_per_serving=100)

        Вызовете метод ``run()`` передав ему набор данных и дополнительные настройки.

        >>> shredder.run(dataframe=df, file_name="small_data", index=False, header=True)

        Для сохранения "меньших" наборов данных в файлы, используются стандартные методы DataFrame ``to_csv()``, ``to_excel()``, ``to_html()``, ``to_xml()``, ``to_json()``.

        При вызове ``run()`` вместо ``kwargs`` вы можете передать поддерживаемые этими методами именнованные аргументы.

        За подробностями обратитесь к официальной документации pandas.

        :param directory: Путь к каталогу, в который будут сохранены итоговые файлы;
        :param extension: Расширение файлов, содержащих результат работы;
        :param lines_per_serving: Максимально количество строк в одном выходном файле;
        :raise UnsupportedFileFormatError: Указанное в extension значение не является одним из поддерживаемых расширений файлов;
        :raise DirectoryDoesNotExistError: Указанное в directory значение не является существующем каталогом в системе;
        :raise NegativeNumberOfRowsError: Указанное в lines_per_serving значение является отрицательным числом или нулём;
        """
        self.extension = extension
        self.directory = directory
        self.lines_per_serving = lines_per_serving

    def run(
            self,
            dataframe: pandas.DataFrame,
            file_name: Optional[str] = None,
            **kwargs
    ) -> None:
        """
        Запустить процесс "нарезки" набора данных на файлы с заданным количество строк.

        :param dataframe: Набор данных pandas.DataFrame, который необходимо разделить на файлы с заданным количество строк в каждом;
        :param file_name: Имя для файлов результата. К имени каждого файла будет добавлен префикс с его номером; Если имя не задано, оно будет сформировано из даты и времени запуска.
        :param kwargs: Опционально. Именованные аргументы, которые допустимы для методов DataFrame: ``to_csv()``, ``to_excel()``, ``to_html()``, ``to_xml()``, ``to_json()``. Подробнее в документации этих методов на сайте pandas.
        :raise LineLimitHasBeenExceededError: Количество строк в переданном dataframe меньше, чем было задано в lines_per_serving при инициализации Shredder
        :return:
        """
        number_output_files = self.__get_number_of_output_files(dataframe)
        base_file_name = self.__get_output_file_name(file_name)
        dataframe_copy = dataframe.copy(deep=True)
        for idx in range(number_output_files):
            file_num = idx + 1
            file_path = self.__get_output_file_path(base_file_name, file_num)
            content = dataframe_copy.iloc[:self.lines_per_serving, :]
            self.__save_content_to_file(content, file_path, **kwargs)
            dataframe_copy = dataframe_copy.iloc[self.lines_per_serving:, :]

    def __get_number_of_output_files(self, dataframe: pandas.DataFrame) -> int:
        dataframe_length = len(dataframe)
        validator = LinesPerServingValidator()
        validator(self.lines_per_serving, dataframe_length)
        return math.ceil(dataframe_length / self.lines_per_serving)

    def __get_output_file_name(self, file_name: Optional[str]) -> str:
        if file_name:
            return ".".join([file_name, self.extension])
        return ".".join([f"Shredder run {datetime.now().strftime('%d.%m.%Y in %H-%M-%S')}", self.extension])

    def __get_output_file_path(self, file_name, file_num) -> str:
        return os.path.join(self.directory, f"{file_num}_{file_name}")

    def __save_content_to_file(self, dataframe: pandas.DataFrame, path: str, **kwargs) -> None:
        match self.extension:
            case "xlsx":
                dataframe.to_excel(path, **kwargs)
            case "csv":
                dataframe.to_csv(path, **kwargs)
            case "html":
                dataframe.to_html(path, **kwargs)
            case "xml":
                dataframe.to_xml(path, **kwargs)
            case "json":
                dataframe.to_json(path, **kwargs)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(directory="{self.directory}", extension="{self.extension}", lines_per_serving={self.lines_per_serving})'
