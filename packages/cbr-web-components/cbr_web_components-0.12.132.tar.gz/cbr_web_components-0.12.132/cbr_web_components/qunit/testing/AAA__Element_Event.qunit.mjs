import AAA__Element_Event from '../../js/testing/AAA__Element_Event.mjs'

const { module, test , only} = QUnit

module('AAA__Element_Event', hooks => {

    test('constructor creates instance with defaults', assert => {
        const instance = new AAA__Element_Event({})                                // Empty config

        assert.ok      (instance.element instanceof HTMLDivElement, 'element is a div'      )
        assert.equal   (instance.event_name, 'test_event'         , 'event_name is default' )
    })

    test('constructor uses provided values', assert => {
        const element = document.createElement('button')
        const instance = new AAA__Element_Event({ element    : element     ,
                                                 event_name : 'my_event'  })

        assert.strictEqual(instance.element   , element     , 'uses provided element'    )
        assert.strictEqual(instance.event_name, 'my_event'  , 'uses provided event name' )
    })

    test('raise_event passes custom detail', async assert => {
        assert.expect(1)
        const expected_detail = { test: 'data' }

        const instance = new AAA__Element_Event({})
        instance.assert = (event) => {
            assert.deepEqual(event.detail, expected_detail, 'detail passed correctly')
        }

        instance.add_event_listener()
        instance.raise_event(expected_detail)
        instance.remove_event_listener()
    })

    test('aaa method executes in correct order', async assert => {
        assert.expect(3)
        const execution_order = []

        const instance = new AAA__Element_Event({})
        instance.arrange = async () => execution_order.push('arrange')
        instance.act     = async () => execution_order.push('act'   )
        instance.assert  = async () => execution_order.push('assert' )

        await instance.aaa()

        assert.strictEqual(execution_order[0], 'arrange', 'arrange executes first' )
        assert.strictEqual(execution_order[1], 'act'    , 'act executes second'   )
        assert.strictEqual(execution_order[2], 'assert' , 'assert executes third' )
    })

    test('assert is called when event raised', async assert => {
        assert.expect(1)
        let assert_called = false

        const instance = new AAA__Element_Event({})
        instance.assert = () => assert_called = true

        instance.add_event_listener()
        instance.raise_event()
        instance.remove_event_listener()

        assert.ok(assert_called, 'assert was called when event raised')
    })

    test('default act method raises event', async assert => {
        assert.expect(1)
        let event_raised = false

        const instance = new AAA__Element_Event({})
        instance.assert = () => event_raised = true

        await instance.aaa()                                                      // Uses default act()

        assert.ok(event_raised, 'event was raised by default act')
    })

    test('event listener cleanup after error', async assert => {
        assert.expect(2)
        let called_after_error = false

        const instance = new AAA__Element_Event({})
        instance.act = () => { throw new Error('Test error') }
        instance.assert = () => called_after_error = true

        try {
            await instance.aaa()
            assert.notOk(true, 'should have thrown')
        } catch (error) {
            assert.ok(error instanceof Error, 'error was thrown')

            instance.raise_event()                                                // Try to trigger event after cleanup
            assert.notOk(called_after_error, 'assert not called after cleanup')
        }
    })

    test('static test method handles method overrides', async assert => {
        assert.expect(3)
        const execution_order = []

        await AAA__Element_Event.test({
            arrange: async function() { execution_order.push('arrange') },
            act:    async function() { execution_order.push('act')    },
            assert: function()       { execution_order.push('assert') }
        })

        assert.strictEqual(execution_order[0], 'arrange', 'arrange executed' )
        assert.strictEqual(execution_order[1], 'act'    , 'act executed'    )
        assert.strictEqual(execution_order[2], 'assert' , 'assert executed' )
    })

    test('methods have correct this binding', async assert => {
        assert.expect(3)
        let arrange_this, act_this, assert_this

        await AAA__Element_Event.test({
            arrange: async function() { arrange_this = this },
            act:    async function() { act_this = this     },
            assert: function()       { assert_this = this  }
        })

        assert.ok(arrange_this instanceof AAA__Element_Event, 'arrange has correct this')
        assert.ok(act_this     instanceof AAA__Element_Event, 'act has correct this'    )
        assert.ok(assert_this  instanceof AAA__Element_Event, 'assert has correct this' )
    })

    test('button click test example', async assert => {
        assert.expect(2)

        const button = document.createElement('button')
        button.textContent = 'Click me'

        await AAA__Element_Event.test({
            element    : button           ,
            event_name: 'click'          ,
            arrange   : async function() {
                document.body.appendChild(this.element)
                assert.ok(document.body.contains(button), 'button was added to DOM')
            },
            assert: function() {
                assert.ok(true, 'click event was triggered')
                document.body.removeChild(this.element)                          // Cleanup
            }
        })
    })

    test('button click test example (with raise_after_act = false)', async assert => {
        assert.expect(2)

        const button = document.createElement('button')
        button.textContent = 'Click me'

        await AAA__Element_Event.test({
            element    : button           ,
            event_name: 'click'          ,
            raise_after_act: false,
            arrange   : async function() {
                document.body.appendChild(this.element)
                assert.ok(document.body.contains(button), 'button was added to DOM')
            },
            act: async function() {
                this.element.click()                                             // Simulate button click
            },
            assert: function() {
                assert.ok(true, 'click event was triggered')
                document.body.removeChild(this.element)                          // Cleanup
            }
        })
    })

    test('input value change test example', async assert => {
        assert.expect(3)

        const input = document.createElement('input')
        const expected_value = 'test value'
        let current_value = null

        await AAA__Element_Event.test({
            element    : input            ,
            event_name: 'input'          ,
            arrange   : async function() {
                document.body.appendChild(this.element)
                assert.equal(this.element.value, '', 'input starts empty')
            },
            act: async function() {
                this.element.value = expected_value
            },
            assert: function(event) {
                current_value = event.target.value
                assert.equal(current_value, expected_value, 'input value was updated')
                assert.equal(this.element.value, expected_value, 'DOM element shows updated value')
                document.body.removeChild(this.element)                          // Cleanup
            }
        })
    })

    test('form submission test example', async assert => {
        //assert.expect(4)

        const form   = document.createElement('form')
        const input  = document.createElement('input')
        const submit = document.createElement('button')

        input.name    = 'test-field'
        input.value   = 'test-value'
        submit.type   = 'submit'

        form.appendChild(input)
        form.appendChild(submit)

        await AAA__Element_Event.test({
            element    : form            ,
            event_name: 'submit'         ,
            raise_after_act: false       ,
            arrange   : async function() {
                document.body.appendChild(this.element)
                assert.ok(document.body.contains(form), 'form added to DOM')
                assert.equal(input.value, 'test-value', 'input has initial value')
            },
            act: async function() {
                submit.click()                                                   // Trigger form submission
            },
            assert: function(event) {
                event.preventDefault()                                           // Prevent actual form submission
                const form_data = new FormData(event.target)

                assert.equal(form_data.get('test-field'), 'test-value', 'form data contains input value')
                assert.ok(event instanceof SubmitEvent, 'received submit event')

                document.body.removeChild(this.element)                         // Cleanup
            }
        })
    })

    test('custom component event bubbling example', async assert => {
        //assert.expect(3)

        const parent = document.createElement('div')
        const child  = document.createElement('div')
        let bubble_received = false

        parent.appendChild(child)

        // Test the child element events
        await AAA__Element_Event.test({
            element     : child           ,
            event_name: 'custom-event'   ,
            raise_after_act: false       ,
            arrange   : async function() {
                document.body.appendChild(parent)
                assert.ok(document.body.contains(child), 'child element in DOM')

                // Setup bubbling listener on parent
                parent.addEventListener('custom-event', () => {
                    bubble_received = true
                })
            },
            act: async function() {
                this.element.dispatchEvent(new CustomEvent('custom-event', {
                    bubbles  : true          ,
                    detail   : { foo: 'bar' }
                }))
            },
            assert: function(event) {
                assert.deepEqual(event.detail, { foo: 'bar' }, 'event detail preserved')
                assert.notOk(bubble_received                 , 'since we are in the child , the event should have not bubbled to parent')
                document.body.removeChild(parent)                               // Cleanup
            }
        })
        assert.ok(bubble_received, 'after the assert is completed, the should see the event bubbled up to the parent')
    })
})