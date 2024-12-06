import Raw_Html from "../../core/Raw_Html.mjs";

export default class CBR__Route__Handler {

    base_path    = '/'
    default_page = 'home/index'

    constructor(component, base_path) {
        this.component = component
        this.add_event_listeners()
    }

    add_event_listeners() {
        window.addEventListener  ('popstate', this.handle_pop_state       .bind(this))        // Listen for popstate events (browser back/forward)
        document.addEventListener('click'   , this.handle_navigation_click.bind(this))        // Intercept navigation clicks
    }

    async handle_pop_state(event) {
        await this.handle_route(window.location.pathname)
    }

    async handle_navigation_click(event) {
        const link = this.find_link_element(event)

        if (!this.should_handle_link(link)) { return }

        event.preventDefault()
        await this.process_link(link)
    }

    async handle_route(path) {
        const contentEl = this.component.query_selector('#content')
        if (!contentEl) return

        const placeholder = contentEl
        const routePath   = path.replace(this.base_path, '').replace(/^\/+/, '') || this.default_page      // Get the route path without the base path

        const pathSegments = routePath.split('/').filter(segment => segment)                        // Create navigation classes from the path segments
        const navClasses   = pathSegments.map((segment, index) => {
            const subPath  = pathSegments.slice(0, index + 1).join('-')                                     // Build cumulative path for each level
            return `nav-${subPath}`
        })

        const div_classes = `nav-content ${navClasses.join(' ')}`
        const wrapperDiv  = new Raw_Html({class: div_classes })                                              // Create wrapper div with all navigation classes


        try {
            const content         = await this.component.routeContent.fetch_content(routePath)
            wrapperDiv.raw_html   = content
            placeholder.innerHTML = wrapperDiv.html()
        } catch (error) {
            //console.error('Error loading content:', error)
            wrapperDiv.value = '<div class="content-error">Error loading content. Please try again.</div>'          // todo: refactor to use Div
            placeholder.innerHTML = wrapperDiv.html()
        }
    }

    find_link_element(event) {
        const path = event.composedPath()
        return path.find(el => el.tagName === 'A')
    }

    should_handle_link(link) {
        if (!link) { return false }

        const base_url = window.location.origin + this.base_path
        return link.href.startsWith(base_url)
    }

    async process_link(link) {
        const target_type     = link.getAttribute('data-target-type'   )
        const component_path  = link.getAttribute('data-component-path')
        const navigation_path = this.extract_navigation_path(link)

        this.update_browser_path(navigation_path)

        switch (target_type) {
            case 'web_component':
                const component_name = link.getAttribute('data-component')
                if (component_name) {
                    await this.load_component(component_name, component_path)
                    return
                }
                console.error('Web component target specified but no component name found')
                break

            case 'link':
                await this.navigate(navigation_path)
                break

            default:
                //console.warn(`Unknown target type: ${target_type}, defaulting to link navigation`)
                await this.navigate(navigation_path)
        }

    }
    extract_navigation_path(link) {
        const base_url = window.location.origin + this.base_path
        return link.href.replace(base_url, '')
    }

    async navigate(path) {
        await this.handle_route(path)
    }

    async load_component(component_name, component_path) {
        const contentEl = this.component.query_selector('#content')
        if (!contentEl) return

        try {
            // First import the module (this executes the .define())
            const base_path     = '/web_components/js/cbr/web-components/'
            const path          = `${base_path}${component_path}${component_name}.mjs`
            const module        = await this.import_module(path)

            // Clear existing content
            contentEl.innerHTML = ''

            // Convert WebC class name to kebab-case for HTML element
            const tag_name     = component_name.replace(/__/g, '-')
                                               .replace(/_/g, '-')
                                               .toLowerCase()
                                               .replace(/-+/g, '-')
            // Create and add the web component
            const component = document.createElement(tag_name)
            contentEl.appendChild(component)

        } catch (error) {
            //console.error('Error loading component:', error)
            contentEl.innerHTML = '<div class="content-error">Error loading component. Please try again.</div>'
        }
    }

    /* istanbul ignore next */
    async import_module(path) {
        return await import(path)
}

    update_browser_path(path) {
        window.history.pushState({}, '', `${this.base_path}${path}`)
    }
    set_base_path(base_path) {
        this.base_path = base_path
    }
}