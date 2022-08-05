# -*- coding: utf-8 -*-

from odoo import fields, models


class Grupo(models.Model):
    _name = "item.grupo"
    _description = "Grupos"
    _order = "name"

    name = fields.Char(string='Grupo', required=True)
    descripcion = fields.Char(string='Descripción')