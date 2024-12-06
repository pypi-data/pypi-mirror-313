import HR  from '../../js/core/HR.mjs'
import Tag from '../../js/core/Tag.mjs'

const { module, test } = QUnit

module('HR', hooks => {
    test('constructor creates hr element', assert => {
        // Basic instantiation
        const hr = new HR({})
        assert.equal(hr.tag                     , 'hr'             , 'Sets correct tag name')
        assert.ok   (hr instanceof Tag                             , 'Inherits from Tag')

        // With attributes
        const styled = new HR({
            class : 'custom-hr'                 ,
            id    : 'hr-1'
        })
        assert.equal(styled.class               , 'custom-hr'      , 'Sets class')
        assert.equal(styled.id       , 'hr-1'           , 'Sets id')
    })

    test('generates correct HTML', assert => {
        const hr = new HR({ class: 'test-hr' })
        assert.equal(hr.html()                  , '<hr class="test-hr"/>\n', 'Generates correct HTML')
    })

    test('constructor handles no parameters', assert => {
        const hr = new HR()
        assert.equal(hr.html()                  , '<hr/>\n'        , 'Generates minimal HTML')
    })
})


