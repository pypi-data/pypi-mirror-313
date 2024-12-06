import H   from '../../js/core/H.mjs';
import Tag from '../../js/core/Tag.mjs';

const { module, test } = QUnit

module('H', function(hooks) {

    test('.constructor',  function (assert) {
        assert.equal(new H().tag, 'h1')
        assert.equal(new H({level:1}).tag, 'h1')
        assert.equal(new H({level:2}).tag, 'h2')
        assert.equal(new H({level:3}).tag, 'h3')

        assert.equal(new H({level:'A'}).tag, 'hA')          // todo: this is a bug, only h1 .. h6 values should be accepted
    })


    test('.add_element', function (assert) {
        assert.equal(new H().add_element('abc'), false)
    })

    test('.inner_html', function (assert) {
        let h = new H()
        assert.deepEqual(h.inner_html(),'')

        h.value = 'abc'
        assert.deepEqual(h.inner_html(),'abc')
    })

    test('.html', function (assert) {
        const h1 = new H();
        assert.equal(h1.html(), `<h1></h1>\n`)

        const h2 = new H({level:2, value:'abc'});
        assert.equal(h2.html(), `<h2>abc</h2>\n`)
    })

    test('_should be an instance and inherit from Html_Tag', function(assert) {
        const h = new H();
        assert.ok(h instanceof Tag, 'Div is an instance of Html_Tag');
        assert.ok(H.prototype instanceof Tag, 'Div.prototype is an instance of Html_Tag');
        assert.equal(h.tag, 'h1');
    });

     test('constructor creates heading element', assert => {
        // Basic instantiation with defaults
        const h1 = new H({})
        assert.equal(h1.tag                     , 'h1'             , 'Sets default h1 tag')
        assert.ok   (h1 instanceof Tag                             , 'Inherits from Tag')
        assert.equal(h1.value                   , ''               , 'Empty default value')

        // With specific level
        const h3 = new H({ level: 3 })
        assert.equal(h3.tag                     , 'h3'             , 'Sets correct heading level')

        // With text content
        const h2_text = new H({
            level : 2                           ,
            value : 'Heading Text'
        })
        assert.equal(h2_text.tag                , 'h2'             , 'Sets h2 tag')
        assert.equal(h2_text.value              , 'Heading Text'   , 'Sets heading text')

        // With multiple attributes
        const complex = new H({
            level : 4                           ,
            value : 'Complex Heading'           ,
            class : 'custom-heading'            ,
            id    : 'head-1'
        })
        assert.equal(complex.tag                , 'h4'             , 'Sets h4 tag')
        assert.equal(complex.value              , 'Complex Heading', 'Sets text')
        assert.equal(complex.class              , 'custom-heading' , 'Sets class')
        assert.equal(complex.id                 , 'head-1'         , 'Sets id')
    })

    test('generates correct HTML', assert => {
        const h1 = new H({
            value : 'Test Heading'              ,
            class : 'test-heading'
        })
        assert.equal(h1.html()                  , '<h1 class="test-heading">Test Heading</h1>\n', 'Generates correct HTML')
    })

    test('prevents adding child elements', assert => {
        const h1 = new H({ value: 'Test' })
        const div = new Tag({ tag: 'div' })

        assert.notOk(h1.add_element(div)                          , 'Returns false when adding element')
        assert.equal(h1.html()                  , '<h1>Test</h1>\n', 'HTML remains unchanged')
    })

    test('config sets correct HTML options', assert => {
        const h1 = new H({})
        assert.notOk(h1.html_config.new_line_before_elements      , 'Disables new lines before elements')
        assert.notOk(h1.html_config.indent_before_last_tag        , 'Disables indent before last tag')
    })

    test('inner_html returns value', assert => {
        const h1 = new H({ value: 'Test Value' })
        assert.equal(h1.inner_html()            , 'Test Value'     , 'Returns correct value')
    })
})
