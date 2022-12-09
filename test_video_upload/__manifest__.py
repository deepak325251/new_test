# -*- coding: utf-8 -*-

{
    'name': "test_video_upload",
    'version': '0.1',
    'summary': """
        Custom Module for video upload""",
    'author'        : 'Test',
    'category'      : 'Uncategorized',
    'description'   : """eLearning Video Uploader facilitates you upload the video from
     your local hence, you are not dependent upon youtube to upload the video.""",
    'depends'       : [
        'website_slides',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizard/attachment_wizard_view.xml',
        'views/website_slides_video_views.xml',
        'views/website_slides.xml',
    ],
    
    'demo':['demo/demo.xml'],
    
    'qweb': [
        'static/xml/extend_video_slides.xml',
    ],
    "images"        :  "",
    "application"   :  False,
    "installable"   :  True,
    "auto_install"  :  False,
    "price"         :  25,
    "currency"      :  "USD",
    'sequence'      :   1,
}
