# -*- coding: utf-8 -*-

from odoo import fields, models


class Especie(models.Model):
    _name = "paciente.especie"
    _description = "Especies"
    _order = "name"

    name = fields.Char(string="Nombre", translate=True, required=True)
    descripcion = fields.Char(string='Descripción')
    razas = fields.One2many("paciente.raza", "especie", string="Razas")
