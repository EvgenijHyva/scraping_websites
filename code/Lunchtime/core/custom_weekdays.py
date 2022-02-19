from datetime import datetime, timedelta


def get_week_tuple(from_day: int = 1, to_day: int = 5, _format: str = "YMD-A") -> tuple:
    """
    Create tuple for current week, you can also adjust days between 1 and 7
    Default Y-Year, m-month, d-day, A-weekday, you can also provide a custom format, check Datetime docs for syntax
    :param _format: YMD-A or DMY-A or create you custom
    :param from_day: int
    :param to_day: int
    :return: tuple
    """
    formats = {
        "YMD-A": "%Y-%m-%d %A",
        "DMY-A": "%d-%m-%Y %A"
    }
    formats.setdefault("custom", _format)
    this_week = []
    if 1 <= to_day <= 7 and 1 <= from_day <= 7:
        for index in range(from_day - 1, to_day):
            year_week_num = datetime.today().strftime("%Y-W%W")
            monday = datetime.strptime(year_week_num + '-1', "%Y-W%W-%w")
            date_day = (monday + timedelta(days=index)).strftime(
                formats.get(_format if _format in formats.keys() else "custom"))
            this_week.append(tuple(date_day.split(" ")))
    else:
        raise UserWarning("Number between 1 and 7")
    return tuple(this_week)


if __name__ == "__main__":
    print(get_week_tuple(1, 7))
    print(get_week_tuple(6, 7))
