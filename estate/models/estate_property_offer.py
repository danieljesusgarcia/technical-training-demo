from odoo import fields, models

class EstatePropertyOffer(models.Model):
   _name = "estate.property.offer"
   _description = "Model per estate.property.offer"
   price = fields.Float('Preu')
   status = fields.Selection([('Accepted', 'Acceptada'), ('Refused', 'Rebutjada')],copy=False)
   partner_id = fields.Many2one('res.partner', string='Comprador',required=True,copy=False)
   property_id = fields.Many2one('estate.property', string='Propietat',required=True)