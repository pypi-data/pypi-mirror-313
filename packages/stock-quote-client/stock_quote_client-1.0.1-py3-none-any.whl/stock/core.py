import re

import click
import tushare
from webrequests import WebRequest as WR
from prettytable import PrettyTable
from requests_cache import CachedSession


class Stock(object):
    def __init__(self):
        self.session = CachedSession('~/.stock_cache.sqlite3')

    def search(self, name):
        """查询关键词"""
        url = f'https://biz.finance.sina.com.cn/suggest/lookup_n.php?country=&q={name}'
        soup = WR.get_soup(url, session=self.session)
        st = soup.select_one('#stock_stock')
        a = st.nextSibling.nextSibling.select_one('a')
        if a:
            code = a.text.split()[0]
            code = code[2:] + '.' + code[:2].upper()
            return code

    def check_symbol(self, *symbols):
        code_pattern = re.compile(r'^\d{6}\.S[ZH]$', re.I)
        codes = []
        for symbol in symbols:
            if not code_pattern.match(symbol):
                query_symbol = self.search(symbol)
                if not query_symbol:
                    click.echo(f'bad query: {symbol}')
                    continue
                symbol = query_symbol
            codes.append(symbol)
        return codes

    def quote(self, *symbols):
        """报价"""
        symbol = ','.join(symbols)
        # print(symbol)
        df = tushare.realtime_quote(symbol)
        # print(df.columns)
        return df

    @staticmethod
    def show_table(quotes, reverse=True):
        fields = [
            'TS_CODE', 'NAME', 'PERCENT', 'CHG', 'AMOUNT',
            'PRICE', 'OPEN', 'HIGH', 'LOW', 
            'B1_V', 'A1_V',
        ]
        table = PrettyTable(fields)

        quotes['PERCENT'] = ((quotes['PRICE'] - quotes['PRE_CLOSE']) / quotes['PRE_CLOSE'] * 100).round(2)
        quotes['CHG'] = (quotes['PRICE'] - quotes['PRE_CLOSE']).round(2)['CHG'] = (quotes['PRICE'] - quotes['PRE_CLOSE']).round(2)

        quotes = quotes.sort_values('PERCENT', ascending=False)

        for _, quote in quotes.iterrows():
            percent = quote['PERCENT'] or 0

            if percent > 0:
                color = 'red'
                percent = f'+{percent}'
                quote['CHG'] = f'+{quote["CHG"]}'
            elif percent < 0:
                color = 'green'
            else:
                color = None
            quote['PERCENT'] = click.style(f'{percent}%', fg=color)

            quote['AMOUNT'] = round(quote['AMOUNT'] / 10000)

            row = list(map(quote.get, fields))
            table.add_row(row)

        table.align['PERCENT'] = 'r'
        table.add_autoindex('INDEX')
        return table
