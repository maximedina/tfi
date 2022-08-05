# -*- coding: utf-8 -*-

from odoo import fields, models


class Fabricante(models.Model):
    _name = "item.fabricante"
    _description = "Fabricantes"
    _order = "name"

    name = fields.Char(string='Nombre', required=True)
    descripcion = fields.Char(string='Descripción')