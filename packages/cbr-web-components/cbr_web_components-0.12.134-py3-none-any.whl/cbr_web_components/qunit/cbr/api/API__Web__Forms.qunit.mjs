import API__Web__Forms from '../../../js/cbr/api/API__Web__Forms.mjs'
import { Mock_Fetch }  from '../../../js/testing/Mock_Fetch.mjs'

const { module, test , only} = QUnit

module('API__Web__Forms', hooks => {
    let api
    let mock_fetch

    hooks.before(() => {
        api = new API__Web__Forms()
        mock_fetch = Mock_Fetch.apply_mock(API__Web__Forms)
    })

    test('submits form data successfully', async assert => {
        const form_data = new FormData()
        form_data.append('name', 'Test User')
        form_data.append('email', 'test@example.com')

        mock_fetch.set_response('/web/test-form', { status: 'success' })

        const response = await api.submit_form(form_data, '/web/test-form')
        const data = await response.json()

        assert.ok(data                                                          , 'Returns response data'    )
        assert.equal(data.status                      , 'success'               , 'Returns success status'   )
    })

    test('handles failed form submission', async assert => {
        const form_data = new FormData()
        mock_fetch.set_response('/web/test-form', null, 500)
        const result = await api.submit_form(form_data, '/web/test-form')
        assert.deepEqual(result.ok     , false  )
        assert.deepEqual(result.status , 500    )
        assert.deepEqual(result.headers, {}     )
        assert.deepEqual(result.body, undefined )
    })

    test('sends correct content type header', async assert => {
        assert.expect(1)  // Expecting 1 assertion

        const form_data = new FormData()
        mock_fetch.set_response('/web/test-form', { status: 'success' })

        // Override fetch_url to check headers
        api.fetch_url = async (url, options) => {
            assert.equal(options.headers['Content-Type'],
                        'application/x-www-form-urlencoded'                     , 'Sets correct content type')
            return { ok: true }
        }

        await api.submit_form(form_data, '/web/test-form')
    })
})