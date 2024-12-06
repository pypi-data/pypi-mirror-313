import WebC__Target_Div from "../../../js/utils/WebC__Target_Div.mjs";
import WebC__Video      from "../../../js/elements/ui/WebC__Video.mjs";
import Web_Component    from "../../../js/core/Web_Component.mjs";

const { module, test, only } = QUnit

// todo: wire back tests commented below

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

    test('loads custom attributes', async assert => {
        const attrs = {
            title : 'Test Video'         ,
            url   : 'test-video.mp4'     ,
            width : '640'                ,
            height: '480'
        }

        const custom_video = await target_div.append_child(WebC__Video, attrs)

        assert.equal(custom_video.video_title   , attrs.title                          , 'Sets title'              )
        assert.equal(custom_video.video_url     , attrs.url                            , 'Sets URL'                )
        assert.equal(custom_video.video_width   , attrs.width                          , 'Sets width'              )
        assert.equal(custom_video.video_height  , attrs.height                         , 'Sets height'             )
    })

    // test('renders video element correctly', async assert => {
    //     const attrs = {
    //         title : 'Test Video'         ,
    //         url   : 'test-video.mp4'     ,
    //         width : '640'                ,
    //         height: '480'
    //     }
    //
    //     const video = await target_div.append_child(WebC__Video, attrs)
    //
    //     const container = video.query_selector(`.${WebC__Video.class__video_section}`)
    //     assert.ok(container                                                            , 'Creates container'        )
    //
    //     const title = video.query_selector(`.${WebC__Video.class__video_title}`)
    //     assert.equal(title.textContent           , attrs.title                         , 'Shows title'             )
    //
    //     const video_element = video.query_selector('video')
    //     assert.ok(video_element                                                        , 'Creates video element'    )
    //     assert.equal(video_element.getAttribute('width' ) , attrs.width                , 'Sets video width'        )
    //     assert.equal(video_element.getAttribute('height'), attrs.height                , 'Sets video height'       )
    //     assert.ok(video_element.hasAttribute('controls')                               , 'Has controls'            )
    //
    //     const source = video_element.querySelector('source')
    //     assert.equal(source.getAttribute('src' ) , attrs.url                           , 'Sets source URL'         )
    //     assert.equal(source.getAttribute('type'), 'video/mp4'                          , 'Sets MIME type'          )
    // })

    test('renders without title when not provided', async assert => {
        const attrs = {
            url   : 'test-video.mp4'     ,
            width : '640'                ,
            height: '480'
        }

        const video = await target_div.append_child(WebC__Video, attrs)
        const title = video.query_selector(`.${WebC__Video.class__video_title}`)

        assert.notOk(title                                                            , 'No title element'         )
    })

    test('applies CSS rules correctly', async assert => {
        const css_rules = webc__video.css_rules()
        const section_class = `.${WebC__Video.class__video_section}`
        const title_class   = `.${WebC__Video.class__video_title}`

        assert.ok(css_rules[section_class]                                            , 'Has section styles'       )
        assert.ok(css_rules[title_class]                                              , 'Has title styles'         )

        assert.equal(css_rules[section_class]['text-align']      , 'center'           , 'Centers content'          )
        assert.equal(css_rules[title_class]['font-weight']       , 'bold'             , 'Bold title'              )
    })

    // test('includes fallback content', async assert => {
    //     const attrs = { url: 'test-video.mp4' }
    //     const video = await target_div.append_child(WebC__Video, attrs)
    //
    //     const source = video.query_selector('source')
    //     assert.equal(source.textContent, 'Your browser does not support the video tag.',
    //                                                                                      'Has fallback message'     )
    // })
})
