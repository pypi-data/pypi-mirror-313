from odoo import api, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)

def migrate(cr, version):
    try:
        env = api.Environment(cr, SUPERUSER_ID, {})
        _logger.warning("### MIGRATING TO 13.0.0.8.0 ###")

        # Set is_sales_deposit_return value
        total_moves = env['account.move'].search([]).write({'is_sales_deposit_return': False})
        _logger.info(f"### Total account.move: {total_moves}")
        deposit_sales_return_moves = env['account.move'].search([
            ('type', '=', 'out_refund'),
            ('is_liquidacion', '=', True)
        ]).write({'is_sales_deposit_return': True})
        _logger.info(f"### Total is_sales_deposit_return: {deposit_sales_return_moves}")

    except Exception as e:
        _logger.error(f"Error while migrating to 13.0.0.8.0 : {str(e)}")
        raise