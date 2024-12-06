// Img.qunit.mjs
import Img from '../../js/core/Img.mjs'
import Tag from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('Img', hooks => {
    test('constructor creates img element', assert => {
        // Basic instantiation
        const img = new Img({})
        assert.equal(img.tag                    , 'img'            , 'Sets correct tag name')
        assert.ok   (img instanceof Tag                            , 'Inherits from Tag')

        // With src attribute
        const with_src = new Img({ src: 'test.jpg' })
        assert.equal(with_src.attributes.src    , 'test.jpg'       , 'Sets src attribute')

        // With dimensions
        const with_dims = new Img({
            src    : 'test.jpg'                 ,
            width  : '100'                      ,
            height : '200'
        })
        assert.equal(with_dims.attributes.width , '100'            , 'Sets width')
        assert.equal(with_dims.attributes.height, '200'            , 'Sets height')

        // With all attributes
        const complex = new Img({
            src    : 'test.jpg'                 ,
            width  : '100'                      ,
            height : '200'                      ,
            class  : 'custom-img'               ,
            id     : 'img-1'                    ,
            alt    : 'Test image'
        })
        assert.equal(complex.attributes.src     , 'test.jpg'       , 'Sets src')
        assert.equal(complex.attributes.width   , '100'            , 'Sets width')
        assert.equal(complex.attributes.height  , '200'            , 'Sets height')
        assert.equal(complex.class              , 'custom-img'     , 'Sets class')
        assert.equal(complex.id                 , 'img-1'          , 'Sets id')
        assert.equal(complex.attributes.alt     , 'Test image'     , 'Sets alt')
    })

    test('generates correct HTML', assert => {
        const img = new Img({
            src    : 'test.jpg'                 ,
            width  : '100'                      ,
            height : '200'                      ,
            class  : 'test-img'
        })
        const expected = '<img class="test-img" src="test.jpg" width="100" height="200"/>\n'
        assert.equal(img.html()                 , expected         , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const img = new Img()
        assert.equal(img.html()                 , '<img src="" width="" height=""/>\n', 'Generates minimal HTML')
    })
})