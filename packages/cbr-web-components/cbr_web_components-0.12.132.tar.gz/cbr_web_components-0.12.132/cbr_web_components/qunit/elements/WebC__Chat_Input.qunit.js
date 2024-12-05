import WebC__Chat_Input     from '../../js/chat-bot/WebC__Chat_Input.mjs'
import WebC__Target_Div     from '../../js/utils/WebC__Target_Div.mjs'
import Web_Component        from "../../js/core/Web_Component.mjs";


QUnit.module('WebC__Chat_Input', function(hooks) {

    let webc_chat_input
    let target_div
    let channel     = 'an_channel'

    hooks.beforeEach(async () => {
        target_div = WebC__Target_Div.add_to_body().build({width: "50%"})
        webc_chat_input = target_div.append_child(WebC__Chat_Input, {channel:channel})
        await webc_chat_input.wait_for__component_ready()
    });

    hooks.afterEach(() => {
        target_div.remove()
    })

    QUnit.test('.constructor()', (assert) => {
        assert.equal(WebC__Chat_Input.element_name, 'webc-chat-input'         , 'WebC__Chat_Message element name was correctly set'           )
        assert.ok   (WebC__Chat_Input.prototype instanceof Web_Component      , 'WebC__Chat_Message.prototype is an instance of Web_Component');
        assert.ok    (webc_chat_input instanceof WebC__Chat_Input)
        assert.ok    (webc_chat_input instanceof Web_Component   )
        assert.ok    (webc_chat_input instanceof Object          )
    })

    QUnit.test('.connectedCallback()', (assert) => {
        assert.deepEqual(webc_chat_input.channels, [ 'Web_Component', 'WebC__Chat_Input' , 'an_channel']);
    })

    QUnit.test('.event_dispatch()',     (assert) => {
        //const target_div        = WebC__Target_Div.add_to_body().build({width:"50%"})
        //const web_chat_input    = target_div.append_child(WebC__Chat_Input)
        const message_to_send   = 'an sent message'
        const expected_message  = {"channel": channel, "images": [], user_prompt: message_to_send }
        const keyevent           = new KeyboardEvent('keydown')
        keyevent._key ='Enter'

        var message_received = null
        var on_new_input_message = (e)=>{
             message_received = e.detail
        }
        window.addEventListener('new_input_message', on_new_input_message);

        assert.equal(message_received, null)

        webc_chat_input.input.value = message_to_send

        webc_chat_input.input.dispatchEvent(keyevent)
        assert.propEqual(message_received, expected_message)
        assert.equal(webc_chat_input.input.value, '')

        target_div.remove()
        window.removeEventListener('new_input_message', on_new_input_message);
    })

    QUnit.test('.input()', (assert) => {
        let events_dispatch = webc_chat_input.events_utils.events_dispatch
        let event_type      = 'set_value'
        let channel         = webc_chat_input.channel
        let value           = 'an value set via set_value event'
        let event_data      = {'value': value}
        let input           = webc_chat_input.input                                 // get reference to input element via 'invoke' event
        events_dispatch.send_to_channel(event_type, channel, event_data)            // use 'set_value' event to set the value of the text area
        assert.deepEqual(input.value, value)                                        // confirm values match
    })

    QUnit.test('.render()', (assert) => {
        // const div_setup = {top: "30%", width: "50%", bottom:"50%"}
        // const target_div = WebC__Target_Div.add_to_body().build(div_setup)
        // const web_chat_input = target_div.append_child(WebC__Chat_Input)
        const expected_html =
`
<div class="chat-images"></div>

<div class="chat-input">
    <!--<input id='file-input' type="file" />-->
    <!--<label for="file-input" class="file-input-label">+</label>-->
    <div class="form-input"></div>
    <!--<webc-form-input channel="an_channel" webc_id="webc-form-input"></webc-form-input>-->
    <!--<input id='user-prompt' type="text" placeholder="Enter a message..." autocomplete=\"off\"/>-->
    <button id=\"action-button\">send</button>
    <button id=\"clear-button\">clear</button>
</div>
`
        assert.equal(webc_chat_input.html(), expected_html)
        target_div.remove()
    })

    QUnit.test('Create test image', (assert) => {
        var base64Image      = create_test_img_base64(200,500);
        const div_setup      = {top: "200px"}
        //const target_div     = WebC__Target_Div.add_to_body().build(div_setup)
        //const web_chat_input = target_div.append_child(WebC__Chat_Input)
        assert.equal(webc_chat_input.images.children.length, 0)
        webc_chat_input.displayImage(base64Image)
        const img = webc_chat_input.images.children[0]
        const style = "width:auto; height:auto; margin:10px;max-width:150px;max-height:150px"
        assert.equal(img.outerHTML,`<img src="${base64Image}" style="${style}">`)
        assert.equal(webc_chat_input.images.children.length, 1)
        assert.equal(img.src,base64Image)


        // trigger an sendmessage event
        var on_new_input_message = (e)=>{}
        window.addEventListener('new_input_message', on_new_input_message);                     // todo add support for generic event listener to the beforeEach afterEach

        const keyevent           = new KeyboardEvent('keydown')
        keyevent._key            ='Enter'          // todo: replace with proper event dispatch
        webc_chat_input.input.value = 'now with an image'
        webc_chat_input.input.dispatchEvent(keyevent)
        assert.equal(webc_chat_input.images.children.length, 0)
        target_div.remove()
        window.removeEventListener('new_input_message', on_new_input_message);
    })


    // QUnit.test('setup_upload_button', (assert) => {
    //     //var base64Image      = create_test_img_base64(200,500);
    //     assert.equal(webc_chat_input.query_selector('#file-input'), null)
    //     let div_file_input             = document.createElement('div');                // todo: find a better way to add this temp DIV
    //     div_file_input.id              = 'file-input';
    //     div_file_input.style.display   = 'none';
    //     div_file_input.type            = 'file'
    //     webc_chat_input.shadow_root_append(div_file_input);
    //
    //     webc_chat_input.setup_upload_button()
    //
    //     assert.equal(webc_chat_input.images.children.length,0)
    //
    //     const blob          = new Blob(['file content'], { type: 'image/png' });
    //     const file          = new File([blob], 'image.png', { type: 'image/png' });      // Create a File from the Blob
    //     const dataTransfer  = new DataTransfer();
    //     dataTransfer.items.add(file);
    //
    //     div_file_input.files = dataTransfer.files;
    //
    //     const event = new Event('change');
    //     div_file_input.dispatchEvent(event);
    //
    //     target_div.remove()
    //     div_file_input.remove()
    // })



    // todo: add tests for the cases where there is data in clipboardData
    QUnit.test('on_process_paste (via paste event)', (assert) => {
        const input = webc_chat_input.input
        const event = new Event('paste');
        input.dispatchEvent(event);
        assert.ok(1)

    })

    QUnit.test('on_input_keydown (via keydown event)', (assert) => {
        let on_new_input_message_data = null
        const on_new_input_message    = (e)=>{ on_new_input_message_data = e.detail }
        const input                   = webc_chat_input.input
        const event = new Event('keydown');

        window.addEventListener('new_input_message', on_new_input_message);
        // no value in key
        input.dispatchEvent(event);
        assert.deepEqual(on_new_input_message_data, null)

        // with  key = 'Enter', value = ''
        event.key = 'Enter'                                             // when we only have an Enter value
        input.dispatchEvent(event);
        assert.deepEqual(on_new_input_message_data, null)               // there will be no event dispatched

        // with  key = 'Enter', value = 'aaaa'
        input.value = 'aaaa'
        event.key   = 'Enter'
        input.dispatchEvent(event);
        assert.deepEqual(on_new_input_message_data, { user_prompt: 'aaaa', images: [], channel: channel })
        assert.deepEqual(input.value, '')

        // with  _key = 'Enter', value = 'bbbb'
        on_new_input_message_data = null
        input.value               = 'bbbb'
        event.key                 = null
        event._key                = 'Enter'
        input.dispatchEvent(event);
        assert.deepEqual(on_new_input_message_data, { user_prompt: 'bbbb', images: [], channel: channel })
        assert.deepEqual(input.value, '')

        // with  key = 'a' and _key = 'b' and    value = 'cccc'
        on_new_input_message_data = null
        input.value               = 'cccc'
        event.key                 = 'a'
        event._key                = 'b'
        input.dispatchEvent(event);
        assert.deepEqual(on_new_input_message_data, null)
        assert.deepEqual(input.value, 'cccc')

        window.removeEventListener('new_input_message', on_new_input_message);
    })

    QUnit.test('on_clear_button (via click event)', (assert) => {
        let on_clear_messages_data = null
        const on_clear_messages    = (e)=>{ on_clear_messages_data       = e.detail }
        const clear_button         = webc_chat_input.clear_button

        window.addEventListener('clear_messages', on_clear_messages);

        const event = new Event('click');
        clear_button.dispatchEvent(event);
        assert.deepEqual(on_clear_messages_data,{channel: channel})

        window.removeEventListener('clear_messages', on_clear_messages);
    })

    QUnit.test('on_action_button (via click event)', (assert) => {

        let on_stop_stream_data = null
        let on_new_input_message_data = null
        const on_stop_stream       = (e)=>{ on_stop_stream_data       = e.detail }
        const on_new_input_message = (e)=>{ on_new_input_message_data = e.detail }
        window.addEventListener('stop_stream'      , on_stop_stream      );                     // todo add support for generic event listener to the beforeEach afterEach
        window.addEventListener('new_input_message', on_new_input_message);

        const action_button = webc_chat_input.action_button
        const event = new Event('click');
        action_button.dispatchEvent(event);

        assert.equal(action_button.innerHTML     , 'send')
        assert.equal(action_button.style.backgroundColor, '')
        assert.equal(on_stop_stream_data      , null)
        assert.equal(on_new_input_message_data, null)


        //with action_button.input.value = ''
        action_button.dispatchEvent(event);
        assert.equal(on_stop_stream_data      , null)
        assert.equal(on_new_input_message_data, null)
        assert.equal(action_button.innerHTML     , 'send')
        assert.equal(action_button.style.backgroundColor, '')

        // ##### with action_button = 'stop'
        action_button.innerHTML = 'stop'
        action_button.dispatchEvent(event);
        assert.deepEqual(on_stop_stream_data                , {channel: channel})
        assert.deepEqual(on_new_input_message_data          , null)
        assert.deepEqual(action_button.innerHTML            , 'send')
        assert.deepEqual(action_button.style.backgroundColor, 'rgb(0, 123, 255)')

        //with a value in action_button.input.value
        webc_chat_input.input.value = 'an message'
        on_stop_stream_data         = null
        on_new_input_message_data   = null
        action_button.dispatchEvent(event);
        assert.deepEqual(on_stop_stream_data, null)
        assert.deepEqual(on_new_input_message_data, { user_prompt: 'an message', images: [], channel: channel })
        assert.deepEqual(action_button.innerHTML            , 'stop')
        assert.deepEqual(action_button.style.backgroundColor, 'black')
        assert.deepEqual(webc_chat_input.input.value        , '')

        // then clicking on stop
        on_stop_stream_data         = null
        on_new_input_message_data   = null
        action_button.dispatchEvent(event);
        assert.deepEqual(on_stop_stream_data                , {channel: channel})
        assert.deepEqual(on_new_input_message_data          , null)
        assert.deepEqual(on_stop_stream_data                , {channel: channel})
        assert.deepEqual(on_new_input_message_data          , null)
        assert.deepEqual(action_button.innerHTML            , 'send')
        assert.deepEqual(action_button.style.backgroundColor, 'rgb(0, 123, 255)')


        window.removeEventListener('stop_stream'      , on_stop_stream      );
        window.removeEventListener('new_input_message', on_new_input_message);
    })
})

//todo: move to util class
function create_test_img_base64(width=50, height=30, color='#496D89') {
    var canvas    = document.createElement('canvas');       // Create a canvas element
    canvas.width  = width;
    canvas.height = height;
    var ctx       = canvas.getContext('2d');                // Get the context of the canvas
    ctx.fillStyle = color;                                  // Fill the canvas with the specified color
    ctx.fillRect(0, 0, width, height);
    return canvas.toDataURL();                              // Convert the canvas to a base64 encoded image
}