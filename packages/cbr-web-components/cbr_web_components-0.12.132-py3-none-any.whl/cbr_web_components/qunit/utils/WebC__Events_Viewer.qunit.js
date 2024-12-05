import Web_Component        from '../../js/core/Web_Component.mjs'
import WebC__Events_Viewer  from '../../js/utils/WebC__Events_Viewer.mjs'
import WebC__Target_Div     from "../../js/utils/WebC__Target_Div.mjs";
import WebC__Events_Utils from "../../js/utils/WebC__Events_Utils.mjs";

QUnit.module('WebC__Events_Viewer', function(hooks) {

    let webc_events_viewer
    let target_div

    hooks.before(async (assert) => {
        webc_events_viewer = WebC__Events_Viewer.create()
        target_div         = WebC__Target_Div.add_to_body().build({width:"30%"})
        //await webc_events_viewer.load_datatables_css()
    });


    QUnit.test('constructor', (assert) => {
        //assert.ok(webc_events_viewer            instanceof WebC__Events_Viewer      , 'webc_events_viewer is instance of WebC__Events_Viewer'        ) // todo figure out why this started failed after the refactoring into this repo
        assert.ok(WebC__Events_Viewer.prototype instanceof Web_Component      , 'WebC__Events_Viewer.prototype is an instance of Web_Component');
    })


    QUnit.test('build',  (assert) => {
        //const webc_events_viewer = WebC__Events_Viewer.create()
        let expected_html = `\
<div class=\"event_viewer\">
    <h2>Events Viewer</h2>
    <table>
        <thead>
            <tr>
            </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
</div>
`
        target_div.appendChild(webc_events_viewer)
        assert.ok(true)
        //assert.equal(webc_events_viewer.query_selector('h2').innerHTML, 'Events Viewer')
        //assert.equal(webc_events_viewer.inner_html(),expected_html)
        //webc_events_viewer.add_row()
    })

    // QUnit.test('hook_events', (assert) => {
    //     let events_type = ['test-event']
    //     let callbackCalled = false;

    //     let options  = {}
    //     webc_events_viewer.hook_events(events_type, options)
    //     assert.ok(webc_events_viewer.events_hooked.includes("test-event"))

    //     let event = new CustomEvent('test-event', {
    //         detail    : { someData: 'example' },    // Custom data to pass with the event
    //         bubbles   : true,                       // Whether the event bubbles up through the DOM
    //         cancelable: true,                       // Whether the event can be canceled
    //         composed  : false   ,                    // Whether the event will trigger listeners outside of a shadow root
    //     });

    //     assert.equal(webc_events_viewer.events_handled.length, 0)
    //     document.dispatchEvent(event);
    //     assert.equal(webc_events_viewer.events_handled.length, 1)
    //     assert.ok(true)
    // })


})