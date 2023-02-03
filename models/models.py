# -*- coding: utf-8 -*-

from odoo import models, fields, api


class aterra(models.Model):
    _name = 'aterra.aterra'
    _description = 'aterra.aterra'



    name = fields.Char()
    volume = fields.Integer()
    series = fields.Text()
    rarity = fields.Text()
    rank = fields.Integer()
    power = fields.Integer()
    defense = fields.Integer()
    elements = fields.Text()
    abilities = fields.Text()
    description = fields.Text()
    # image = fields.Binary('Image', related='aterra.image')

    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100
