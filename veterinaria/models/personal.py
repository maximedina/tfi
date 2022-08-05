# -*- coding: utf-8 -*-

from odoo import fields, models


class Personal(models.Model):
    _name = "veterinaria.personal"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Personal"
    _rec_name = 'name'

    dni = fields.Char(string='Dni', required=True, tracking=True)
    foto = fields.Binary(string="Foto")
    name = fields.Char(string='Nombre', required=True, tracking=True)
    matricula = fields.Char(string='Matrícula')
    genero = fields.Selection([
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otro', 'Otro'),
    ], required=True, default='masculino', tracking=True)
    fecha_nacimiento = fields.Date(string="Fecha nacimiento")
    activo = fields.Boolean(string="Activo", default=True)