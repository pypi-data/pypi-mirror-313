// Raw_Html.qunit.mjs
import Raw_Html from '../../js/core/Raw_Html.mjs'
import Tag      from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('Raw_Html', hooks => {
    test('constructor creates raw HTML element', assert => {
        // Basic instantiation
        const raw = new Raw_Html({})
        assert.equal(raw.tag                    , 'div'            , 'Sets div tag as container')
        assert.ok   (raw instanceof Tag                            , 'Inherits from Tag')
        assert.equal(raw.raw_html               , ''               , 'Empty default raw HTML')

        // With HTML content
        const html_content = '<span>Test</span>'
        const with_html = new Raw_Html({ value: html_content })
        assert.equal(with_html.raw_html         , html_content     , 'Sets raw HTML content')

        // With multiple attributes
        const complex = new Raw_Html({
            value : '<p>Complex</p>'            ,
            class : 'custom-raw'                ,
            id    : 'raw-1'
        })
        assert.equal(complex.raw_html           , '<p>Complex</p>' , 'Sets HTML')
        assert.equal(complex.class              , 'custom-raw'     , 'Sets class')
        assert.equal(complex.id                 , 'raw-1'          , 'Sets id')
    })

    test('prevents adding child elements', assert => {
        const raw  = new Raw_Html({ value: '<p>Test</p>' })
        const div  = new Tag({ tag: 'div' })

        assert.notOk(raw.add_element(div)                         , 'Returns false when adding element')
    })

    test('inner_html handles various inputs', assert => {
        // Empty content
        const empty = new Raw_Html({})
        assert.equal(empty.inner_html(0)        , ''               , 'Handles empty content')

        // Single line content
        const single = new Raw_Html({ value: '<p>Test</p>' })
        assert.equal(single.inner_html(0)       , '    <p>Test</p>\n', 'Indents single line')

        // Multi-line content
        const multi = new Raw_Html({ value: '<p>\nTest\n</p>' })
        const expected_multi = '    <p>\n    Test\n    </p>\n'
        assert.equal(multi.inner_html(0)        , expected_multi   , 'Indents multiple lines')

        // Non-string content
        const non_string = new Raw_Html({ value: null })
        assert.equal(non_string.inner_html(0)   , ''               , 'Handles non-string content')
    })

    test('generates correct HTML', assert => {
        const raw = new Raw_Html({
            value : '<span>Test</span>'         ,
            class : 'test-raw'
        })
        const expected = '<div class="test-raw">\n    <span>Test</span>\n</div>\n'
        assert.equal(raw.html()                 , expected         , 'Generates correct HTML')
    })
})