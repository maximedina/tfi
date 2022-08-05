# -*- coding: utf-8 -*-

from odoo import fields, models


class Categoria(models.Model):
    _name = "item.categoria"
    _description = "Categorías"
    _order = "grupo,rubro,name"

    name = fields.Char(string='Categoría', required=True)
    descripcion = fields.Char(string='Descripción')
    turno = fields.Boolean(String='Turno')
    rubro = fields.Many2one('item.rubro', string="Rubro", required=True)
    grupo = fields.Many2one('item.grupo', string="Grupo", required=True)

