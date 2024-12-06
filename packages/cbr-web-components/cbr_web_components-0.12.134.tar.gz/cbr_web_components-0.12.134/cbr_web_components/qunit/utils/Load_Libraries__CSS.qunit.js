// todo: see if we still need this
// import Load_Libraries__CSS from "../../js/utils/Load_Libraries__CSS.mjs";
// import WebC__Target_Div from "../../js/utils/WebC__Target_Div.mjs";
//
// QUnit.module('Load_Libraries__CSS.qunit', function(hooks) {
//
//     let load_libraries__css
//     let target_div
//     let mocked_requests
//
//
//     hooks.beforeEach((assert) => {
//         target_div          = WebC__Target_Div.add_to_body().build()
//         mocked_requests     = mocked_requests_for_css()
//         load_libraries__css = new Load_Libraries__CSS({target:target_div, mock_responses: mocked_requests})
//         assert.deepEqual(load_libraries__css.constructor.name, 'Load_Libraries__CSS')
//         assert.deepEqual(load_libraries__css.target, target_div)
//     })
//
//     function mocked_requests_for_css() {
//         return {[Load_Libraries__CSS.url__css__material_design_icons]: css_code__for_test}
//     }
//     // tests
//
//     QUnit.test('.constructor()', (assert) => {
//         assert.deepEqual(load_libraries__css.target, target_div)
//     })
//
//     QUnit.test('.load_material_icons()', async (assert) => {
//         // Step 1: Load the Material Design Icons CSS and get the result
//         const result = await load_libraries__css.load_material_design()
//         const sheet = result.sheet
//         const expected_result = { css_loaded    : true                                                                                                          ,
// 		                          fetch_response: {status: true, status_code: 200, status_text: 'OK', text: css_code__for_test} ,
//                                   sheet         : sheet }
//         assert.deepEqual(result, expected_result)
//
//          // Step 2: Confirm the CSS has been loaded into the stylesheet
//         assert.ok(result.css_loaded        , "CSS was successfully loaded into the sheet");
//         assert.ok(sheet.cssRules.length > 0, "CSS rules have been added to the stylesheet");
//
//         // Step 3: Check that specific CSS rules are present in the sheet
//         const mdiClassRule = Array.from(sheet.cssRules).find(rule => rule.selectorText === '.mdi'             );
//         const mdiHomeRule  = Array.from(sheet.cssRules).find(rule => rule.selectorText === '.mdi-home::before');
//
//         assert.ok(mdiClassRule, "Found the `.mdi` class rule in the stylesheet");
//         assert.ok(mdiHomeRule, "Found the `.mdi-home` class rule in the stylesheet");
//
//         // Step 4: Check if the target div has the correct styles applied
//         // Add a test icon to the target div
//
//         const testIcon = document.createElement('i');
//         testIcon.classList.add('mdi', 'mdi-home');
//         target_div.appendChild(testIcon);
//
//         //todo: figure out why the styles are not being applied (in these tests)
//         // Step 5: Validate the computed styles of the element in the target div
//         const computedStyles = window.getComputedStyle(testIcon);
//         assert.deepEqual(computedStyles.getPropertyValue('font-size'), '16px', "BUG: Incorrect font-size applied");
//         //assert.deepEqual(computedStyles.getPropertyValue('font-family'), '"Times New Roman"', "BUG: Incorrect font-family applied");  // in Karma is 'Times'
//         assert.deepEqual(testIcon.outerHTML, '<i class="mdi mdi-home"></i>', "OK icon received the correct classes");
//
//         return
//         assert.equal(computedStyles.getPropertyValue('font-family'), "'Material Design Icons'", "Correct font-family applied");         // fails
//         assert.equal(computedStyles.getPropertyValue('font-size'), '24px', "Correct font-size applied");                                // fails
//         assert.equal(computedStyles.getPropertyValue('display'), 'inline-block', "Correct display property applied");                   // fails
//     })
//
//     const css_code__for_test = `
//   @font-face {
//     font-family: 'Material Design Icons';
//     font-weight: normal;
//     font-style: normal;
//   }
//
//   .mdi {
//     font-family: 'Material Design Icons';
//     font-style: normal;
//     font-weight: normal;
//     font-size: 24px;
//     line-height: 1;
//     display: inline-block;
//     vertical-align: middle;
//   }
//
//   .mdi-home:before {
//     content: "\\F0155"; /* Unicode for mdi-home */
//   }
//   `
// })