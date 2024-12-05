import Web_Component                        from '../../../js/core/Web_Component.mjs'
import WebC__User_Files__Markdown__Toolbar  from '../../../js/cbr/markdown-editor/WebC__User_Files__Markdown__Toolbar.mjs';
import WebC__Target_Div                     from '../../../js/utils/WebC__Target_Div.mjs';
import CBR_Events                           from "../../../js/cbr/CBR_Events.mjs";
import { setup_mock_responses}              from '../../../js/testing/Mock_API__Data.mjs'

const { module, test, only } = QUnit;

module('WebC__User_Files__Markdown__Toolbar', hooks => {
    let toolbar;
    let targetDiv;

    hooks.before(async () => {
        setup_mock_responses()
        targetDiv = WebC__Target_Div.add_to_body();
        toolbar   = await targetDiv.append_child(WebC__User_Files__Markdown__Toolbar);
        await toolbar.wait_for__component_ready();
    });

    hooks.after(() => {
        toolbar.remove();
        targetDiv.remove();
    });

    test('constructor and inheritance', assert => {
        assert.ok(toolbar instanceof WebC__User_Files__Markdown__Toolbar , 'Is an instance of Markdown Toolbar');
        assert.ok(toolbar instanceof Web_Component                       , 'Extends Web_Component');
    });

    test('loads and applies CSS frameworks', assert => {
        const cssRules = toolbar.all_css_rules();
        assert.ok(Object.keys(cssRules).length > 0     , 'Has CSS rules');
        assert.ok(cssRules['.markdown-toolbar']        , 'Includes toolbar styles');
        assert.ok(cssRules['.markdown-data']           , 'Includes markdown-data styles');
    });

    test('renders initial state correctly', assert => {
        assert.ok(toolbar.query_selector('.markdown-toolbar'), 'Toolbar exists');
        assert.ok(toolbar.btn_edit                          , 'Edit button exists');
        assert.ok(toolbar.btn_save                          , 'Save button exists');
        assert.ok(toolbar.btn_cancel                        , 'Cancel button exists');
        assert.ok(toolbar.btn_show_history                  , 'Show History button exists');
        assert.ok(toolbar.btn_hide_history                  , 'Hide History button exists');
        assert.ok(toolbar.query_selector('.markdown-data')  , 'Markdown data div exists'                );
        assert.ok(toolbar.btn_edit        .is_visible()     , 'Edit button is initially visible'        );
        assert.ok(toolbar.btn_save        .is_visible()     , 'Save button is initially visible'        );
        assert.ok(toolbar.btn_cancel      .is_visible()     , 'Cancel button is initially visible'      );
        assert.ok(toolbar.btn_show_history.is_visible()     , 'Show History button is initially visible');
        assert.ok(toolbar.btn_hide_history.is_hidden()      , 'Hide History button is initially hidden' )
    });

    test('button click triggers correct events', assert => {
        assert.expect(5);

        const done = assert.async(5);

        toolbar.addEventListener(CBR_Events.CBR__FILE__EDIT_MODE, event => {
            assert.ok(true, 'Edit event triggered');
            done();
        });
        toolbar.btn_edit.click();

        toolbar.addEventListener(CBR_Events.CBR__FILE__CANCEL, event => {
            assert.ok(true, 'Cancel event triggered');
            done();
        });
        toolbar.btn_cancel.click();

        toolbar.addEventListener(CBR_Events.CBR__FILE__SAVE, event => {
            assert.ok(true, 'Save event triggered');
            done();
        });
        toolbar.btn_save.click();

        toolbar.addEventListener(CBR_Events.CBR__FILE__SHOW_HISTORY, event => {
            assert.ok(true, 'Show History event triggered');
            done();
        });
        toolbar.btn_show_history.click();

        toolbar.addEventListener(CBR_Events.CBR__FILE__HIDE_HISTORY, event => {
            assert.ok(true, 'Hide History event triggered');
            done();
        });
        toolbar.btn_hide_history.click();
    });

    test('event handlers update UI correctly', assert => {
        toolbar.on_file_view_mode();
        assert.ok   (toolbar.btn_edit  .is_enabled ()         , 'Edit button is enabled in view mode');
        assert.ok   (toolbar.btn_cancel.is_disabled()         , 'Cancel button is disabled in view mode');
        assert.ok   (toolbar.btn_save  .is_disabled()         , 'Save button is disabled in view mode');

        toolbar.on_file_edit_mode();
        assert.ok   (toolbar.btn_edit  .is_disabled()         , 'Edit button is disabled in edit mode');
        assert.ok   (toolbar.btn_cancel.is_enabled ()         , 'Cancel button is enabled in edit mode');
        assert.ok   (toolbar.btn_save  .is_enabled ()         , 'Save button is enabled in edit mode');

        toolbar.on_show_history();
        assert.ok   (toolbar.btn_hide_history.is_visible(), 'Hide History button is visible after show history');
        assert.notOk(toolbar.btn_show_history.is_visible(), 'Show History button is hidden after show history');

        toolbar.on_hide_history();
        assert.ok   (toolbar.btn_show_history.is_visible(), 'Show History button is visible after hide history');
        assert.notOk(toolbar.btn_hide_history.is_visible(), 'Hide History button is hidden after hide history');
    });

    test('loads attributes correctly', assert => {
        toolbar.setAttribute('file-id'  , 'test-file-id');
        toolbar.setAttribute('edit-mode', 'true');
        toolbar.setAttribute('view-mode', 'summary');

        toolbar.load_attributes();

        assert.equal(toolbar.file_id  , 'test-file-id', 'File ID attribute loaded');
        assert.ok   (toolbar.edit_mode, 'Edit mode attribute loaded as true');
        assert.equal(toolbar.view_mode, 'summary'     , 'View mode attribute loaded as summary');
    });

    test('on_file_load', assert => {
        toolbar.file_id = null
        const event = { detail: { file_id: 'test-file-id' }}
        toolbar.on_file_load(event)
        assert.deepEqual(toolbar.file_id, 'test-file-id')
        toolbar.file_id = null

    })
});