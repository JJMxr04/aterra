from odoo import models, fields, api, _

class AterraPartner(models.Model):
    _inherit = 'res.partner'

    coins = fields.Integer(string='Coins')
