import Tag  from  './Tag.mjs'

export default class Table extends Tag {
    constructor({ headers = [], rows = [], ...kwargs } = {})  {
        super({tag:'table',...kwargs})
        this.headers = headers
        this.rows    = rows
    }

    build_thead() {
        let thead    = new Tag({'tag':'thead'})
        let thead_tr = new Tag({'tag':'tr'})
        thead.add_element(thead_tr)
        this.headers.forEach((header)=>{
            let td = new Tag({tag:'td', value:header})
            thead_tr.add_element(td)
        })
        return thead
    }
    
    build_tbody() {
        let tbody    = new Tag({'tag':'tbody'})        
        
        this.rows.forEach((row)=>{
            let tr = new Tag({'tag':'tr'})
            row.forEach((cell)=>{
                let td = new Tag({tag:'td', value:cell})
                tr.add_element(td)
            })
            tbody.add_element(tr)
        })
        return tbody
    }

    build() {
        let thead = this.build_thead()
        let tbody = this.build_tbody()
        this.add_element(thead)
        this.add_element(tbody)

    }
    connectedCallback() {
        this.build()        
    }

    html(depth) {
        this.build()        
        return super.html(depth)
    }


    table_css__simple() {
        return { 'table *' : { 'padding'         : '5px'            },
                 'table'   : { 'border'          : '0px solid black',
                               'width'           : '100%'           },
                 'thead'   : { 'background-color': 'lightgrey'      ,
                               'font-color'      : 'black'          },
                 'td'      : { 'border'          : '1px solid black'}}
    }
    
}