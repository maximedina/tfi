# -*- coding: utf-8 -*-
from email.policy import default
from odoo import api, fields, models


class Item(models.Model):
    _name = "veterinaria.item"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Items"
    _order = "name"

    name = fields.Char(string='Nombre', required=True, tracking=True)
    codigo = fields.Char(string='Código', required=True)
    descripcion = fields.Text(string='Descripción')
    precio_costo = fields.Float(string='Precio costo', required=True, default=0)
    porcentaje_precio = fields.Float(string='Porcentaje precio', required=True, default=30)
    iva = fields.Float(string='Iva', default=21, required=True)
    precio_venta = fields.Float(string='Precio de venta', compute='_calcularPrecio', readonly=True)
    presentacion = fields.Text(string='Presentación')
    duracion = fields.Float(string='Duración', default=0)
    stock = fields.Float(string='Stock', default=0)
    stock_minimo = fields.Float(string='Stock mínimo', default=0)
    activo = fields.Boolean(string="Activo", default=True)
    proveedor = fields.Many2one('res.partner', string='Proveedor', required=True)
    grupo = fields.Many2one('item.grupo', string="Grupo")
    rubro = fields.Many2one('item.rubro', string="Rubro")
    categoria = fields.Many2one('item.categoria', string="Categoría")
    fabricante = fields.Many2one('item.fabricante', string="Fabricante")
    imagen = fields.Binary(string="Imagen producto")

    @api.depends('precio_costo', 'porcentaje_precio', 'iva')
    def _calcularPrecio(self):
        self[0]['precio_venta'] = self[0]['precio_costo'] * (1 + self[0]['iva'] / 100) * (1 + self[0]['porcentaje_precio'] / 100)

    def name_get(self):
         result = []
         for rec in self:
             name = '[' + rec.codigo + '] ' + rec.name
             result.append((rec.id, name))
         return result