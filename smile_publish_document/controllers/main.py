# -*- coding: utf-8 -*-
import io
import mimetypes
import os
# from io import BytesIO
import base64

from odoo import http, _
from odoo.http import request
from werkzeug.utils import redirect


class WebsiteAttachmentPage(http.Controller):

    def get_attachments(self):
        attachment_ids = request.env['ir.attachment'].sudo().search(
            [('website_published', '=', True)])
        documents = {}
        for record in attachment_ids:
            document_type = record.document_type_id and record.document_type_id.name or _(
                'Others')
            if document_type in documents:
                documents[document_type].append(record)
            else:
                vals = {document_type: [record]}
                documents.update(vals)
        return documents

    @http.route('/PublishAttachments', type='http', auth="public", website=True)
    def attachment_details(self, **kw):
        return request.render('smile_publish_document.attachment_template',
                              {'attachments': self.get_attachments()})

    @http.route(['/publish-attachment/download'], type='http', auth='public')
    def download_attachment(self, attachment_id, **kw):
        fields = ["name", "store_fname", "datas", "mimetype", "res_model", "res_id",
                  "type", "url"]
        attachment = request.env['ir.attachment'].sudo().search_read(
            [('id', '=', int(attachment_id))], fields)
        if attachment:
            attachment = attachment[0]
        else:
            return redirect('/PublishAttachments')

        if attachment["type"] == "url":
            if attachment["url"]:
                return redirect(attachment["url"])
            else:
                return request.not_found()
        elif attachment["datas"]:
            data = io.BytesIO(base64.standard_b64decode(attachment["datas"]))
            # we follow what is done in ir_http's binary_content for the extension management D:\addons\odoo-formio\formio_storage_filestore\controllers\main.py
            extension = os.path.splitext(attachment["name"] or '')[1]
            extension = extension if extension else mimetypes.guess_extension(attachment["mimetype"] or '')
            filename = attachment['name']
            filename = filename if os.path.splitext(filename)[1] else filename + extension
            return http.send_file(data, filename=filename, as_attachment=True)
        else:
            return request.not_found()
