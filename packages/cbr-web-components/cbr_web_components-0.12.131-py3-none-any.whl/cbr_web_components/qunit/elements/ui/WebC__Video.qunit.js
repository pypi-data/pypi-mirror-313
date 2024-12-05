import WebC__Target_Div from "../../../js/utils/WebC__Target_Div.mjs";
import WebC__Video      from "../../../js/elements/ui/WebC__Video.mjs";
import Web_Component    from "../../../js/core/Web_Component.mjs";


QUnit.module('WebC__API_Markdown_To_Html', function(hooks) {
    let target_div
    let webc__video
    let content_path

    hooks.beforeEach(async (assert) =>{
        //content_path               = 'en/web-pages/demos/index.md'
        target_div                 = WebC__Target_Div.add_to_body()
        let attributes             = expected_attributes
        webc__video = await target_div.append_child(WebC__Video, attributes)
    })
    hooks.afterEach(() => {
        webc__video.remove()
        target_div .remove()
    })

    QUnit.test('.constructor', (assert) => {
        assert.deepEqual(target_div.constructor.name          , 'WebC__Target_Div' )
        assert.deepEqual(WebC__Video.name                     , 'WebC__Video'      )
        assert.deepEqual(webc__video.getAttributeNames()      , ['url', 'width', 'height', 'title'])
        assert.deepEqual(webc__video.video_url                , expected_attributes.url   )
        assert.deepEqual(webc__video.video_width              , expected_attributes.width )
        assert.deepEqual(webc__video.video_height             , expected_attributes.height)

        assert.ok       (WebC__Video.prototype      instanceof Web_Component     )
        assert.ok       (webc__video                instanceof Web_Component     )
        assert.ok       (webc__video                instanceof HTMLElement       )
    })

    QUnit.test('.build', (assert) => {
        assert.deepEqual(webc__video.inner_html(), expected_html    )
    })

    const expected_attributes = { url     : 'https://www.youtube.com/embed/1q1Q1q1q1q1',
                                  width   : '560' ,
                                  height  : '315' ,
                                  title   : 'the video title' }

    const expected_html = `\
<div class="video_section">
    <div class="video_title">the video title</div>
    <video width="${expected_attributes.width}" height="${expected_attributes.height}" controls="">
        <source src="${expected_attributes.url}" type="video/mp4">Your browser does not support the video tag.
    </video>
</div>
`
})
