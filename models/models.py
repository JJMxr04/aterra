# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Aterra(models.Model):
    _name = 'aterra.aterra'
    _description = 'aterra.aterra'
    api_id = fields.Char(compute="def_api_id", store =True)
    name = fields.Char()
    volume = fields.Integer()
    series = fields.Char()
    card_number_id = fields.Integer()
    rarity = fields.Char()
    rank = fields.Integer()
    power = fields.Integer()
    defense = fields.Integer()
    elements = fields.Char()
    abilities = fields.Text()
    description = fields.Text()
    image_Attachment_name = fields.Char(compute="def_att_name", store =True)  
    image = fields.Binary(string="Image")
    image_url = fields.Char(compute='_compute_image_url', store=True)  # Added store=True to store the computed URL
    
    
    @api.model
    def create(self, values):
        # Create a new record
        record = super(Aterra, self).create(values)

        # Check if an image is provided
        if 'image' in values:
            # Attach the image as an attachment
            attachment = self.env['ir.attachment'].create({
                'name': record.image_Attachment_name,
                'type': 'binary',
                'datas': values['image'],
                'res_model': 'aterra.aterra',
                'res_id': record.id,
            })
            # Update the image URL
            #record.image_url = attachment._get_download_url()

        return record

    @api.depends('image','image_Attachment_name')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for record in self:
            if record.image:
                # Generate the attachment URL based on the attachment ID and file name
                attachment_id = self.env['ir.attachment'].search([
                    ('res_model', '=', 'aterra.aterra'),
                    ('res_id', '=', record.id),
                    ('name', '=', record.image_Attachment_name)
                    #('name', '=', record.name)
                ], limit=1)
                if attachment_id:
                    # record.image_url = '{}/web/content/{}/{}'.format(base_url, attachment_id.card_series, attachment_id.name)
                    record.image_url = '{}/web/content/{}/{}'.format(base_url, attachment_id.id, attachment_id.name)
                else:
                    record.image_url = False
            else:
                record.image_url = False

    @api.depends('name','volume','card_number_id')
    def def_api_id(self):
        for record in self:
            if record.name:
                num = len("{}".format(record.card_number_id))
                if num == 3:
                    record.api_id = "{}".format(record.name[0]) + "{}".format(record.name[-1]) + "{}".format(record.volume) + "{}".format(record.card_number_id)
                elif num == 2:
                    record.api_id = "{}".format(record.name[0]) + "{}".format(record.name[-1]) + "{}".format(record.volume) + '0' + "{}".format(record.card_number_id)
                elif num == 1:
                    record.api_id = "{}".format(record.name[0]) + "{}".format(record.name[-1]) + "{}".format(record.volume) + '00' + "{}".format(record.card_number_id)
            else:
                record.api_id = ""

    @api.depends('name','series','card_number_id')
    def def_att_name(self):
        for record in self:
            if (record.name):
                #record.image_Attachment_name = '{} {} {}'.format(record.series, record.card_number_id, record.name)
                #record.image_Attachment_name = record.name
                record.image_Attachment_name = '{}-{}-{}'.format(record.series,record.card_number_id,record.name)
            else:
                record.image_Attachment_name =  'Image Name'



class AterraCardRarity(models.Model):
    _name = 'aterra.cardrarity'
    _description = 'aterra.cardrarity'
    name = fields.Char()
    # rarity = fields.Char()
    image = fields.Binary(string="Image")
    image_url = fields.Char(compute='_compute_image_url', store=True)  # Added store=True to store the computed URL

    @api.model
    def create(self, values):
        # Create a new record
        record = super(AterraCardRarity, self).create(values)

        # Check if an image is provided
        if 'image' in values:
            # Attach the image as an attachment
            attachment = self.env['ir.attachment'].create({
                'name': record.name,
                'type': 'binary',
                'datas': values['image'],
                'res_model': 'aterra.cardrarity',
                'res_id': record.id,
            })


        return record
    
    @api.depends('image','name')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for record in self:
            if record.image:
                # Generate the attachment URL based on the attachment ID and file name
                attachment_id = self.env['ir.attachment'].search([
                    ('res_model', '=', 'aterra.cardrarity'),
                    ('res_id', '=', record.id),
                    ('name', '=', record.name)
                ], limit=1)
                if attachment_id:
                    record.image_url = '{}/web/content/{}/{}'.format(base_url, attachment_id.id, attachment_id.name)
                else:
                    record.image_url = False
            else:
                record.image_url = False
            
    

