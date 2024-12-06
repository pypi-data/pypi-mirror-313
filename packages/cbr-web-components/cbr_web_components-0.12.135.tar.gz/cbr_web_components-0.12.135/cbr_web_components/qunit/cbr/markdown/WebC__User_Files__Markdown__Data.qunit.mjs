import Web_Component                     from "../../../js/core/Web_Component.mjs";
import WebC__User_Files__Markdown__Data  from '../../../js/cbr/markdown-editor/WebC__User_Files__Markdown__Data.mjs';
import WebC__Target_Div                  from '../../../js/utils/WebC__Target_Div.mjs';
import CBR_Events                        from "../../../js/cbr/CBR_Events.mjs";
import {
    setup_mock_responses, set_mock_response, MOCK_FILE_ID, MOCK_CONTENT, MOCK_FILE_DATA
} from '../../../js/testing/Mock_API__Data.mjs';


const { module, test , only} = QUnit;

module('WebC__User_Files__Markdown__Data', hooks => {
    let markdownData;
    let targetDiv;

    hooks.before(async () => {
        setup_mock_responses();
        targetDiv     = WebC__Target_Div.add_to_body();
        markdownData  = await targetDiv.append_child(WebC__User_Files__Markdown__Data);
        await markdownData.wait_for__component_ready();
    });

    hooks.after(() => {
        markdownData.remove();
        targetDiv.remove();
    });

    test('constructor and inheritance', assert => {
        assert.ok(markdownData instanceof WebC__User_Files__Markdown__Data , 'Is an instance of Markdown Data');
        assert.ok(markdownData instanceof Web_Component                   , 'Extends Web_Component');
    });

    test('loads and applies CSS frameworks', assert => {
        const cssRules = markdownData.all_css_rules();
        assert.ok(Object.keys(cssRules).length > 0    , 'Has CSS rules');
        assert.ok(cssRules['.data-panel .alert']      , 'Includes data-panel alert styles');
    });

    test('renders initial state correctly', assert => {
        const panel = markdownData.query_selector('.data-panel');
        const message = markdownData.query_selector('.data-message');

        assert.ok(panel   , 'Data panel exists');
        assert.ok(message , 'Primary data message exists');
        assert.ok(message.classList.contains('alert-primary'), 'Primary message has correct class');
    });

    test('displays messages correctly', assert => {
        markdownData.show_message__info('Info message');
        assert.equal(markdownData.text_data_message.innerText, 'Info message', 'Displays info message');
        assert.ok(markdownData.text_data_message.classList.contains('alert-secondary'), 'Info message has correct class');

        markdownData.show_message__success('Success message');
        assert.equal(markdownData.text_data_message.innerText, 'Success message', 'Displays success message');
        assert.ok(markdownData.text_data_message.classList.contains('alert-success'), 'Success message has correct class');

        markdownData.show_message__error('Error message');
        assert.equal(markdownData.text_data_message.innerText, 'Error message', 'Displays error message');
        assert.ok(markdownData.text_data_message.classList.contains('alert-danger'), 'Error message has correct class');

        markdownData.show_message();
        assert.ok(markdownData.text_data_message.is_hidden(), 'Hides message when no text is provided');
    });

    test('handles edit mode correctly', assert => {
        markdownData.on_edit_mode();
        assert.ok(markdownData.text_data_message.is_hidden(), 'Clears message on edit mode');
    });

    test('handles file changed event correctly', assert => {
        markdownData.on_file_changed();
        assert.equal(markdownData.text_data_message.innerText, '... unsaved changes...', 'Displays warning message for unsaved changes');
        assert.ok(markdownData.text_data_message.classList.contains('alert-warning'), 'Warning message has correct class');
    });

    test('handles file load event correctly', async assert => {
        markdownData.raise_event_global(CBR_Events.CBR__FILE__LOAD, { file_id: MOCK_FILE_ID });

        await markdownData.wait_for_event(CBR_Events.CBR__FILE__VIEW_MODE)

        assert.equal(markdownData.file_id, MOCK_FILE_ID, 'File ID is set correctly');
        assert.equal(markdownData.text_data_message.innerText, 'file data loaded ok', 'Displays success message after loading file');
    });

    test('handles file save event correctly', async assert => {
        markdownData.raise_event_global(CBR_Events.CBR__FILE__SAVE)

        await markdownData.wait_for_event(CBR_Events.CBR__FILE__SAVED)

        assert.deepEqual(markdownData.text_data_message.innerText, 'Changes saved'        , 'Displays success message after saving file');
        assert.ok      (markdownData.text_data_message.classList.contains('alert-success'), 'Success message has correct class');
    });


    test('handles file load handles error ok correctly', async assert => {
        set_mock_response(`/api/user-data/files/file-contents?file_id=${MOCK_FILE_ID}` , 'GET', null)
        markdownData.raise_event_global(CBR_Events.CBR__FILE__LOAD, { file_id: MOCK_FILE_ID });
        await markdownData.wait_for_event(CBR_Events.CBR__FILE__LOAD_ERROR)
        assert.equal(markdownData.text_data_message.innerText, 'Mock response is null for GET:/api/user-data/files/file-contents?file_id=test-file-123')
    });

    test('handles file save handles error ok correctly', async assert => {
        set_mock_response(`/api/user-data/files/update-file` , 'PUT', null)
        markdownData.raise_event_global(CBR_Events.CBR__FILE__SAVE, { file_id: MOCK_FILE_ID });
        await markdownData.wait_for_event(CBR_Events.CBR__FILE__SAVE_ERROR)
        assert.equal(markdownData.text_data_message.innerText, 'Mock response is null for PUT:/api/user-data/files/update-file')
    });
});
