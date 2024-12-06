import WebC__Target_Div      from '../../../js/utils/WebC__Target_Div.mjs'
import Web_Component         from '../../../js/core/Web_Component.mjs'
import WebC__Home__Container from '../../../js/cbr/web-components/WebC__Home__Container.mjs'
import { setup_mock_responses,
         set_mock_response } from '../../../js/testing/Mock_API__Data.mjs'

const { module, test } = QUnit

const MOCK_WELCOME_CONTENT = {
    html    : '<h1>Welcome to Cyber Boardroom</h1>',
    metadata: { title: 'Welcome' }
}

const MOCK_CARD_1_CONTENT = {
    html    : '<h2>Card 1</h2><p>Content 1</p>',
    metadata: { title: 'Card 1' }
}

const MOCK_CARD_2_CONTENT = {
    html    : '<h2>Card 2</h2><p>Content 2</p>',
    metadata: { title: 'Card 2' }
}

module('WebC__Home__Container', hooks => {
    let target_div
    let container

    hooks.before(async () => {
        setup_mock_responses()

        // Setup mock responses for markdown content
        set_mock_response('https://static.dev.aws.cyber-boardroom.com/cbr-content/latest/en/web-site/home-page/welcome.md.json', 'GET', MOCK_WELCOME_CONTENT)
        set_mock_response('https://static.dev.aws.cyber-boardroom.com/cbr-content/latest/en/web-site/home-page/card-1.md.json' , 'GET', MOCK_CARD_1_CONTENT )
        set_mock_response('https://static.dev.aws.cyber-boardroom.com/cbr-content/latest/en/web-site/home-page/card-2.md.json' , 'GET', MOCK_CARD_2_CONTENT )

        target_div = WebC__Target_Div.add_to_body()
        container  = await target_div.append_child(WebC__Home__Container)
        await container.wait_for__component_ready()
    })

    hooks.after(() => {
        container .remove()
        target_div.remove()
    })

    test('constructor and inheritance', assert => {
        assert.equal(container.tagName.toLowerCase()    , 'webc-home-container'    , 'Has correct tag name'     )
        assert.equal(container.constructor.element_name , 'webc-home-container'    , 'Has correct element name' )
        assert.equal(container.constructor.name        , 'WebC__Home__Container'  , 'Has correct class name'   )

        assert.ok(container.shadowRoot                                            , 'Has shadow root'          )
        assert.ok(container.api_invoke                                           , 'Has API__Invoke'          )

        assert.ok(container instanceof Web_Component                             , 'Extends Web_Component'     )
        assert.ok(container instanceof HTMLElement                               , 'Is HTML Element'          )
    })

    test('loads and applies CSS frameworks', assert => {
        const css_rules = container.all_css_rules()

        assert.ok(Object.keys(css_rules).length > 0                             , 'Has CSS rules'            )
        assert.ok(css_rules['.home-container']                                  , 'Has container styles'     )
        assert.ok(css_rules['.video-card']                                      , 'Has video card styles'    )
        assert.ok(css_rules['.cards-section']                                   , 'Has cards section styles' )
    })

    test('renders layout structure correctly', async assert => {
        const home_container = container.query_selector('.home-container')
        assert.ok(home_container                                                , 'Main container exists'    )

        // Welcome section
        const welcome = container.query_selector('.welcome-section')
        assert.ok(welcome                                                       , 'Welcome section exists'   )
        assert.ok(welcome.classList.contains('card')                           , 'Welcome has card class'   )

        // Videos section
        const videos = container.query_selector_all('.video-card')
        assert.equal(videos.length                     , 2                      , 'Has two video sections'   )
        assert.ok(videos[0].querySelector('.video-title')                      , 'First video has title'    )
        assert.ok(videos[0].querySelector('.video-player')                     , 'First video has player'   )

        // Cards section
        const cards = container.query_selector_all('.cards-section')
        assert.equal(cards.length                      , 2                      , 'Has two card sections'    )
        assert.ok(cards[0].classList.contains('card-1')                        , 'First card has correct class')
        assert.ok(cards[1].classList.contains('card-2')                        , 'Second card has correct class')
    })

    test('creates video section correctly', async assert => {
        const title = 'Test Video'
        const url   = 'https://test-url.com/video.mp4'

        const video_section = container.create_video_section(title, url)
        const dom           = video_section.dom_create()

        assert.ok(dom.classList.contains('video-card')                         , 'Has video-card class'     )
        assert.ok(dom.classList.contains('card')                               , 'Has card class'           )

        const title_element = dom.querySelector('.video-title')
        assert.equal(title_element.textContent        , title                  , 'Shows correct title'      )

        const video = dom.querySelector('video')
        assert.ok(video                                                        , 'Video element exists'     )
        assert.equal(video.querySelector('source').getAttribute('src'), url    , 'Has correct video URL'   )
    })

    test('adds web components correctly', async assert => {
        const welcome_component = container.query_selector('.welcome-section webc-api-markdown-to-html')
        const card_1_component  = container.query_selector('.card-1 webc-markdown-card')
        const card_2_component  = container.query_selector('.card-2 webc-markdown-card')

        assert.ok(welcome_component                                            , 'Welcome component added'   )
        assert.ok(card_1_component                                             , 'Card 1 component added'    )
        assert.ok(card_2_component                                             , 'Card 2 component added'    )

        assert.equal(welcome_component.getAttribute('content-path'),
                    'en/web-site/home-page/welcome.md'                         , 'Welcome has correct path'  )
        assert.equal(card_1_component.getAttribute('content-path'),
                    'en/web-site/home-page/card-1.md'                          , 'Card 1 has correct path'   )
        assert.equal(card_2_component.getAttribute('content-path'),
                    'en/web-site/home-page/card-2.md'                          , 'Card 2 has correct path'   )
    })

    test('handles responsive design', async assert => {
        const css_rules = container.css_rules()
        const mobile_rules = css_rules['@media (max-width: 768px)']

        assert.ok(mobile_rules                                                 , 'Has mobile breakpoint'    )
        assert.ok(mobile_rules['.card']                                       , 'Has mobile card styles'   )
        assert.equal(mobile_rules['.card'].marginBottom, '1rem'               , 'Correct mobile margin'    )
    })
})