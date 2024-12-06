"use strict";
(self["webpackChunk_JUPYTERLAB_CORE_OUTPUT"] = self["webpackChunk_JUPYTERLAB_CORE_OUTPUT"] || []).push([[9672],{

/***/ 99672:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {


// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  o: () => (/* binding */ Search_Search)
});

// EXTERNAL MODULE: ../node_modules/@jupyter/web-components/dist/esm/jupyter-design-system.js + 1 modules
var jupyter_design_system = __webpack_require__(68866);
// EXTERNAL MODULE: ../node_modules/tslib/tslib.es6.mjs
var tslib_es6 = __webpack_require__(82616);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/components/attributes.js
var attributes = __webpack_require__(98332);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/node_modules/tslib/tslib.es6.js
var tslib_tslib_es6 = __webpack_require__(95185);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/dom.js
var dom = __webpack_require__(91211);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/observation/observable.js
var observable = __webpack_require__(92221);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/patterns/aria-global.js
var aria_global = __webpack_require__(14869);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/patterns/start-end.js
var start_end = __webpack_require__(52865);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/utilities/apply-mixins.js
var apply_mixins = __webpack_require__(89155);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/form-associated/form-associated.js
var form_associated = __webpack_require__(940);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/foundation-element/foundation-element.js
var foundation_element = __webpack_require__(50755);
;// CONCATENATED MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/search/search.form-associated.js


class _Search extends foundation_element/* FoundationElement */.I {
}
/**
 * A form-associated base class for the {@link @microsoft/fast-foundation#(Search:class)} component.
 *
 * @internal
 */
class FormAssociatedSearch extends (0,form_associated/* FormAssociated */.Um)(_Search) {
    constructor() {
        super(...arguments);
        this.proxy = document.createElement("input");
    }
}

;// CONCATENATED MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/search/search.js





/**
 * A Search Custom HTML Element.
 * Based largely on the {@link https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/search | <input type="search" /> element }.
 *
 * @slot start - Content which can be provided before the search input
 * @slot end - Content which can be provided after the search clear button
 * @slot - The default slot for the label
 * @slot close-button - The clear button
 * @slot close-glyph - The clear glyph
 * @csspart label - The label
 * @csspart root - The element wrapping the control, including start and end slots
 * @csspart control - The element representing the input
 * @csspart clear-button - The button to clear the input
 *
 * @public
 */
class Search extends FormAssociatedSearch {
    readOnlyChanged() {
        if (this.proxy instanceof HTMLInputElement) {
            this.proxy.readOnly = this.readOnly;
            this.validate();
        }
    }
    autofocusChanged() {
        if (this.proxy instanceof HTMLInputElement) {
            this.proxy.autofocus = this.autofocus;
            this.validate();
        }
    }
    placeholderChanged() {
        if (this.proxy instanceof HTMLInputElement) {
            this.proxy.placeholder = this.placeholder;
        }
    }
    listChanged() {
        if (this.proxy instanceof HTMLInputElement) {
            this.proxy.setAttribute("list", this.list);
            this.validate();
        }
    }
    maxlengthChanged() {
        if (this.proxy instanceof HTMLInputElement) {
            this.proxy.maxLength = this.maxlength;
            this.validate();
        }
    }
    minlengthChanged() {
        if (this.proxy instanceof HTMLInputElement) {
            this.proxy.minLength = this.minlength;
            this.validate();
        }
    }
    patternChanged() {
        if (this.proxy instanceof HTMLInputElement) {
            this.proxy.pattern = this.pattern;
            this.validate();
        }
    }
    sizeChanged() {
        if (this.proxy instanceof HTMLInputElement) {
            this.proxy.size = this.size;
        }
    }
    spellcheckChanged() {
        if (this.proxy instanceof HTMLInputElement) {
            this.proxy.spellcheck = this.spellcheck;
        }
    }
    /**
     * @internal
     */
    connectedCallback() {
        super.connectedCallback();
        this.validate();
        if (this.autofocus) {
            dom/* DOM */.SO.queueUpdate(() => {
                this.focus();
            });
        }
    }
    /** {@inheritDoc (FormAssociated:interface).validate} */
    validate() {
        super.validate(this.control);
    }
    /**
     * Handles the internal control's `input` event
     * @internal
     */
    handleTextInput() {
        this.value = this.control.value;
    }
    /**
     * Handles the control's clear value event
     * @public
     */
    handleClearInput() {
        this.value = "";
        this.control.focus();
        this.handleChange();
    }
    /**
     * Change event handler for inner control.
     * @remarks
     * "Change" events are not `composable` so they will not
     * permeate the shadow DOM boundary. This fn effectively proxies
     * the change event, emitting a `change` event whenever the internal
     * control emits a `change` event
     * @internal
     */
    handleChange() {
        this.$emit("change");
    }
}
(0,tslib_tslib_es6/* __decorate */.gn)([
    (0,attributes/* attr */.Lj)({ attribute: "readonly", mode: "boolean" })
], Search.prototype, "readOnly", void 0);
(0,tslib_tslib_es6/* __decorate */.gn)([
    (0,attributes/* attr */.Lj)({ mode: "boolean" })
], Search.prototype, "autofocus", void 0);
(0,tslib_tslib_es6/* __decorate */.gn)([
    attributes/* attr */.Lj
], Search.prototype, "placeholder", void 0);
(0,tslib_tslib_es6/* __decorate */.gn)([
    attributes/* attr */.Lj
], Search.prototype, "list", void 0);
(0,tslib_tslib_es6/* __decorate */.gn)([
    (0,attributes/* attr */.Lj)({ converter: attributes/* nullableNumberConverter */.Id })
], Search.prototype, "maxlength", void 0);
(0,tslib_tslib_es6/* __decorate */.gn)([
    (0,attributes/* attr */.Lj)({ converter: attributes/* nullableNumberConverter */.Id })
], Search.prototype, "minlength", void 0);
(0,tslib_tslib_es6/* __decorate */.gn)([
    attributes/* attr */.Lj
], Search.prototype, "pattern", void 0);
(0,tslib_tslib_es6/* __decorate */.gn)([
    (0,attributes/* attr */.Lj)({ converter: attributes/* nullableNumberConverter */.Id })
], Search.prototype, "size", void 0);
(0,tslib_tslib_es6/* __decorate */.gn)([
    (0,attributes/* attr */.Lj)({ mode: "boolean" })
], Search.prototype, "spellcheck", void 0);
(0,tslib_tslib_es6/* __decorate */.gn)([
    observable/* observable */.LO
], Search.prototype, "defaultSlottedNodes", void 0);
/**
 * Includes ARIA states and properties relating to the ARIA textbox role
 *
 * @public
 */
class DelegatesARIASearch {
}
(0,apply_mixins/* applyMixins */.e)(DelegatesARIASearch, aria_global/* ARIAGlobalStatesAndProperties */.v);
(0,apply_mixins/* applyMixins */.e)(Search, start_end/* StartEnd */.hW, DelegatesARIASearch);

// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/templating/template.js + 3 modules
var template = __webpack_require__(25269);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/templating/slotted.js
var slotted = __webpack_require__(17832);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/templating/ref.js
var ref = __webpack_require__(62564);
;// CONCATENATED MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/utilities/whitespace-filter.js
/**
 * a method to filter out any whitespace _only_ nodes, to be used inside a template
 * @param value - The Node that is being inspected
 * @param index - The index of the node within the array
 * @param array - The Node array that is being filtered
 *
 * @public
 */
function whitespaceFilter(value, index, array) {
    return value.nodeType !== Node.TEXT_NODE
        ? true
        : typeof value.nodeValue === "string" && !!value.nodeValue.trim().length;
}

;// CONCATENATED MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/search/search.template.js



/**
 * The template for the {@link @microsoft/fast-foundation#(Search:class)} component.
 * @public
 */
const searchTemplate = (context, definition) => (0,template/* html */.d) `
    <template
        class="
            ${x => (x.readOnly ? "readonly" : "")}
        "
    >
        <label
            part="label"
            for="control"
            class="${x => x.defaultSlottedNodes && x.defaultSlottedNodes.length
    ? "label"
    : "label label__hidden"}"
        >
            <slot
                ${(0,slotted/* slotted */.Q)({ property: "defaultSlottedNodes", filter: whitespaceFilter })}
            ></slot>
        </label>
        <div class="root" part="root" ${(0,ref/* ref */.i)("root")}>
            ${(0,start_end/* startSlotTemplate */.m9)(context, definition)}
            <div class="input-wrapper" part="input-wrapper">
                <input
                    class="control"
                    part="control"
                    id="control"
                    @input="${x => x.handleTextInput()}"
                    @change="${x => x.handleChange()}"
                    ?autofocus="${x => x.autofocus}"
                    ?disabled="${x => x.disabled}"
                    list="${x => x.list}"
                    maxlength="${x => x.maxlength}"
                    minlength="${x => x.minlength}"
                    pattern="${x => x.pattern}"
                    placeholder="${x => x.placeholder}"
                    ?readonly="${x => x.readOnly}"
                    ?required="${x => x.required}"
                    size="${x => x.size}"
                    ?spellcheck="${x => x.spellcheck}"
                    :value="${x => x.value}"
                    type="search"
                    aria-atomic="${x => x.ariaAtomic}"
                    aria-busy="${x => x.ariaBusy}"
                    aria-controls="${x => x.ariaControls}"
                    aria-current="${x => x.ariaCurrent}"
                    aria-describedby="${x => x.ariaDescribedby}"
                    aria-details="${x => x.ariaDetails}"
                    aria-disabled="${x => x.ariaDisabled}"
                    aria-errormessage="${x => x.ariaErrormessage}"
                    aria-flowto="${x => x.ariaFlowto}"
                    aria-haspopup="${x => x.ariaHaspopup}"
                    aria-hidden="${x => x.ariaHidden}"
                    aria-invalid="${x => x.ariaInvalid}"
                    aria-keyshortcuts="${x => x.ariaKeyshortcuts}"
                    aria-label="${x => x.ariaLabel}"
                    aria-labelledby="${x => x.ariaLabelledby}"
                    aria-live="${x => x.ariaLive}"
                    aria-owns="${x => x.ariaOwns}"
                    aria-relevant="${x => x.ariaRelevant}"
                    aria-roledescription="${x => x.ariaRoledescription}"
                    ${(0,ref/* ref */.i)("control")}
                />
                <slot name="close-button">
                    <button
                        class="clear-button ${x => x.value ? "" : "clear-button__hidden"}"
                        part="clear-button"
                        tabindex="-1"
                        @click=${x => x.handleClearInput()}
                    >
                        <slot name="close-glyph">
                            <svg
                                width="9"
                                height="9"
                                viewBox="0 0 9 9"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    d="M0.146447 0.146447C0.338683 -0.0478972 0.645911 -0.0270359 0.853553 0.146447L4.5 3.793L8.14645 0.146447C8.34171 -0.0488155 8.65829 -0.0488155 8.85355 0.146447C9.04882 0.341709 9.04882 0.658291 8.85355 0.853553L5.207 4.5L8.85355 8.14645C9.05934 8.35223 9.03129 8.67582 8.85355 8.85355C8.67582 9.03129 8.35409 9.02703 8.14645 8.85355L4.5 5.207L0.853553 8.85355C0.658291 9.04882 0.341709 9.04882 0.146447 8.85355C-0.0488155 8.65829 -0.0488155 8.34171 0.146447 8.14645L3.793 4.5L0.146447 0.853553C-0.0268697 0.680237 -0.0457894 0.34079 0.146447 0.146447Z"
                                />
                            </svg>
                        </slot>
                    </button>
                </slot>
            </div>
            ${(0,start_end/* endSlotTemplate */.LC)(context, definition)}
        </div>
    </template>
`;

// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/styles/css.js
var css = __webpack_require__(12634);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/design-token/design-token.js + 2 modules
var design_token = __webpack_require__(27002);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/utilities/style/focus.js
var style_focus = __webpack_require__(58201);
// EXTERNAL MODULE: ../node_modules/@jupyter/web-components/dist/esm/design-tokens.js + 30 modules
var design_tokens = __webpack_require__(87206);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/utilities/style/display.js
var display = __webpack_require__(21601);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/utilities/style/disabled.js
var disabled = __webpack_require__(61424);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/utilities/match-media-stylesheet-behavior.js
var match_media_stylesheet_behavior = __webpack_require__(98242);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-web-utilities/dist/system-colors.js
var system_colors = __webpack_require__(30550);
// EXTERNAL MODULE: ../node_modules/@jupyter/web-components/dist/esm/styles/size.js
var size = __webpack_require__(13370);
;// CONCATENATED MODULE: ../node_modules/@jupyter/web-components/dist/esm/styles/patterns/field.js
// Copyright (c) Jupyter Development Team.
// Copyright (c) Microsoft Corporation.
// Distributed under the terms of the Modified BSD License.





const BaseFieldStyles = (0,css/* css */.i) `
  ${(0,display/* display */.j)('inline-block')} :host {
    font-family: ${design_tokens/* bodyFont */.SV};
    outline: none;
    user-select: none;
    /* Ensure to display focus highlight */
    margin: calc((${design_tokens/* focusStrokeWidth */.vx} - ${design_tokens/* strokeWidth */.H}) * 1px);
  }

  .root {
    box-sizing: border-box;
    position: relative;
    display: flex;
    flex-direction: row;
    color: ${design_tokens/* neutralForegroundRest */.hY};
    background: ${design_tokens/* neutralFillInputRest */._B};
    border-radius: calc(${design_tokens/* controlCornerRadius */.UW} * 1px);
    border: calc(${design_tokens/* strokeWidth */.H} * 1px) solid ${design_tokens/* neutralFillStrongRest */.P0};
    height: calc(${size/* heightNumber */.i} * 1px);
  }

  :host([aria-invalid='true']) .root {
    border-color: ${design_tokens/* errorFillRest */.a6};
  }

  .control {
    -webkit-appearance: none;
    font: inherit;
    background: transparent;
    border: 0;
    color: inherit;
    height: calc(100% - 4px);
    width: 100%;
    margin-top: auto;
    margin-bottom: auto;
    border: none;
    padding: 0 calc(${design_tokens/* designUnit */._5} * 2px + 1px);
    font-size: ${design_tokens/* typeRampBaseFontSize */.cS};
    line-height: ${design_tokens/* typeRampBaseLineHeight */.RU};
  }

  .control:placeholder-shown {
    text-overflow: ellipsis;
  }

  .control:hover,
  .control:${style_focus/* focusVisible */.b},
  .control:disabled,
  .control:active {
    outline: none;
  }

  .label {
    display: block;
    color: ${design_tokens/* neutralForegroundRest */.hY};
    cursor: pointer;
    font-size: ${design_tokens/* typeRampBaseFontSize */.cS};
    line-height: ${design_tokens/* typeRampBaseLineHeight */.RU};
    margin-bottom: 4px;
  }

  .label__hidden {
    display: none;
    visibility: hidden;
  }

  .start,
  .end {
    margin: auto;
    fill: currentcolor;
  }

  ::slotted(svg) {
    /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
    width: 16px;
    height: 16px;
  }

  .start {
    margin-inline-start: 11px;
  }

  .end {
    margin-inline-end: 11px;
  }

  :host(:hover:not([disabled])) .root {
    background: ${design_tokens/* neutralFillInputHover */.Tm};
    border-color: ${design_tokens/* neutralFillStrongHover */.Dg};
  }

  :host([aria-invalid='true']:hover:not([disabled])) .root {
    border-color: ${design_tokens/* errorFillHover */.ek};
  }

  :host(:active:not([disabled])) .root {
    background: ${design_tokens/* neutralFillInputHover */.Tm};
    border-color: ${design_tokens/* neutralFillStrongActive */.hP};
  }

  :host([aria-invalid='true']:active:not([disabled])) .root {
    border-color: ${design_tokens/* errorFillActive */.GB};
  }

  :host(:focus-within:not([disabled])) .root {
    border-color: ${design_tokens/* accentFillFocus */.D8};
    box-shadow: 0 0 0 calc((${design_tokens/* focusStrokeWidth */.vx} - ${design_tokens/* strokeWidth */.H}) * 1px)
      ${design_tokens/* accentFillFocus */.D8};
  }

  :host([aria-invalid='true']:focus-within:not([disabled])) .root {
    border-color: ${design_tokens/* errorFillFocus */.mH};
    box-shadow: 0 0 0 calc((${design_tokens/* focusStrokeWidth */.vx} - ${design_tokens/* strokeWidth */.H}) * 1px)
      ${design_tokens/* errorFillFocus */.mH};
  }

  :host([appearance='filled']) .root {
    background: ${design_tokens/* neutralFillRest */.wF};
  }

  :host([appearance='filled']:hover:not([disabled])) .root {
    background: ${design_tokens/* neutralFillHover */.Xi};
  }

  :host([disabled]) .label,
  :host([readonly]) .label,
  :host([readonly]) .control,
  :host([disabled]) .control {
    cursor: ${disabled/* disabledCursor */.H};
  }

  :host([disabled]) {
    opacity: ${design_tokens/* disabledOpacity */.VF};
  }

  :host([disabled]) .control {
    border-color: ${design_tokens/* neutralStrokeRest */.ak};
  }
`.withBehaviors((0,match_media_stylesheet_behavior/* forcedColorsStylesheetBehavior */.vF)((0,css/* css */.i) `
    .root,
    :host([appearance='filled']) .root {
      forced-color-adjust: none;
      background: ${system_colors/* SystemColors */.H.Field};
      border-color: ${system_colors/* SystemColors */.H.FieldText};
    }
    :host([aria-invalid='true']) .root {
      border-style: dashed;
    }
    :host(:hover:not([disabled])) .root,
    :host([appearance='filled']:hover:not([disabled])) .root,
    :host([appearance='filled']:hover) .root {
      background: ${system_colors/* SystemColors */.H.Field};
      border-color: ${system_colors/* SystemColors */.H.Highlight};
    }
    .start,
    .end {
      fill: currentcolor;
    }
    :host([disabled]) {
      opacity: 1;
    }
    :host([disabled]) .root,
    :host([appearance='filled']:hover[disabled]) .root {
      border-color: ${system_colors/* SystemColors */.H.GrayText};
      background: ${system_colors/* SystemColors */.H.Field};
    }
    :host(:focus-within:enabled) .root {
      border-color: ${system_colors/* SystemColors */.H.Highlight};
      box-shadow: 0 0 0 calc((${design_tokens/* focusStrokeWidth */.vx} - ${design_tokens/* strokeWidth */.H}) * 1px)
        ${system_colors/* SystemColors */.H.Highlight};
    }
    input::placeholder {
      color: ${system_colors/* SystemColors */.H.GrayText};
    }
  `));

;// CONCATENATED MODULE: ../node_modules/@jupyter/web-components/dist/esm/search/search.styles.js
// Copyright (c) Jupyter Development Team.
// Copyright (c) Microsoft Corporation.
// Distributed under the terms of the Modified BSD License.




const clearButtonHover = design_token.DesignToken.create('clear-button-hover').withDefault((target) => {
    const buttonRecipe = design_tokens/* neutralFillStealthRecipe */.DF.getValueFor(target);
    const inputRecipe = design_tokens/* neutralFillRecipe */.At.getValueFor(target);
    return buttonRecipe.evaluate(target, inputRecipe.evaluate(target).hover)
        .hover;
});
const clearButtonActive = design_token.DesignToken.create('clear-button-active').withDefault((target) => {
    const buttonRecipe = design_tokens/* neutralFillStealthRecipe */.DF.getValueFor(target);
    const inputRecipe = design_tokens/* neutralFillRecipe */.At.getValueFor(target);
    return buttonRecipe.evaluate(target, inputRecipe.evaluate(target).hover)
        .active;
});
const searchStyles = (context, definition) => (0,css/* css */.i) `
  ${BaseFieldStyles}

  .control::-webkit-search-cancel-button {
    -webkit-appearance: none;
  }

  .control:hover,
    .control:${style_focus/* focusVisible */.b},
    .control:disabled,
    .control:active {
    outline: none;
  }

  .clear-button {
    height: calc(100% - 2px);
    opacity: 0;
    margin: 1px;
    background: transparent;
    color: ${design_tokens/* neutralForegroundRest */.hY};
    fill: currentcolor;
    border: none;
    border-radius: calc(${design_tokens/* controlCornerRadius */.UW} * 1px);
    min-width: calc(${size/* heightNumber */.i} * 1px);
    font-size: ${design_tokens/* typeRampBaseFontSize */.cS};
    line-height: ${design_tokens/* typeRampBaseLineHeight */.RU};
    outline: none;
    font-family: ${design_tokens/* bodyFont */.SV};
    padding: 0 calc((10 + (${design_tokens/* designUnit */._5} * 2 * ${design_tokens/* density */.hV})) * 1px);
  }

  .clear-button:hover {
    background: ${design_tokens/* neutralFillStealthHover */.Qp};
  }

  .clear-button:active {
    background: ${design_tokens/* neutralFillStealthActive */.sG};
  }

  :host([appearance='filled']) .clear-button:hover {
    background: ${clearButtonHover};
  }

  :host([appearance='filled']) .clear-button:active {
    background: ${clearButtonActive};
  }

  .input-wrapper {
    display: flex;
    position: relative;
    width: 100%;
  }

  .start,
  .end {
    display: flex;
    margin: 1px;
    fill: currentcolor;
  }

  ::slotted([slot='end']) {
    height: 100%;
  }

  .end {
    margin-inline-end: 1px;
    height: calc(100% - 2px);
  }

  ::slotted(svg) {
    /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
    width: 16px;
    height: 16px;
    margin-inline-end: 11px;
    margin-inline-start: 11px;
    margin-top: auto;
    margin-bottom: auto;
  }

  .clear-button__hidden {
    opacity: 0;
  }

  :host(:hover:not([disabled], [readOnly])) .clear-button,
  :host(:active:not([disabled], [readOnly])) .clear-button,
  :host(:focus-within:not([disabled], [readOnly])) .clear-button {
    opacity: 1;
  }

  :host(:hover:not([disabled], [readOnly])) .clear-button__hidden,
  :host(:active:not([disabled], [readOnly])) .clear-button__hidden,
  :host(:focus-within:not([disabled], [readOnly])) .clear-button__hidden {
    opacity: 0;
  }
`;

;// CONCATENATED MODULE: ../node_modules/@jupyter/web-components/dist/esm/search/index.js
// Copyright (c) Jupyter Development Team.
// Copyright (c) Microsoft Corporation.
// Distributed under the terms of the Modified BSD License.




/**
 * Search field class
 *
 * @public
 * @tagname jp-search
 *
 * @fires input - Fires a custom 'input' event when the value has changed
 * @fires change - Fires a custom 'change' event when the value has changed
 */
class JupyterSearch extends Search {
    constructor() {
        super(...arguments);
        /**
         * The appearance of the element.
         *
         * @public
         * @remarks
         * HTML Attribute: appearance
         */
        this.appearance = 'outline';
    }
}
(0,tslib_es6/* __decorate */.gn)([
    attributes/* attr */.Lj
], JupyterSearch.prototype, "appearance", void 0);
/**
 * A function that returns a {@link @microsoft/fast-foundation#Search} registration for configuring the component with a DesignSystem.
 * Implements {@link @microsoft/fast-foundation#searchTemplate}
 *
 *
 * @public
 * @remarks
 * Generates HTML Element: `<jp-search>`
 *
 * {@link https://developer.mozilla.org/en-US/docs/Web/API/ShadowRoot/delegatesFocus | delegatesFocus}
 */
const jpSearch = JupyterSearch.compose({
    baseName: 'search',
    baseClass: Search,
    template: searchTemplate,
    styles: searchStyles,
    shadowOptions: {
        delegatesFocus: true
    }
});


// EXTERNAL MODULE: consume shared module (default) react@~18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var index_js_ = __webpack_require__(78156);
var index_js_default = /*#__PURE__*/__webpack_require__.n(index_js_);
// EXTERNAL MODULE: ../node_modules/@jupyter/react-components/lib/react-utils.js
var react_utils = __webpack_require__(4444);
;// CONCATENATED MODULE: ../node_modules/@jupyter/react-components/lib/Search.js



(0,jupyter_design_system/* provideJupyterDesignSystem */.W)().register(jpSearch());

const Search_Search = (0,index_js_.forwardRef)((props, forwardedRef) => {
  const ref = (0,index_js_.useRef)(null);
  const {
    className,
    readonly,
    appearance,
    placeholder,
    list,
    pattern,
    readOnly,
    autofocus,
    maxlength,
    minlength,
    size,
    spellcheck,
    disabled,
    required,
    ...filteredProps
  } = props;

  /** Event listeners - run once */
  (0,react_utils/* useEventListener */.O)(ref, 'input', props.onInput);
  (0,react_utils/* useEventListener */.O)(ref, 'change', props.onChange);

  /** Properties - run whenever a property has changed */
  (0,react_utils/* useProperties */.h)(ref, 'readOnly', props.readOnly);
  (0,react_utils/* useProperties */.h)(ref, 'autofocus', props.autofocus);
  (0,react_utils/* useProperties */.h)(ref, 'maxlength', props.maxlength);
  (0,react_utils/* useProperties */.h)(ref, 'minlength', props.minlength);
  (0,react_utils/* useProperties */.h)(ref, 'size', props.size);
  (0,react_utils/* useProperties */.h)(ref, 'spellcheck', props.spellcheck);
  (0,react_utils/* useProperties */.h)(ref, 'disabled', props.disabled);
  (0,react_utils/* useProperties */.h)(ref, 'required', props.required);

  /** Methods - uses `useImperativeHandle` hook to pass ref to component */
  (0,index_js_.useImperativeHandle)(forwardedRef, () => ref.current, [ref.current]);

  return index_js_default().createElement(
    'jp-search',
    {
      ref,
      ...filteredProps,
      appearance: props.appearance,
      placeholder: props.placeholder,
      list: props.list,
      pattern: props.pattern,
      class: props.className,
      exportparts: props.exportparts,
      for: props.htmlFor,
      part: props.part,
      tabindex: props.tabIndex,
      readonly: props.readonly ? '' : undefined,
      style: { ...props.style }
    },
    props.children
  );
});


/***/ })

}]);
//# sourceMappingURL=9672.b55f9504fd5af290b047.js.map?v=b55f9504fd5af290b047