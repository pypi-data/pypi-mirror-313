import API__Invoke from '../../data/API__Invoke.mjs'
import {CBR__Paths} from "../CBR__Paths.mjs";

export default class API__Markdown {

    constructor() {
        this.api_invoke = new API__Invoke()
    }

    // API endpoints
    //static url__markdown_render = '/markdown/render/markdown-file-to-html-and-metadata'

    async get_data__markdown_page(content_path) {
        try {
            const url      =`${CBR__Paths.API__MARKDOWN_RENDER}?path=${content_path}`
            const response = await this.api_invoke.invoke_api(url, 'GET')
            return {
                html     : response?.html       ,    // Rendered HTML content
                metadata : response?.metadata   ,    // Metadata from markdown
                success  : true                      // API call status         // todo: add better support error detection which in some cases is provided inside the metadata
            }
        } catch (error) {
            return {
                html     : '<p>Error loading content</p>'              ,    // Fallback content
                metadata : { title: 'Error'              }             ,    // Fallback metadata
                success  : false                                           // Error status
            }
        }
    }

    async get_data__athena_examples() {
        try {
            const url = `${CBR__Paths.API__MARKDOWN_DATA_FILE}?path=${CBR__Paths.FILE__DATA__SITE__ATHENA__QUESTIONS}`
            return await this.api_invoke.invoke_api(url, 'GET')
        } catch (error) {
            //console.error('Error loading examples:', error)
            return {
                title   : 'Prompt examples'                                            ,
                examples: [ 'Hello, what do you know about me?'                        ,
                            'What questions should I ask my CISO?'                     ,
                            'What is DORA?'                                            ,
                            'What are my legal responsibilities?'                      ,
                            'What is the best way to learn more about cyber security?' ]
            }
        }
    }
}