# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions
from odoo.addons.alfresco_connection.models import decorators as alfcon

class anuncios(models.Model):
    _name = 'anuncios.anuncios'
    _rec_name = 'propietarios'

    state = fields.Selection(selection=[('rechazada', 'Rechazada'),('recibida', 'Recibida')],
                             default="recibida")
    propietarios = fields.Many2one(
        'res.partner.contactosalternos', string="Nombre")
    representante_legal = fields.Many2one(
        'res.partner.contactosalternos', string="Representante Legal")
    tipo_a = fields.Boolean(string="Tipo A")
    tipo_b = fields.Boolean(string="Tipo B")
    tipo_c = fields.Boolean(string="Tipo C")

    # Datos de domicilio
    estado_notific = fields.Char(string='Estado', compute="get_propietario_info_notific")
    ciudad_notific = fields.Char(string='Ciudad', compute="get_propietario_info_notific")
    colonia_notific = fields.Char(string='Ciudad', compute="get_propietario_info_notific")
    cp_notific = fields.Char(string='Código postal', compute="get_propietario_info_notific")
    calle_notific = fields.Char(string='Calle', compute="get_propietario_info_notific")
    no_exterior_notific = fields.Char(string='No. Exterior', compute="get_propietario_info_notific")
    no_interior_notific = fields.Char(string='No. Interior', compute="get_propietario_info_notific")
    rfc_noti = fields.Char(string="RFC", compute="get_propietario_info_notific")
    nombre_lega = fields.Char(string="Nombre del representate legal", compute="legal")
    curp_lega = fields.Char(string="Curp del representante legal", compute="legal")

    # documentacion
    identificacion = fields.Binary(string="Identificaion Oficial, Carta Poder o Poder Notarial")
    croquis = fields.Binary(string="Croquis de localización. (Tipo A indicar calles, días y horarios)")
    foto_anuncio = fields.Binary(strinf="Fotografías del anuncio publicitario")
    selec_categororia = fields.Many2many('categoria.anuncios', string="Categorias de anuncios ")
    horario = fields.One2many('horas', 'ho', string="Horario")

    # tipo b
    copia_contrato = fields.Binary(string="Copia del contrato de arrendamiento o escritura del inmueble")
    copia_anterior = fields.Binary(string="Copia de Licencia Anterior")
    uso_suelo = fields.Binary(string="Uso de Suelo, Uso Comercial o Cedula de Funcionamiento")
    # tipo c
    responsiva_perito = fields.Binary(string="Responsiva de Perito. (B en caso de anuncios mayores a 10 metros)")
    memoria_calculo = fields.Binary(string="Memoria de Cálculo.")
    seguro_personas = fields.Binary(string="Seguro a terceras personas.")
    factibilidad = fields.Binary(string="Factibilidad de Protección Civil.")
    responsiva_mantenimiento = fields.Binary(string="Responsiva de mantenimiento.")

    # validacion del tramite
    estatus_docum = fields.Selection([('DI', 'Trámite debidamente integrado'), (
        'DNI', 'Trámite no debidamente integrado')], string='Estatus de trámite', track_visibility=True)
    textoadjuntomail = fields.Text(
        string="Motivo de correo electrónico", track_visibility=True)
    fecha_env_correo = fields.Datetime(
        string="Fecha de envio de correo", track_visibility=True)

    campos_modificar = fields.One2many('anuncios.campos_editafront', 'id_solicitud')
    #mapa
    address = fields.Char(string="Dirección")
    latitud = fields.Char(string='Latitud', track_visibility=True)
    longitud = fields.Char(string='Longitud', track_visibility=True)
    latitud_aux = fields.Char(string="Latitud", compute="_get_latitud")
    longitud_aux = fields.Char(string="Longitud", compute="_get_longitud")

    def _get_latitud(self):
        for rec in self:
            rec.latitud_aux = str(rec.latitud)

    def _get_longitud(self):
        for rec in self:
            rec.longitud_aux = str(rec.longitud)

    def get_propietario_info_notific(self):
        for modelo in self:
            modelo.estado_notific = modelo.propietarios.state.d_estado
            modelo.ciudad_notific = modelo.propietarios.city.d_municipio
            modelo.colonia_notific = modelo.propietarios.suburb.name
            modelo.cp_notific = modelo.propietarios.zip_cp.cp
            modelo.calle_notific = modelo.propietarios.street
            modelo.no_exterior_notific = modelo.propietarios.external_number
            modelo.no_interior_notific = modelo.propietarios.internal_number
            modelo.rfc_noti = modelo.propietarios.rfc

    def legal(self):
        for r in self:
            r.nombre_lega = r.propietarios.name
            r.curp_lega = r.propietarios.curp

    def rechazado(self):
        self.state = 'rechazada'


class Categoria_Anuncios(models.Model):
    _name = 'categoria.anuncios'

    name = fields.Char(string="Nombre de la categoria")


class horas(models.Model):
    _name = 'horas'

    name = fields.Selection(selection=[('L', 'Lunes'), ('M', 'Martes'),
                                       ('Mi', 'Miercoles'), ('J', 'Jueves'),
                                       ('v', 'Viernes')],
                            string="Dia")
    hora_inicio = fields.Float(string="Hora inicio")
    hora_fin = fields.Float(string="Hora Fin")
    ho = fields.Many2one('anuncios.anuncios')

class settings_config_anuncios(models.Model):
    _name = 'settings_config_anuncios'

    titulo = fields.Text(string="Título")
    descripcon = fields.Html(string="Descripción")
    requisitos = fields.Html(string="Requisitos")
    icon_module = fields.Binary(string="Icono")

class anuncios_campos_editafront(models.Model):
    _name = 'anuncios.campos_editafront'

    id_solicitud  = fields.Many2one('anuncios.anuncios')
    
    campo_modific = fields.Many2one('estructura_front.estrucuta_fields', domain="[('estructura_front','=',8), ('editable','=',True)]")


    @api.model
    @alfcon.related_files
    def create(self, values):
        if not values['campo_modific']:
            raise exceptions.Warning("Imposible guardar un campo vacio, verifique la lista de campos seleccionados.")
        campo_rep = self.env['anuncios.campos_editafront'].sudo().search([('id_solicitud', '=',values['id_solicitud']),('campo_modific', '=',values['campo_modific'])])
        if campo_rep:
            raise exceptions.Warning("El campo seleccionado " + campo_rep.campo_modific.display_name +" ya lo selecciono previamente.")
        return super(anuncios_campos_editafront, self).create(values)
 
    @api.multi
    @alfcon.related_files
    def write(self, values):
        # raise exceptions.Warning("Imposible editar registro, deberar eliminar o agregar un nuevo registro.")
        return super(anuncios_campos_editafront, self).write(values)

    @api.multi
    @alfcon.dummy_read
    def read(self, fields=None, load='_classic_read'):
        return super(anuncios_campos_editafront, self).read(fields, load=load)