odoo.define("website_slide_video.website_slide_video",function(require){
    "use strict";
    var publicWidget = require('web.public.widget');
    var fullscreen = require('website_slides.fullscreen');
    // console.log(fullscreen);
    publicWidget.registry.websiteSlidesFullscreenPlayer.include({
        xmlDependencies: (publicWidget.registry.websiteSlidesFullscreenPlayer.prototype.xmlDependencies || [])
        .concat(['/test_video_upload/static/xml/extend_video_slides.xml']),
    })
})