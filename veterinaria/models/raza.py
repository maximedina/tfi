# -*- coding: utf-8 -*-

from odoo import fields, models


class Raza(models.Model):
    _name = "paciente.raza"
    _description = "Razas"
    _order = "especie,name"

    name = fields.Char(string="Raza", translate=True, required=True)
    descripcion = fields.Char(string='Descripción')
    especie = fields.Many2one("paciente.especie", string="Especie", required=True)
