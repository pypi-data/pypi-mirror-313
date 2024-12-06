import API__User_Data__Files     from '../../../js/cbr/api/API__User_Data__Files.mjs'
import { setup_mock_responses,
         MOCK_FILE_ID,
         MOCK_VERSION_ID,
         MOCK_CONTENT,
         MOCK_FILE_DATA,
         MOCK_VERSIONS }         from '../../../js/testing/Mock_API__Data.mjs'

const { module, test } = QUnit

// Setup mocks once before all tests
setup_mock_responses()

module('API__User_Data__Files', hooks => {
    let api

    hooks.before(() => {
        api = new API__User_Data__Files()
    })

    test('get_file_contents handles successful response', async assert => {
        // Act
        const result = await api.get_file_contents(MOCK_FILE_ID)

        // Assert
        assert.equal(result.content.trim()    , MOCK_CONTENT        , 'Returns decoded content'    )
        assert.deepEqual(result.file_data     , MOCK_FILE_DATA      , 'Returns file metadata'      )
    })

    test('get_file_contents handles invalid response', async assert => {
        try {
            await api.get_file_contents('invalid-file')
            assert.notOk(true, 'Should throw error')
        } catch (error) {
            assert.equal(error.message, 'Invalid file content response', 'Throws expected error')
        }
    })

    test('update_file completes successfully', async assert => {
        // Act
        const result = await api.update_file(MOCK_FILE_ID, MOCK_CONTENT)

        // Assert
        assert.ok   (result.success               , 'Returns success status'    )
        assert.equal(result.data.status, 'updated', 'Indicates update completed')
    })

    test('get_file_versions returns expected data', async assert => {
        // Act
        const result = await api.get_file_versions(MOCK_FILE_ID)

        // Assert
        assert.deepEqual(result, MOCK_VERSIONS, 'Returns versions array')
    })

    test('get_file_versions handles empty response with fallback', async assert => {
        // Act
        const result = await api.get_file_versions('empty-versions')

        // Assert
        assert.deepEqual(result, [], 'Returns empty array when data is null')
    })

    test('get_version_content handles successful response', async assert => {
        // Act
        const result = await api.get_version_content(MOCK_FILE_ID, MOCK_VERSION_ID)

        // Assert
        assert.equal(result.trim(), MOCK_CONTENT, 'Returns decoded content')
    })

    test('get_version_content handles invalid response', async assert => {
        try {
            await api.get_version_content(MOCK_FILE_ID, 'invalid-version')
            assert.notOk(true, 'Should throw error')
        } catch (error) {
            assert.equal(error.message, 'Invalid version content response', 'Throws expected error')
        }
    })

    test('encoding and decoding methods work correctly', assert => {
        const test_strings = [
            'Hello World',
            'Special chars: åäö',
            'Unicode: 🌟✨',
            'Multi\nline\ncontent'
        ]

        test_strings.forEach(original => {
            const encoded = api.encode_content_to_base64(original)
            const decoded = api.decode_base64_content(encoded)
            assert.equal(decoded, original, `Correctly encodes and decodes: ${original}`)
        })
    })
})