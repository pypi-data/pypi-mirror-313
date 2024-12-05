import {CBR__Paths} from "../../../js/cbr/CBR__Paths.mjs";
import API__Markdown from '../../../js/cbr/api/API__Markdown.mjs'
import { setup_mock_responses   ,
         MOCK_CONTENT_PATH      ,
         MOCK_MARKDOWN_METADATA ,
         MOCK_RAW_HTML          } from '../../../js/testing/Mock_API__Data.mjs'

const { module, test , only} = QUnit


module('API__Markdown', hooks => {
    let api

    hooks.before(() => {
        setup_mock_responses()
        api = new API__Markdown()
    })

    test('get_markdown_content handles successful response', async assert => {
        // Act
        const result = await api.get_data__markdown_page(MOCK_CONTENT_PATH)

        // Assert
        assert.equal(result.html.trim()           , MOCK_RAW_HTML.trim()    , 'Returns correct HTML'     )
        assert.deepEqual(result.metadata          , MOCK_MARKDOWN_METADATA   , 'Returns correct metadata' )
        assert.ok(result.success                                            , 'Indicates success'        )
    })

    test('get_markdown_content handles invalid path', async assert => {
        // Act
        const result = await api.get_data__markdown_page('invalid/path.md')

        // Assert
        assert.equal(result.html                  , '<p>Error loading content</p>', 'Returns error HTML'      )
        assert.deepEqual(result.metadata          , { title: 'Error' }           , 'Returns error metadata'  )
        assert.notOk(result.success                                              , 'Indicates failure'       )
    })

    test('static URL is correctly defined', assert => {
        // Assert
        assert.equal(CBR__Paths.API__MARKDOWN_RENDER,
                    '/markdown/render/markdown-file-to-html-and-metadata',
                    'Has correct endpoint URL')
    })

    test('creates instance with API__Invoke', assert => {
        // Assert
        assert.ok(api.api_invoke                       , 'Has API invoke instance' )
        assert.equal(typeof api.get_data__markdown_page, 'function'             , 'Has content method'      )
    })

    test('maintains consistent response structure', async assert => {
        // Act
        const success = await api.get_data__markdown_page(MOCK_CONTENT_PATH)
        const failure = await api.get_data__markdown_page('invalid/path.md')

        // Assert
        assert.propEqual(Object.keys(success).sort(),
                        ['html', 'metadata', 'success'].sort(),
                        'Success response has all expected keys')

        assert.propEqual(Object.keys(failure).sort(),
                        ['html', 'metadata', 'success'].sort(),
                        'Failure response has all expected keys')
    })
})