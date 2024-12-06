from odoo import models, fields


class EditorialPartners(models.Model):
    """ Extend res.partner template for editorial management """

    _description = "Editorial Partners"
    _inherit = 'res.partner'
    # we inherited res.partner model which is Odoo built in model and edited several fields in that model.
    cliente_num = fields.Integer(string="Num. cliente",
                           help="Número interno de cliente")
    is_author = fields.Boolean(string="Es autor", default=False,
                           help="Indica que el contacto es autor")
    contact_type = fields.Many2many('res.partner.type', string='Contact type')
    purchase_liq_pricelist = fields.Many2one(
        comodel_name='product.pricelist',
        string="Tarifa liquidaciones de compras",
        company_dependent=False,
        domain=lambda self: [('company_id', 'in', (self.env.company.id, False))],
        help="Esta tarifa se usará por defecto para liquidaciones de compra en depósito de este contacto")
    default_purchase_type = fields.Many2one(
        comodel_name='stock.picking.type',
        string="Tipo de compra",
        help="Este tipo de compra se usará por defecto en los pedidos de compra de este contacto",
        domain="[('code', '=', 'incoming')]"
    )

    def export_sales_deposit(self):
        wizard = self.env['wizard.deposito.history'].create({
            'deposit': 'ventas',
            'owner': self.id,
        })
        return wizard.export_resumen_xls()
    
    def export_purchases_deposit(self):
        wizard = self.env['wizard.deposito.history'].create({
            'deposit': 'compras',
            'owner': self.id,
        })
        return wizard.export_resumen_xls()


class EditorialPartnerType(models.Model):
    """ Editorial contact tags management """

    _description = 'Editorial contact type'
    _name = 'res.partner.type'
    _rec_name = 'name'

    name = fields.Char(string='Contact type', required=True)