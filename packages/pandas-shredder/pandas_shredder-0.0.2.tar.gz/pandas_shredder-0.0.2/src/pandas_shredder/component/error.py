
class UnsupportedFileFormatError(ValueError):
    """Не поддерживаемый формат файла"""
    def __init__(self, incorrect_format: str, allowed_format: list[str]):
        self.message = "Не поддерживаемый формат файла «%s»! Доступные варианты: %s" % (incorrect_format, ", ".join([f"«{f}»" for f in allowed_format]))
        super().__init__(self.message)


class DirectoryDoesNotExistError(FileNotFoundError):
    """Выбранный каталог не существует или не является директорией"""

    def __init__(self, path: str):
        self.message = "Путь «%s» не существует или не является директорией!" % path
        super().__init__(self.message)


class LineLimitHasBeenExceededError(ValueError):
    """Выбранные размер для одного файла больше общего размера исходного массива"""

    def __init__(self, selected_size: int, array_size: int):
        self.message = (
                           "Количество строк в выходном файле не может быть больше количества строк в исходном наборе данных."
                           " Был задан размер %s строк, в наборе данных %s строк") % (selected_size, array_size)
        super().__init__(self.message)


class NegativeNumberOfRowsError(ValueError):
    """Выбрано отрицательное количество строк"""

    def __init__(self, selected_size: int):
        self.message = "Количество строк не может быть отрицательным или равно 0. Задано значение %s" % selected_size
        super().__init__(self.message)
