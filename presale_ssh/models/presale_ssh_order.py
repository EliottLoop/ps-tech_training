from traitlets import default

from odoo import api, fields, models


class PresaleSshOrder(models.Model):
    _name = "presale.ssh.order"
    _description = "Table with presale orders"
    _inherit = "mail.thread"
    name = fields.Char(string="Name", readonly=True, copy=False, default="New")
    customer_id = fields.Many2one("res.partner", string="Customer")
    stage = fields.Selection(selection=[("draft", "Draft"), ("confirmed", "Confirmed")], default="draft")
    order_lines_ids = fields.Many2many("presale.ssh.order.line", string="Order Lines")
    sale_order_id = fields.Many2one("sale.order")
    active = fields.Boolean(default=True)

    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("presale.ssh.order") or "New"
        return super().create(vals)

    def action_presale_order_validate(self):
        # Sale order creation
        for rec in self:
            vals = {"partner_id": rec.customer_id.id, "presale_order_id": rec.id}
            sale_order = rec.env["sale.order"].create(vals)
            for line in rec.order_lines_ids:
                rec.env["sale.order.line"].create(
                    {
                        "product_id": line.product_id.id,
                        "order_id": sale_order.id,
                        "name": line.product_id.name,
                        "price_unit": line.price,
                        "product_uom_qty": line.quantity,
                    }
                )
        # Change state
        rec.stage = "confirmed"
        # Send email
        rec.send_email()
        return sale_order

    def send_email(self):
        self.ensure_one()
        template_id = self.env["mail.template"].search([("name", "=", "Presale Order Mail")], limit=1)
        template_id.send_mail(self.id)

    @api.model
    def _archive(self):
        for presale in self.env["presale.ssh.order"].search([("stage", "=", "confirmed")]):
            presale.active = False
