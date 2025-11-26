import logging
from odoo.upgrade import util

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    util.records.remove_view(cr, xml_id="fel_digifact.invoice_form_fel_digifact")
    util.records.remove_view(cr, xml_id="fel_digifact.journal_form_fel_digifact")
    util.records.remove_view(cr, xml_id="fel_digifact.view_company_form_fel_digifact")
    util.records.remove_view(cr, xml_id="fel_digifact.view_partner_form_fel_digifact")
    _logger.info("Vistas viejas borradas")
