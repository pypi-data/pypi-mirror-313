import Web_Component   from '../../core/Web_Component.mjs';
import Div             from '../../core/Div.mjs';
import H               from '../../core/H.mjs';
import HR              from '../../core/HR.mjs';
import P               from '../../core/P.mjs';
import Text            from '../../core/Text.mjs';
import Table           from '../../core/Table.mjs';
import THead           from '../../core/THead.mjs';
import TBody           from '../../core/TBody.mjs';
import TFoot           from '../../core/TFoot.mjs';
import TR              from '../../core/TR.mjs';
import TH              from '../../core/TH.mjs';
import TD              from '../../core/TD.mjs';
import Caption         from '../../core/Caption.mjs';
import CSS__Tables     from '../CSS__Tables.mjs';
import CSS__Typography from '../CSS__Typography.mjs';

export default class WebC__CSS__Demo__Tables extends Web_Component {
    load_attributes() {
        this.css_tables = new CSS__Tables(this)
        this.css_typography = new CSS__Typography(this)
        this.apply_css = this.hasAttribute('no-css') === false
    }

    render() {
        let div_root = new Div({ id: 'tables-demo' })

        // Header
        let header = [
            new HR(),
            new Text({ value: 'Tables Demo' + (this.apply_css ? ' (with CSS)' : '') }),
            new HR()
        ]

        // Basic Table
        let h_basic = new H({ level: 2, value: 'Basic Table' })
        let basic_table = new Table({ class: 'table' }).add_elements(
            new THead().add_elements(
                new TR().add_elements(
                    new TH({ value: '#' }),
                    new TH({ value: 'First' }),
                    new TH({ value: 'Last' }),
                    new TH({ value: 'Handle' })
                )
            ),
            new TBody().add_elements(
                new TR().add_elements(
                    new TD({ value: '1' }),
                    new TD({ value: 'Mark' }),
                    new TD({ value: 'Otto' }),
                    new TD({ value: '@mdo' })
                ),
                new TR().add_elements(
                    new TD({ value: '2' }),
                    new TD({ value: 'Jacob' }),
                    new TD({ value: 'Thornton' }),
                    new TD({ value: '@fat' })
                ),
                new TR().add_elements(
                    new TD({ value: '3' }),
                    new TD({ value: 'Larry' }),
                    new TD({ value: 'Bird' }),
                    new TD({ value: '@twitter' })
                )
            )
        )

        // Table Variants
        let h_variants = new H({ level: 2, value: 'Table Variants' })
        let variants_table = new Table({ class: 'table table-striped table-hover table-bordered' }).add_elements(
            new Caption({ value: 'Table with striped rows, hover effect, and borders' }),
            new THead().add_elements(
                new TR().add_elements(
                    new TH({ value: '#' }),
                    new TH({ value: 'Status' }),
                    new TH({ value: 'Project' }),
                    new TH({ value: 'Progress' })
                )
            ),
            new TBody().add_elements(
                new TR({ class: 'table-success' }).add_elements(
                    new TD({ value: '1' }),
                    new TD({ value: 'Active' }),
                    new TD({ value: 'Website' }),
                    new TD({ value: '80%' })
                ),
                new TR({ class: 'table-warning' }).add_elements(
                    new TD({ value: '2' }),
                    new TD({ value: 'Pending' }),
                    new TD({ value: 'Mobile App' }),
                    new TD({ value: '45%' })
                ),
                new TR({ class: 'table-error' }).add_elements(
                    new TD({ value: '3' }),
                    new TD({ value: 'Delayed' }),
                    new TD({ value: 'Desktop App' }),
                    new TD({ value: '20%' })
                )
            )
        )

        // Small Table
        let h_small = new H({ level: 2, value: 'Small Table' })
        let small_table = new Table({ class: 'table table-sm table-bordered' }).add_elements(
            new THead().add_elements(
                new TR().add_elements(
                    new TH({ value: '#' }),
                    new TH({ value: 'Item' }),
                    new TH({ value: 'Price' })
                )
            ),
            new TBody().add_elements(
                new TR().add_elements(
                    new TD({ value: '1' }),
                    new TD({ value: 'Coffee' }),
                    new TD({ value: '$3.50' })
                ),
                new TR().add_elements(
                    new TD({ value: '2' }),
                    new TD({ value: 'Tea' }),
                    new TD({ value: '$2.50' })
                )
            )
        )

        // Dark Table
        let h_dark = new H({ level: 2, value: 'Dark Table' })
        let dark_table = new Table({ class: 'table table-dark table-striped' }).add_elements(
            new THead().add_elements(
                new TR().add_elements(
                    new TH({ value: '#' }),
                    new TH({ value: 'Type' }),
                    new TH({ value: 'Value' })
                )
            ),
            new TBody().add_elements(
                new TR().add_elements(
                    new TD({ value: '1' }),
                    new TD({ value: 'Data 1' }),
                    new TD({ value: '500' })
                ),
                new TR().add_elements(
                    new TD({ value: '2' }),
                    new TD({ value: 'Data 2' }),
                    new TD({ value: '300' })
                )
            )
        )

        // Responsive Table
        let h_responsive = new H({ level: 2, value: 'Responsive Table' })
        let responsive_wrapper = new Div({ class: 'table-responsive' }).add_elements(
            new Table({ class: 'table' }).add_elements(
                new THead().add_elements(
                    new TR().add_elements(
                        new TH({ value: '#' }),
                        new TH({ value: 'Heading 1' }),
                        new TH({ value: 'Heading 2' }),
                        new TH({ value: 'Heading 3' }),
                        new TH({ value: 'Heading 4' }),
                        new TH({ value: 'Heading 5' })
                    )
                ),
                new TBody().add_elements(
                    new TR().add_elements(
                        new TD({ value: '1' }),
                        new TD({ value: 'Cell 1' }),
                        new TD({ value: 'Cell 2' }),
                        new TD({ value: 'Cell 3' }),
                        new TD({ value: 'Cell 4' }),
                        new TD({ value: 'Cell 5' })
                    )
                )
            )
        )

         // Header
        let h_with_colors = [
            new H({ level: 1, value: 'Variants' }),
            new P({ value: 'Use contextual classes to color tables, table rows or individual cells.' })
        ]

        // Variants Table
        let table_with_colors = new Table({ class: 'table' }).add_elements(
            new THead().add_elements(
                new TR().add_elements(
                    new TH({ value: 'Class' }),
                    new TH({ value: 'Heading' }),
                    new TH({ value: 'Heading' })
                )
            ),
            new TBody().add_elements(
                // Default row
                new TR().add_elements(
                    new TD({ value: 'Default' }),
                    new TD({ value: 'Cell' }),
                    new TD({ value: 'Cell' })
                ),
                // Primary row
                new TR({ class: 'table-primary' }).add_elements(
                    new TD({ value: 'Primary' }),
                    new TD({ value: 'Cell' }),
                    new TD({ value: 'Cell' })
                ),
                // Secondary row
                new TR({ class: 'table-secondary' }).add_elements(
                    new TD({ value: 'Secondary' }),
                    new TD({ value: 'Cell' }),
                    new TD({ value: 'Cell' })
                ),
                // Success row
                new TR({ class: 'table-success' }).add_elements(
                    new TD({ value: 'Success' }),
                    new TD({ value: 'Cell' }),
                    new TD({ value: 'Cell' })
                ),
                // Danger row
                new TR({ class: 'table-error' }).add_elements(
                    new TD({ value: 'Danger' }),
                    new TD({ value: 'Cell' }),
                    new TD({ value: 'Cell' })
                ),
                // Warning row
                new TR({ class: 'table-warning' }).add_elements(
                    new TD({ value: 'Warning' }),
                    new TD({ value: 'Cell' }),
                    new TD({ value: 'Cell' })
                ),
                // Info row
                new TR({ class: 'table-info' }).add_elements(
                    new TD({ value: 'Info' }),
                    new TD({ value: 'Cell' }),
                    new TD({ value: 'Cell' })
                ),
                // Light row
                new TR({ class: 'table-light' }).add_elements(
                    new TD({ value: 'Light' }),
                    new TD({ value: 'Cell' }),
                    new TD({ value: 'Cell' })
                ),
                // Dark row
                new TR({ class: 'table-dark' }).add_elements(
                    new TD({ value: 'Dark' }),
                    new TD({ value: 'Cell' }),
                    new TD({ value: 'Cell' })
                )
            )
        )

        let h_sales_table = [
            new H({ level: 1, value: 'Table with Footer' }),
            new P({ value: 'Example of a table with header, body, and footer sections showing sales data.' })
        ]

        // Sales Table with Footer
        let sales_table = new Table({ class: 'table table-bordered' }).add_elements(
            // Caption
            new Caption({ value: 'Monthly Sales Report' }),

            // Header
            new THead().add_elements(
                new TR().add_elements(
                    new TH({ class: 'cell-fit', value: 'Month' }),
                    new TH({ class: 'text-end', value: 'Orders' }),
                    new TH({ class: 'text-end', value: 'Revenue' }),
                    new TH({ class: 'text-end', value: 'Expenses' }),
                    new TH({ class: 'text-end', value: 'Profit' })
                )
            ),

            // Body
            new TBody().add_elements(
                new TR().add_elements(
                    new TD({ value: 'January' }),
                    new TD({ class: 'text-end', value: '45' }),
                    new TD({ class: 'text-end', value: '$15,000' }),
                    new TD({ class: 'text-end', value: '$8,000' }),
                    new TD({ class: 'text-end', value: '$7,000' })
                ),
                new TR().add_elements(
                    new TD({ value: 'February' }),
                    new TD({ class: 'text-end', value: '58' }),
                    new TD({ class: 'text-end', value: '$20,000' }),
                    new TD({ class: 'text-end', value: '$10,000' }),
                    new TD({ class: 'text-end', value: '$10,000' })
                ),
                new TR().add_elements(
                    new TD({ value: 'March' }),
                    new TD({ class: 'text-end', value: '65' }),
                    new TD({ class: 'text-end', value: '$25,000' }),
                    new TD({ class: 'text-end', value: '$12,000' }),
                    new TD({ class: 'text-end', value: '$13,000' })
                )
            ),

            // Footer with summary rows
            new TFoot({ class: 'table-group-divider' }).add_elements(
                // Quarterly Total
                new TR({ class: 'table-active' }).add_elements(
                    new TH({ value: 'Q1 Total' }),
                    new TD({ class: 'text-end weight-bold', value: '168' }),
                    new TD({ class: 'text-end weight-bold', value: '$60,000' }),
                    new TD({ class: 'text-end weight-bold', value: '$30,000' }),
                    new TD({ class: 'text-end weight-bold', value: '$30,000' })
                ),
                // Average
                new TR({ class: 'table-light' }).add_elements(
                    new TH({ value: 'Monthly Average' }),
                    new TD({ class: 'text-end', value: '56' }),
                    new TD({ class: 'text-end', value: '$20,000' }),
                    new TD({ class: 'text-end', value: '$10,000' }),
                    new TD({ class: 'text-end', value: '$10,000' })
                ),
                // Year to Date
                new TR({ class: 'table-primary' }).add_elements(
                    new TH({ value: 'YTD Performance' }),
                    new TD({ class: 'text-end', colSpan: '4', value: '25% above target' })
                )
            )
        )

        // Add all sections to root
        div_root.add_elements(...header,
                              h_basic         , basic_table        ,
                              h_variants      , variants_table     ,
                              h_small         , small_table        ,
                              h_dark          , dark_table         ,
                              h_responsive    , responsive_wrapper ,
                              ...h_with_colors, table_with_colors  ,
                              ...h_sales_table, sales_table        )

        // Apply CSS if needed
        if (this.apply_css) {
            this.css_tables.apply_framework()
            this.css_typography.apply_framework()
        }

        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Tables.define()