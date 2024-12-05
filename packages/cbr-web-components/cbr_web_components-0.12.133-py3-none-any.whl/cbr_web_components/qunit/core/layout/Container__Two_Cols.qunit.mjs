import Div                 from '../../../js/core/Div.mjs'
import Container__Two_Cols from "../../../js/core/layout/Container__Two_Cols.mjs";

const { module, test, only } = QUnit

module('Table', function(hooks) {

    let container

    hooks.before(() => {
        container = new Container__Two_Cols({ id: 'test_container', class: 'test_class' })
    })

    test('constructor and inheritance', assert => {
        assert.ok   (container instanceof Div                     , 'Inherits from Div')
        assert.equal(container.id                , 'test_container', 'Sets ID correctly')
        assert.equal(container.class            , 'test_class'    , 'Sets class correctly')
    })

    test('setup creates correct structure', assert => {
        assert.ok   (container.div_root                           , 'Creates root container')
        assert.ok   (container.row_1                              , 'Creates row')
        assert.ok   (container.col_1                              , 'Creates first column')
        assert.ok   (container.col_2                              , 'Creates second column')

        assert.equal(container.div_root.class   , 'container'     , 'Root has container class')
        assert.equal(container.row_1.class      , 'row'           , 'Row has row class')
        assert.equal(container.col_1.class      , 'col'           , 'Col 1 has col class')
        assert.equal(container.col_2.class      , 'col'           , 'Col 2 has col class')
    })

    test('handles no parameters', assert => {
        const empty_container = new Container__Two_Cols()
        assert.ok   (empty_container                              , 'Creates instance')
        assert.ok   (empty_container.div_root                     , 'Creates structure')
        assert.equal(empty_container.html()     , expected_html__constructor, 'Generates correct HTML')
    })

    test('css_rules defines all required styles', assert => {
        const rules = container.css_rules()

        // Container rules
        assert.ok   (rules['.container']                         , 'Has container rules')
        assert.equal(rules['.container'].display , 'flex'        , 'Container uses flex')
        assert.equal(rules['.container'].width  , '100%'        , 'Container full width')

        // Row rules
        assert.ok   (rules['.row']                              , 'Has row rules')
        assert.equal(rules['.row'].display      , 'flex'        , 'Row uses flex')
        assert.equal(rules['.row'].flex         , '1'           , 'Row takes equal space')

        // Column rules
        assert.ok   (rules['.col']                              , 'Has column rules')
        assert.ok   (rules['.col:nth-child(1)']                 , 'Has first column rules')
        assert.ok   (rules['.col:nth-child(2)']                 , 'Has second column rules')

        // Content rules
        assert.ok   (rules['#file_contents']                    , 'Has file contents rules')
        assert.equal(rules['#file_contents']['white-space'], 'pre-wrap', 'Preserves whitespace')
    })

    test('content can be added to columns', assert => {
        const test_content_1 = new Div({ value: 'Column 1 Content' })
        const test_content_2 = new Div({ value: 'Column 2 Content' })

        container.col_1.add_element(test_content_1)
        container.col_2.add_element(test_content_2)

        const html = container.html()
        assert.ok   (html.includes('Column 1 Content')          , 'First column content added')
        assert.ok   (html.includes('Column 2 Content')          , 'Second column content added')
    })

    test('columns handle long content', assert => {
        const long_text = 'a'.repeat(100)
        const test_content = new Div({ value: long_text })

        container.col_1.add_element(test_content)
        const html = container.html()

        assert.ok   (html.includes(long_text)                   , 'Long content preserved')
        assert.equal(container.col_1.class     , 'col'          , 'Column styling intact')
    })

    test('constructor', (assert) => {
        let container_two_cols = new Container__Two_Cols({id: 'an_container', class: 'an_class'})
        let container_html = container_two_cols.html()
        assert.equal(container_html, expected_html__constructor)
    })

    let expected_html__constructor = `\
<div class="container">
    <div class="row">
        <div class="col">
        </div>
        <div class="col">
        </div>
    </div>
</div>
`
})