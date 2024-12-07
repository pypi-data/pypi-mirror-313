import os
import click

from stock.core import Stock
from stock import version_info


CONTEXT_SETTINGS = dict(help_option_names=['-?', '-h', '--help'])

@click.command(
    name=version_info['prog'],
    help=click.style(version_info['desc'], italic=True, fg='cyan', bold=True),
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
)
@click.argument('symbols', nargs=-1)
def cli(symbols):

    if len(symbols) == 1 and os.path.isfile(symbols[0]):
        symbols = open(symbols[0]).read().strip().split()

    st = Stock()
    codes = st.check_symbol(*symbols)
    if codes:
        quotes = st.quote(*codes)
        table = st.show_table(quotes)
        print(table)


def main():
    cli()


if __name__ == '__main__':
    main()
