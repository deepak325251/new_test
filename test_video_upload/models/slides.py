# -*- coding: utf-8 -*-
#################################################################################

from odoo import api, fields, models, _
import logging
from werkzeug import urls
import re

logger = logging.getLogger(__name__)

class Slide(models.Model):
    _inherit = 'slide.slide'

    slide_attachment = fields.Many2one('ir.attachment', help="Video/Document")
    document_type = fields.Selection([('binary', 'File')],
                             string='Document Type', required=True, default='binary', change_default=True,
                             help="You can either upload a file from your computer or copy/paste an internet link to your file.")
    
    embed_code_val = fields.Text('Embed Code Val', readonly=True,)
    custom_slide_type = fields.Selection([
        ('infographic', 'Infographic'),
        ('presentation', 'Presentation'),
        ('document', 'Document'),
        ('video', 'Video/Audio'),
        ('quiz', "Quiz"),
        # ('scorm', 'Scorm'),
        ('certification', 'Certification')],
        string='Type', required=True,
        default='document',
        help="The document type will be set automatically based on the document URL and properties (e.g. height and width for presentation and document).")

    @api.model
    def create(self, values):
        channel_id = self._context.get('default_channel_id')
        if channel_id:
            values['channel_id'] = channel_id
        if values.get('slide_type') == 'document':
            values['slide_type'] = 'document'
        if values.get('slide_type') == 'video':
            values['slide_type'] = 'video'
        res = super(Slide, self).create(values)
        return res

    def write(self, values):
        if values.get('document_type') == 'binary':
            values['slide_type'] = 'video'
        res = super(Slide, self).write(values)
        return res
    
    def _parse_document_url(self, url, only_preview_fields=False):
        document_source, document_id = self._find_document_data_from_url(url)
        if document_source and hasattr(self, '_parse_%s_document' % document_source):
            return getattr(self, '_parse_%s_document' % document_source)(document_id, only_preview_fields)
        return {'error': _('Unknown document')}

    def _find_document_data_from_url(self, url):
        url_obj = urls.url_parse(url)
        if url_obj.ascii_host == 'youtu.be':
            return ('youtube', url_obj.path[1:] if url_obj.path else False)
        elif url_obj.ascii_host in ('youtube.com', 'www.youtube.com', 'm.youtube.com', 'www.youtube-nocookie.com'):
            v_query_value = url_obj.decode_query().get('v')
            if v_query_value:
                return ('youtube', v_query_value)
            split_path = url_obj.path.split('/')
            if len(split_path) >= 3 and split_path[1] in ('v', 'embed'):
                return ('youtube', split_path[2])
        expr = re.compile(r'(^https:\/\/docs.google.com|^https:\/\/drive.google.com).*\/d\/([^\/]*)')
        arg = expr.match(url)
        document_id = arg and arg.group(2) or False
        if document_id:
            return ('google', document_id)

        return (None, False)

    @api.onchange('document_type')
    def remove_link(self):
        self.url = ''

    @api.onchange('url')
    def remove_attachment_link(self):
        self.slide_attachment = False

class WebsiteSlides(models.Model):
    _name = "website.slide.video"
    
    allowed_types = fields.Many2many("wk.video.types")
    is_active = fields.Boolean("Is Active")

    @api.onchange('is_active')
    def set_active(self):
        if self.is_active:
            for setting in self.search([]):
                if setting.id != self.id:
                    setting.is_active = False
            self.is_active = True

class VideoTypes(models.Model):
    _name = "wk.video.types"

    name = fields.Char("Types",help="Write extension of videos allowed")

    @api.onchange('name')
    def add_prefix(self):

        if self.name:
            self.name = "video/"+self.name


