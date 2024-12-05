import Table from '../../js/core/Table.mjs';

QUnit.module('Table', function(hooks) {

    QUnit.test('constructor', (assert) => {
        let table = new Table({id:'an_table', class:'an_class'})
        let table_html = '<table id="an_table" class="an_class">\n    <thead>\n        <tr>\n        </tr>\n    </thead>\n    <tbody>\n    </tbody>\n</table>\n'
        assert.equal(table.html(), table_html)

    })

    QUnit.test('build_thead', (assert) => {
        let table = new Table()
        table.headers = ['header1','header2']
        let thead = table.build_thead()
        let thead_html = '<thead>\n' +
                         '    <tr>\n' +
                         '        <td>header1</td>\n' +
                         '        <td>header2</td>\n' +
                         '    </tr>\n' +
                         '</thead>\n'
        assert.equal(thead.html(), thead_html)
    })

    QUnit.test('build_tbody', (assert) => {
        let table = new Table()
        table.rows = [['cell1','cell2'],['cell3','cell4']]
        let tbody = table.build_tbody()
        let tbody_html = '<tbody>\n' +
                         '    <tr>\n' +
                         '        <td>cell1</td>\n' +
                         '        <td>cell2</td>\n' +
                         '    </tr>\n' +
                         '    <tr>\n' +
                         '        <td>cell3</td>\n' +
                         '        <td>cell4</td>\n' +
                         '    </tr>\n' +
                         '</tbody>\n'
        assert.equal(tbody.html(), tbody_html)
    })

})