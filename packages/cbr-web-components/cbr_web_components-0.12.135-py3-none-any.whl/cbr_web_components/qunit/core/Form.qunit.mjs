import Form from '../../js/core/Form.mjs'
import Tag  from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('Form', hooks => {
    test('constructor creates form element', assert => {
        // Basic instantiation
        const form = new Form({})
        assert.equal(form.tag                   , 'form'            , 'Sets correct tag name')
        assert.ok   (form instanceof Tag                            , 'Inherits from Tag')

        // With method and action
        const with_attrs = new Form({
            method : 'POST'                     ,
            action : '/submit'
        })
        assert.equal(with_attrs.attributes.method, 'POST'           , 'Sets method')
        assert.equal(with_attrs.attributes.action, '/submit'        , 'Sets action')

        // With multiple attributes
        const complex = new Form({
            method   : 'GET'                    ,
            action   : '/search'                ,
            class    : 'search-form'            ,
            id       : 'form-1'                 ,
            onsubmit : 'return false;'
        })
        assert.equal(complex.attributes.method  , 'GET'             , 'Sets method'  )
        assert.equal(complex.attributes.action  , '/search'         , 'Sets action'  )
        assert.equal(complex.class              , 'search-form'     , 'Sets class'   )
        assert.equal(complex.id                 , 'form-1'          , 'Sets id'      )
        assert.equal(complex.attributes.onsubmit, 'return false;'   , 'Sets onsubmit')
    })

    test('generates correct HTML', assert => {
        const form = new Form({
            method : 'POST'                     ,
            action : '/submit'                  ,
            class  : 'test-form'
        })
        const expected = '<form class="test-form" method="POST" action="/submit">\n</form>\n'
        assert.equal(form.html()                , expected          , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const form = new Form()

        assert.equal(form.tag                   , 'form'           , 'Sets correct tag name')
        assert.ok   (form instanceof Tag                           , 'Inherits from Tag')
        assert.deepEqual(form.attributes        , {}               , 'Has empty attributes')
        assert.equal(form.html()                , '<form>\n</form>\n', 'Generates minimal HTML')
    })
})