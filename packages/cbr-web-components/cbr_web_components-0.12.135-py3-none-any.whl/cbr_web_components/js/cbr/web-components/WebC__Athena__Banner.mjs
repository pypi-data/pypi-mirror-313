import Web_Component        from '../../core/Web_Component.mjs';
import CSS__Grid            from '../../css/grid/CSS__Grid.mjs';
import CSS__Typography      from '../../css/CSS__Typography.mjs';
import CSS__Cards           from '../../css/CSS__Cards.mjs';
import H                    from '../../core/H.mjs';
import Div                  from '../../core/Div.mjs';
import Raw_Html             from '../../core/Raw_Html.mjs';
import API__Invoke          from '../../data/API__Invoke.mjs';
import API__Markdown        from "../api/API__Markdown.mjs";
import CBR__Paths           from "../CBR__Paths.mjs";

export default class WebC__Athena__Banner extends Web_Component {

    constructor() {
        super()
        this.api_markdown  = new API__Markdown()
    }
    load_attributes() {
        new CSS__Grid       (this).apply_framework()
        new CSS__Typography (this).apply_framework()
        new CSS__Cards      (this).apply_framework()
        this.api_invoke = new API__Invoke()
    }

    async load_data() {
        this.content      = await this.api_markdown.get_data__markdown_page(CBR__Paths.FILE__CONTENT__SITE__ATHENA__BANNER)
    }

    html() {
        const content_card = new Div     ({ class: 'card m-1'      })
        const content_body = new Div     ({ class: 'card-body' })
        const card_title   = new H       ({ level: 1,  class: 'card-title',  value: this.content?.metadata?.title})
        const card_text    = new Raw_Html({ class: 'card-text',  value: this.content?.html })
        content_card.add_element(content_body)
        content_body.add_elements(card_title , card_text)
        return content_card
    }
}

WebC__Athena__Banner.define()