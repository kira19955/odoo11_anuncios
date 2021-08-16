# -*- coding: utf-8 -*-
from odoo import http

# class Anuncios(http.Controller):
#     @http.route('/anuncios/anuncios/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anuncios/anuncios/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anuncios.listing', {
#             'root': '/anuncios/anuncios',
#             'objects': http.request.env['anuncios.anuncios'].search([]),
#         })

#     @http.route('/anuncios/anuncios/objects/<model("anuncios.anuncios"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anuncios.object', {
#             'object': obj
#         })