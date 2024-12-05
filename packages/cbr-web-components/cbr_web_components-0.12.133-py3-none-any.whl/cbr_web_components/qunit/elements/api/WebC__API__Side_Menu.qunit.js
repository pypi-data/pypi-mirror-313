import WebC__Target_Div             from "../../../js/utils/WebC__Target_Div.mjs";
import Web_Component                from "../../../js/core/Web_Component.mjs";
import API__Invoke                  from "../../../js/data/API__Invoke.mjs";
import WebC__API__Side_Menu         from "../../../js/elements/api/WebC__API__Side_Menu.mjs";
import WebC__API_Markdown_To_Html   from "../../../js/elements/api/WebC__API_Markdown_To_Html.mjs";
import {MOCK_MENU_DATA,
        setup_mock_responses        } from '../../../js/testing/Mock_API__Data.mjs'

if (typeof window.__karma__ !== 'undefined') {
    //console.log('Skipping QUnit module WebC__API__Side_Menu in Karma environment');
    QUnit.module.skip('WebC__API__Side_Menu', function(hooks) {
        // This module will be skipped entirely in Karma
    });
} else {
    QUnit.module('WebC__API__Side_Menu', function(hooks) {
        let target_div
        let webc__api_side_menu
        let api_path
        let data_file

        hooks.beforeEach(async (assert) =>{
            setup_mock_responses()

            data_file                = WebC__API__Side_Menu.data_file__default_menu
            data_file                = WebC__API__Side_Menu.data_file__default_menu
            target_div               = WebC__Target_Div.add_to_body()
            let attributes           = {['disable-cdn']:'True', ['data-file']: data_file, api_path: api_path }
            webc__api_side_menu      = await target_div.append_child(WebC__API__Side_Menu, attributes)
            webc__api_side_menu.wait_for__component_ready()
        })

        hooks.afterEach(() => {
            webc__api_side_menu.remove()
            target_div         .remove()
        })

        QUnit.test('.constructor', (assert) => {
            const  url__api__data_file = WebC__API__Side_Menu.url__api__data_file + WebC__API__Side_Menu.data_file__default_menu
            assert.deepEqual(url__api__data_file, '/markdown/static_content/data-file?path=en/web-pages/dev/web-components/api/side-menu/side-menu-1.toml')
            assert.deepEqual(target_div.constructor.name                  , 'WebC__Target_Div'                            )
            assert.deepEqual(WebC__API__Side_Menu.name                    , 'WebC__API__Side_Menu'                   )
            assert.deepEqual(webc__api_side_menu.data_file                , data_file                                  )
            assert.deepEqual(webc__api_side_menu.getAttributeNames()      , ['disable-cdn', 'data-file', 'api_path'])

            assert.ok       (WebC__API__Side_Menu.prototype          instanceof Web_Component              )
            assert.ok       (webc__api_side_menu                instanceof WebC__API_Markdown_To_Html )
            assert.ok       (webc__api_side_menu                instanceof Web_Component              )
            assert.ok       (webc__api_side_menu                instanceof HTMLElement                )
            assert.ok       (webc__api_side_menu.api_invoke     instanceof API__Invoke                )
            //assert.ok       (webc__api_side_menu.css_load_result.css_loaded)
        })

        // todo: fix this test which started failing after adding the screenshot link (which has a dynamic link)
        // QUnit.test('.build', (assert) => {
        //     assert.deepEqual(webc__api_side_menu.inner_html(), expected_html    )
        // })

        QUnit.test ('.load_menu_data', async (assert) => {
            assert.deepEqual(await webc__api_side_menu.api_invoke.invoke_api('/ping', 'GET'), { success: true, data: { status: 'pong' } })
            assert.deepEqual(webc__api_side_menu.menu_data, MOCK_MENU_DATA, 'Loads expected menu data')

        })

        const expected_html = `\
    <div class="side_menu_section">
        <div class="side_menu_item">
            <a class="side_menu_link" href="${MOCK_MENU_DATA.first_link.href}">
                <div class="mdi me-2 ${MOCK_MENU_DATA.first_link.icon} side_menu_icon">
                </div>
                <div class="side_menu_text">${MOCK_MENU_DATA.first_link.text}</div>
            </a>
        </div>
        <div class="side_menu_item">
            <a class="side_menu_link" href="${MOCK_MENU_DATA.second_link.href}">
                <div class="mdi me-2 ${MOCK_MENU_DATA.second_link.icon} side_menu_icon">
                </div>
                <div class="side_menu_text">${MOCK_MENU_DATA.second_link.text}</div>
            </a>
        </div>    
    </div>
    `

    })
}