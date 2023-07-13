from odoo import models, fields, api, _

class AterraPartner(models.Model):
    _inherit = 'res.partner'

    coins = fields.Integer(string='Coins')



# NEED TO ADD EVERYTHING ELSE, THE VIEW TO ADD IT TO THE PRODUCT TEMPLATE ETC

