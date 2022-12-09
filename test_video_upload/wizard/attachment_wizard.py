#################################################################################
from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class VideoAttachmentWizard(models.TransientModel):
    _name = "video.attachment.wizard"

    attachment = fields.Binary(
        string="Attachment",
        required=True)
    name = fields.Char(
        string='Name')

    # @api.multi
    def add_video_attachment(self):
        modelName = self._context.get('active_model')
        modelId = self._context.get('active_id')

        attachmentValue = {
            'name': self.name,
            'datas': self.attachment,
            'res_model': modelName,
            'res_id': modelId,
            'type': 'binary',
            'db_datas': self.name,
            'res_name': self.name,
        }
        res = self.env['ir.attachment'].create(attachmentValue)
        file_size = 500 * 1024 * 1024

        allowed_types = self.env['website.slide.video'].search(
            [('is_active', '=', True)], limit=1)
        allowed_format = []
        flag = False
        for format in allowed_types.allowed_types:
            allowed_format.append(format.name)
        if allowed_format:
            if res.mimetype not in allowed_format:
                flag = True
        # if (not flag and res.file_size <= file_size):
        attachmentObj = self.env['slide.slide'].browse(modelId)
        attachmentObj.slide_attachment = res.id
        # print('-----------------------',attachmentObj.s3_bucket_url)
        
        attachmentObj.embed_code_val= '<iframe src="/web/content?model=ir.attachment&amp;field=datas&amp;id=%s"  allow="autoplay" allowFullScreen="true" frameborder="0"></iframe>' % (attachmentObj.slide_attachment.id)
        
        # attachmentObj.embed_code_val= '<iframe src="%s"  allow="autoplay" allowFullScreen="true" frameborder="0"></iframe>' % (attachmentObj.s3_bucket_url)

        # else:
        #     res.unlink()
        #     raise UserError(
        #         _("Only allowed formats and size less than 25Mb can be uploaded."))

        return True
