from odoo import fields, models


class EditorialResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_editorial_ddaa = fields.Boolean(
        string="Módulo derechos de autoría",
        related="company_id.module_editorial_ddaa",
        readonly=False,
    )

    product_category_ddaa_id = fields.Many2one(
        related="company_id.product_category_ddaa_id", readonly=False
    )

    product_categories_genera_ddaa_ids = fields.Many2many(
        related="company_id.product_categories_genera_ddaa_ids", readonly=False
    )

    stock_picking_type_compra_deposito_id = fields.Many2one(
        related="company_id.stock_picking_type_compra_deposito_id", readonly=False
    )

    account_journal_deposito_compra_id = fields.Many2one(
        related="company_id.account_journal_deposito_compra_id", readonly=False
    )

    location_venta_deposito_id = fields.Many2one(
        related="company_id.location_venta_deposito_id", readonly=False
    )

    location_authors_id = fields.Many2one(
        related="company_id.location_authors_id", readonly=False
    )

    location_promotion_id = fields.Many2one(
        related="company_id.location_promotion_id", readonly=False
    )

    visibility_limited_by_supplier = fields.Boolean(
        string="Limited visibility for supplier by default",
        related="company_id.visibility_limited_by_supplier",
        help="If enabled, new products will by default have limited visibility per supplier. \n"
             "The product will only be visible in purchasing for the configured suppliers. \n"
             "Then it is possible to edit each product individually",
        readonly=False,
    )
