import Web_Component from "../../core/Web_Component.mjs";
import Div           from "../../core/Div.mjs";
import Tag           from "../../core/Tag.mjs";

export default class WebC__Video extends Web_Component {

    static class__video_section = 'video_section'
    static class__video_title   = 'video_title'

  // base class methods overrides
    apply_css() {
        this.add_css_rules(this.css_rules())
    }

    load_attributes() {
        super.load_attributes()
        this.video_title    = this.getAttribute('title'   )
        this.video_url      = this.getAttribute('url'     )
        this.video_width    = this.getAttribute('width'   )
        this.video_height   = this.getAttribute('height'  )
    }

    html () {
        const attr_video   = {width: this.video_width, height: this.video_height, controls: null}           // add the controls extra attribute so that controls are always present
        const div_video    = new Div({class: WebC__Video.class__video_section     })
        if (this.video_title) {
            const div_title = new Div({class: WebC__Video.class__video_title , value: this.video_title   })
            div_video.add_element(div_title)
        }
        const tag_video    = new Tag({tag: 'video', class: Web_Component.class__video, attributes: attr_video})
        const tag_source   = new Tag({tag: 'source', attributes: {src: this.video_url, type: 'video/mp4'}})

        tag_source.value = "Your browser does not support the video tag."
        tag_video.add_element(tag_source)
        div_video.add_element(tag_video)

        return div_video
    }

    css_rules() {
        return {
            [`.${WebC__Video.class__video_section}`] : { 'display'          : 'block'             ,
                                                         'text-align'       : 'center'            ,
                                                         'background-color' : '#fff'           ,
                                                         'border'           : '1px solid #ddd'    ,
                                                         'padding'          : '10px'              ,
                                                         'border-radius'    : '8px'               },

            [`.${WebC__Video.class__video_title}`  ] : { 'font-size'        : '20px'              ,
                                                         'font-weight'      : 'bold'              ,
                                                         'color'            : '#333'              ,
                                                         'margin-bottom'    : '10px'              },
        };
    }
}

WebC__Video.define()