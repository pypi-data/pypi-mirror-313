import WebC__Target_Div             from "../../../js/utils/WebC__Target_Div.mjs";
import Web_Component                from "../../../js/core/Web_Component.mjs";
import API__Invoke                  from "../../../js/data/API__Invoke.mjs";
import WebC__API_Markdown_To_Html   from "../../../js/elements/api/WebC__API_Markdown_To_Html.mjs";
import WebC__Markdown__Card         from "../../../js/elements/markdown/WebC__Markdown__Card.mjs";
import { MOCK_CONTENT_PATH     ,
         MOCK_MARKDOWN_METADATA,
         setup_mock_responses  }    from '../../../js/testing/Mock_API__Data.mjs'



QUnit.module('WebC__Markdown__Card', function(hooks) {
    let target_div
    let webc__markdown_card
    let mock_responses
    let api_path

    hooks.beforeEach(async (assert) =>{
        setup_mock_responses()
        target_div                 = WebC__Target_Div.add_to_body()
        let attributes             = { ['disable-cdn']:'True', ['content-path']:MOCK_CONTENT_PATH, api_path: api_path }
        webc__markdown_card        = target_div.append_child(WebC__Markdown__Card, attributes)
        webc__markdown_card.wait_for__component_ready()

    })

    hooks.afterEach(() => {
        webc__markdown_card.remove()
        target_div         .remove()
    })


    QUnit.test('.constructor', (assert) => {
        assert.deepEqual(target_div.constructor.name                  , 'WebC__Target_Div'                        )
        assert.deepEqual(WebC__Markdown__Card.name                    , 'WebC__Markdown__Card'                    )
        assert.deepEqual(webc__markdown_card.content_path             , MOCK_CONTENT_PATH                         )
        assert.deepEqual(webc__markdown_card.getAttributeNames()      , ['disable-cdn', 'content-path', 'api_path'])

        assert.ok       (WebC__Markdown__Card.prototype      instanceof Web_Component            )
        assert.ok       (webc__markdown_card                instanceof WebC__API_Markdown_To_Html)
        assert.ok       (webc__markdown_card                instanceof Web_Component             )
        assert.ok       (webc__markdown_card                instanceof HTMLElement               )
        assert.ok       (webc__markdown_card.api_invoke     instanceof API__Invoke               )
    })

    QUnit.test('.build', async (assert) => {
        assert.deepEqual(await webc__markdown_card.api_invoke.invoke_api('/ping', 'GET'), { success: true, data: { status: 'pong' } })
        assert.deepEqual(webc__markdown_card.inner_html(), expected_html)
    })

    const expected_raw_html = `\
<h1>Markdown content</h1>
<ul>
    <li>will go here
    </li>
</ul>`

    const expected_html = `\
<div class="markdown_card">
    <div class="markdown_card_body">
        <div class="markdown_card_title">${MOCK_MARKDOWN_METADATA.title}</div>
        <div class="markdown_card_subtitle">${MOCK_MARKDOWN_METADATA.sub_title}</div>
        <div class="markdown_content_div">
            <h1>Markdown content</h1>
            <ul>
                <li>will go here
                </li>
            </ul>
        </div>
        <div class="markdown_action">
            <a class="markdown_action_link" href="${MOCK_MARKDOWN_METADATA.action_link}">${MOCK_MARKDOWN_METADATA.action_text}</a>
        </div>
    </div>
</div>
`
})


