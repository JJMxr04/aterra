# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Aterra(models.Model):
    _name = 'aterra.aterra'
    _description = 'aterra.aterra'
    name = fields.Char(string = 'Name')
    volume = fields.Integer(string = 'Volume')
    series = fields.Char(string = 'Series')
    card_number_id = fields.Integer(string = 'Card Number ID')
    type = fields.Many2one('aterra.cardtype', string='Card Type')
    rarity = fields.Many2one('aterra.cardrarity', string='Card Rarity')
    rank = fields.Integer(string = 'Rank')
    power = fields.Integer(string = 'Power')
    defense = fields.Integer(string = 'Defense')
    element1 = fields.Many2one('aterra.cardelement', string='1st Card Element')
    element2 = fields.Many2one('aterra.cardelement', string='2nd Card Element')
    element3 = fields.Many2one('aterra.cardelement', string='3rd Card Element')
    element4 = fields.Many2one('aterra.cardelement', string='4th Card Element')
    element5 = fields.Many2one('aterra.cardelement', string='5th Card Element')
    element6 = fields.Many2one('aterra.cardelement', string='6th Card Element')
    contract = fields.Many2one('aterra.cardcontract', string='Contract')
    abilities = fields.Text(string = 'Abilities')
    description = fields.Text(string = 'Description')
    image = fields.Binary(string="Image")
    is_published = fields.Boolean(string="Published",default=False)
    api_id = fields.Char(compute="def_api_id", store =True)
    image_Attachment_name = fields.Char(compute="def_att_name", store =True) 
    elements = fields.Char(compute='_get_list_of_elememts', store=True, string = 'Elements')
    image_url = fields.Char(string='Image URL', compute='_compute_image_url', store=True, compute_sudo=True, readonly=True)
    # image_url = fields.Char(string='Image URL', compute='_compute_image_url', store=True, compute_sudo=True, readonly=True, inverse='_inverse_image_url', search='_search_image_url', compute='_check_access')
    # image_url = fields.Char(compute='_compute_image_url', store=True, string = 'Card Photo')  # Added store=True to store the computed URL
    # rarity_image_url = fields.Char(compute='_get_rarity_image_url', store=True, string = 'Rarity Image URL')
    # type_image_url = fields.Char(compute='_get_type_image_url', store=True, string = 'Type Image URL')
    # contract_image_url = fields.Char(compute='_get_contract_image_url', store=True, string = 'Contract Image URL')
    # element1_image_url = fields.Char(compute='_get_element1_image_url', store=True, string = '1st Element Image URL')
    # element2_image_url = fields.Char(compute='_get_element2_image_url', store=True, string = '2nd Element Image URL')
    # element3_image_url = fields.Char(compute='_get_element3_image_url', store=True, string = '3rd Element Image URL')
    # element4_image_url = fields.Char(compute='_get_element4_image_url', store=True, string = '4th Element Image URL')
    # element5_image_url = fields.Char(compute='_get_element5_image_url', store=True, string = '5th Element Image URL')
    # element6_image_url = fields.Char(compute='_get_element6_image_url', store=True, string = '6th Element Image URL')
    
    
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
                'public': True,  # Set the attachment as public
            })
            # Update the image URL
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            record.image_url = '{}/web/content/{}'.format(base_url, attachment.id)

        return record

    #     @api.depends('element1','element2','element3','element4','element5','element6')
    # def _get_elements(self):
    #     for record in self:
    #         elementlist = []
    #         if self.element1:
    #             elementlist.append(self.element1.name)
    #         if self.element2:
    #             elementlist.append(self.element2.name)
    #         if self.element3:
    #             elementlist.append(self.element3.name)
    #         if self.element4:
    #             elementlist.append(self.element4.name)
    #         if self.element5:
    #             elementlist.append(self.element5.name)
    #         if self.element6:
    #             elementlist.append(self.element6.name)
    #     self.elements = elementslist.join(str(i) for i in elementlist)

    @api.depends('image', 'image_Attachment_name')
    def _compute_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for record in self:
            if record.image:
                # Generate the attachment URL based on the attachment ID
                attachment_id = self.env['ir.attachment'].search([
                    ('res_model', '=', 'aterra.aterra'),
                    ('res_id', '=', record.id),
                    ('name', '=', record.image_Attachment_name)
                ], limit=1)
                if attachment_id:
                    # Use the web.base.url to construct the attachment URL
                    record.image_url = '{}/web/content/{}'.format(base_url, attachment_id.id)
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

    # @api.depends('rarity')
    # def _get_rarity_image_url(self):
    #     for record in self:
    #         if record.rarity:
    #             record.rarity_image_url = record.rarity.image_url
    #         else:
    #             record.rarity_image_url = False

    # @api.depends('type')
    # def _get_type_image_url(self):
    #     for record in self:
    #         if record.type:
    #             record.type_image_url = record.type.image_url
    #         else:
    #             record.type_image_url = False

    # @api.depends('element1')
    # def _get_element1_image_url(self):
    #     for record in self:
    #         if record.element1:
    #             record.element1_image_url = record.element1.image_url
    #         else:
    #             record.element1_image_url = False

    # @api.depends('element2')
    # def _get_element2_image_url(self):
    #     for record in self:
    #         if record.element2:
    #             record.element2_image_url = record.element2.image_url
    #         else:
    #             record.element2_image_url = False

    # @api.depends('element3')
    # def _get_element3_image_url(self):
    #     for record in self:
    #         if record.element3:
    #             record.element3_image_url = record.element3.image_url
    #         else:
    #             record.element3_image_url = False

    # @api.depends('element4')
    # def _get_element4_image_url(self):
    #     for record in self:
    #         if record.element4:
    #             record.element4_image_url = record.element4.image_url
    #         else:
    #             record.element4_image_url = False

    # @api.depends('element5')
    # def _get_element5_image_url(self):
    #     for record in self:
    #         if record.element5:
    #             record.element5_image_url = record.element5.image_url
    #         else:
    #             record.element5_image_url = False
    
    # @api.depends('element6')
    # def _get_element6_image_url(self):
    #     for record in self:
    #         if record.element6:
    #             record.element6_image_url = record.element6.image_url
    #         else:
    #             record.element6_image_url = False

    # # this field is not used in the API, its simply there for backend display. To show the elements 
    # # on the card without having to have all 6 elemental fields showing in the list view.
    # @api.depends('element1','element2','element3','element4','element5','element6')
    # def _get_list_of_elememts(self):
    #     element_list_string = ""
    #     for record in self:
    #         if record.element1:
    #             element_list_string += " " + record.element1.name
    #         if record.element2:
    #             element_list_string += " " + record.element2.name
    #         if record.element3:
    #             element_list_string += " " + record.element3.name
    #         if record.element4:
    #             element_list_string += " " + record.element4.name
    #         if record.element5:
    #             element_list_string += " " + record.element5.name
    #         if record.element6:
    #             element_list_string += " " + record.element6.name
    #     record.elements = element_list_string

    # @api.depends('contract')
    # def _get_contract_image_url(self):
    #     for record in self:
    #         if record.contract:
    #             record.contract_image_url = record.contract.image_url
    #         else:
    #             record.contract_image_url = False
                    



#________________________________________________________________________-
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
            
    
#________________________________________________________________________-
class AterraCardType(models.Model):
    _name = 'aterra.cardtype'
    _description = 'aterra.cardtype'
    name = fields.Char()
    # rarity = fields.Char()
    image = fields.Binary(string="Image")
    image_url = fields.Char(compute='_compute_image_url', store=True)  # Added store=True to store the computed URL

    @api.model
    def create(self, values):
        # Create a new record
        record = super(AterraCardType, self).create(values)

        # Check if an image is provided
        if 'image' in values:
            # Attach the image as an attachment
            attachment = self.env['ir.attachment'].create({
                'name': record.name,
                'type': 'binary',
                'datas': values['image'],
                'res_model': 'aterra.cardtype',
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
                    ('res_model', '=', 'aterra.cardtype'),
                    ('res_id', '=', record.id),
                    ('name', '=', record.name)
                ], limit=1)
                if attachment_id:
                    record.image_url = '{}/web/content/{}/{}'.format(base_url, attachment_id.id, attachment_id.name)
                else:
                    record.image_url = False
            else:
                record.image_url = False


    @api.model
    def getAllCards(self):
        all_records = self.search([])
        return all_records

        



#________________________________________________________________________-
class AterraCardElement(models.Model):
    _name = 'aterra.cardelement'
    _description = 'aterra.cardelement'
    name = fields.Char()
    # rarity = fields.Char()
    image = fields.Binary(string="Image")
    image_url = fields.Char(compute='_compute_image_url', store=True)  # Added store=True to store the computed URL

    @api.model
    def create(self, values):
        # Create a new record
        record = super(AterraCardElement, self).create(values)

        # Check if an image is provided
        if 'image' in values:
            # Attach the image as an attachment
            attachment = self.env['ir.attachment'].create({
                'name': record.name,
                'type': 'binary',
                'datas': values['image'],
                'res_model': 'aterra.cardelement',
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
                    ('res_model', '=', 'aterra.cardelement'),
                    ('res_id', '=', record.id),
                    ('name', '=', record.name)
                ], limit=1)
                if attachment_id:
                    record.image_url = '{}/web/content/{}/{}'.format(base_url, attachment_id.id, attachment_id.name)
                else:
                    record.image_url = False
            else:
                record.image_url = False


#________________________________________________________________________-
class AterraCardContract(models.Model):
    _name = 'aterra.cardcontract'
    _description = 'aterra.cardcontract'
    name = fields.Char()
    # rarity = fields.Char()
    image = fields.Binary(string="Image")
    image_url = fields.Char(compute='_compute_image_url', store=True)  # Added store=True to store the computed URL

    @api.model
    def create(self, values):
        # Create a new record
        record = super(AterraCardContract, self).create(values)

        # Check if an image is provided
        if 'image' in values:
            # Attach the image as an attachment
            attachment = self.env['ir.attachment'].create({
                'name': record.name,
                'type': 'binary',
                'datas': values['image'],
                'res_model': 'aterra.cardcontract',
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
                    ('res_model', '=', 'aterra.cardcontract'),
                    ('res_id', '=', record.id),
                    ('name', '=', record.name)
                ], limit=1)
                if attachment_id:
                    record.image_url = '{}/web/content/{}/{}'.format(base_url, attachment_id.id, attachment_id.name)
                else:
                    record.image_url = False
            else:
                record.image_url = False


class AterraPlayerCards(models.Model):
    _name = 'aterra.playercards'
    _description = 'aterra.playercards'
    name = fields.Char(string='Owner Name')
    ownerid = fields.Integer(string='Owner ID')
    apikey= fields.Char(string='API Key')