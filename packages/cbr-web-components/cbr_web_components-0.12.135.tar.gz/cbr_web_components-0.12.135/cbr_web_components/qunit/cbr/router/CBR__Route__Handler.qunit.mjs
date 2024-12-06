import CBR__Content__Loader from '../../../js/cbr/router/CBR__Content__Loader.mjs'
import CBR__Route__Handler from '../../../js/cbr/router/CBR__Route__Handler.mjs'
import CBR__Route__Content from '../../../js/cbr/router/CBR__Route__Content.mjs'
import { Mock_Fetch,
         set_mock_response } from '../../../js/testing/Mock_Fetch.mjs'

const { module, test, only } = QUnit

const MOCK_CONTENT = {
    html    : '<div>Test Content</div>'    ,
    metadata: {
        title   : 'Test Page'              ,
        subtitle: 'Test Description'
    }
}

module('CBR__Route__Handler', hooks => {
    let handler
    let mock_component
    let content_div
    let route_content

    hooks.beforeEach(() => {
        //Mock_Fetch.apply_mock(CBR__Route__Content)                                // Apply mock to Route Content
        Mock_Fetch.apply_mock(CBR__Content__Loader)

        // Setup mock responses for common paths
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/test-page.md'     , MOCK_CONTENT)
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/home/index.md'    , MOCK_CONTENT)
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/test/path.md'     , MOCK_CONTENT)

        // Setup DOM elements
        content_div = document.createElement('div')
        content_div.id = 'content'
        document.body.appendChild(content_div)

        // Setup mock component
        route_content = new CBR__Route__Content()
        mock_component = {
            query_selector: (selector) => document.querySelector(selector),
            routeContent  : route_content
        }

        handler = new CBR__Route__Handler(mock_component)
    })

    hooks.afterEach(() => {
        content_div.remove()
        window.history.pushState({}, '', '/')                                      // Reset URL
    })

    test('constructor initializes with correct defaults', assert => {
        // Assert
        assert.equal(handler.base_path    , '/'           , 'Sets default base_path'    )
        assert.equal(handler.default_page , 'home/index'  , 'Sets default page'         )
        assert.equal(handler.component    , mock_component , 'Sets component reference'  )
    })

    test ('handle_route processes path correctly', async assert => {
        // Arrange
        const test_path = 'test-page'

        // Act
        await handler.handle_route(test_path)

        // Assert
        assert.ok(1)

        assert.ok(content_div.innerHTML.includes(MOCK_CONTENT.html)               , 'Renders correct content'          )
        assert.ok(content_div.firstChild.classList.contains('nav-content')        , 'Adds nav-content class'          )
        assert.ok(content_div.firstChild.classList.contains('nav-test-page')      , 'Adds navigation class'           )
    })

    test('handle_route handles empty path', async assert => {
        // Act
        await handler.handle_route('/')

        // Assert
        assert.ok(content_div.innerHTML.includes(MOCK_CONTENT.html), 'Renders default page content')
    })

    test('handle_route handles fetch errors gracefully', async assert => {
        // Arrange
        const error_path = 'error-page'
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/error-page.md', null, 404)
        const expected_error = `\
<div class="nav-content nav-error-page">
    ... failed to load content ...
</div>
`

        // Act
        await handler.handle_route(error_path)

        // Assert
        assert.deepEqual(content_div.innerHTML,expected_error)
    })

    test('should_handle_link validates links correctly', assert => {
        // Arrange
        handler.base_path = '/en/site/'
        const base_url = window.location.origin + handler.base_path
        const test_cases = [{ href: `${base_url}test`        , expected: true  , desc: 'Valid internal link' },
                            { href: 'https://external.com'   , expected: false , desc: 'External link'       },
                            { href: 'javascript:void(0)'     , expected: false , desc: 'JavaScript link'     },
                            { href: `${base_url}`            , expected: true  , desc: 'Root path'           },
                            { href: '/relative/path'         , expected: false , desc: 'Relative path'       }]

        // Act & Assert
        test_cases.forEach(test_case => {
            const link = document.createElement('a')
            link.href = test_case.href
            assert.equal(handler.should_handle_link(link), test_case.expected, test_case.desc)
        })
        assert.equal(handler.should_handle_link(null), false, 'Handles null link')
        assert.equal(handler.should_handle_link()    , false, 'Handles empty link')
    })

    test('handle_navigation_click processes internal links', async assert => {
        // Arrange
        const link = document.createElement('a')
        link.href  = window.location.origin + '/test-page'
        document.body.appendChild(link)

        // Create click event with path
        const click_event = new MouseEvent('click', {
            bubbles   : true              ,
            cancelable: true              ,
            composed  : true
        })

        // Mock composedPath to return path with link
        click_event.composedPath = () => [link, document.body, document]

        // Act
        await handler.handle_navigation_click(click_event)

        // Assert
        assert.ok(content_div.innerHTML.includes(MOCK_CONTENT.html), 'Navigation processed content')

        // Cleanup
        link.remove()
    })

    test('set_base_path updates path handling', async assert => {
        // Arrange
        const new_base = '/new-base/'
        handler.set_base_path(new_base)

        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/test-in-new-base.md',
                          MOCK_CONTENT)

        const link = document.createElement('a')
        link.href = window.location.origin + new_base + 'test-in-new-base'

        // Act
        await handler.process_link(link)

        // Assert
        assert.equal(handler.base_path, new_base                                  , 'Base path was updated'    )
        assert.ok(content_div.innerHTML.includes(MOCK_CONTENT.html)              , 'Content loads with new base path')
    })

    test('handle_route handles null content response', async assert => {
        // Arrange
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/null-page.md', null)
        const expected_error = `\
<div class="nav-content nav-null-page">
    ... failed to load content ...
</div>
`

        // Act
        await handler.handle_route('null-page')

        // Assert
        assert.deepEqual(content_div.innerHTML , expected_error)
    })

    test('handle_pop_state processes browser navigation', async assert => {
        // Arrange
        window.history.pushState({}, '', '/test/path')
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/test/path.md',
                          MOCK_CONTENT)

        // Act
        await handler.handle_pop_state(new PopStateEvent('popstate'))

        // Assert
        assert.ok(content_div.innerHTML.includes(MOCK_CONTENT.html), 'Pop state loads correct content')
    })

    test('process_link handles web component loading', async assert => {
        // Arrange
        const link = document.createElement('a')
        const mock_module = { default: class TestComponent extends HTMLElement {
            static define() { customElements.define('webc-test-component', this) }
        }}

        link.href = window.location.origin + '/test-component'
        link.setAttribute('data-target-type'   , 'web_component'          )
        link.setAttribute('data-component'     , 'WebC__Test__Component'  )
        link.setAttribute('data-component-path', 'test/components/'       )

        // Mock the import_module method
        handler.import_module = async (path) => {
            assert.equal(path,
                        '/web_components/js/cbr/web-components/test/components/WebC__Test__Component.mjs',
                        'Loads correct module path')
            return mock_module
        }

        // Act
        await handler.process_link(link)

        // Assert
        const component = content_div.querySelector('webc-test-component')
        assert.ok(component, 'Component was created')
    })

    test('handle_route handles missing content element', async assert => {
        // Arrange - simulate missing content element
        const original_querySelector = mock_component.query_selector
        mock_component.query_selector = () => null

        // Act
        await handler.handle_route('test/path')

        // Assert
        assert.ok(true, 'No error thrown when content element missing')

        // Cleanup
        mock_component.query_selector = original_querySelector
    })

    test('handle_route creates correct navigation classes', async assert => {
        // Arrange
        handler.base_path = '/en/site/'
        const test_routes = [

            { path: 'single'                        , expected: ['nav-single']                               },
            { path: 'parent/child'                  , expected: ['nav-parent', 'nav-parent-child']           },
            { path: 'a/very/deep/path'              , expected: ['nav-a', 'nav-a-very', 'nav-a-very-deep',
                                                                 'nav-a-very-deep-path']                     },
            { path: '/path/with/slashes/'           , expected: ['nav-path', 'nav-path-with',
                                                                 'nav-path-with-slashes']                    },
            { path: `${handler.base_path}with/base` , expected: ['nav-with', 'nav-with-base']                },]

        for (const route of test_routes) {
            // Act
            await handler.handle_route(route.path)

            // Assert
            const content_wrapper = content_div.firstChild
            assert.ok(content_wrapper.classList.contains('nav-content'), `Base nav-content class present for ${route.path}`)


            route.expected.forEach(className => {
                assert.ok(content_wrapper.classList.contains(className), `${className} present for ${route.path}`)
            })
        }
    })

    test('handle_navigation_click prevents default on valid links', async assert => {
        // Arrange
        const link = document.createElement('a')
        link.href = window.location.origin + handler.base_path + 'test-path'
        let default_prevented = false

        const click_event = new MouseEvent('click', {
            bubbles   : true          ,
            cancelable: true          ,
            composed  : true
        })
        click_event.preventDefault = () => { default_prevented = true }
        click_event.composedPath = () => [link, document.body, document]

        // Act
        await handler.handle_navigation_click(click_event)

        // Assert
        assert.ok(default_prevented, 'Default event was prevented')
    })

    test('handle_navigation_click ignores invalid links', async assert => {
        // Arrange
        const external_link = document.createElement('a')
        external_link.href = 'https://external-site.com'
        let processed = false

        const click_event = new MouseEvent('click', {
            bubbles   : true              ,
            cancelable: true              ,
            composed  : true
        })
        click_event.composedPath = () => [external_link, document.body, document]

        // Save original process_link
        const original_process = handler.process_link
        handler.process_link = () => { processed = true }

        // Act
        await handler.handle_navigation_click(click_event)

        // Assert
        assert.notOk(processed, 'Did not process external link')

        // Cleanup
        handler.process_link = original_process
    })

    test('handle_route handles fetch content errors', async assert => {
        // Arrange
        const original_fetch = mock_component.routeContent.fetch_content
        mock_component.routeContent.fetch_content = async () => {
            throw new Error('Fetch failed')
        }

        // Act
        await handler.handle_route('error/path')

        // Assert
        assert.ok(content_div.innerHTML.includes('content-error'),
                 'Shows error message on fetch failure')
        assert.ok(content_div.innerHTML.includes('Error loading content'),
                 'Shows user-friendly error message')

        // Cleanup
        mock_component.routeContent.fetch_content = original_fetch
    })

    test('process_link handles missing component name for web_component type', async assert => {
        // Arrange
        const link = document.createElement('a')
        link.href = window.location.origin + '/test-component'
        link.setAttribute('data-target-type', 'web_component')
        // Deliberately not setting data-component attribute

        const console_messages = []
        const original_console_error = console.error
        console.error = (msg) => console_messages.push(msg)

        // Act
        await handler.process_link(link)

        // Assert
        assert.ok(console_messages.includes('Web component target specified but no component name found'),
                 'Logs correct error message')

        // Cleanup
        console.error = original_console_error
    })

    test('process_link handles link target type', async assert => {
        // Arrange
        const link = document.createElement('a')
        link.href = window.location.origin + '/test-link'
        link.setAttribute('data-target-type', 'link')

        let navigated = false
        const expected_path = 'test-link'
        const original_navigate = handler.navigate
        handler.navigate = async (path) => {
            navigated = true
            assert.equal(path, expected_path, 'Navigates to correct path')
        }

        // Act
        await handler.process_link(link)

        // Assert
        assert.ok(navigated, 'Navigation was triggered')

        // Cleanup
        handler.navigate = original_navigate
    })

    test('process_link handles unknown target type using default case', async assert => {
        // Arrange
        const link = document.createElement('a')
        link.href = window.location.origin + '/test-default'
        link.setAttribute('data-target-type', 'unknown-type')

        let navigated = false
        const expected_path = 'test-default'
        const original_navigate = handler.navigate
        handler.navigate = async (path) => {
            navigated = true
            assert.equal(path, expected_path, 'Navigates to correct path')
        }

        // Act
        await handler.process_link(link)

        // Assert
        assert.ok(navigated, 'Navigation was triggered for unknown type')

        // Cleanup
        handler.navigate = original_navigate
    })

    test('load_component handles missing content element', async assert => {
        // Arrange
        const original_querySelector = mock_component.query_selector
        mock_component.query_selector = () => null
        let component_created = false

        // Mock document.createElement to track if it's called
        const original_createElement = document.createElement
        document.createElement = () => {
            component_created = true
            return original_createElement.call(document, 'div')
        }

        // Act
        await handler.load_component('WebC__Test__Component', 'test/path/')

        // Assert
        assert.notOk(component_created, 'Component creation was skipped when content element missing')

        // Cleanup
        mock_component.query_selector = original_querySelector
        document.createElement = original_createElement
    })

    test('load_component handles component loading error', async assert => {
        // Arrange
        const error_message = 'Failed to load module'
        handler.import_module = async () => {
            throw new Error(error_message)
        }

        const expected_error = '<div class="content-error">Error loading component. Please try again.</div>'

        // Act
        await handler.load_component('WebC__Test__Component', 'test/path/')

        // Assert
        assert.equal(content_div.innerHTML, expected_error, 'Shows error message when component loading fails')
    })
})