from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        order = super(SaleOrder, self).create(vals)

        for line in order.order_line:
            product = line.product_id
            line.coins_ok = product.coins_ok

        return order
    

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        for order in self:
            for line in order.order_line:
                product = line.product_id
                partner = order.partner_id
                line.coins_ok = product.coins_ok
                if product.coins_ok:
                    partner.coins += product.coin_amount * line.product_uom_qty

        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    coins_ok = fields.Boolean(string='Coins OK')
