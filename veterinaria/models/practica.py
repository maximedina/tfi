# -*- coding: utf-8 -*-

from odoo import time, api, fields, models, _
from datetime import datetime


class Practica(models.Model):
    _name = "veterinaria.practica"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Práctica veterinaria"
    _order = "nro_practica"

    nro_practica = fields.Char(string='Nro práctica', required=True, copy=False, readonly=True,
                               default=lambda self: _('New'))
    paciente = fields.Many2one('veterinaria.paciente', string="Paciente", required=True)
    imagen = fields.Binary(string="Foto", related='paciente.imagen')
    practicas_paciente = fields.One2many(string="Practicas del paciente", related='paciente.practicas')
    especie = fields.Char(string="Especie", related='paciente.especie.name', readonly=True)
    raza = fields.Char(string="Raza", related='paciente.raza.name', readonly=True)
    color = fields.Char(string="Color", related='paciente.color', readonly=True)
    peso = fields.Float(string="Peso (kg)", related='paciente.peso', readonly=True)
    fecha_nacimiento = fields.Date(string="Fecha nacimiento", related='paciente.fecha_nacimiento', readonly=True)
    sexo = fields.Selection(string="Sexo", related='paciente.sexo', readonly=True)
    responsable = fields.Many2one('res.partner', string="Responsable", related='paciente.responsable')
    personal = fields.Many2one('veterinaria.personal', string="Personal", required=True)
    fecha = fields.Datetime(string="Fecha", required=True, default=fields.Datetime.now)
    turno = fields.Many2one('veterinaria.turno', string="Turno")
    proxima_practica = fields.Date(string="Próxima visita", default=fields.Datetime.today)
    notas = fields.Text(string='Notas')
    practica_items = fields.One2many('practica.items', 'practica_id', string="Items")
    total = fields.Float(string='Total', default=0)

    @api.model
    def create(self, vals):
        if vals.get('nro_practica', _('New')) == _('New'):
            vals['nro_practica'] = self.env['ir.sequence'].next_by_code('veterinaria.practica') or _('New')
        res = super(Practica, self).create(vals)
        return res

    def aviso_proxima_visita(self):
        practicas = self.search([])
        for r in practicas:
            dias = (datetime.combine(r.proxima_practica, datetime.min.time()) - datetime.now()).days
            if dias == 7:
                mail_from = 'medvet@veterinaria.com'
                mail_to = r.responsable.email

                mail_vals = {
                    'subject': 'Veterinaria - Recordatorio próxima visita',
                    'email_from': mail_from,
                    'email_to': mail_to,
                    'message_type': 'email',
                    'body_html': 'Le recordamos su próxima visita recomendada para ' + str(r.paciente.name) + ', el ' + str(
                        r.proxima_practica) + ', por favor, comuniquese para solicitar un turno.',
                }

                mail_id = self.env['mail.mail'].create(mail_vals)
                mail_id.send()

    @api.onchange('practica_items')
    def onchange_practica_items(self):
        self.total = 0
        for e in self.practica_items:
            self.total += e.subtotal


class PracticaItems(models.Model):
    _name = "practica.items"
    _description = "Items de la práctica"

    item = fields.Many2one('veterinaria.item', string="Item")
    precio_venta = fields.Float(string="Precio", related='item.precio_venta', readonly=True, store=True)
    cantidad = fields.Float(string="Cantidad", default=1)
    descuento = fields.Float(string="Descuento")
    subtotal = fields.Float(string="Total", readonly=True, compute='_subtotal', store=True)
    stock = fields.Float(string="Stock", store=True, related='item.stock')
    practica_id = fields.Many2one('veterinaria.practica', string="Práctica")

    @api.depends('precio_venta', 'cantidad', 'descuento')
    def _subtotal(self):
        for e in self:
            e.subtotal = e.precio_venta * e.cantidad * (1 - e.descuento / 100)
            # self[0]['subtotal'] = self[0]['precio_venta'] * self[0]['cantidad'] * (1 - self[0]['descuento'] / 100)

    # @api.depends('cantidad')
    # def _stock(self):
    #     if self[0]['item.stock_minimo'] > 0:
    #         if self[0]['item.stock'] - self[0]['cantidad'] <= 0:
    #             mensaje = f'El stock no es suficiente para cubrir la cantidad solicitada.'
    #             self[0]['cantidad'] = self[0]['item.stock']
    #             self[0]['item.stock'] = 0
    #             view = self.env.ref('sh_message.sh_message_wizard')
    #             view_id = view and view.id or False
    #             context = dict(self._context or {})
    #             context['message'] = mensaje
    #             return {
    #                 'name': 'Aviso',
    #                 'type': 'ir.actions.act_window',
    #                 'view_type': 'form',
    #                 'view_mode': 'form',
    #                 'res_model': 'sh.message.wizard',
    #                 'views': [(view.id, 'form')],
    #                 'views_id': view.id,
    #                 'target': 'new',
    #                 'context': context,
    #             }
    #         else:
    #             if self[0]['item.stock'] - self[0]['cantidad'] <= self[0]['item.stock_minimo']:
    #                 mensaje = f'Se alcanzo el stock minimo.'
    #                 view = self.env.ref('sh_message.sh_message_wizard')
    #                 view_id = view and view.id or False
    #                 context = dict(self._context or {})
    #                 context['message'] = mensaje
    #                 return {
    #                     'name': 'Aviso',
    #                     'type': 'ir.actions.act_window',
    #                     'view_type': 'form',
    #                     'view_mode': 'form',
    #                     'res_model': 'sh.message.wizard',
    #                     'views': [(view.id, 'form')],
    #                     'views_id': view.id,
    #                     'target': 'new',
    #                     'context': context,
    #                 }
    #             self[0]['item.stock'] = self[0]['item.stock'] - self[0]['cantidad']
