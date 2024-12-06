import CBR__Content__Loader from '../../../js/cbr/router/CBR__Content__Loader.mjs'

import { Mock_Fetch,
         set_mock_response } from '../../../js/testing/Mock_Fetch.mjs'

const { module, test , only, skip} = QUnit

const MOCK_CONTENT = {
    title: 'Test Content',
    body: 'Test body content'
}

module('CBR__Content__Loader', hooks => {
    let loader
    let default_config

    hooks.beforeEach(() => {
        Mock_Fetch.apply_mock(CBR__Content__Loader)

        default_config = {
            dev_mode    : false                         ,
            base_url    : 'https://static.dev.aws.cyber-boardroom.com',
            version     : 'latest'                      ,
            language    : 'en'                          ,
            content_type: 'site'
        }
        loader = new CBR__Content__Loader(default_config)

        // Setup mock responses
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/test-page.md', MOCK_CONTENT)
    })

    test('constructor sets default values correctly', assert => {
        // Arrange
        const empty_loader = new CBR__Content__Loader()

        // Assert
        assert.equal(empty_loader.base_url    , 'https://static.dev.aws.cyber-boardroom.com', 'Sets default base_url'     )
        assert.equal(empty_loader.version     , 'latest'                                    , 'Sets default version'      )
        assert.equal(empty_loader.language    , 'en'                                        , 'Sets default language'     )
        assert.equal(empty_loader.content_type, 'site'                                      , 'Sets default content_type' )
    })

    test('constructor accepts custom config', assert => {
        // Arrange
        const custom_config = {
            dev_mode    : true                          ,
            base_url    : 'https://custom.url'          ,
            version     : 'v1.0'                        ,
            language    : 'fr'                          ,
            content_type: 'blog'
        }

        // Act
        const custom_loader = new CBR__Content__Loader(custom_config)

        // Assert
        assert.equal(custom_loader.dev_mode    , true                  , 'Sets custom dev_mode'     )
        assert.equal(custom_loader.base_url    , 'https://custom.url'  , 'Sets custom base_url'     )
        assert.equal(custom_loader.version     , 'v1.0'               , 'Sets custom version'      )
        assert.equal(custom_loader.language    , 'fr'                 , 'Sets custom language'     )
        assert.equal(custom_loader.content_type, 'blog'               , 'Sets custom content_type' )
    })

    test('_build_prod_url generates correct URL', assert => {
        // Arrange
        const page = 'test-page'
        const expected_url = `${default_config.base_url}/cbr-content/${default_config.version}/` +
                           `${default_config.language}/${default_config.content_type}/${page}.md.json`

        // Act
        const url = loader._build_prod_url(page)

        // Assert
        assert.equal(url, expected_url, 'Generates correct production URL')
    })

    test('_build_dev_url generates correct URL', assert => {
        // Arrange
        const page = 'test-page'
        const expected_url = `/markdown/render/markdown-file-to-html-and-metadata?path=${default_config.language}/` +
                           `${default_config.content_type}/${page}.md`

        // Act
        const url = loader._build_dev_url(page)

        // Assert
        assert.equal(url, expected_url, 'Generates correct development URL')
    })

    test('set_language updates language', assert => {
        // Arrange
        const new_language = 'es'

        // Act
        loader.set_language(new_language)

        // Assert
        assert.equal(loader.language, new_language, 'Language is updated correctly')
    })

    test('set_version updates version', assert => {
        // Arrange
        const new_version = 'v2.0'

        // Act
        loader.set_version(new_version)

        // Assert
        assert.equal(loader.version, new_version, 'Version is updated correctly')
    })

    test('load_content returns expected content in dev mode', async assert => {
        // Arrange
        loader.dev_mode = true
        const page = 'test-page'

        // Act
        assert.ok(1)
        const result = await loader.load_content(page)

        // Assert
        assert.deepEqual(result, MOCK_CONTENT, 'Returns correct content in dev mode')
    })

    test('load_content handles errors', async assert => {
        // Arrange
        const page = 'error-page'
        const url = 'https://static.dev.aws.cyber-boardroom.com/cbr-content/latest/en/site/error-page.md.json'
        set_mock_response(url, null,  404)

        // Act & Assert
        try {
            await loader.load_content(page)
            assert.notOk(true, 'Should throw error')
        } catch (error) {
            assert.ok(error instanceof Error, 'Throws error on failed fetch')
            assert.deepEqual(error.message, `Failed to load content | 404 | ${url}`, 'Wrong error message')
        }
    })
})