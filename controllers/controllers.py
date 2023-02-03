# -*- coding: utf-8 -*-
# from odoo import http


# class Aterra(http.Controller):
#     @http.route('/aterra/aterra', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aterra/aterra/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('aterra.listing', {
#             'root': '/aterra/aterra',
#             'objects': http.request.env['aterra.aterra'].search([]),
#         })

#     @http.route('/aterra/aterra/objects/<model("aterra.aterra"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aterra.object', {
#             'object': obj
#         })
