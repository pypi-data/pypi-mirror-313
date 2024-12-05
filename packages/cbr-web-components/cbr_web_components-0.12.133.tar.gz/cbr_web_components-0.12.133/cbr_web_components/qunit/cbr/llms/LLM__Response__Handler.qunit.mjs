import LLM__Response__Handler from '../../../js/cbr/llms/LLM__Response__Handler.mjs'

const { module, test, only, skip } = QUnit

module('LLM__Response__Handler', hooks => {
    let handler
    let original_marked

    hooks.before((assert) => {
        assert.timeout(10)
        original_marked = window.marked
        handler = new LLM__Response__Handler()
    })

    hooks.after(() => {
        window.marked = original_marked
    })

    test('constructor sets default config', assert => {
        assert.equal(handler.markdown_enabled          , true                    , 'Markdown enabled by default'       )

        const custom_handler = new LLM__Response__Handler({ markdown_enabled: false })
        assert.equal(custom_handler.markdown_enabled   , false                   , 'Custom markdown setting applied'   )
    })

    test('format_response handles markdown when enabled', assert => {
        const test_markdown = '**bold** text'
        window.marked = { marked: (text) => `<p><strong>bold</strong> text</p>` }

        const result = handler.format_response(test_markdown)
        assert.equal(result                            , '<p><strong>bold</strong> text</p>', 'Markdown properly formatted')
    })
    test('format_response returns raw text when marked undefined', assert => {
        const test_text = '**bold** text'
        window.marked = undefined

        const result = handler.format_response(test_text)
        assert.equal(result                            , '**bold** text'         , 'Returns raw text when marked undefined')
    })

    test('format_response returns raw text when markdown disabled', assert => {
        const custom_handler = new LLM__Response__Handler({ markdown_enabled: false })
        const test_markdown = '**bold** text'
        window.marked = { marked: (text) => `<p><strong>bold</strong> text</p>` }

        const result = custom_handler.format_response(test_markdown)
        assert.notOk(custom_handler.markdown_enabled)
        assert.equal(result                            , '**bold** text'         , 'Returns raw text when markdown disabled')
        window.marked = null
    })

    test('create_response_element generates correct HTML', assert => {
        const test_response = 'Test response'
        const result = handler.create_response_element(test_response, 'custom-class')

        assert.ok(result.includes('class="llm-response custom-class"')           , 'Includes correct classes'         )
        assert.ok(result.includes('Test response')                               , 'Includes response content'        )
        assert.ok(result.startsWith('<div')                                      , 'Starts with div tag'             )
        assert.ok(result.endsWith('</div>')                                      , 'Ends with closing div tag'       )
    })

    test('create_response_element works with empty class', assert => {
        const test_response = 'Test response'
        const result = handler.create_response_element(test_response)

        assert.ok(result.includes('class="llm-response "')                        , 'Includes base class only'        )
        assert.ok(result.includes('Test response')                               , 'Includes response content'       )
    })

    test('handles empty response', assert => {
        const result = handler.create_response_element('')
        assert.equal(result                            , '<div class="llm-response "></div>', 'Creates empty element')
    })

    test('handles null response', assert => {
        const result = handler.create_response_element(null)
        assert.equal(result , '<div class="llm-response "></div>', 'Creates empty element')
    })

    test('handles complex markdown content', assert => {
        const complex_markdown = '# Title\n- List item\n```code```'
        window.marked = { marked: (text) => '<h1>Title</h1><ul><li>List item</li></ul><pre><code>code</code></pre>' }

        const result = handler.format_response(complex_markdown)
        assert.ok(result.includes('<h1>')                                        , 'Formats headings'                )
        assert.ok(result.includes('<ul>')                                        , 'Formats lists'                   )
        assert.ok(result.includes('<code>')                                      , 'Formats code blocks'             )
        window.marked = null
    })
})