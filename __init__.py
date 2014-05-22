#This file is part sale_asterisk module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import Pool
from .opportunity import *

def register():
    Pool.register(
        SaleAsteriskResult,
        module='sale_asterisk', type_='model')
    Pool.register(
        SaleAsterisk,
        module='sale_asterisk', type_='wizard')
