"use strict";
(self["webpackChunk_JUPYTERLAB_CORE_OUTPUT"] = self["webpackChunk_JUPYTERLAB_CORE_OUTPUT"] || []).push([[2424],{

/***/ 63956:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {


// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  k: () => (/* binding */ TreeItem)
});

// EXTERNAL MODULE: ../node_modules/@jupyter/web-components/dist/esm/jupyter-design-system.js + 1 modules
var jupyter_design_system = __webpack_require__(68866);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/tree-item/tree-item.js
var tree_item = __webpack_require__(80189);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/templating/template.js + 3 modules
var template = __webpack_require__(25269);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/templating/children.js
var children = __webpack_require__(58545);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/templating/node-observation.js
var node_observation = __webpack_require__(41681);
;// CONCATENATED MODULE: ../node_modules/@microsoft/fast-element/dist/esm/interfaces.js
/**
 * Determines whether or not an object is a function.
 * @public
 */
const isFunction = (object) => typeof object === "function";

;// CONCATENATED MODULE: ../node_modules/@microsoft/fast-element/dist/esm/templating/when.js

const noTemplate = () => null;
function normalizeBinding(value) {
    return value === undefined ? noTemplate : isFunction(value) ? value : () => value;
}
/**
 * A directive that enables basic conditional rendering in a template.
 * @param binding - The condition to test for rendering.
 * @param templateOrTemplateBinding - The template or a binding that gets
 * the template to render when the condition is true.
 * @param elseTemplateOrTemplateBinding - Optional template or binding that that
 * gets the template to render when the conditional is false.
 * @public
 */
function when(binding, templateOrTemplateBinding, elseTemplateOrTemplateBinding) {
    const dataBinding = isFunction(binding) ? binding : () => binding;
    const templateBinding = normalizeBinding(templateOrTemplateBinding);
    const elseBinding = normalizeBinding(elseTemplateOrTemplateBinding);
    return (source, context) => dataBinding(source, context)
        ? templateBinding(source, context)
        : elseBinding(source, context);
}

// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/templating/ref.js
var ref = __webpack_require__(62564);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/templating/slotted.js
var slotted = __webpack_require__(17832);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/patterns/start-end.js
var start_end = __webpack_require__(52865);
;// CONCATENATED MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/tree-item/tree-item.template.js


/**
 * The template for the {@link @microsoft/fast-foundation#(TreeItem:class)} component.
 * @public
 */
const treeItemTemplate = (context, definition) => (0,template/* html */.d) `
    <template
        role="treeitem"
        slot="${x => (x.isNestedItem() ? "item" : void 0)}"
        tabindex="-1"
        class="${x => (x.expanded ? "expanded" : "")} ${x => x.selected ? "selected" : ""} ${x => (x.nested ? "nested" : "")}
            ${x => (x.disabled ? "disabled" : "")}"
        aria-expanded="${x => x.childItems && x.childItemLength() > 0 ? x.expanded : void 0}"
        aria-selected="${x => x.selected}"
        aria-disabled="${x => x.disabled}"
        @focusin="${(x, c) => x.handleFocus(c.event)}"
        @focusout="${(x, c) => x.handleBlur(c.event)}"
        ${(0,children/* children */.p)({
    property: "childItems",
    filter: (0,node_observation/* elements */.R)(),
})}
    >
        <div class="positioning-region" part="positioning-region">
            <div class="content-region" part="content-region">
                ${when(x => x.childItems && x.childItemLength() > 0, (0,template/* html */.d) `
                        <div
                            aria-hidden="true"
                            class="expand-collapse-button"
                            part="expand-collapse-button"
                            @click="${(x, c) => x.handleExpandCollapseButtonClick(c.event)}"
                            ${(0,ref/* ref */.i)("expandCollapseButton")}
                        >
                            <slot name="expand-collapse-glyph">
                                ${definition.expandCollapseGlyph || ""}
                            </slot>
                        </div>
                    `)}
                ${(0,start_end/* startSlotTemplate */.m9)(context, definition)}
                <slot></slot>
                ${(0,start_end/* endSlotTemplate */.LC)(context, definition)}
            </div>
        </div>
        ${when(x => x.childItems &&
    x.childItemLength() > 0 &&
    (x.expanded || x.renderCollapsedChildren), (0,template/* html */.d) `
                <div role="group" class="items" part="items">
                    <slot name="item" ${(0,slotted/* slotted */.Q)("items")}></slot>
                </div>
            `)}
    </template>
`;

// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/styles/css.js
var css = __webpack_require__(12634);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/design-token/design-token.js + 2 modules
var design_token = __webpack_require__(27002);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/utilities/style/display.js
var display = __webpack_require__(21601);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/utilities/style/focus.js
var style_focus = __webpack_require__(58201);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/utilities/style/disabled.js
var disabled = __webpack_require__(61424);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/utilities/match-media-stylesheet-behavior.js
var match_media_stylesheet_behavior = __webpack_require__(98242);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-web-utilities/dist/system-colors.js
var system_colors = __webpack_require__(30550);
// EXTERNAL MODULE: ../node_modules/@jupyter/web-components/dist/esm/design-tokens.js + 30 modules
var design_tokens = __webpack_require__(87206);
// EXTERNAL MODULE: ../node_modules/@jupyter/web-components/dist/esm/styles/size.js
var size = __webpack_require__(13370);
;// CONCATENATED MODULE: ../node_modules/@jupyter/web-components/dist/esm/styles/direction.js
// Copyright (c) Jupyter Development Team.
// Copyright (c) Microsoft Corporation.
// Distributed under the terms of the Modified BSD License.

/**
 * Behavior to conditionally apply LTR and RTL stylesheets. To determine which to apply,
 * the behavior will use the nearest DesignSystemProvider's 'direction' design system value.
 *
 * @public
 * @example
 * ```ts
 * import { css } from "@microsoft/fast-element";
 * import { DirectionalStyleSheetBehavior } from "@microsoft/fast-foundation";
 *
 * css`
 *  // ...
 * `.withBehaviors(new DirectionalStyleSheetBehavior(
 *   css`:host { content: "ltr"}`),
 *   css`:host { content: "rtl"}`),
 * )
 * ```
 */
class DirectionalStyleSheetBehavior {
    constructor(ltr, rtl) {
        this.cache = new WeakMap();
        this.ltr = ltr;
        this.rtl = rtl;
    }
    /**
     * @internal
     */
    bind(source) {
        this.attach(source);
    }
    /**
     * @internal
     */
    unbind(source) {
        const cache = this.cache.get(source);
        if (cache) {
            design_tokens/* direction */.o7.unsubscribe(cache);
        }
    }
    attach(source) {
        const subscriber = this.cache.get(source) ||
            new DirectionalStyleSheetBehaviorSubscription(this.ltr, this.rtl, source);
        const value = design_tokens/* direction */.o7.getValueFor(source);
        design_tokens/* direction */.o7.subscribe(subscriber);
        subscriber.attach(value);
        this.cache.set(source, subscriber);
    }
}
/**
 * Subscription for {@link DirectionalStyleSheetBehavior}
 */
class DirectionalStyleSheetBehaviorSubscription {
    constructor(ltr, rtl, source) {
        this.ltr = ltr;
        this.rtl = rtl;
        this.source = source;
        this.attached = null;
    }
    handleChange({ target, token }) {
        this.attach(token.getValueFor(target));
    }
    attach(direction) {
        if (this.attached !== this[direction]) {
            if (this.attached !== null) {
                this.source.$fastController.removeStyles(this.attached);
            }
            this.attached = this[direction];
            if (this.attached !== null) {
                this.source.$fastController.addStyles(this.attached);
            }
        }
    }
}

;// CONCATENATED MODULE: ../node_modules/@jupyter/web-components/dist/esm/tree-item/tree-item.styles.js
// Copyright (c) Jupyter Development Team.
// Copyright (c) Microsoft Corporation.
// Distributed under the terms of the Modified BSD License.





/**
 * Tree item expand collapse button size CSS Partial
 * @public
 */
const expandCollapseButtonSize = (0,css/* cssPartial */.j) `(((${design_tokens/* baseHeightMultiplier */.nf} + ${design_tokens/* density */.hV}) * 0.5 + 2) * ${design_tokens/* designUnit */._5})`;
const ltr = (0,css/* css */.i) `
  .expand-collapse-glyph {
    transform: rotate(0deg);
  }
  :host(.nested) .expand-collapse-button {
    left: var(
      --expand-collapse-button-nested-width,
      calc(
        (
            ${expandCollapseButtonSize} +
              ((${design_tokens/* baseHeightMultiplier */.nf} + ${design_tokens/* density */.hV}) * 1.25)
          ) * -1px
      )
    );
  }
  :host([selected])::after {
    left: calc(${design_tokens/* focusStrokeWidth */.vx} * 1px);
  }
  :host([expanded]) > .positioning-region .expand-collapse-glyph {
    transform: rotate(90deg);
  }
`;
const rtl = (0,css/* css */.i) `
  .expand-collapse-glyph {
    transform: rotate(180deg);
  }
  :host(.nested) .expand-collapse-button {
    right: var(
      --expand-collapse-button-nested-width,
      calc(
        (
            ${expandCollapseButtonSize} +
              ((${design_tokens/* baseHeightMultiplier */.nf} + ${design_tokens/* density */.hV}) * 1.25)
          ) * -1px
      )
    );
  }
  :host([selected])::after {
    right: calc(${design_tokens/* focusStrokeWidth */.vx} * 1px);
  }
  :host([expanded]) > .positioning-region .expand-collapse-glyph {
    transform: rotate(90deg);
  }
`;
const expandCollapseHoverBehavior = design_token.DesignToken.create('tree-item-expand-collapse-hover').withDefault((target) => {
    const recipe = design_tokens/* neutralFillStealthRecipe */.DF.getValueFor(target);
    return recipe.evaluate(target, recipe.evaluate(target).hover).hover;
});
const selectedExpandCollapseHoverBehavior = design_token.DesignToken.create('tree-item-expand-collapse-selected-hover').withDefault((target) => {
    const baseRecipe = design_tokens/* neutralFillRecipe */.At.getValueFor(target);
    const buttonRecipe = design_tokens/* neutralFillStealthRecipe */.DF.getValueFor(target);
    return buttonRecipe.evaluate(target, baseRecipe.evaluate(target).rest).hover;
});
/**
 * Styles for Tree Item
 * @public
 */
const treeItemStyles = (context, definition) => (0,css/* css */.i) `
    /**
     * This animation exists because when tree item children are conditionally loaded
     * there is a visual bug where the DOM exists but styles have not yet been applied (essentially FOUC).
     * This subtle animation provides a ever so slight timing adjustment for loading that solves the issue.
     */
    @keyframes treeItemLoading {
      0% {
        opacity: 0;
      }
      100% {
        opacity: 1;
      }
    }

    ${(0,display/* display */.j)('block')} :host {
      contain: content;
      position: relative;
      outline: none;
      color: ${design_tokens/* neutralForegroundRest */.hY};
      background: ${design_tokens/* neutralFillStealthRest */.jq};
      cursor: pointer;
      font-family: ${design_tokens/* bodyFont */.SV};
      --tree-item-nested-width: 0;
    }

    :host(:focus) > .positioning-region {
      outline: none;
    }

    :host(:focus) .content-region {
      outline: none;
    }

    :host(:${style_focus/* focusVisible */.b}) .positioning-region {
      border-color: ${design_tokens/* accentFillFocus */.D8};
      box-shadow: 0 0 0 calc((${design_tokens/* focusStrokeWidth */.vx} - ${design_tokens/* strokeWidth */.H}) * 1px)
        ${design_tokens/* accentFillFocus */.D8} inset;
      color: ${design_tokens/* neutralForegroundRest */.hY};
    }

    .positioning-region {
      display: flex;
      position: relative;
      box-sizing: border-box;
      background: ${design_tokens/* neutralFillStealthRest */.jq};
      border: transparent calc(${design_tokens/* strokeWidth */.H} * 1px) solid;
      border-radius: calc(${design_tokens/* controlCornerRadius */.UW} * 1px);
      height: calc((${size/* heightNumber */.i} + 1) * 1px);
    }

    .positioning-region::before {
      content: '';
      display: block;
      width: var(--tree-item-nested-width);
      flex-shrink: 0;
    }

    :host(:not([disabled])) .positioning-region:hover {
      background: ${design_tokens/* neutralFillStealthHover */.Qp};
    }

    :host(:not([disabled])) .positioning-region:active {
      background: ${design_tokens/* neutralFillStealthActive */.sG};
    }

    .content-region {
      display: inline-flex;
      align-items: center;
      white-space: nowrap;
      width: 100%;
      min-width: 0;
      height: calc(${size/* heightNumber */.i} * 1px);
      margin-inline-start: calc(${design_tokens/* designUnit */._5} * 2px + 8px);
      font-size: ${design_tokens/* typeRampBaseFontSize */.cS};
      line-height: ${design_tokens/* typeRampBaseLineHeight */.RU};
      font-weight: 400;
    }

    .items {
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      font-size: calc(1em + (${design_tokens/* designUnit */._5} + 16) * 1px);
    }

    .expand-collapse-button {
      background: none;
      border: none;
      outline: none;
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      width: calc(${expandCollapseButtonSize} * 1px);
      height: calc(${expandCollapseButtonSize} * 1px);
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      cursor: pointer;
      margin-left: 6px;
      margin-right: 6px;
    }

    .expand-collapse-glyph {
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      width: calc((16 + ${design_tokens/* density */.hV}) * 1px);
      height: calc((16 + ${design_tokens/* density */.hV}) * 1px);
      transition: transform 0.1s linear;

      pointer-events: none;
      fill: currentcolor;
    }

    .start,
    .end {
      display: flex;
      fill: currentcolor;
    }

    ::slotted(svg) {
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      width: 16px;
      height: 16px;

      /* Something like that would do if the typography is adaptive
      font-size: inherit;
      width: ${design_tokens/* typeRampPlus1FontSize */.Pw};
      height: ${design_tokens/* typeRampPlus1FontSize */.Pw};
      */
    }

    .start {
      /* TODO: horizontalSpacing https://github.com/microsoft/fast/issues/2766 */
      margin-inline-end: calc(${design_tokens/* designUnit */._5} * 2px + 2px);
    }

    .end {
      /* TODO: horizontalSpacing https://github.com/microsoft/fast/issues/2766 */
      margin-inline-start: calc(${design_tokens/* designUnit */._5} * 2px + 2px);
    }

    :host([expanded]) > .items {
      animation: treeItemLoading ease-in 10ms;
      animation-iteration-count: 1;
      animation-fill-mode: forwards;
    }

    :host([disabled]) .content-region {
      opacity: ${design_tokens/* disabledOpacity */.VF};
      cursor: ${disabled/* disabledCursor */.H};
    }

    :host(.nested) .content-region {
      position: relative;
      /* Add left margin to collapse button size */
      margin-inline-start: calc(
        (
            ${expandCollapseButtonSize} +
              ((${design_tokens/* baseHeightMultiplier */.nf} + ${design_tokens/* density */.hV}) * 1.25)
          ) * 1px
      );
    }

    :host(.nested) .expand-collapse-button {
      position: absolute;
    }

    :host(.nested:not([disabled])) .expand-collapse-button:hover {
      background: ${expandCollapseHoverBehavior};
    }

    :host([selected]) .positioning-region {
      background: ${design_tokens/* neutralFillRest */.wF};
    }

    :host([selected]:not([disabled])) .positioning-region:hover {
      background: ${design_tokens/* neutralFillHover */.Xi};
    }

    :host([selected]:not([disabled])) .positioning-region:active {
      background: ${design_tokens/* neutralFillActive */.Gy};
    }

    :host([selected]:not([disabled])) .expand-collapse-button:hover {
      background: ${selectedExpandCollapseHoverBehavior};
    }

    :host([selected])::after {
      /* The background needs to be calculated based on the selected background state
         for this control. We currently have no way of changing that, so setting to
         accent-foreground-rest for the time being */
      background: ${design_tokens/* accentForegroundRest */.go};
      border-radius: calc(${design_tokens/* controlCornerRadius */.UW} * 1px);
      content: '';
      display: block;
      position: absolute;
      top: calc((${size/* heightNumber */.i} / 4) * 1px);
      width: 3px;
      height: calc((${size/* heightNumber */.i} / 2) * 1px);
    }

    ::slotted(${context.tagFor(tree_item/* TreeItem */.k)}) {
      --tree-item-nested-width: 1em;
      --expand-collapse-button-nested-width: calc(
        (
            ${expandCollapseButtonSize} +
              ((${design_tokens/* baseHeightMultiplier */.nf} + ${design_tokens/* density */.hV}) * 1.25)
          ) * -1px
      );
    }
  `.withBehaviors(new DirectionalStyleSheetBehavior(ltr, rtl), (0,match_media_stylesheet_behavior/* forcedColorsStylesheetBehavior */.vF)((0,css/* css */.i) `
      :host {
        forced-color-adjust: none;
        border-color: transparent;
        background: ${system_colors/* SystemColors */.H.Field};
        color: ${system_colors/* SystemColors */.H.FieldText};
      }
      :host .content-region .expand-collapse-glyph {
        fill: ${system_colors/* SystemColors */.H.FieldText};
      }
      :host .positioning-region:hover,
      :host([selected]) .positioning-region {
        background: ${system_colors/* SystemColors */.H.Highlight};
      }
      :host .positioning-region:hover .content-region,
      :host([selected]) .positioning-region .content-region {
        color: ${system_colors/* SystemColors */.H.HighlightText};
      }
      :host .positioning-region:hover .content-region .expand-collapse-glyph,
      :host .positioning-region:hover .content-region .start,
      :host .positioning-region:hover .content-region .end,
      :host([selected]) .content-region .expand-collapse-glyph,
      :host([selected]) .content-region .start,
      :host([selected]) .content-region .end {
        fill: ${system_colors/* SystemColors */.H.HighlightText};
      }
      :host([selected])::after {
        background: ${system_colors/* SystemColors */.H.Field};
      }
      :host(:${style_focus/* focusVisible */.b}) .positioning-region {
        border-color: ${system_colors/* SystemColors */.H.FieldText};
        box-shadow: 0 0 0 2px inset ${system_colors/* SystemColors */.H.Field};
        color: ${system_colors/* SystemColors */.H.FieldText};
      }
      :host([disabled]) .content-region,
      :host([disabled]) .positioning-region:hover .content-region {
        opacity: 1;
        color: ${system_colors/* SystemColors */.H.GrayText};
      }
      :host([disabled]) .content-region .expand-collapse-glyph,
      :host([disabled]) .content-region .start,
      :host([disabled]) .content-region .end,
      :host([disabled])
        .positioning-region:hover
        .content-region
        .expand-collapse-glyph,
      :host([disabled]) .positioning-region:hover .content-region .start,
      :host([disabled]) .positioning-region:hover .content-region .end {
        fill: ${system_colors/* SystemColors */.H.GrayText};
      }
      :host([disabled]) .positioning-region:hover {
        background: ${system_colors/* SystemColors */.H.Field};
      }
      .expand-collapse-glyph,
      .start,
      .end {
        fill: ${system_colors/* SystemColors */.H.FieldText};
      }
      :host(.nested) .expand-collapse-button:hover {
        background: ${system_colors/* SystemColors */.H.Field};
      }
      :host(.nested) .expand-collapse-button:hover .expand-collapse-glyph {
        fill: ${system_colors/* SystemColors */.H.FieldText};
      }
    `));

;// CONCATENATED MODULE: ../node_modules/@jupyter/web-components/dist/esm/tree-item/index.js
// Copyright (c) Jupyter Development Team.
// Copyright (c) Microsoft Corporation.
// Distributed under the terms of the Modified BSD License.


/**
 * Tree item class
 *
 * @public
 * @tagname jp-tree-item
 */
class JupyterTreeItem extends tree_item/* TreeItem */.k {
}
/**
 * A function that returns a {@link @microsoft/fast-foundation#TreeItem} registration for configuring the component with a DesignSystem.
 * Implements {@link @microsoft/fast-foundation#treeItemTemplate}
 *
 *
 * @public
 * @remarks
 * Generates HTML Element: `<jp-tree-item>`
 *
 */
const jpTreeItem = JupyterTreeItem.compose({
    baseName: 'tree-item',
    baseClass: tree_item/* TreeItem */.k,
    template: treeItemTemplate,
    styles: treeItemStyles,
    expandCollapseGlyph: /* html */ `
        <svg
            viewBox="0 0 16 16"
            xmlns="http://www.w3.org/2000/svg"
            class="expand-collapse-glyph"
        >
            <path
                d="M5.00001 12.3263C5.00124 12.5147 5.05566 12.699 5.15699 12.8578C5.25831 13.0167 5.40243 13.1437 5.57273 13.2242C5.74304 13.3047 5.9326 13.3354 6.11959 13.3128C6.30659 13.2902 6.4834 13.2152 6.62967 13.0965L10.8988 8.83532C11.0739 8.69473 11.2153 8.51658 11.3124 8.31402C11.4096 8.11146 11.46 7.88966 11.46 7.66499C11.46 7.44033 11.4096 7.21853 11.3124 7.01597C11.2153 6.81341 11.0739 6.63526 10.8988 6.49467L6.62967 2.22347C6.48274 2.10422 6.30501 2.02912 6.11712 2.00691C5.92923 1.9847 5.73889 2.01628 5.56823 2.09799C5.39757 2.17969 5.25358 2.30817 5.153 2.46849C5.05241 2.62882 4.99936 2.8144 5.00001 3.00369V12.3263Z"
            />
        </svg>
    `
});


// EXTERNAL MODULE: consume shared module (default) react@~18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var index_js_ = __webpack_require__(78156);
var index_js_default = /*#__PURE__*/__webpack_require__.n(index_js_);
// EXTERNAL MODULE: ../node_modules/@jupyter/react-components/lib/react-utils.js
var react_utils = __webpack_require__(4444);
;// CONCATENATED MODULE: ../node_modules/@jupyter/react-components/lib/TreeItem.js



(0,jupyter_design_system/* provideJupyterDesignSystem */.W)().register(jpTreeItem());

const TreeItem = (0,index_js_.forwardRef)((props, forwardedRef) => {
  const ref = (0,index_js_.useRef)(null);
  const { className, expanded, selected, disabled, ...filteredProps } = props;

  /** Event listeners - run once */
  (0,react_utils/* useEventListener */.O)(ref, 'expanded-change', props.onExpand);
  (0,react_utils/* useEventListener */.O)(ref, 'selected-change', props.onSelect);

  /** Properties - run whenever a property has changed */
  (0,react_utils/* useProperties */.h)(ref, 'expanded', props.expanded);
  (0,react_utils/* useProperties */.h)(ref, 'selected', props.selected);
  (0,react_utils/* useProperties */.h)(ref, 'disabled', props.disabled);

  /** Methods - uses `useImperativeHandle` hook to pass ref to component */
  (0,index_js_.useImperativeHandle)(forwardedRef, () => ref.current, [ref.current]);

  // Add web component internal classes on top of `className`
  let allClasses = className ?? '';
  if (ref.current?.nested) {
    allClasses += ' nested';
  }

  return index_js_default().createElement(
    'jp-tree-item',
    {
      ref,
      ...filteredProps,
      class: allClasses.trim(),
      exportparts: props.exportparts,
      for: props.htmlFor,
      part: props.part,
      tabindex: props.tabIndex,
      style: { ...props.style }
    },
    props.children
  );
});


/***/ }),

/***/ 55947:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {


// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  L: () => (/* binding */ TreeView_TreeView)
});

// EXTERNAL MODULE: ../node_modules/@jupyter/web-components/dist/esm/jupyter-design-system.js + 1 modules
var jupyter_design_system = __webpack_require__(68866);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/node_modules/tslib/tslib.es6.js
var tslib_es6 = __webpack_require__(95185);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/dom.js
var dom = __webpack_require__(91211);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/components/attributes.js
var attributes = __webpack_require__(98332);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/observation/observable.js
var observable = __webpack_require__(92221);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-web-utilities/dist/key-codes.js
var key_codes = __webpack_require__(27081);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-web-utilities/dist/dom.js + 1 modules
var dist_dom = __webpack_require__(99415);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/tree-item/tree-item.js
var tree_item = __webpack_require__(80189);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/foundation-element/foundation-element.js
var foundation_element = __webpack_require__(50755);
;// CONCATENATED MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/tree-view/tree-view.js





/**
 * A Tree view Custom HTML Element.
 * Implements the {@link https://w3c.github.io/aria-practices/#TreeView | ARIA TreeView }.
 *
 * @slot - The default slot for tree items
 *
 * @public
 */
class TreeView extends foundation_element/* FoundationElement */.I {
    constructor() {
        super(...arguments);
        /**
         * The tree item that is designated to be in the tab queue.
         *
         * @internal
         */
        this.currentFocused = null;
        /**
         * Handle focus events
         *
         * @internal
         */
        this.handleFocus = (e) => {
            if (this.slottedTreeItems.length < 1) {
                // no child items, nothing to do
                return;
            }
            if (e.target === this) {
                if (this.currentFocused === null) {
                    this.currentFocused = this.getValidFocusableItem();
                }
                if (this.currentFocused !== null) {
                    tree_item/* TreeItem */.k.focusItem(this.currentFocused);
                }
                return;
            }
            if (this.contains(e.target)) {
                this.setAttribute("tabindex", "-1");
                this.currentFocused = e.target;
            }
        };
        /**
         * Handle blur events
         *
         * @internal
         */
        this.handleBlur = (e) => {
            if (e.target instanceof HTMLElement &&
                (e.relatedTarget === null || !this.contains(e.relatedTarget))) {
                this.setAttribute("tabindex", "0");
            }
        };
        /**
         * KeyDown handler
         *
         *  @internal
         */
        this.handleKeyDown = (e) => {
            if (e.defaultPrevented) {
                return;
            }
            if (this.slottedTreeItems.length < 1) {
                return true;
            }
            const treeItems = this.getVisibleNodes();
            switch (e.key) {
                case key_codes/* keyHome */.tU:
                    if (treeItems.length) {
                        tree_item/* TreeItem */.k.focusItem(treeItems[0]);
                    }
                    return;
                case key_codes/* keyEnd */.Kh:
                    if (treeItems.length) {
                        tree_item/* TreeItem */.k.focusItem(treeItems[treeItems.length - 1]);
                    }
                    return;
                case key_codes/* keyArrowLeft */.BE:
                    if (e.target && this.isFocusableElement(e.target)) {
                        const item = e.target;
                        if (item instanceof tree_item/* TreeItem */.k &&
                            item.childItemLength() > 0 &&
                            item.expanded) {
                            item.expanded = false;
                        }
                        else if (item instanceof tree_item/* TreeItem */.k &&
                            item.parentElement instanceof tree_item/* TreeItem */.k) {
                            tree_item/* TreeItem */.k.focusItem(item.parentElement);
                        }
                    }
                    return false;
                case key_codes/* keyArrowRight */.mr:
                    if (e.target && this.isFocusableElement(e.target)) {
                        const item = e.target;
                        if (item instanceof tree_item/* TreeItem */.k &&
                            item.childItemLength() > 0 &&
                            !item.expanded) {
                            item.expanded = true;
                        }
                        else if (item instanceof tree_item/* TreeItem */.k && item.childItemLength() > 0) {
                            this.focusNextNode(1, e.target);
                        }
                    }
                    return;
                case key_codes/* keyArrowDown */.iF:
                    if (e.target && this.isFocusableElement(e.target)) {
                        this.focusNextNode(1, e.target);
                    }
                    return;
                case key_codes/* keyArrowUp */.SB:
                    if (e.target && this.isFocusableElement(e.target)) {
                        this.focusNextNode(-1, e.target);
                    }
                    return;
                case key_codes/* keyEnter */.kL:
                    // In single-select trees where selection does not follow focus (see note below),
                    // the default action is typically to select the focused node.
                    this.handleClick(e);
                    return;
            }
            // don't prevent default if we took no action
            return true;
        };
        /**
         * Handles the selected-changed events bubbling up
         * from child tree items
         *
         *  @internal
         */
        this.handleSelectedChange = (e) => {
            if (e.defaultPrevented) {
                return;
            }
            if (!(e.target instanceof Element) || !(0,tree_item/* isTreeItemElement */.t)(e.target)) {
                return true;
            }
            const item = e.target;
            if (item.selected) {
                if (this.currentSelected && this.currentSelected !== item) {
                    this.currentSelected.selected = false;
                }
                // new selected item
                this.currentSelected = item;
            }
            else if (!item.selected && this.currentSelected === item) {
                // selected item deselected
                this.currentSelected = null;
            }
            return;
        };
        /**
         * Updates the tree view when slottedTreeItems changes
         */
        this.setItems = () => {
            // force single selection
            // defaults to first one found
            const selectedItem = this.treeView.querySelector("[aria-selected='true']");
            this.currentSelected = selectedItem;
            // invalidate the current focused item if it is no longer valid
            if (this.currentFocused === null || !this.contains(this.currentFocused)) {
                this.currentFocused = this.getValidFocusableItem();
            }
            // toggle properties on child elements
            this.nested = this.checkForNestedItems();
            const treeItems = this.getVisibleNodes();
            treeItems.forEach(node => {
                if ((0,tree_item/* isTreeItemElement */.t)(node)) {
                    node.nested = this.nested;
                }
            });
        };
        /**
         * check if the item is focusable
         */
        this.isFocusableElement = (el) => {
            return (0,tree_item/* isTreeItemElement */.t)(el);
        };
        this.isSelectedElement = (el) => {
            return el.selected;
        };
    }
    slottedTreeItemsChanged() {
        if (this.$fastController.isConnected) {
            // update for slotted children change
            this.setItems();
        }
    }
    connectedCallback() {
        super.connectedCallback();
        this.setAttribute("tabindex", "0");
        dom/* DOM */.SO.queueUpdate(() => {
            this.setItems();
        });
    }
    /**
     * Handles click events bubbling up
     *
     *  @internal
     */
    handleClick(e) {
        if (e.defaultPrevented) {
            // handled, do nothing
            return;
        }
        if (!(e.target instanceof Element) || !(0,tree_item/* isTreeItemElement */.t)(e.target)) {
            // not a tree item, ignore
            return true;
        }
        const item = e.target;
        if (!item.disabled) {
            item.selected = !item.selected;
        }
        return;
    }
    /**
     * Move focus to a tree item based on its offset from the provided item
     */
    focusNextNode(delta, item) {
        const visibleNodes = this.getVisibleNodes();
        if (!visibleNodes) {
            return;
        }
        const focusItem = visibleNodes[visibleNodes.indexOf(item) + delta];
        if ((0,dist_dom/* isHTMLElement */.Re)(focusItem)) {
            tree_item/* TreeItem */.k.focusItem(focusItem);
        }
    }
    /**
     * checks if there are any nested tree items
     */
    getValidFocusableItem() {
        const treeItems = this.getVisibleNodes();
        // default to selected element if there is one
        let focusIndex = treeItems.findIndex(this.isSelectedElement);
        if (focusIndex === -1) {
            // otherwise first focusable tree item
            focusIndex = treeItems.findIndex(this.isFocusableElement);
        }
        if (focusIndex !== -1) {
            return treeItems[focusIndex];
        }
        return null;
    }
    /**
     * checks if there are any nested tree items
     */
    checkForNestedItems() {
        return this.slottedTreeItems.some((node) => {
            return (0,tree_item/* isTreeItemElement */.t)(node) && node.querySelector("[role='treeitem']");
        });
    }
    getVisibleNodes() {
        return (0,dist_dom/* getDisplayedNodes */.UM)(this, "[role='treeitem']") || [];
    }
}
(0,tslib_es6/* __decorate */.gn)([
    (0,attributes/* attr */.Lj)({ attribute: "render-collapsed-nodes" })
], TreeView.prototype, "renderCollapsedNodes", void 0);
(0,tslib_es6/* __decorate */.gn)([
    observable/* observable */.LO
], TreeView.prototype, "currentSelected", void 0);
(0,tslib_es6/* __decorate */.gn)([
    observable/* observable */.LO
], TreeView.prototype, "slottedTreeItems", void 0);

// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/templating/template.js + 3 modules
var template = __webpack_require__(25269);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/templating/ref.js
var ref = __webpack_require__(62564);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/templating/slotted.js
var slotted = __webpack_require__(17832);
;// CONCATENATED MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/tree-view/tree-view.template.js

/**
 * The template for the {@link @microsoft/fast-foundation#TreeView} component.
 * @public
 */
const treeViewTemplate = (context, definition) => (0,template/* html */.d) `
    <template
        role="tree"
        ${(0,ref/* ref */.i)("treeView")}
        @keydown="${(x, c) => x.handleKeyDown(c.event)}"
        @focusin="${(x, c) => x.handleFocus(c.event)}"
        @focusout="${(x, c) => x.handleBlur(c.event)}"
        @click="${(x, c) => x.handleClick(c.event)}"
        @selected-change="${(x, c) => x.handleSelectedChange(c.event)}"
    >
        <slot ${(0,slotted/* slotted */.Q)("slottedTreeItems")}></slot>
    </template>
`;

// EXTERNAL MODULE: ../node_modules/@microsoft/fast-element/dist/esm/styles/css.js
var css = __webpack_require__(12634);
// EXTERNAL MODULE: ../node_modules/@microsoft/fast-foundation/dist/esm/utilities/style/display.js
var display = __webpack_require__(21601);
;// CONCATENATED MODULE: ../node_modules/@jupyter/web-components/dist/esm/tree-view/tree-view.styles.js
// Copyright (c) Jupyter Development Team.
// Copyright (c) Microsoft Corporation.
// Distributed under the terms of the Modified BSD License.


/**
 * Styles for Tree View
 * @public
 */
const treeViewStyles = (context, definition) => (0,css/* css */.i) `
  ${(0,display/* display */.j)('flex')} :host {
    flex-direction: column;
    align-items: stretch;
    min-width: fit-content;
    font-size: 0;
  }

  :host:focus-visible {
    outline: none;
  }
`;

;// CONCATENATED MODULE: ../node_modules/@jupyter/web-components/dist/esm/tree-view/index.js
// Copyright (c) Jupyter Development Team.
// Copyright (c) Microsoft Corporation.
// Distributed under the terms of the Modified BSD License.


/**
 * Tree view class
 *
 * @public
 * @tagname jp-tree-view
 */
class JupyterTreeView extends TreeView {
    /**
     * Handles click events bubbling up
     *
     *  @internal
     */
    handleClick(e) {
        if (e.defaultPrevented) {
            // handled, do nothing
            return;
        }
        if (!(e.target instanceof Element)) {
            // not a tree item, ignore
            return true;
        }
        let item = e.target;
        while (item && !(0,tree_item/* isTreeItemElement */.t)(item)) {
            item = item.parentElement;
            // Escape if we get out of the tree view component
            if (item === this) {
                item = null;
            }
        }
        if (item && !item.disabled) {
            // Force selection - it is not possible to unselect
            item.selected = true;
        }
        return;
    }
}
/**
 * A function that returns a {@link @microsoft/fast-foundation#TreeView} registration for configuring the component with a DesignSystem.
 * Implements {@link @microsoft/fast-foundation#treeViewTemplate}
 *
 *
 * @public
 * @remarks
 * Generates HTML Element: `<jp-tree-view>`
 *
 */
const jpTreeView = JupyterTreeView.compose({
    baseName: 'tree-view',
    baseClass: TreeView,
    template: treeViewTemplate,
    styles: treeViewStyles
});


// EXTERNAL MODULE: consume shared module (default) react@~18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var index_js_ = __webpack_require__(78156);
var index_js_default = /*#__PURE__*/__webpack_require__.n(index_js_);
// EXTERNAL MODULE: ../node_modules/@jupyter/react-components/lib/react-utils.js
var react_utils = __webpack_require__(4444);
;// CONCATENATED MODULE: ../node_modules/@jupyter/react-components/lib/TreeView.js




(0,jupyter_design_system/* provideJupyterDesignSystem */.W)().register(jpTreeView());

const TreeView_TreeView = (0,index_js_.forwardRef)((props, forwardedRef) => {
  const ref = (0,index_js_.useRef)(null);
  const { className, renderCollapsedNodes, currentSelected, ...filteredProps } =
    props;

  (0,index_js_.useLayoutEffect)(() => {
    // Fix using private API to force refresh of nested flag on
    // first level of tree items.
    ref.current?.setItems();
  }, [ref.current]);

  /** Properties - run whenever a property has changed */
  (0,react_utils/* useProperties */.h)(ref, 'currentSelected', props.currentSelected);

  /** Methods - uses `useImperativeHandle` hook to pass ref to component */
  (0,index_js_.useImperativeHandle)(forwardedRef, () => ref.current, [ref.current]);

  return index_js_default().createElement(
    'jp-tree-view',
    {
      ref,
      ...filteredProps,
      class: props.className,
      exportparts: props.exportparts,
      for: props.htmlFor,
      part: props.part,
      tabindex: props.tabIndex,
      'render-collapsed-nodes': props.renderCollapsedNodes ? '' : undefined,
      style: { ...props.style }
    },
    props.children
  );
});


/***/ }),

/***/ 80189:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   k: () => (/* binding */ TreeItem),
/* harmony export */   t: () => (/* binding */ isTreeItemElement)
/* harmony export */ });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(95185);
/* harmony import */ var _microsoft_fast_element__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(98332);
/* harmony import */ var _microsoft_fast_element__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(92221);
/* harmony import */ var _microsoft_fast_web_utilities__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(99415);
/* harmony import */ var _patterns_start_end_js__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(52865);
/* harmony import */ var _utilities_apply_mixins_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(89155);
/* harmony import */ var _foundation_element_foundation_element_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(50755);






/**
 * check if the item is a tree item
 * @public
 * @remarks
 * determines if element is an HTMLElement and if it has the role treeitem
 */
function isTreeItemElement(el) {
    return (0,_microsoft_fast_web_utilities__WEBPACK_IMPORTED_MODULE_0__/* .isHTMLElement */ .Re)(el) && el.getAttribute("role") === "treeitem";
}
/**
 * A Tree item Custom HTML Element.
 *
 * @slot start - Content which can be provided before the tree item content
 * @slot end - Content which can be provided after the tree item content
 * @slot - The default slot for tree item text content
 * @slot item - The slot for tree items (fast tree items manage this assignment themselves)
 * @slot expand-collapse-button - The expand/collapse button
 * @csspart positioning-region - The element used to position the tree item content with exception of any child nodes
 * @csspart content-region - The element containing the expand/collapse, start, and end slots
 * @csspart items - The element wrapping any child items
 * @csspart expand-collapse-button - The expand/collapse button
 * @fires expanded-change - Fires a custom 'expanded-change' event when the expanded state changes
 * @fires selected-change - Fires a custom 'selected-change' event when the selected state changes
 *
 * @public
 */
class TreeItem extends _foundation_element_foundation_element_js__WEBPACK_IMPORTED_MODULE_1__/* .FoundationElement */ .I {
    constructor() {
        super(...arguments);
        /**
         * When true, the control will be appear expanded by user interaction.
         * @public
         * @remarks
         * HTML Attribute: expanded
         */
        this.expanded = false;
        /**
         * Whether the item is focusable
         *
         * @internal
         */
        this.focusable = false;
        /**
         * Whether the tree is nested
         *
         * @public
         */
        this.isNestedItem = () => {
            return isTreeItemElement(this.parentElement);
        };
        /**
         * Handle expand button click
         *
         * @internal
         */
        this.handleExpandCollapseButtonClick = (e) => {
            if (!this.disabled && !e.defaultPrevented) {
                this.expanded = !this.expanded;
            }
        };
        /**
         * Handle focus events
         *
         * @internal
         */
        this.handleFocus = (e) => {
            this.setAttribute("tabindex", "0");
        };
        /**
         * Handle blur events
         *
         * @internal
         */
        this.handleBlur = (e) => {
            this.setAttribute("tabindex", "-1");
        };
    }
    expandedChanged() {
        if (this.$fastController.isConnected) {
            this.$emit("expanded-change", this);
        }
    }
    selectedChanged() {
        if (this.$fastController.isConnected) {
            this.$emit("selected-change", this);
        }
    }
    itemsChanged(oldValue, newValue) {
        if (this.$fastController.isConnected) {
            this.items.forEach((node) => {
                if (isTreeItemElement(node)) {
                    // TODO: maybe not require it to be a TreeItem?
                    node.nested = true;
                }
            });
        }
    }
    /**
     * Places document focus on a tree item
     *
     * @public
     * @param el - the element to focus
     */
    static focusItem(el) {
        el.focusable = true;
        el.focus();
    }
    /**
     * Gets number of children
     *
     * @internal
     */
    childItemLength() {
        const treeChildren = this.childItems.filter((item) => {
            return isTreeItemElement(item);
        });
        return treeChildren ? treeChildren.length : 0;
    }
}
(0,tslib__WEBPACK_IMPORTED_MODULE_2__/* .__decorate */ .gn)([
    (0,_microsoft_fast_element__WEBPACK_IMPORTED_MODULE_3__/* .attr */ .Lj)({ mode: "boolean" })
], TreeItem.prototype, "expanded", void 0);
(0,tslib__WEBPACK_IMPORTED_MODULE_2__/* .__decorate */ .gn)([
    (0,_microsoft_fast_element__WEBPACK_IMPORTED_MODULE_3__/* .attr */ .Lj)({ mode: "boolean" })
], TreeItem.prototype, "selected", void 0);
(0,tslib__WEBPACK_IMPORTED_MODULE_2__/* .__decorate */ .gn)([
    (0,_microsoft_fast_element__WEBPACK_IMPORTED_MODULE_3__/* .attr */ .Lj)({ mode: "boolean" })
], TreeItem.prototype, "disabled", void 0);
(0,tslib__WEBPACK_IMPORTED_MODULE_2__/* .__decorate */ .gn)([
    _microsoft_fast_element__WEBPACK_IMPORTED_MODULE_4__/* .observable */ .LO
], TreeItem.prototype, "focusable", void 0);
(0,tslib__WEBPACK_IMPORTED_MODULE_2__/* .__decorate */ .gn)([
    _microsoft_fast_element__WEBPACK_IMPORTED_MODULE_4__/* .observable */ .LO
], TreeItem.prototype, "childItems", void 0);
(0,tslib__WEBPACK_IMPORTED_MODULE_2__/* .__decorate */ .gn)([
    _microsoft_fast_element__WEBPACK_IMPORTED_MODULE_4__/* .observable */ .LO
], TreeItem.prototype, "items", void 0);
(0,tslib__WEBPACK_IMPORTED_MODULE_2__/* .__decorate */ .gn)([
    _microsoft_fast_element__WEBPACK_IMPORTED_MODULE_4__/* .observable */ .LO
], TreeItem.prototype, "nested", void 0);
(0,tslib__WEBPACK_IMPORTED_MODULE_2__/* .__decorate */ .gn)([
    _microsoft_fast_element__WEBPACK_IMPORTED_MODULE_4__/* .observable */ .LO
], TreeItem.prototype, "renderCollapsedChildren", void 0);
(0,_utilities_apply_mixins_js__WEBPACK_IMPORTED_MODULE_5__/* .applyMixins */ .e)(TreeItem, _patterns_start_end_js__WEBPACK_IMPORTED_MODULE_6__/* .StartEnd */ .hW);


/***/ })

}]);
//# sourceMappingURL=2424.6f13f59f4bc472c3d07d.js.map?v=6f13f59f4bc472c3d07d