#!/usr/bin/env python

import sys
import click
from onlineshop.onlineshop import main

@click.command()
@click.argument('receipt_file', type=click.File('r'))
def cli(*args, **kwargs):
    return main(*args, **kwargs)


if __name__ == '__main__':
    sys.exit(cli())