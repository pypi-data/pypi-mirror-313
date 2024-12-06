import Tag  from '../../js/core/Tag.mjs' ;

const { module, test, only } = QUnit

QUnit.module('Html_Tag', function(hooks) {


    QUnit.test('. parent', function (assert) {
        const tag_parent = new Tag({id:'tag_parent'})
        const tag_child  = new Tag({id:'tag_child' })
        tag_parent.add(tag_child)
        assert.equal(tag_child.parent(), tag_parent)
    });

    QUnit.test('.clone', function (assert) {
        const tag = new Tag({class:'an_class', id:'clone'})
        const tag_cloned_1 = tag.clone()
        assert.equal(tag.class , tag_cloned_1.class )

        assert.notEqual(tag.id    , tag_cloned_1.id, "cloned id is differentfrom original tag" )
        assert.notEqual(tag.html(), tag_cloned_1.html())

        const tag_cloned_2 = tag.clone({id:'changed'})
        assert.notEqual(tag.id, tag_cloned_2.id    )
        assert.equal   (tag.class, tag_cloned_2.class )
        assert.equal   (tag.element_parent         , tag_cloned_2.element_parent           )
        assert.equal   (tag.styles.top             , tag_cloned_2.styles.top               )
        assert.notEqual(tag.elements               , tag_cloned_2.elements                 )

        const tag_cloned_3 = tag.clone({id:'changed'})
        tag_cloned_3.element_parent = 'aaaa'
        tag_cloned_3.styles.top     = '20'
        tag_cloned_3.html_config.include_tag = false
        assert.notEqual(tag.element_parent         , tag_cloned_3.element_parent)
        assert.equal   (tag.styles.top             , null                       )
        assert.equal   (tag.html_config.include_tag, true                       )
        assert.equal   (tag.html_config.include_tag, true                       )
        assert.notEqual(tag.elements               , tag_cloned_3.elements      )

    })

    QUnit.test('.constructor', function (assert) {
        const tag           = new Tag({id:'constuctor_with_random_id'})
        const random_id     = tag.id
        const expected_html = `<tag id="${random_id}">\n</tag>\n`

        assert.equal(tag.tag, 'tag')
        assert.ok(tag instanceof Tag)
        assert.equal(tag.tag, 'tag')
        assert.propEqual(tag.styles, { background_color: null,
                                       border          : null,
                                       bottom          : null,
                                       left            : null,
                                       margin          : null,
                                       overflow        : null,
                                       padding         : null,
                                       position        : null,
                                       right           : null,
                                       top             : null,
                                       width           : null,
                                       z_index         : null})
        assert.propEqual(tag.html_config, { include_end_tag         : true,
                                            include_tag             : true ,
                                            include_id              : true ,
                                            indent_before_last_tag  : true ,
                                            new_line_before_elements: true ,
                                            new_line_after_final_tag: true ,
                                            trim_final_html_code    : false})
        assert.equal(tag.html(),expected_html)
    });

    QUnit.test('.add', function (assert) {
        const tag_id         = 'parent'
        const tag_child_1_id = 'child_1'
        const tag_child_2_id = 'child_1'
        const tag_child_3_id = 'child_1'
        const tag            = new Tag({id: tag_id         })
        const tag_child_1    = new Tag({id: tag_child_1_id })
        const tag_child_2    = new Tag({id: tag_child_2_id })
        const tag_child_3    = new Tag({id: tag_child_3_id })

        assert.deepEqual(tag.elements,[])
        tag.add(tag_child_1)

        assert.deepEqual(tag.elements,[tag_child_1])
        tag.add([tag_child_2, tag_child_3])

        assert.deepEqual(tag.elements,[tag_child_1,tag_child_2, tag_child_3])
    })


    QUnit.test('.add_element', function (assert) {
        const tag_id         = 'parent'
        const tag_child_1_id = 'child_1'
        const tag            = new Tag({id: tag_id         })                                    // parent div
        const tag_child_1    = new Tag({id: tag_child_1_id })                                    // add a div to the parent div
        const expected_inner_html_1 =
`    <tag id="child_1">
    </tag>
`
        const expected_html_1 =
`<tag id="parent">
    <tag id="child_1">
    </tag>
</tag>
`
        assert.equal(tag.tag        , 'tag'         )
        assert.equal(tag_child_1.tag, 'tag'         )
        assert.equal(tag.id              , tag_id        )
        assert.equal(tag_child_1.id      , tag_child_1_id)

        tag.add_element(tag_child_1)
        assert.equal(tag.elements.length,1)
        assert.equal(tag.elements[0], tag_child_1)
        assert.equal(tag.parent()        , null)
        assert.equal(tag_child_1.parent(), tag )
        assert.equal(tag.inner_html(), expected_inner_html_1)
        assert.equal(tag.html(), expected_html_1)

        const tag_child_2 = new Tag({tag_name:'tag', id:'child_2'})                                           // add another tag to the parent tag
        const expected_inner_html_2 =
`    <tag id="child_1">
    </tag>
    <tag id="child_2" tag_name="tag">
    </tag>
`
        const expected_html_2 =
`<tag id="parent">
    <tag id="child_1">
    </tag>
    <tag id="child_2" tag_name="tag">
    </tag>
</tag>
`
        tag.add_element(tag_child_2)
        assert.equal(tag.elements.length,2)
        assert.equal(tag.elements[0],tag_child_1)
        assert.equal(tag.elements[1],tag_child_2)
        assert.equal(tag.parent()        , null)
        assert.equal(tag_child_1.parent(), tag )
        assert.equal(tag_child_2.parent(), tag )
        assert.equal(tag.inner_html(), expected_inner_html_2)
        assert.equal(tag.html(), expected_html_2)

        const tag_child_3 = new Tag({tag_name:'tag',id:'child_3'})                                            // add another tag to the parent tag
        const expected_inner_html_3 =
`    <tag id="child_1">
        <tag id="child_3" tag_name="tag">
        </tag>
    </tag>
    <tag id="child_2" tag_name="tag">
    </tag>
`
const expected_html_3 =
`<tag id="parent">
    <tag id="child_1">
        <tag id="child_3" tag_name="tag">
        </tag>
    </tag>
    <tag id="child_2" tag_name="tag">
    </tag>
</tag>
`

        tag_child_1.add_element(tag_child_3)
        assert.equal(tag.elements.length,2)
        assert.equal(tag_child_1.elements.length,1)
        assert.equal(tag_child_1.elements[0],tag_child_3)
        assert.equal(tag.parent()        , null        )
        assert.equal(tag_child_1.parent(), tag         )
        assert.equal(tag_child_2.parent(), tag         )
        assert.equal(tag_child_3.parent(), tag_child_1 )
        assert.equal(tag.inner_html(), expected_inner_html_3)
        assert.equal(tag.html(),expected_html_3)

        const tag_child_4 = new Tag({tag_name:'tag',id:'child_4'})                                            // add a child tag to the last child tag
        const expected_inner_html_4 =
`    <tag id="child_1">
        <tag id="child_3" tag_name="tag">
            <tag id="child_4" tag_name="tag">
            </tag>
        </tag>
    </tag>
    <tag id="child_2" tag_name="tag">
    </tag>
`
        const expected_html_4 =
`<tag id="parent">
    <tag id="child_1">
        <tag id="child_3" tag_name="tag">
            <tag id="child_4" tag_name="tag">
            </tag>
        </tag>
    </tag>
    <tag id="child_2" tag_name="tag">
    </tag>
</tag>
`
        tag_child_3.add_element(tag_child_4)
        assert.equal(tag.elements.length,2)
        assert.equal(tag_child_3.elements.length,1)
        assert.equal(tag_child_3.elements[0],tag_child_4)
        assert.equal(tag.parent()        , null        )
        assert.equal(tag_child_1.parent(), tag         )
        assert.equal(tag_child_2.parent(), tag         )
        assert.equal(tag_child_3.parent(), tag_child_1 )
        assert.equal(tag_child_4.parent(), tag_child_3 )
        assert.equal(tag.inner_html(), expected_inner_html_4)
        assert.equal(tag.html(),expected_html_4)



    })



    QUnit.test('.add_to', function (assert) {
        const tag_id = 'an_id'
        const target = $(`<tag id='${tag_id}'>`)[0]                                     // todo: remove jQuery dependency (once Div API is more mature)
        assert.equal(target.outerHTML, `<tag id="${tag_id}"></tag>`)

        assert.equal($(`#${tag_id}`).html(), undefined, `${tag_id} is undefined`)
        $(`<div id='${tag_id}'>`).appendTo('body')                                      // todo: remove jQuery dependency (once Div API is more mature)
        assert.equal($(`#${tag_id}`).html(), ''       , `${tag_id} is an empty string`)

        const tag = new Tag({tag_name:'tag', id:'an_tag'});
        tag.set_style('top', '10px');
        tag.set_style('border', '2px solid');
        const expectedHtml = '<tag id="an_tag" style="border: 2px solid; top: 10px;" tag_name="tag">\n</tag>\n';        // Expected HTML result
        assert.equal(tag.dom_add_to_id(tag_id), true, "tag added to dom")

        const actualHtml = $(`#${tag_id}`).html()                                       // Get the value of the id from the DOM
        assert.strictEqual(actualHtml, expectedHtml, "The tag's HTML should match the expected HTML and be appended to the body");   // Test whether the tag was added to the fixture

        // Clean up by removing the added div
        $(`#${tag_id}`).remove()                                                        // todo: remove jQuery dependency (once Div API is more mature)
        assert.equal($(`#${tag_id}`).html(), undefined)

    });

    QUnit.test('.default_styles()',  function (assert) {
        const tag = new Tag();

        const random_styles = {};                                                          // Generate random values for attributes and set them
        Object.keys(tag.default_styles()).forEach((attr) => {
            random_styles[attr] = Math.random().toString(36).substring(2, 15);       // Generate a random string for each attribute
        });
        tag.set_styles(random_styles)


        let expected_styles = ""
        for (let [attr, value] of Object.entries(random_styles)) {
            expected_styles += `${attr}: ${value}; `;
        }
        expected_styles = expected_styles.trim()
        let expected_html = `<tag style="${expected_styles}">\n</tag>\n`;

        const actual_html = tag.html();
        assert.equal(actual_html, expected_html, "Html generated with all attributes matches the expected output");
    })

    QUnit.test('.dom_add_class', function (assert) {
        const tag = new Tag()
        tag.dom_add_class('test-class', { backgroundColor: 'red', fontSize: '14px' });

        const styleSheets = document.styleSheets;
        let ruleFound = false;

        for (let i = 0; i < styleSheets.length; i++) {
            const rules = styleSheets[i].cssRules || styleSheets[i].rules;
            for (let j = 0; j < rules.length; j++) {
                if (rules[j].selectorText === '.test-class') {
                    ruleFound = true;
                    assert.ok(rules[j].style.backgroundColor === 'red', 'Background color is red');
                    assert.ok(rules[j].style.fontSize === '14px', 'Font size is 14px');
                }
            }
        }

        assert.ok(ruleFound, '.test-class rule found in style sheets');

    });

    QUnit.test('.dom_parent', function (assert) {
        const tag = new Tag()
        assert.equal(tag.dom_parent(), null)
        tag.parent_dom = 'aaaa'
        assert.equal(tag.dom_parent(), 'aaaa')
    })

    QUnit.test('.generate_random_id', function (assert) {
        const tag__tag = new Tag()
        const tag__div = new Tag({tag:'Div'})
        const tag_random_id = tag__tag.generate_random_id()
        const div_random_id = tag__div.generate_random_id()
        assert.equal(tag_random_id.length, 9)
        assert.equal(div_random_id.length, 9)
        assert.ok(tag_random_id.startsWith('tag'))
        assert.ok(div_random_id.startsWith('div'))
        assert.notEqual(new Tag().generate_random_id(), new Tag().generate_random_id())


    })
    QUnit.test('.html.html_config.include_tag', function (assert) {
        const tag = new Tag()
        assert.equal(tag.html_config.include_tag, true)
        assert.equal(tag.html(), `<tag>\n</tag>\n`)

        tag.html_config.include_tag = false
        assert.equal(tag.html_config.include_tag, false)
        assert.equal(tag.html(), `\n\n`)                            // todo: understand better the side effects, this is casued by html_config.new_line_before_elements and html_config.new_line_after_final_tag
    })

    QUnit.test('.html.html_config.include_end_tag', function (assert) {
        const tag = new Tag()
        assert.equal(tag.html_config.include_end_tag, true)
        assert.equal(tag.html(), `<tag>\n</tag>\n`)

        tag.html_config.include_end_tag = false
        assert.equal(tag.html_config.include_end_tag, false)
        assert.equal(tag.html(), `<tag/>\n`)
    })

    QUnit.test('.html - with no id', function (assert) {
        const tag = new Tag()
        assert.equal(tag.html_config.include_id, true)
        tag.html_config.include_id = false
        assert.equal(tag.html(), `<tag>\n</tag>\n`)
    })

    QUnit.test('.html - extra attributes',  function (assert) {
        const key   = 'an key'
        const value = 'an value'
        const tag = new Tag({id:'html-extra-attributes', attributes: {key, value}})
        const expected_html = `<tag id="${tag.id}" key="${key}" value="${value}">\n</tag>\n`
        assert.equal(tag.html(), expected_html)
    })

    QUnit.test('.html - mixed attributes',  function (assert) {
        const expected_html = '<textarea placeholder="Enter a message..." spellcheck="false" required></textarea>'
        const attributes = {placeholder:"Enter a message...", spellcheck:"false", required:null}
        const textarea    = new Tag({tag:'textarea', attributes:attributes})
        textarea.html_config.include_id               = false
        textarea.html_config.new_line_before_elements = false
        textarea.html_config.new_line_after_final_tag = false
        assert.equal(textarea.html(), expected_html)
        //assert.expect(0)
    });

    QUnit.test('.html - with value',  function (assert) {
        const value = 'an value'
        const tag = new Tag({value: value, id:'html-with-value'})
        assert.equal(tag.value, value)
        const expected_html = `<tag id="${tag.id}">${value}</tag>\n`
        assert.equal(tag.html(), expected_html)                             // when value is set, the html should just be the value
    })


    QUnit.test('.set_style', function (assert) {
        const tag        =   new Tag()
        const tag_styles = tag.styles
        tag.set_style('top', '10px')
        assert.equal(tag_styles.top, '10px')
    })

    QUnit.test('.dom_set_styles',  function (assert) {
        const tag        =   new Tag({id:'dom_set_styles'})
        assert.equal(tag.dom_add       ()        , true  )
        assert.equal(tag.dom_styles    ().opacity, 1     )
        assert.equal(tag.dom_styles    ().top    , 'auto')
        assert.equal(tag.dom_set_style ('opacity', 0.3     ), tag)
        assert.equal(tag.dom_set_styles({opacity: 0.3, top:'50px'}) , tag)
        assert.equal(tag.dom_styles    ().opacity, 0.3   )
        assert.equal(tag.dom_styles    ().top    , '50px')
        assert.equal(tag.dom_remove    ()        , true  )
    })

    QUnit.test('.dom_apply_styles',  function (assert) {
        const tag  =   new Tag({id:'dom_apply_styles'})
        tag.set_style('top', '10px')
        tag.dom_add()
        assert.equal(tag.dom_styles().top, '10px')
        assert.equal(tag.dom().style.top , '10px')
        tag.styles.top = '20px'
        assert.equal(tag.dom().style.top , '10px')
        tag.dom_apply_styles()
        assert.equal(tag.dom().style.top, '20px')
    });

    QUnit.test('.html_escape', function (assert) {
        const tag = new Tag()

        assert.equal(tag.html_escape(null       ), ''                                   , 'handles null input')
        assert.equal(tag.html_escape(undefined  ), ''                                   , 'handles undefined input')

        const unsafe_string  = '<script>alert("xss")</script>'
        const escaped_html   = tag.html_escape(unsafe_string)
        const expected       = '&lt;script&gt;alert("xss")&lt;/script&gt;'
        assert.equal(escaped_html, expected                                             , 'escapes HTML entities correctly')

        const mixed_content  = '<div class="test">Hello & World</div>'
        const expected_mixed = '&lt;div class="test"&gt;Hello &amp; World&lt;/div&gt;'
        assert.equal(tag.html_escape(mixed_content), expected_mixed                     , 'handles mixed content with attributes')

        const special_chars  = '< > & " \''
        const expected_chars = '&lt; &gt; &amp; " \''
        assert.equal(tag.html_escape(special_chars), expected_chars                     , 'escapes only HTML structural characters')

        const safe_string    = 'Hello World 123'
        assert.equal(tag.html_escape(safe_string), safe_string                          , 'does not modify safe strings')

        const number_input  = 42
        assert.equal(tag.html_escape(number_input), '42'                                , 'handles number input')
    });

    QUnit.test('_should be an instance and inherit from Html_Tag', function(assert) {
        const html_tag = new Tag();
        assert.ok(html_tag instanceof Tag                     , 'Instance created is an instance of Html_Tag');
        assert.strictEqual(Tag.prototype.constructor, Tag, 'Html_Tag.prototype.constructor is Html_Tag');
        assert.equal(html_tag.tag, 'tag')
  });

       test('constructor sets default values', assert => {
        const tag = new Tag()

        assert.equal   (tag.tag            , 'tag'             , 'Sets default tag name'  )
        assert.deepEqual(tag.attributes    , {}                , 'Sets empty attributes'  )
        assert.equal   (tag.class          , null              , 'No default class'       )
        assert.equal   (tag.element_dom    , null              , 'No DOM element'         )
        assert.equal   (tag.element_parent , null              , 'No parent element'      )
        assert.deepEqual(tag.elements      , []                , 'Empty elements array'   )
        assert.ok     (tag.html_config                         , 'Has HTML config'        )
        assert.equal   (tag.id             , null              , 'No default ID'          )
        assert.equal   (tag.parent_dom     , null              , 'No parent DOM'          )
        assert.ok     (tag.styles                              , 'Has styles object'      )
        assert.equal   (tag.value          , null              , 'No default value'       )
    })

    test('constructor accepts custom values', assert => {
        const tag = new Tag({
            tag        : 'div'                 ,
            id         : 'test-id'             ,
            class      : 'test-class'          ,
            attributes : { 'data-test': 'test' },
            value      : 'test-value'
        })

        assert.equal   (tag.tag                    , 'div'            , 'Sets custom tag'        )
        assert.equal   (tag.id                     , 'test-id'        , 'Sets custom ID'         )
        assert.equal   (tag.class                  , 'test-class'     , 'Sets custom class'      )
        assert.equal   (tag.attributes['data-test'], 'test'           , 'Sets custom attributes' )
        assert.equal   (tag.value                  , 'test-value'     , 'Sets custom value'      )
    })

    test('add_class method', assert => {
        const tag = new Tag()

        tag.add_class('class1')
        assert.equal(tag.class           , 'class1'          , 'Adds first class'       )

        tag.add_class('class2')
        assert.equal(tag.class           , 'class1 class2'   , 'Appends second class'   )
    })

    test('add_element and add_elements methods', assert => {
        const parent = new Tag()
        const child1 = new Tag({ tag: 'child1' })
        const child2 = new Tag({ tag: 'child2' })
        const child3 = new Tag({ tag: 'child3' })

        parent.add_element(child1)
        assert.equal   (parent.elements.length , 1                , 'Adds single element'  )
        assert.equal   (child1.element_parent  , parent           , 'Sets parent reference')

        parent.add_elements(child2, child3)
        assert.equal   (parent.elements.length , 3                , 'Adds multiple elements')
        assert.equal   (child2.element_parent  , parent           , 'Sets parent for child2')
        assert.equal   (child3.element_parent  , parent           , 'Sets parent for child3')

        parent.clear_elements()
        assert.equal   (parent.elements.length , 0                , 'confirms no elements')

    })

    test('clone method', assert => {
        const original = new Tag({
            tag        : 'div'                 ,
            id         : 'original-id'         ,
            class      : 'test-class'          ,
            value      : 'test-value'          ,
            attributes : { 'data-test': 'test' }
        })

        const cloned = original.clone({ id: 'cloned-id' })

        assert.equal   (cloned.tag                     , original.tag              , 'Copies tag'            )
        assert.equal   (cloned.class                   , original.class           , 'Copies class'          )
        assert.equal   (cloned.value                   , original.value           , 'Copies value'          )
        assert.deepEqual(cloned.attributes             , original.attributes      , 'Copies attributes'     )
        assert.equal   (cloned.id                      , 'cloned-id'             , 'Sets new ID'           )
        assert.deepEqual(cloned.elements               , []                       , 'Empty elements array'   )
        assert.notEqual(cloned.html_config             , original.html_config    , 'New html_config object')
        assert.notEqual(cloned.styles                  , original.styles         , 'New styles object'     )
    })

    test('html generation', assert => {
        // Simple tag
        const simple = new Tag({ tag: 'div' })
        assert.equal(simple.html()          , '<div>\n</div>\n'   , 'Generates basic tag'   )

        // Tag with attributes
        const with_attrs = new Tag({
            tag        : 'div'                 ,
            id         : 'test-id'             ,
            class      : 'test-class'          ,
            attributes : { 'data-test': 'test' }
        })
        assert.equal(with_attrs.html()      , '<div id="test-id" class="test-class" data-test="test">\n</div>\n',
                                                                    'Includes attributes'    )

        // Tag with value
        const with_value = new Tag({
            tag   : 'span'                     ,
            value : 'test content'
        })
        assert.equal(with_value.html()      , '<span>test content</span>\n',
                                                                    'Includes value'         )

        // Nested tags
        const parent = new Tag({ tag: 'div' })
        const child = new Tag({ tag: 'span', value: 'child' })
        parent.add_element(child)
        assert.equal(parent.html()          , '<div>\n    <span>child</span>\n</div>\n',
                                                                    'Handles nesting'        )
    })

    test('html_config options', assert => {
        const tag = new Tag({ tag: 'div', value: 'test' })

        // Test include_tag
        tag.html_config.include_tag = false
        assert.equal(tag.html()             , 'test\n'           , 'Can omit tags'          )

        // Test include_end_tag
        tag.html_config.include_tag = true
        tag.html_config.include_end_tag = false
        assert.equal(tag.html()             , '<div/>\n'         , 'Can use self-closing'   )

        // Test new_line settings
        tag.html_config.include_end_tag = true
        tag.html_config.new_line_after_final_tag = false
        assert.equal(tag.html()             , '<div>test</div>'  , 'Can control newlines'   )
    })

    test('html escaping', assert => {
        const tag = new Tag({
            tag   : 'div'                     ,
            value : '<script>alert("xss")</script>'
        })

        const escaped_html = tag.html()
        assert.ok    (escaped_html.includes('&lt;script&gt;')    , 'Escapes < and >'       )
        assert.notOk (escaped_html.includes('&quot;')            , 'Does NOT Escape quotes'         )
        assert.ok    (escaped_html.includes('"')            , 'Does NOT Escape quotes'         )
        assert.notOk (escaped_html.includes('<script>')          , 'No raw script tags'     )
    })

    test('style handling', assert => {
        const tag = new Tag({ tag: 'div' })

        tag.set_style('backgroundColor', 'red')
        assert.equal(tag.styles.backgroundColor , 'red'           , 'Sets single style'     )

        tag.set_styles({
            border : '1px solid black'         ,
            margin : '10px'
        })
        assert.equal(tag.styles.border         , '1px solid black', 'Sets multiple styles'  )
        assert.equal(tag.styles.margin         , '10px'           , 'Preserves all styles'  )

        const html = tag.html()
        assert.ok(html.includes('style="'                      )  , 'Includes style attribute')
        assert.ok(html.includes('background-color: red'        )  , 'Converts camelCase to kebab-case')
        assert.ok(html.includes('border: 1px solid black'      )  , 'Includes multiple styles')
    })
})