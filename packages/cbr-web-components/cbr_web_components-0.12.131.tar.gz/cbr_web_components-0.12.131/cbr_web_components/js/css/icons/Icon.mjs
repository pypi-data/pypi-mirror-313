import Icon__Mappings from './Icon__Mappings.mjs'
import Span           from '../../core/Span.mjs'

export default class Icon extends Span {
    constructor({icon,  size,  color,  rotate, spin = false,  pulse = false, spacing, ...kwargs} = {}) {

        kwargs.class = `icon ${kwargs.class || ''}`                     // Set up base class name
        super(kwargs)                                                   // Initialize Span with our kwargs

        if (icon) {
            this.value = Icon__Mappings.getIcon(icon)                   // Add icon from Icon__Mappings
            this.attributes = {                                         // Merge with existing attributes
                ...this.attributes || {},                               // Preserve existing attributes
                icon: icon                                              // Add icon attribute
            }
        }
        if (size    ) { this.add_class(`icon-${size}`           ) }     // Handle size
        if (color   ) { this.add_class(`icon-${color}`          ) }     // Handle color
        if (rotate  ) { this.add_class(`icon-rotate-${rotate}`  ) }     // Handle rotation
        if (spin    ) { this.add_class('icon-spin'              ) }     // Handle spin
        if (pulse   ) { this.add_class('icon-pulse'             ) }     // Handle pulse
        if (spacing ) { this.add_class(`icon-spacing-${spacing}`) }     // Handle spacing
    }
}