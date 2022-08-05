# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Rubro(models.Model):
    _name = "item.rubro"
    _description = "Rubros"
    _order = "grupo,name"

    name = fields.Char(string='Rubro', required=True)
    descripcion = fields.Char(string='Descripción')
    grupo = fields.Many2one('item.grupo', string="Grupo", required=True)

