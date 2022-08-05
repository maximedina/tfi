# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Categoria(models.Model):
    _name = "veterinaria.turno"
    _description = "Turnos"
    _order = "inicio desc"

    name = fields.Char(compute='_armarNombre', store=True)
    inicio = fields.Datetime(string="Inicio", required=True)
    fin = fields.Datetime(string="Fin", required=True)
    paciente = fields.Many2one('veterinaria.paciente', string="Paciente", required=True)
    personal = fields.Many2one('veterinaria.personal', string="Personal")
    responsable = fields.Many2one('res.partner', string="Responsable", related='paciente.responsable')
    practica = fields.Many2one('veterinaria.item', string="Práctica", required=True)
    observaciones = fields.Text(string='Observaciones')
    tomado = fields.Boolean(string='Tomado')

    @api.depends('paciente', 'practica', 'personal', 'inicio')
    def _armarNombre(self):
        self[0]['name'] = str(self[0]['paciente'].name)+ '-' + str(self[0]['practica'].name) + '-' + str(self[0]['personal'].name) + '-' + str(self[0]['inicio'])
