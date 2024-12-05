import { set_mock_response , Mock_API__Invoke } from './Mock_API__Invoke.mjs'
import CBR__Paths from "../cbr/CBR__Paths.mjs";
export { set_mock_response                    }                                 // expose this function for the users of this module

export const MOCK_FILE_ID    = 'test-file-123'
export const MOCK_VERSION_ID = 'v1'
export const MOCK_CONTENT    = 'Test file content'
export const MOCK_FILE_DATA  = { name     : 'test.txt'  ,
                                 size     : 1024        ,
                                 type     : 'text/plain',
                                 created  : '2024-01-01',
                                 modified : '2024-01-02'}

export const MOCK_VERSIONS = [ { version_id       : 'v1'        ,
                                 version_number   : 1           ,
                                 file_size        : 1024        ,
                                 created_date     : '2024-01-01',
                                 created_time     : '10:00:00'  ,
                                 is_latest_version: true        },
                               { version_id       : 'v2'        ,
                                 version_number   : 2           ,
                                 file_size        : 1024        ,
                                 created_date     : '2024-01-02',
                                 created_time     : '11:00:00'  ,
                                 is_latest_version: false       }]


export const MOCK_MENU_DATA = { first_link : { text       : 'First Link'     ,
                                               icon       : 'mdi-home'        ,
                                               href       : '/test/first'     ,
                                               visibility : true              },
                                second_link: { text       : 'Second Link'     ,
                                               icon       : 'mdi-cog'         ,
                                               href       : '/test/second'    ,
                                               visibility : true              },
                                hidden_link: { text       : 'Hidden Link'     ,                    // for Testing visibility=false
                                               icon       : 'mdi-eye-off'     ,
                                               href       : '/test/hidden'    ,
                                               visibility : false             }}
export const MOCK_MENU_DATA_FILE = 'en/web-pages/dev/web-components/api/side-menu/side-menu-1.toml'

export const MOCK_SERVER_REQUESTS_API_PATH = '/an/path/to/load'
export const MOCK_SERVER_REQUESTS_DATA     = { headers: ['requests_ids'],
                                               rows   : [['2', 'a'     ],
                                                         [2  , 'b'     ],
                                                         [3  , 'c'     ]],
                                               title  : 'an table'}

export const MOCK_CONTENT_PATH = 'en/web-pages/demos/index.md'

export const MOCK_MARKDOWN_METADATA = { title       : 'Markdown content',
                                        sub_title   : 'will go here'    ,
                                        action_link : 'some/page'       ,
                                        action_text : 'Go to page'      }
export const MOCK_RAW_HTML = `\
<h1>Markdown content</h1>
<ul>
    <li>will go here
    </li>
</ul>`

export const MOCK_MARKDOWN_RESPONSE = { html    : MOCK_RAW_HTML          ,
                                        metadata: MOCK_MARKDOWN_METADATA }

export const MOCK_API_CHANNEL   = 'api_invoke__qunit'
export const MOCK_CONFIG_PATH   = '/config/version'
export const MOCK_CONFIG_DATA   = { version: 'v0.6.8' }

export const MOCK_USER_ID          = "11111111-aaaa-bbbb-cccc-222222222222"
export const MOCK_USER_NAME        = 'guest_abc_123'
export const MOCK_USER_SESSION_ID  = "17b40038-aaaa-bbbb-cccc-a4a19f211833"

export const MOCK_SESSION_SECURITY =  { "is_admin_global": false ,
                                        "is_admin_site"  : false ,
                                        "is_blocked"     : false ,
                                        "is_customer"    : false ,
                                        "is_guest"       : false ,
                                        "is_malicious"   : false ,
                                        "is_user"        : false ,
                                        "is_user_qa"     : false ,
                                        "is_suspended"   : false ,
                                        "is_suspicious"  : false }

export const MOCK_PERSONA_1_USER_ID    = "33333333-aaaa-bbbb-cccc-444444444444"
export const MOCK_PERSONA_1_USER_NAME  = 'persona_efg_456'
export const MOCK_PERSONA_1_SESSION_ID = "17b40038-eeee-ffff-gggg-a4a19f211833"

export const MOCK_PERSONA_2_USER_ID      = "55555555-aaaa-bbbb-cccc-666666666666"
export const MOCK_PERSONA_2_USER_NAME    = 'persona__hij_789'
export const MOCK_PERSONA_2_SESSION_ID   = "17b40038-hhhh-iiii-jjjj-a4a19f211833"

export const MOCK_PERSONA_BAD_SESSION_ID = "xxxxxxxx-yyyy-yyyy-yyyy-zzzzzzzzzzzz"

export const MOCK_USER_SESSION       = { "data"              : { "username": MOCK_USER_NAME },
                                         "security"          : MOCK_SESSION_SECURITY         ,
                                         "session_id"        : MOCK_USER_SESSION_ID          ,
                                         "user_name"         : MOCK_USER_NAME                ,
                                         "user_id"           : MOCK_USER_ID                  ,
                                         "created__date"     : "2024-11-19"                  ,
                                         "created__time"     : "11:17:12"                    ,
                                         "created__timestamp": 1732015032823                 }

export const MOCK_PERSONA_1_SESSION     = { "data"            : { "username": MOCK_PERSONA_1_USER_NAME },
                                            "security"          : MOCK_SESSION_SECURITY                 ,
                                            "session_id"        : MOCK_PERSONA_1_SESSION_ID             ,
                                            "user_name"         : MOCK_PERSONA_1_USER_NAME              ,
                                            "user_id"           : MOCK_PERSONA_1_USER_ID                ,
                                            "created__date"     : "2023-11-19"                          ,
                                            "created__time"     : "01:17:12"                            ,
                                            "created__timestamp": 1732015111111                         }

export const MOCK_PERSONA_2_SESSION     = { "data"            : { "username": MOCK_PERSONA_2_USER_NAME },
                                            "security"          : MOCK_SESSION_SECURITY                 ,
                                            "session_id"        : MOCK_PERSONA_2_SESSION_ID             ,
                                            "user_name"         : MOCK_PERSONA_2_USER_NAME              ,
                                            "user_id"           : MOCK_PERSONA_2_USER_ID                ,
                                            "created__date"     : "2022-11-19"                          ,
                                            "created__time"     : "06:17:12"                            ,
                                            "created__timestamp": 1732015222222                         }

export const MOCK__API_RESPONSE__OK__LOGIN_AS_PERSONA   = {"data":null,"error":null,"message":"Found persona, set CBR__SESSION_ID__PERSONA cookie to persona id, so that user is now logged in as the provided persona id","status":"ok"}

export const MOCK__API_RESPONSE__FAIL__LOGIN_AS_PERSONA = {"data":null,"error":null,"message":"Persona not found","status":"error"}

export function setup_mock_responses() {
    Mock_API__Invoke.apply_mock()                                                           // we need to keep doing this due to some internal ways of wallaby and KarmaJS (which would lost the mock)

    set_mock_response('/ping', 'GET', { success: true, data: { status: 'pong' }})

    // Setup success responses
    set_mock_response(`/api/user-data/files/file-contents?file_id=${MOCK_FILE_ID}`                           , 'GET', { data: { file_bytes__base64: btoa(MOCK_CONTENT) , file_data : MOCK_FILE_DATA }})
    set_mock_response(`/api/user-data/files/file-contents?file_id=invalid-file`                              , 'GET', { data: {}   })                                      // Missing file_bytes__base64
    set_mock_response('/api/user-data/files/update-file'                                                     , 'PUT', { success: true, data   : { status: 'updated'    }})
    set_mock_response(`/api/user-data/files/file-versions?file_id=${MOCK_FILE_ID}`                           , 'GET', { data: MOCK_VERSIONS                             })
    set_mock_response(`/api/user-data/files/file-versions?file_id=empty-versions`                            , 'GET', { data: null })                                      // Will trigger the || [] fallback
    set_mock_response(`/api/user-data/files/file-bytes?file_id=${MOCK_FILE_ID}&version_id=${MOCK_VERSION_ID}`, 'GET', { data: { file_bytes__base64: btoa(MOCK_CONTENT) }})
    set_mock_response(`/api/user-data/files/file-bytes?file_id=${MOCK_FILE_ID}&version_id=invalid-version`   , 'GET', { data: {}   })                                      // Missing file_bytes__base64

    set_mock_response(`/api/user-session/session/session-details?session_id=${MOCK_USER_SESSION_ID}`         , 'GET' , MOCK_USER_SESSION    )
    set_mock_response(`/api/user-session/session/session-details?session_id=${MOCK_PERSONA_1_SESSION_ID}`    , 'GET' , MOCK_PERSONA_1_SESSION)
    set_mock_response(`/api/user-session/session/session-details?session_id=${MOCK_PERSONA_2_SESSION_ID}`    , 'GET' , MOCK_PERSONA_2_SESSION)
    set_mock_response('/api/user-session/session/current-session'                                            , 'GET' , MOCK_USER_SESSION   )

    set_mock_response(`/api/user-session/guest/login-as-persona?persona_id=${MOCK_PERSONA_1_SESSION_ID  }`   , 'POST', MOCK__API_RESPONSE__OK__LOGIN_AS_PERSONA   )
    set_mock_response(`/api/user-session/guest/login-as-persona?persona_id=${MOCK_PERSONA_2_SESSION_ID  }`   , 'POST', MOCK__API_RESPONSE__OK__LOGIN_AS_PERSONA   )
    set_mock_response(`/api/user-session/guest/login-as-persona?persona_id=${MOCK_PERSONA_BAD_SESSION_ID}`   , 'POST', MOCK__API_RESPONSE__FAIL__LOGIN_AS_PERSONA )
    set_mock_response('/api/user-session/guest/logout-persona'                                               , 'POST', { success: true }   )
    set_mock_response('/api/user-session/guest/logout-all'                                                   , 'POST', { success: true }   )

    set_mock_response(`/markdown/static_content/data-file?path=${MOCK_MENU_DATA_FILE}`                       , 'GET', MOCK_MENU_DATA            )
    set_mock_response(`/markdown/render/markdown-file-to-html-and-metadata?path=${MOCK_CONTENT_PATH}`        , 'GET', MOCK_MARKDOWN_RESPONSE    )

    set_mock_response(MOCK_SERVER_REQUESTS_API_PATH, 'GET', MOCK_SERVER_REQUESTS_DATA )
    set_mock_response(MOCK_CONFIG_PATH             , 'GET', MOCK_CONFIG_DATA          )


}

// Helper function to create base64 content of any size
// export function create_mock_file_content(size_kb = 1) {
//     const chunk = 'x'.repeat(1024)  // 1KB of data
//     return chunk.repeat(size_kb)
// }

export function add_padding_to_string(input, padding = 4) {
    const pad = ' '.repeat(padding); // Generate the padding
    return input
        .split('\n')                 // Split string into lines
        .map(line => pad + line)     // Add padding to each line
        .join('\n');                 // Join lines back into a string
}

export function add_mock_markdown_path(path, content=MOCK_RAW_HTML, metadata=MOCK_MARKDOWN_METADATA) {
    Mock_API__Invoke.apply_mock()
    set_mock_response(`${CBR__Paths.API__MARKDOWN_RENDER}?path=${path}`, 'GET', { html: content, metadata: metadata })
}