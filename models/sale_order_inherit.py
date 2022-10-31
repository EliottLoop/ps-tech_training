from odoo import fields,models

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    presale_order_id = fields.Many2one('presale.ssh.order',string="Presale Order")