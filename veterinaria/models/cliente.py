# -*- coding: utf-8 -*-
from odoo import fields, models



class Cliente(models.Model):
    _description = "Clientes"
    _order = "name"
    _inherit = ['res.partner']

    pacientes = fields.One2many('veterinaria.paciente', 'responsable', string="Pacientes")
