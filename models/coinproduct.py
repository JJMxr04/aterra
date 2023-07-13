from odoo import models, fields, api, _



class CoinProduct(models.Model):
    _inherit = 'product.template'

    coins_ok = fields.Boolean(string='Coins?')
    coin_amount = fields.Integer(string='Coin Amount')

