# -*- coding: utf-8 -*-

from odoo import models, fields, api, _ 

# class ResPartner(models.Model):
   
#     _inherit = 'res.partner'
#     # coins = fields.Integer(string = 'Coins')


    # coins = volume = fields.Integer(string = 'Coins')


class Aterra(models.Model):
    _name = 'aterra.aterra'
    _description = 'aterra.aterra'
    name = fields.Char(string = 'Name')
    volume = fields.Integer(string = 'Volume')
    series = fields.Many2one('aterra.cardseries', string = 'Series')
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
    is_found = fields.Boolean(string="Found",default=False)

    api_id = fields.Char(compute="def_api_id", store =True)
    image_Attachment_name = fields.Char(compute="def_att_name", store =True) 
    elements = fields.Char(compute='_get_list_of_elememts', store=True, string = 'Elements')
    image_url = fields.Char(string='Image URL', compute='_compute_image_url', store=True, compute_sudo=True, readonly=True)

    card_number_id = fields.Integer(string = 'Card Number ID')


    @api.model
    def getAllCards(self):
        all_records = self.env['aterra.aterra'].sudo().search([])
        return all_records


    @api.model
    def getCardNumber(self):
        for record in self:
            cards = self.getAllCards()
            num = 0
            if cards:
                for card in cards:

                    if card.card_number_id > num:
                        num = card.card_number_id

            record.card_number_id = num + 1


    
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
            record.image_url = '{}/web/content/{}/{}'.format(base_url, attachment.id, attachment.name)
        record.getCardNumber()
        return record

    #     

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
                record.image_Attachment_name = '{}-{}-{}'.format(record.series.name,record.card_number_id,record.name)
            else:
                record.image_Attachment_name =  'Image Name'

    def _get_list_of_elememts(self):
        element_list_string = ""
        for record in self:
            if record.element1:
                element_list_string += " " + record.element1.name
            if record.element2:
                element_list_string += " " + record.element2.name
            if record.element3:
                element_list_string += " " + record.element3.name
            if record.element4:
                element_list_string += " " + record.element4.name
            if record.element5:
                element_list_string += " " + record.element5.name
            if record.element6:
                element_list_string += " " + record.element6.name
        record.elements = element_list_string



    # # this field is not used in the API, its simply there for backend display. To show the elements 
    # # on the card without having to have all 6 elemental fields showing in the list view.
    @api.depends('element1','element2','element3','element4','element5','element6')
    def _get_list_of_elememts(self):
        element_list_string = ""
        for record in self:
            if record.element1:
                element_list_string += " " + record.element1.name
            if record.element2:
                element_list_string += " " + record.element2.name
            if record.element3:
                element_list_string += " " + record.element3.name
            if record.element4:
                element_list_string += " " + record.element4.name
            if record.element5:
                element_list_string += " " + record.element5.name
            if record.element6:
                element_list_string += " " + record.element6.name
        record.elements = element_list_string


                    



#________________________________________________________________________-
class AterraCardRarity(models.Model):
    _name = 'aterra.cardrarity'
    _description = 'aterra.cardrarity'
    name = fields.Char()
   
    
   
            
    
#________________________________________________________________________-
class AterraCardType(models.Model):
    _name = 'aterra.cardtype'
    _description = 'aterra.cardtype'
    name = fields.Char()



#________________________________________________________________________-
class AterraCardElement(models.Model):
    _name = 'aterra.cardelement'
    _description = 'aterra.cardelement'
    name = fields.Char()



#________________________________________________________________________-
class AterraCardContract(models.Model):
    _name = 'aterra.cardcontract'
    _description = 'aterra.cardcontract'
    name = fields.Char()


#_____________________________________________________________________________
class AterraPlayerCards(models.Model):
    _name = 'aterra.playercards'
    _description = 'aterra.playercards'
    name = fields.Char(string='Owner Name')
    ownerid = fields.Integer(string='Owner ID')
    apikey= fields.Char(string='API Key')

