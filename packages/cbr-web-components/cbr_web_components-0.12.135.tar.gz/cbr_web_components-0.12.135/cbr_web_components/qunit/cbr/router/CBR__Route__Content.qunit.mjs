import CBR__Route__Content  from '../../../js/cbr/router/CBR__Route__Content.mjs'
import CBR__Content__Loader from '../../../js/cbr/router/CBR__Content__Loader.mjs'
import { Mock_Fetch,
         set_mock_response } from '../../../js/testing/Mock_Fetch.mjs'

const { module, test , only} = QUnit

const MOCK_HTML_CONTENT = '<div>Test Content</div>'
const MOCK_RESPONSE = {
    html     : MOCK_HTML_CONTENT,
    metadata : {
        title    : 'Test Page',
        subtitle : 'Test Description'
    }
}

module('CBR__Route__Content', hooks => {
    let route_content
    let default_config

    hooks.beforeEach(() => {
        Mock_Fetch.apply_mock(CBR__Content__Loader)                    // Apply mock to the loader since it's used internally

        default_config = {
            dev_mode     : true                                      ,
            base_url     : 'https://static.dev.aws.cyber-boardroom.com',
            version      : 'latest'                                   ,
            language     : 'en'                                       ,
            content_type : 'site'
        }
        route_content = new CBR__Route__Content(default_config)

        // Setup mock responses for common paths
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/test-page.md', MOCK_RESPONSE)
    })

    test('constructor initializes with correct defaults', assert => {
        // Assert
        assert.ok(route_content.content_loader instanceof CBR__Content__Loader, 'Creates content loader instance')
    })

    test('constructor handles empty config correctly', assert => {
        // Arrange & Act
        const route_content_empty = new CBR__Route__Content()

        // Assert - Verify default values propagated to content_loader
        const content_loader = route_content_empty.content_loader
        assert.ok  (content_loader instanceof CBR__Content__Loader             , 'Creates content loader instance'    )
        assert.equal(content_loader.base_url    , 'https://static.dev.aws.cyber-boardroom.com', 'Uses default base_url'     )
        assert.equal(content_loader.version     , 'latest'                    , 'Uses default version'      )
        assert.equal(content_loader.language    , 'en'                        , 'Uses default language'     )
        assert.equal(content_loader.content_type, 'site'                      , 'Uses default content_type' )
    })

    test('fetch_content returns HTML content for valid route', async assert => {
        // Arrange
        const route_path = 'test-page'

        // Act
        const content = await route_content.fetch_content(route_path)

        // Assert
        assert.equal(content, MOCK_HTML_CONTENT, 'Returns correct HTML content')
    })

    test('fetch_content handles missing HTML in response', async assert => {
        // Arrange
        const invalid_response = { metadata: { title: 'Test' } }
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/invalid-page.md',
                          invalid_response)

        // Act
        const content = await route_content.fetch_content('invalid-page')

        // Assert
        assert.equal(content, '... failed to load content ...', 'Returns error message when HTML missing')
    })

    test('fetch_content handles fetch errors gracefully', async assert => {
        // Arrange
        const error_path = 'error-page'
        const url        = 'https://static.dev.aws.cyber-boardroom.com/cbr-content/latest/en/site/error-page.md.json'
        set_mock_response(url, null, 404)

        // Act
        const content = await route_content.fetch_content(error_path)

        // Assert
        assert.equal(content, '... failed to load content ...', 'Returns error message on fetch failure')
    })

    test('map_route_to_page returns same path by default', assert => {
        // Arrange
        const test_paths = [
            'home/index',
            'about/team',
            'products/details'
        ]

        // Act & Assert
        test_paths.forEach(path => {
            assert.equal(route_content.map_route_to_page(path), path,
                        `Correctly maps ${path} to itself`)
        })
    })

    test('set_language updates content loader language', assert => {
        // Arrange
        const new_language = 'fr'

        // Act
        route_content.set_language(new_language)

        // Assert
        assert.equal(route_content.content_loader.language, new_language,
                    'Updates content loader language')
    })

    test('set_version updates content loader version', assert => {
        // Arrange
        const new_version = 'v2.0'

        // Act
        route_content.set_version(new_version)

        // Assert
        assert.equal(route_content.content_loader.version, new_version,
                    'Updates content loader version')
    })

    test('fetch_content handles null response gracefully', async assert => {
        // Arrange
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/null-page.md',
                          null)

        // Act
        const content = await route_content.fetch_content('null-page')

        // Assert
        assert.equal(content, '... failed to load content ...',
                    'Returns error message for null response')
    })

    test('fetch_content with empty route uses default', async assert => {
        // Arrange
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/.md',
                          MOCK_RESPONSE)

        // Act
        const content = await route_content.fetch_content('')

        // Assert
        assert.equal(content, MOCK_HTML_CONTENT, 'Successfully loads default route content')
    })
})