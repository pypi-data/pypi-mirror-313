from odoo import api, SUPERUSER_ID


def set_company_default_values(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Set company default values if it doesnt have them
    if not env.company.location_venta_deposito_id:
        env.company.location_venta_deposito_id = env.ref(
            "gestion_editorial.stock_location_deposito_venta"
        ).id

    if not env.company.product_category_ddaa_id:
        env.company.product_category_ddaa_id = env.ref(
            "gestion_editorial.product_category_ddaa"
        ).id

    if not env.company.stock_picking_type_compra_deposito_id:
        env.company.stock_picking_type_compra_deposito_id = env.ref(
            "gestion_editorial.stock_picking_type_compra_deposito"
        ).id

    if not env.company.account_journal_deposito_compra_id:
        env.company.account_journal_deposito_compra_id = env.ref(
            "gestion_editorial.account_journal_compra_deposito"
        ).id

    # Set new name for receptions picking type
    receptions_translation_es = env["ir.translation"].search(
        [
            ("module", "=", "stock"),
            ("name", "=", "stock.picking.type,name"),
            ("lang", "=", "es_ES"),
            ("src", "=", "Receipts"),
        ],
        limit=1,
    )

    receptions_translation_ca = env["ir.translation"].search(
        [
            ("module", "=", "stock"),
            ("name", "=", "stock.picking.type,name"),
            ("lang", "=", "ca_ES"),
            ("src", "=", "Receipts"),
        ],
        limit=1,
    )

    if receptions_translation_es:
        receptions_translation_es.write({"value": "Recepciones en firme"})
    if receptions_translation_ca:
        receptions_translation_ca.write({"value": "Recepcions en ferm"})
