# -*- coding: utf-8 -*-
# (C) 2019 Smile (<http://www.smile.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, tools
from odoo.addons.base.models.ir_mail_server import _logger


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    @api.model
    def send_email(self, message, mail_server_id=None, smtp_server=None,  *args, **kwargs):
        if not tools.config.get('enable_email_sending'):
            _logger.warning('Email sending not enabled')
            return False
        return super(IrMailServer, self).send_email(
            message, mail_server_id, smtp_server,  *args, **kwargs)

    def build_email(self, email_from, email_to, subject, body, email_cc=None,
                    email_bcc=None, reply_to=False, attachments=None,
                    message_id=None, references=None, object_id=False,
                    subtype='plain', headers=None, body_alternative=None,
                    subtype_alternative='plain'):
        if tools.config.get('email_to'):
            email_to = tools.email_split_and_format(tools.config['email_to'])
            email_cc = None
            email_bcc = None
        msg = super(IrMailServer, self).build_email(
            email_from, email_to, subject, body, email_cc, email_bcc, reply_to,
            attachments, message_id, references, object_id, subtype, headers,
            body_alternative, subtype_alternative)
        return msg
