// Svg.qunit.mjs
import Svg from '../../js/core/Svg.mjs'
import Tag from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('Svg', hooks => {
    test('constructor creates svg element', assert => {
        // Basic instantiation
        const svg = new Svg({})
        assert.equal(svg.tag                    , 'svg'            , 'Sets correct tag name')
        assert.ok   (svg instanceof Tag                            , 'Inherits from Tag')

        // With dimensions
        const with_dims = new Svg({
            width  : '100'                      ,
            height : '200'                      ,
            src    : 'test.svg'
        })
        assert.equal(with_dims.attributes.width , '100'            , 'Sets width')
        assert.equal(with_dims.attributes.height, '200'            , 'Sets height')
        assert.equal(with_dims.attributes.src   , 'test.svg'       , 'Sets src')

        // With multiple attributes
        const complex = new Svg({
            width      : '100'                  ,
            height     : '200'                  ,
            src        : 'test.svg'             ,
            class      : 'custom-svg'           ,
            id         : 'svg-1'                ,
            viewBox    : '0 0 100 200'
        })
        assert.equal(complex.attributes.width   , '100'            , 'Sets width')
        assert.equal(complex.attributes.height  , '200'            , 'Sets height')
        assert.equal(complex.attributes.src     , 'test.svg'       , 'Sets src')
        assert.equal(complex.class              , 'custom-svg'     , 'Sets class')
        assert.equal(complex.id                 , 'svg-1'          , 'Sets id')
        assert.equal(complex.attributes.viewBox , '0 0 100 200'    , 'Sets viewBox')
    })

    test('generates correct HTML', assert => {
        const svg = new Svg({
            width  : '100'                      ,
            height : '200'                      ,
            class  : 'test-svg'                 ,
            src    : 'test.svg'
        })
        const expected = '<svg class="test-svg" src="test.svg" width="100" height="200">\n</svg>\n'
        assert.equal(svg.html()                 , expected         , 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const svg = new Svg()
        assert.equal(svg.html()                 , '<svg src="" width="" height="">\n</svg>\n', 'Generates minimal HTML')
    })
})