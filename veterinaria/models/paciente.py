# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Paciente(models.Model):
    _name = "veterinaria.paciente"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Pacientes"
    _order = "especie,name"


    name = fields.Char(string='Nombre', required=True, tracking=True)
    numero = fields.Char(string='Número', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    microchip = fields.Char('Microchip')
    especie = fields.Many2one("paciente.especie", string="Especie", required=True)
    raza = fields.Many2one("paciente.raza", string="Raza", required=True)
    color = fields.Char(string="Color")
    peso = fields.Float(string="Peso (kg)")
    fecha_nacimiento = fields.Date(string="Fecha nacimiento")
    fecha_muerte = fields.Date(string="Fecha muerte")
    sexo = fields.Selection(
        string="Sexo",
        selection=[
            ("hembra", "Hembra"),
            ("macho", "Macho"),
            ("otro", "Otro")
        ],
        default="macho",
        required=True,
    )
    activo = fields.Boolean(default=True)
    muerto = fields.Boolean(default=False)
    comentarios = fields.Text(string="Comentarios")
    imagen = fields.Binary(
        "Imagen", attachment=True, help="Foto del paciente."
    )
    responsable = fields.Many2one('res.partner', string="Responsable")
    # cantidad_practicas = fields.Integer(string='Cantidad prácticas', compute='_contarPracticas')
    practicas = fields.One2many('veterinaria.practica', 'paciente', string="Prácticas")


    # def _contarPracticas(self):
    #     for rec in self:
    #         cantidad_practicas = self.env['veterinaria.practica'].search_count([('paciente', '=', rec.id)])
    #         rec.cantidad_practicas = cantidad_practicas

    @api.onchange('fecha_muerte')
    def onchange_fecha_muerte(self):
        self.muerto = True

    @api.model
    def create(self, vals):
        if vals.get('numero', _('New')) == _('New'):
            vals['numero'] = self.env['ir.sequence'].next_by_code('veterinaria.paciente') or _('New')
        res = super(Paciente, self).create(vals)
        return res

    def name_get(self):
         result = []
         for rec in self:
             name = '[' + rec.numero + '] ' + rec.name
             result.append((rec.id, name))
         return result

    # def abrir_practicas(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Practicas',
    #         'res_model': 'veterinaria.practica',
    #         'domain': [('paciente', '=', self.id)],
    #         'context': {'default_paciente': self.id},
    #         'view_mode': 'tree,form',
    #         'target': 'current',
    #     }
