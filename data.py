from datetime import date

def _parse_br_format_date(dtstr: str):
    splitted_dtstr = dtstr.split("/")
    if not len(splitted_dtstr) == 3:
        raise ValueError("Inconsistent use of slash separator")

    if len(splitted_dtstr[0]) not in (1, 2):
        raise ValueError("Day must have one or two digits")

    if len(splitted_dtstr[1]) not in (1, 2):
        raise ValueError("Month must have one or two digits")

    if len(splitted_dtstr[2]) != 4:
        raise ValueError("Year must have four digits")

    [day, month, year] = map(lambda x: int(x), splitted_dtstr)
    return day, month, year

class data(date):
    def __new__(cls, day: int, month: int, year: int):
        """Inverte a ordem dos parametros para melhor se adaptar ao nosso uso de datas"""
        return super().__new__(cls, year, month, day)

    @classmethod
    def frombrformat(cls, date_string):
        """Constrói um objeto data a partir de uma string em formato d[d]/m[m]/aaaa"""
        if not isinstance(date_string, str):
            raise TypeError("frombrformat: argument must be str")

        if len(date_string) not in (8, 9, 10):
            raise ValueError(f'Invalid brformat string: {date_string!r}')

        try:
            return cls(*_parse_br_format_date(date_string))
        except:
            raise ValueError(f'Invalid brformat string: {date_string!r}')

    def __str__(self) -> str:
        return self.strftime("%d/%m/%y")

