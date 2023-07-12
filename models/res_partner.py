from odoo import models, fields, api, _

class AterraPartner(models.Model):
    _inherit = 'res.partner'

    # custom_field = fields.Char(string='Custom Field')
    coins = fields.Integer(string='Coins')


#     # coins = volume = fields.Integer(string = 'Coins')