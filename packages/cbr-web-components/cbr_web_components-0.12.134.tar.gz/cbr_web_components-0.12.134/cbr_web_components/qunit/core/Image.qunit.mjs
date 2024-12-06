import Image from '../../js/core/Image.mjs'
import Tag   from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('Image', hooks => {
    test('constructor creates image element', assert => {
        // Basic instantiation
        const image = new Image({})
        assert.equal(image.tag                  , 'image'          , 'Sets correct tag name')
        assert.ok   (image instanceof Tag                          , 'Inherits from Tag')

        // With attributes
        const complex = new Image({
            class : 'custom-image'              ,
            id    : 'img-1'                     ,
            src   : 'test.jpg'
        })
        assert.equal(complex.class              , 'custom-image'   , 'Sets class')
        assert.equal(complex.id                 , 'img-1'          , 'Sets id')
        assert.equal(complex.attributes.src     , 'test.jpg'       , 'Sets src')
    })

    test('generates correct HTML', assert => {
        const image = new Image({
            class : 'test-image'                ,
            src   : 'test.jpg'
        })
        assert.equal(image.html()               , '<image class="test-image" src="test.jpg">\n</image>\n', 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const image = new Image()
        assert.equal(image.html()               , '<image>\n</image>\n', 'Generates minimal HTML')
    })
})