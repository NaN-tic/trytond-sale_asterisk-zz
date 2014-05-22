#This file is part of sale_asterisk module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import ModelView, fields
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.pyson import Eval
from trytond.wizard import Wizard, StateView, StateTransition, Button

__all__ = ['SaleAsteriskResult', 'SaleAsterisk']


class SaleAsteriskResult(ModelView):
    'Sale Asterisk Result'
    __name__ = 'sale.asterisk.result'

    phone = fields.Selection('get_phones', 'Phone', required=True)
    allowed_contacts_mechanisms = fields.Function(fields.One2Many(
            'party.contact_mechanism', None, 'Allowed Contacts Mechanisms'),
        'on_change_with_allowed_contacts_mechanisms')
    contact_mechanisms = fields.Many2One('party.contact_mechanism', 'party',
        'Contact Mechanisms',
        domain=[
            ('id', 'in', Eval('allowed_contacts_mechanisms', [])),
            ],
        depends=['allowed_contacts_mechanisms'])


class SaleAsterisk(Wizard):
    'Sale Asterisk'
    __name__ = 'sale.asterisk'

    start = StateView('sale.asterisk.result',
        'sale_asterisk.sale_asterisk_result_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Dial', 'dial', 'tryton-ok', default=True),
            ])
    dial = StateTransition()

    def default_start(self, fields):
        """
        This method searches phones of a sale order to show in the wizard.
        """
        sale = Transaction().context.get('active_id')
        Sale = Pool().get('sale.sale')
        sale = Sale(sale)
        mechanisms = []
        if sale:
            if sale.party:
                for mechanism in sale.party.contact_mechanisms:
                    if mechanism.type in ('phone', 'mobile'):
                        mechanisms.append(mechanism)
                if sale.party.relations:
                    for relationship in sale.party.relations:
                        for mechanism in relationship.to.contact_mechanisms:
                            if mechanism.type in ('phone', 'mobile'):
                                mechanisms.append(mechanism)
        mechanisms = list(set(mechanisms))
        return {
            'allowed_contacts_mechanisms': [m.id for m in mechanisms],
            'contact_mechanisms': mechanisms[0].id
            }

    def transition_dial(self, values=False):
        """
        Function called by the button 'Dial'
        """
        party = self.start.contact_mechanisms.party
        number = self.start.contact_mechanisms.value
        Asterisk = Pool().get('asterisk.configuration')
        Asterisk.dial(party, number)
        return 'end'
