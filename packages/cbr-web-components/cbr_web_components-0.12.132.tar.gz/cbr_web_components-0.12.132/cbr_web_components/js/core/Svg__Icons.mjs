import Raw_Html from "./Raw_Html.mjs";

export default class Svg__Icons{
    constructor() {
    }

    picture_as_pdf(...attributes) {
        const svg_code = this.apply_attributes_to_svg_code(Svg__Icons.picture_as_pdf,...attributes)
        const span_svg = new Raw_Html({class:'icon-svg picture-as-pdf', value:svg_code})
        return span_svg
    }

    screenshot_monitor(...attributes) {
        const svg_code = this.apply_attributes_to_svg_code(Svg__Icons.screenshot_monitor,...attributes)
        return new Raw_Html({class:'icon-svg screenshot-monitor', value:svg_code})
    }

    apply_attributes_to_svg_code(svg_code, attributes) {
        const svg_element = new DOMParser().parseFromString(svg_code, 'image/svg+xml').documentElement;

        for (let [key, value] of Object.entries(attributes || {})) {          // Apply the attributes to the SVG element
            svg_element.setAttribute(key, value);
        }

        return new XMLSerializer().serializeToString(svg_element);       // Return the updated SVG as a string
    }

    icon(icon_name, ...attributes) {
        const svg_code_raw = Svg__Icons[icon_name]
        if (svg_code_raw) {
            const icon_class_name = icon_name.replace(/_/g, '-').toLowerCase()
            const classes = `icon-svg ${icon_class_name}`
            const svg_code = this.apply_attributes_to_svg_code(svg_code_raw, attributes)
            return new Raw_Html({class:classes, value:svg_code})
        }

    }
    //icons SVG from: https://fonts.google.com/icons
    static picture_as_pdf     = `<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#5f6368"><path d="M360-460h40v-80h40q17 0 28.5-11.5T480-580v-40q0-17-11.5-28.5T440-660h-80v200Zm40-120v-40h40v40h-40Zm120 120h80q17 0 28.5-11.5T640-500v-120q0-17-11.5-28.5T600-660h-80v200Zm40-40v-120h40v120h-40Zm120 40h40v-80h40v-40h-40v-40h40v-40h-80v200ZM320-240q-33 0-56.5-23.5T240-320v-480q0-33 23.5-56.5T320-880h480q33 0 56.5 23.5T880-800v480q0 33-23.5 56.5T800-240H320Zm0-80h480v-480H320v480ZM160-80q-33 0-56.5-23.5T80-160v-560h80v560h560v80H160Zm160-720v480-480Z"/></svg>`
    static screenshot_monitor = `<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#5f6368"><path d="M600-320h160v-160h-60v100H600v60ZM200-560h60v-100h100v-60H200v160Zm120 440v-80H160q-33 0-56.5-23.5T80-280v-480q0-33 23.5-56.5T160-840h640q33 0 56.5 23.5T880-760v480q0 33-23.5 56.5T800-200H640v80H320ZM160-280h640v-480H160v480Zm0 0v-480 480Z"/></svg>`
    // icons SVG from: https://www.svgrepo.com/
    static user_profile = `<?xml version="1.0" encoding="utf-8"?><!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                            <svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="24" height="24" fill="white"/><path fill-rule="evenodd" clip-rule="evenodd" d="M2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12ZM11.9999 6C9.79077 6 7.99991 7.79086 7.99991 10C7.99991 12.2091 9.79077 14 11.9999 14C14.209 14 15.9999 12.2091 15.9999 10C15.9999 7.79086 14.209 6 11.9999 6ZM17.1115 15.9974C17.8693 16.4854 17.8323 17.5491 17.1422 18.1288C15.7517 19.2966 13.9581 20 12.0001 20C10.0551 20 8.27215 19.3059 6.88556 18.1518C6.18931 17.5723 6.15242 16.5032 6.91351 16.012C7.15044 15.8591 7.40846 15.7251 7.68849 15.6097C8.81516 15.1452 10.2542 15 12 15C13.7546 15 15.2018 15.1359 16.3314 15.5954C16.6136 15.7102 16.8734 15.8441 17.1115 15.9974Z" fill="#323232"/></svg>`
}