// Table.qunit.mjs
import Table from '../../js/core/Table.mjs'
import Tag   from '../../js/core/Tag.mjs'

const { module, test , only} = QUnit

module('Table', hooks => {
    test('constructor creates table with headers and rows', assert => {
        // Basic instantiation
        const table = new Table({})
        assert.equal(table.tag                  , 'table'          , 'Sets correct tag name')
        assert.ok   (table instanceof Tag                          , 'Inherits from Tag')
        assert.deepEqual(table.headers          , []               , 'Empty default headers')
        assert.deepEqual(table.rows             , []               , 'Empty default rows')

        // With headers and rows
        const complex = new Table({
            headers : ['Col 1', 'Col 2']        ,
            rows    : [['A1', 'A2'], ['B1', 'B2']],
            class   : 'custom-table'            ,
            id      : 'table-1'
        })
        assert.deepEqual(complex.headers        , ['Col 1', 'Col 2'], 'Sets headers')
        assert.deepEqual(complex.rows           , [['A1', 'A2'], ['B1', 'B2']], 'Sets rows')
        assert.equal(complex.class              , 'custom-table'   , 'Sets class')
        assert.equal(complex.id                 , 'table-1'        , 'Sets id')
    })

    test('builds thead correctly', assert => {
        const table = new Table({
            headers : ['Header 1', 'Header 2']  ,
            class   : 'test-table'
        })
        const thead = table.build_thead()
        assert.equal(thead.tag                  , 'thead'          , 'Creates thead element')
        assert.equal(thead.elements[0].tag      , 'tr'             , 'Creates tr element')
        assert.equal(thead.elements[0].elements.length, 2          , 'Creates correct number of cells')
        assert.equal(thead.elements[0].elements[0].value, 'Header 1', 'Sets header cell content')
    })

    test('builds tbody correctly', assert => {
        const table = new Table({
            rows: [['Cell 1', 'Cell 2'], ['Cell 3', 'Cell 4']]
        })
        const tbody = table.build_tbody()
        assert.equal(tbody.tag                  , 'tbody'          , 'Creates tbody element')
        assert.equal(tbody.elements.length      , 2                , 'Creates correct number of rows')
        assert.equal(tbody.elements[0].elements.length, 2          , 'Creates correct number of cells')
        assert.equal(tbody.elements[0].elements[0].value, 'Cell 1' , 'Sets cell content')
    })

    test('builds complete table structure', assert => {
        const table = new Table({
            headers : ['H1', 'H2']              ,
            rows    : [['A1', 'A2'], ['B1', 'B2']]
        })
        table.build()
        assert.equal(table.elements.length      , 2                , 'Creates both thead and tbody')
        assert.equal(table.elements[0].tag      , 'thead'          , 'First element is thead')
        assert.equal(table.elements[1].tag      , 'tbody'          , 'Second element is tbody')
    })

    test('generates correct HTML', assert => {
        const table = new Table({
            headers : ['H1']                    ,
            rows    : [['A1']]                  ,
            class   : 'test-table'
        })
        const expected = '<table class="test-table">\n' +
                        '    <thead>\n' +
                        '        <tr>\n' +
                        '            <td>H1</td>\n' +
                        '        </tr>\n' +
                        '    </thead>\n' +
                        '    <tbody>\n' +
                        '        <tr>\n' +
                        '            <td>A1</td>\n' +
                        '        </tr>\n' +
                        '    </tbody>\n' +
                        '</table>\n'
        assert.equal(table.html()               , expected         , 'Generates correct HTML')
    })

    test('table_css__simple returns correct styles', assert => {
        const table = new Table()
        const css = table.table_css__simple()

        assert.deepEqual(css['table *']         , { padding: '5px' }, 'Sets cell padding')
        assert.deepEqual(css['table']           , { border: '0px solid black', width: '100%' }, 'Sets table styles')
        assert.deepEqual(css['thead']           , { 'background-color': 'lightgrey', 'font-color': 'black' }, 'Sets header styles')
        assert.deepEqual(css['td']              , { border: '1px solid black' }, 'Sets cell border')
    })
})

