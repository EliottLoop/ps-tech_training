from odoo import fields,models

class PresaleSshOrderLine(models.Model):
    _name = "presale.ssh.order.line"
    _description = "Table with order lines"

    product_id = fields.Many2one('product.product',string="Product",required=True)
    quantity = fields.Float(required=True)
    price = fields.Float(required=True)