# -*- coding: utf-8 -*-

from odoo import fields, models


class Contact_Inherit(models.Model):
    _inherit = ['contacts','mail.thread', 'mail.activity.mixin']

    pacientes = fields.One2many('veterinaria.paciente', 'paciente', string="Paciente")