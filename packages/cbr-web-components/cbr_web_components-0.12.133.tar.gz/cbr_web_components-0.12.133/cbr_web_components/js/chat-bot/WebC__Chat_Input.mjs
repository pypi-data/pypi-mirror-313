import Events__Utils      from "../events/Events__Utils.mjs";
import Web_Component      from "../core/Web_Component.mjs";
import Tag                from "../core/Tag.mjs";
import WebC__Form_Input   from "./WebC__Form_Input.mjs";       // used in .build()

export default class WebC__Chat_Input extends Web_Component {

    constructor() {
        super();
        this.events_utils = new Events__Utils()
        this.channels.push('WebC__Chat_Input')
    }

    // Web_Component overrides

    apply_css() {
        this.add_css_rules(this.css_rules())
    }

    add_event_listeners() {
        this.events_utils.events_receive.add_event_listener('keydown', this.channel, this.on_input_keydown)
        this.events_utils.events_receive.add_event_listener('paste'  , this.channel, this.process_paste    )


        this.bound_on_action_button   = this.on_action_button  .bind(this)                  // Create bound versions of handlers
        this.bound_on_clear_button    = this.on_clear_button   .bind(this)                  // that we can reference later on the removeEventListener
        this.bound_on_prompt_sent     = this.on_prompt_sent    .bind(this)
        this.bound_on_stream_complete = this.on_stream_complete.bind(this)

        this.action_button.addEventListener('click'         , this.bound_on_action_button  )    // Use bound handlers
        this.clear_button.addEventListener ('click'         , this.bound_on_clear_button   )
        window.addEventListener           ('promptSent'     , this.bound_on_prompt_sent    )
        window.addEventListener           ('streamComplete' , this.bound_on_stream_complete)
    }

    remove_event_listeners() {
        this.events_utils.events_receive.remove_all_event_listeners()
        this.action_button.removeEventListener('click'         , this.bound_on_action_button  )    // Remove using same
        this.clear_button.removeEventListener ('click'         , this.bound_on_clear_button   )    // bound references
        window.removeEventListener           ('promptSent'     , this.bound_on_prompt_sent    )
        window.removeEventListener           ('streamComplete' , this.bound_on_stream_complete)
    }

    async add_web_components() {
        this.add_web_component_to('.form-input', WebC__Form_Input, {channel: this.channel, webc_id:"webc-form-input"})
    }

    // other methods


    // setup_upload_button() {
    //     const element = this.query_selector('#file-input')
    //     //window.element = element
    //     element.addEventListener('change', () => {
    //           var reader = new FileReader();
    //           reader.onloadend = () => {
    //                 var base64String = reader.result.replace('data:', '').replace(/^.+,/, '');
    //                 //console.log(`got image of size ${base64String.length}`)
    //                 const image_prefix = 'data:image/png;base64,'
    //                 this.displayImage(image_prefix + base64String);
    //           }
    //           reader.readAsDataURL(element.files[0]);
    //         });
    //
    // }

    input_images_urls() {
        const images_urls = []
        if (this.images.children.length) {
            for (let image of this.images.children) {
                images_urls.push(image.src)
            }
        }
        return images_urls
    }

    send_user_message_event() {
        const user_prompt = this.input.value + ''
        const images = this.input_images_urls()
        const event_detail = {"user_prompt": user_prompt, 'images': images, 'channel': this.channel}
        this.event_dispatch('new_input_message', event_detail)
        this.input.value = ''
        this.images.innerHTML  =''
    }

    on_input_keydown = (event) =>{
        let keyboard_event = event.event_data?.keyboard_event
        let key            = keyboard_event?.key || keyboard_event?._key        //todo: see if there is a better way to set the key value (using ._key because it is not possible to set KeyboardEvent.key, due to it only having a getter)
        let shift_key      = keyboard_event.shiftKey                            // don't trigger the event when the shift key is also pressed
        if (key === "Enter") {
            if (this.input.value === '') {
                keyboard_event.preventDefault();
                return;
            }
            if (!shift_key) {
                this.send_user_message_event()
            }
        }
    }


    set_action_button(mode){
        if (mode==='stop') {
            this.action_button.innerHTML             = 'stop'
            this.action_button.style.backgroundColor = 'black'
        }
        else {
            this.action_button.innerHTML             = 'send'
            this.action_button.style.backgroundColor = '#007bff'
        }
    }

    // set_input_value(value)  {
    //     console.log('[WebC__Chat_Input] Setting value: ' + value)
    // }

    on_action_button() {
        if (this.action_button.innerHTML==='stop') {
            this.set_action_button('start')
            this.send_to_channel("stop_stream", {})
        }
        else {
            if (this.input.value.trim() !== '') {
                this.set_action_button('stop')
                this.send_user_message_event()
            }
        }
    }

    on_clear_button() {
        this.send_to_channel('clear_messages', {})
    }

    async on_prompt_sent(event){
        this.set_action_button('stop')
        this.input.disabled = true
    }

    async on_stream_complete(event) {
        this.set_action_button('send')
        this.input.disabled = false
    }

    send_to_channel(event_name, event_data) {
        event_data.channel = this.channel
        this.event_dispatch(event_name, event_data)
    }

    event_dispatch(event_name, detail) {
        const event_data = {
            bubbles: true,                         // allows the event to bubble up through the DOM
            composed: true,                         // allows the event to cross shadow DOM boundaries
            detail: detail
        }
        this.dispatchEvent(new CustomEvent(event_name, event_data))
    }

    process_paste = async  (event) =>{
        let paste_event = event.event_data?.paste_event

        let items;

        if (paste_event.clipboardData)                                                 { items = paste_event.clipboardData.items;                 }
        else if (paste_event.originalEvent && paste_event.originalEvent.clipboardData) { items = paste_event.originalEvent.clipboardData.items;   }
        else                                                                           { items = []                                         }


        const imageItem = Array.from(items).find(item => item.type.startsWith('image')); // Find the first image item in the paste data
        if (imageItem) {
            //console.log('got an image')
            const imageFile = imageItem.getAsFile();
            const base64Image = await this.convertImageToBase64(imageFile); // Convert the image file to Base64
            this.displayImage(base64Image)
        }
    }

    // Converts an image file to a base64-encoded string
    convertImageToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    displayImage(base64Image) {
        const style = "width:auto; height:auto; margin:10px;max-width:150px;max-height:150px"
        //"width:50px; height:50px; margin:10px"
        const img = new Tag({tag: 'img', attributes: {src: base64Image, style: style}})
        img.html_config.include_end_tag = false
        var parser = new DOMParser();
        var doc = parser.parseFromString(img.html(), 'text/html');
        var dom_img = doc.body.firstChild;


        // dom_img.onload = () => {
        //     const realWidth = dom_img.naturalWidth;
        //     const realHeight = dom_img.naturalHeight;
        //     const sizeInBytes = this.calculateImageSize(base64Image);  // Calculate the size of the base64 string in bytes
        //     //console.log(`Real Width: ${realWidth}px, Real Height: ${realHeight}px, Size: ${sizeInBytes} bytes`);    // Log the statistics or do something with them
        //     //this.resizeImage(dom_img,512)
        //
        // };
        this.images.appendChild(dom_img)
    }

    calculateImageSize(base64String) {
        const base64WithoutHeader = base64String.split(',')[1];      // Remove the header from the base64 string and calculate the size
        return base64WithoutHeader.length * 0.75;                    // Each base64 character represents 6 bits of data
    }
    //todo implement a resize image function
    // resizeImage(image, maxSize) {
    //     let width = image.naturalWidth;
    //     let height = image.naturalHeight;
    //     // Check if the image needs to be resized
    //     console.log(`resizeImage: width: ${width} height: ${height} maxSize: ${maxSize}`)
    //     if (width > maxSize || height > maxSize) {      // Calculate the new dimensions
    //         if (width > height) {                       // Landscape
    //             height *= maxSize / width;
    //             width = maxSize;
    //         } else {                                    // Portrait or square
    //             width *= maxSize / height;
    //             height = maxSize;
    //         }
    //
    //         const canvas = document.createElement('canvas');    // Create a canvas and get the context
    //         canvas.width = width;
    //         canvas.height = height;
    //         const ctx = canvas.getContext('2d');
    //         ctx.drawImage(image, 0, 0, width, height);          // Draw the resized image on the canvas
    //         const resizedDataUrl = canvas.toDataURL('image/jpeg');  // Get the resized image data
    //         image.src = resizedDataUrl;                                 // Set the image source to the resized image
    //     }
    // }

    html() {
        //todo add back this HTML mode
        // const tag = new Tag()
        // const div_chat_input = tag.clone({tag: 'div', class: 'chat-input'})
        // const div_images = tag.clone({tag: 'div', class: 'chat-images'})
        // const input_chat_input = tag.clone({
        //     tag: 'input',
        //     attributes: {type: 'text', placeholder: 'Enter a message...'}
        // })
        //
        // div_chat_input.add(div_images)
        // div_chat_input.add(input_chat_input)
        // input_chat_input.html_config.include_end_tag = false
        //return div_chat_input.html()
        const new_html = `
<div class="chat-images"></div>

<div class="chat-input">
    <!--<input id='file-input' type="file" />-->
    <!--<label for="file-input" class="file-input-label">+</label>-->
    <div class="form-input"></div>
    <!--<webc-form-input channel="${this.channel}" webc_id="webc-form-input"></webc-form-input>-->
    <!--<input id='user-prompt' type="text" placeholder="Enter a message..." autocomplete="off"/>-->
    <button id="action-button">send</button>
    <button id="clear-button">clear</button>
</div>
`
        return new_html
    }

    // properties
    get input() {                       // todo refactor this into a help method to return the result of a query selector

        let webc_form_input = this.query_selector('webc-form-input')
        return webc_form_input.text_area

        // let event_type      = 'invoke'
        // let channel         = this.channel
        // let event_data      = { method: 'query_selector', params: {'selector' : '#text_area'}}
        // let webc_form_input = this.query_selector('webc-form-input')
        // let webc_id         = this.query_selector('webc-form-input').webc_id
        // console.log(webc_id)
        // let text_area   = null
        //
        // let callback    = function(result) {
        //     text_area = result
        // }
        // let events_dispatch = this.events_utils.events_dispatch
        // events_dispatch.send_to_channel(event_type, channel, event_data, webc_id, callback)
        //
        // return text_area
    }

    get action_button() {
        return this.query_selector('#action-button')
    }

    get clear_button() {
        return this.query_selector('#clear-button')
    }

    get images() {
        return this.query_selector('.chat-images')
    }

    css_rules() {
        return { "*": {"font-family": "Verdana"},
                 ".chat-input"       : { "padding":       "10px"                         ,
                                         "background"    : "#fff"                        ,
                                         "box-shadow"    : "0 -2px 10px rgba(0,0,0,0.1)" ,
                                         "display"       : "flex"                        ,
                                         "align-items"   : "center"                      },
                 //".webc-form-input" : { "width"         : "96%"                         },
                ".form-input"        : { "width"         : "96%"                         },
                 "#file-input"       : { "opacity"       : "0px"                         ,   /* Hide the file input */
                                         "position"      : "absolute"                    ,
                                         "z-index"       : "-1"                          },  /* Place it behind the scene */
                 ".file-input-label" : { "margin-right"  : "8px"                         ,   /* Spacing between button and input box */
                                         "cursor"        : "pointer"                     },
                 "#action-button"    : { "padding"         : "10px 20px"                    ,
                                         "font-size"       : "16px"                         ,
                                         "cursor"          : "pointer"                      ,
                                         "background-color": "#007bff"                      ,
                                         "color"           : "white"                        ,
                                         "border"          : "none"                         ,
                                         "border-radius"   : "4px"                          ,
                                         "margin-left"     : "10px"                         ,
                                         "display"         : "flex"                         ,
                                         "align-items"     : "center"                       ,
                                         "justify-content" : "center"                      },
                 "#clear-button"     : { "padding"         : "10px 20px"                    ,
                                         "background-color": "#808080"                        ,
                                         "border"          : "none"                         ,
                                         "color"           : "white"                        ,
                                         "border-radius"   : "4px"                          ,
                                         "margin-left"     : "10px"                         ,
                                         "font-size"       : "16px"                         ,
                                         "cursor"          : "pointer"                      },
        }
    }
}

WebC__Chat_Input.define()



//
//     // Display the image in the UI
//     displayImage(base64Image);
//
//     // Create the payload for API call
//     const payload = createPayload(base64Image);
//
//     // Example of what to do with the payload (e.g., log to console)
//     console.log(payload);
//
//     // Prevent the default paste behavior
//     event.preventDefault();
//   }
// });
//

//
// // Displays the base64-encoded image in the designated <img> element
// function displayImage(base64Data) {
//     console.log('got base64data')
//     window.base64Data = base64Data
//   //const imgElement = document.getElementById('previewImage');
//   //imgElement.src = base64Data;
//   //imgElement.style.display = 'block';
// }
//
// // Creates the payload for the API call
// function createPayload(base64Image) {
//   return {
//     "model": "gpt-4-vision-preview",
//     "messages": [
//       {
//         "role": "user",
//         "content": [
//           {
//             "type": "text",
//             "text": "What’s in this image?"
//           },
//           {
//             "type": "image_url",
//             "image_url": {
//               "url": `data:image/jpeg;base64,${base64Image.substring(base64Image.indexOf(',') + 1)}`
//             }
//           }
//         ]
//       }
//     ],
//     "max_tokens": 300
//   };
// }