import asyncio
import calendar
import datetime
import math


class DateUtil:

    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        """判断是否是一个有效的日期字符串"""
        try:
            if ":" in date_str:
                datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            else:
                datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def get_tax_period(start_date: str | datetime.date, end_date: str | datetime.date) -> str:
        """获取报税周期:次、月、季、半年、年"""
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        end_days_num = calendar.monthrange(end_date.year, end_date.month)[1]
        valid_first_last_day = (start_date.day == 1 and end_date.day == end_days_num)

        if start_date.year != end_date.year:
            return ""

        if start_date.month == end_date.month and start_date.day == end_date.day:
            tax_period = '次'
        elif start_date.month == end_date.month and valid_first_last_day:
            tax_period = '月'
        elif start_date.month + 2 == end_date.month and valid_first_last_day:
            tax_period = '季'
        elif start_date.month + 5 == end_date.month and valid_first_last_day:
            tax_period = '半年'
        elif start_date.month == 1 and end_date.month == 12 and valid_first_last_day:
            tax_period = '年'
        else:
            tax_period = ""
        return tax_period

    @staticmethod
    def _get_month_day(base_day: str | datetime.date, offset: int = 0, return_type: str = 'str') -> tuple:
        """
        获取某月的起止日期
        :param base_day: 基准日期:
        :param offset: 月份偏移，本月：0 上月：-1 下月：1，以此类推。
        :param return_type: str：字符串 date：日期
        :return:某月起止日期的字符串元组 eg:('2020-11-01', '2020-11-30')
        """
        if isinstance(base_day, str):
            base_day = datetime.datetime.strptime(base_day, "%Y-%m-%d")

        month = base_day.month + offset  # 年月计算 month的合法值为1-12
        if 1 <= month <= 12:
            year = base_day.year
        else:
            if month % 12 == 0:  # 0、-12等需要往前计算一年
                year = base_day.year + math.floor(month / 12) - 1
                month = 12
            else:
                year = base_day.year + math.floor(month / 12)  # 往前推算年份月份
                month = month % 12

        # 年月获取首尾日期
        first_day = datetime.datetime(year, month, 1)
        days_num = calendar.monthrange(first_day.year, first_day.month)[1]
        last_day = datetime.datetime(year, month, days_num)
        if return_type == 'str':
            return first_day.strftime('%Y-%m-%d'), last_day.strftime('%Y-%m-%d')
        return first_day, last_day

    @staticmethod
    def _get_quarter_day(base_day: str | datetime.date, offset: int = 0, return_type: str = 'str') -> tuple:
        """
        获取某季度的起止日期
        :param base_day: 基准日期:
        :param offset: 季度偏移，本季度：0 上季度：-1 下季度：1，以此类推。
        :param return_type: str：字符串 date：日期
        :return:某季度起止日期的字符串元组 eg:('2020-10-01', '2020-12-31')
        """
        if isinstance(base_day, str):
            # 字符类型转换为日期
            base_day = datetime.datetime.strptime(base_day, "%Y-%m-%d")

        offset = offset * 3
        month_start_date, _ = DateUtil._get_month_day(base_day, offset=offset, return_type='date')

        year = month_start_date.year
        month = month_start_date.month
        if 0 < month <= 3:
            start_month = 1
            end_month = 3
        elif 4 <= month <= 6:
            start_month = 4
            end_month = 6
        elif 7 <= month <= 9:
            start_month = 7
            end_month = 9
        elif 10 <= month <= 12:
            start_month = 10
            end_month = 12
        else:
            raise Exception(f"月份【{month}】有误")

        # 年月获取首尾日期
        first_day = datetime.datetime(year, start_month, 1)
        days_num = calendar.monthrange(year, end_month)[1]
        last_day = datetime.datetime(year, end_month, days_num)
        if return_type == 'str':
            return first_day.strftime('%Y-%m-%d'), last_day.strftime('%Y-%m-%d')
        return first_day, last_day

    @staticmethod
    def _get_half_year_day(base_day: str | datetime.date, offset: int = 0, return_type: str = 'str') -> tuple:
        """
        获取某半年的起止日期
        :param base_day: 基准日期:
        :param offset: 半年偏移，本半年：0 上一个半年：-1 下一个半年：1，以此类推。
        :param return_type: str：字符串 date：日期
        :return:某半年起止日期的字符串元组 eg:('2020-01-01', '2020-12-31')
        """
        if isinstance(base_day, str):
            # 字符类型转换为日期
            base_day = datetime.datetime.strptime(base_day, "%Y-%m-%d")

        offset = offset * 6
        month_start_date, _ = DateUtil._get_month_day(base_day, offset=offset, return_type='date')

        year = month_start_date.year
        month = month_start_date.month
        if 0 < month <= 6:
            start_month = 1
            end_month = 6
        elif 7 <= month <= 12:
            start_month = 7
            end_month = 12
        else:
            raise Exception(f"月份【{month}】有误")

        # 年月获取首尾日期
        first_day = datetime.datetime(year, start_month, 1)
        days_num = calendar.monthrange(year, end_month)[1]
        last_day = datetime.datetime(year, end_month, days_num)
        if return_type == 'str':
            return first_day.strftime('%Y-%m-%d'), last_day.strftime('%Y-%m-%d')
        return first_day, last_day

    @staticmethod
    def _get_year_day(base_day: str | datetime.date, offset: int = 0, return_type: str = 'str') -> tuple:
        """
        获取某年的起止日期
        :param base_day: 基准日期:
        :param offset: 年偏移，本年：0 上一年：-1 下一年：1，以此类推。
        :param return_type: str：字符串 date：日期
        :return:某年起止日期的字符串元组 eg:('2020-01-01', '2020-12-31')
        """
        if isinstance(base_day, str):
            base_day = datetime.datetime.strptime(base_day, "%Y-%m-%d")
        year = base_day.year + offset

        # 年月获取首尾日期
        first_day = datetime.datetime(year, 1, 1)
        days_num = calendar.monthrange(year, 12)[1]
        last_day = datetime.datetime(year, 12, days_num)
        if return_type == 'str':
            return first_day.strftime('%Y-%m-%d'), last_day.strftime('%Y-%m-%d')
        return first_day, last_day

    @staticmethod
    def get_today_date():
        """
        获取当天日期
        :return:
        """
        return datetime.date.today().strftime("%Y-%m-%d")

    @staticmethod
    def get_last_month_day(date: str):
        date = date.strip()[:10]  # 仅保留YYYY-mm-dd长度
        return DateUtil._get_month_day(date, offset=-1)

    @staticmethod
    def get_last_quarter_day(date: str):
        date = date.strip()[:10]  # 仅保留YYYY-mm-dd长度
        return DateUtil._get_quarter_day(date, offset=-1)

    @staticmethod
    def get_last_half_year_day(date: str):
        date = date.strip()[:10]  # 仅保留YYYY-mm-dd长度
        return DateUtil._get_half_year_day(date, offset=-1)

    @staticmethod
    def get_last_year_day(date: str):
        date = date.strip()[:10]  # 仅保留YYYY-mm-dd长度
        return DateUtil._get_year_day(date, offset=-1)

    @staticmethod
    def get_current_month_day(date: str):
        date = date.strip()[:10]  # 仅保留YYYY-mm-dd长度
        return DateUtil._get_month_day(date)

    @staticmethod
    def get_current_quarter_day(date: str):
        date = date.strip()[:10]  # 仅保留YYYY-mm-dd长度
        return DateUtil._get_quarter_day(date)

    @staticmethod
    def get_current_half_year_day(date: str):
        date = date.strip()[:10]  # 仅保留YYYY-mm-dd长度
        return DateUtil._get_half_year_day(date)

    @staticmethod
    def get_current_year_day(date: str):
        date = date.strip()[:10]  # 仅保留YYYY-mm-dd长度
        return DateUtil._get_year_day(date)

    @staticmethod
    def get_next_month_day(date: str):
        date = date.strip()[:10]  # 仅保留YYYY-mm-dd长度
        return DateUtil._get_month_day(date, offset=1)

    @staticmethod
    def get_next_quarter_day(date: str):
        date = date.strip()[:10]  # 仅保留YYYY-mm-dd长度
        return DateUtil._get_quarter_day(date, offset=1)

    @staticmethod
    def get_next_half_year_day(date: str):
        date = date.strip()[:10]  # 仅保留YYYY-mm-dd长度
        return DateUtil._get_half_year_day(date, offset=1)

    @staticmethod
    def get_next_year_day(date: str):
        date = date.strip()[:10]  # 仅保留YYYY-mm-dd长度
        return DateUtil._get_year_day(date, offset=1)

    def today(self):
        """
        获取当前时间
        """
        return datetime.datetime.today()

    def now(self):
        """
        获取现在时间
        """
        return datetime.datetime.now()

    def ntc_now(self):
        """
        获取utc现在时间
        """
        return datetime.datetime.utcnow()
