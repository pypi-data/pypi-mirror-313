"use strict";
(self["webpackChunk_amphi_ui_component"] = self["webpackChunk_amphi_ui_component"] || []).push([["lib_index_js"],{

/***/ "../../node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!*******************************************************************!*\
  !*** ../../node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \*******************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/sourceMaps.js */ "../../node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ "../../node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `/*-----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/

`, "",{"version":3,"sources":["webpack://./style/index.css"],"names":[],"mappings":"AAAA;;;8EAG8E","sourcesContent":["/*-----------------------------------------------------------------------------\n| Copyright (c) Jupyter Development Team.\n| Distributed under the terms of the Modified BSD License.\n|----------------------------------------------------------------------------*/\n\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../../node_modules/css-loader/dist/runtime/api.js":
/*!*********************************************************!*\
  !*** ../../node_modules/css-loader/dist/runtime/api.js ***!
  \*********************************************************/
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ "../../node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!****************************************************************!*\
  !*** ../../node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \****************************************************************/
/***/ ((module) => {



module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];
  if (!cssMapping) {
    return content;
  }
  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    return [content].concat([sourceMapping]).join("\n");
  }
  return [content].join("\n");
};

/***/ }),

/***/ "../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!********************************************************************************!*\
  !*** ../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \********************************************************************************/
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "../../node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!************************************************************************!*\
  !*** ../../node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \************************************************************************/
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ "../../node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**************************************************************************!*\
  !*** ../../node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**************************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ "../../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**************************************************************************************!*\
  !*** ../../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**************************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ "../../node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!*******************************************************************!*\
  !*** ../../node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \*******************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ "../../node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*************************************************************************!*\
  !*** ../../node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*************************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ }),

/***/ "./lib/BrowseFileDialog.js":
/*!*********************************!*\
  !*** ./lib/BrowseFileDialog.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   showBrowseFileDialog: () => (/* binding */ showBrowseFileDialog)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/*
 * Copyright 2018-2023 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */



const BROWSE_FILE_CLASS = 'elyra-browseFileDialog';
const BROWSE_FILE_OPEN_CLASS = 'elyra-browseFileDialog-open';
/**
 * Breadcrumbs widget for browse file dialog body.
 */
class BrowseFileDialogBreadcrumbs extends _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.BreadCrumbs {
    constructor(options) {
        super(options);
        this.model = options.model;
        this.rootPath = options.rootPath;
    }
    onUpdateRequest(msg) {
        super.onUpdateRequest(msg);
        const contents = this.model.manager.services.contents;
        const localPath = contents.localPath(this.model.path);
        // if 'rootPath' is defined prevent navigating to it's parent/grandparent directories
        if (localPath && this.rootPath && localPath.indexOf(this.rootPath) === 0) {
            const breadcrumbs = document.querySelectorAll('.elyra-browseFileDialog .jp-BreadCrumbs > span[title]');
            breadcrumbs.forEach((crumb) => {
                var _a;
                if (crumb.title.indexOf((_a = this.rootPath) !== null && _a !== void 0 ? _a : '') === 0) {
                    crumb.className = crumb.className
                        .replace('elyra-BreadCrumbs-disabled', '')
                        .trim();
                }
                else if (crumb.className.indexOf('elyra-BreadCrumbs-disabled') === -1) {
                    crumb.className += ' elyra-BreadCrumbs-disabled';
                }
            });
        }
    }
}
/**
 * Browse file widget for dialog body
 */
class BrowseFileDialog extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    constructor(props) {
        super(props);
        this.model = new _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.FilterFileBrowserModel({
            manager: props.manager,
            filter: props.filter
        });
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.PanelLayout());
        this.directoryListing = new _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.DirListing({
            model: this.model
        });
        this.acceptFileOnDblClick = props.acceptFileOnDblClick;
        this.multiselect = props.multiselect;
        this.includeDir = props.includeDir;
        this.dirListingHandleEvent = this.directoryListing.handleEvent;
        this.directoryListing.handleEvent = (event) => {
            this.handleEvent(event);
        };
        this.breadCrumbs = new BrowseFileDialogBreadcrumbs({
            model: this.model,
            rootPath: props.rootPath
        });
        layout.addWidget(this.breadCrumbs);
        layout.addWidget(this.directoryListing);
    }
    static async init(options) {
        const browseFileDialog = new BrowseFileDialog(options);
        if (options.startPath) {
            if (!options.rootPath ||
                options.startPath.indexOf(options.rootPath) === 0) {
                await browseFileDialog.model.cd(options.startPath);
            }
        }
        else if (options.rootPath) {
            await browseFileDialog.model.cd(options.rootPath);
        }
        return browseFileDialog;
    }
    getValue() {
        const selected = [];
        let item = null;
        for (const item of this.directoryListing.selectedItems()) {
            if (this.includeDir || item.type !== 'directory') {
                selected.push(item);
            }
        }
        return selected;
    }
    handleEvent(event) {
        let modifierKey = false;
        if (event instanceof MouseEvent) {
            modifierKey =
                event.shiftKey || event.metaKey;
        }
        else if (event instanceof KeyboardEvent) {
            modifierKey =
                event.shiftKey || event.metaKey;
        }
        switch (event.type) {
            case 'keydown':
            case 'keyup':
            case 'mousedown':
            case 'mouseup':
            case 'click':
                if (this.multiselect || !modifierKey) {
                    this.dirListingHandleEvent.call(this.directoryListing, event);
                }
                break;
            case 'dblclick': {
                const clickedItem = this.directoryListing.modelForClick(event);
                if ((clickedItem === null || clickedItem === void 0 ? void 0 : clickedItem.type) === 'directory') {
                    this.dirListingHandleEvent.call(this.directoryListing, event);
                }
                else {
                    event.preventDefault();
                    event.stopPropagation();
                    if (this.acceptFileOnDblClick) {
                        const okButton = document.querySelector(`.${BROWSE_FILE_OPEN_CLASS} .jp-mod-accept`);
                        if (okButton) {
                            okButton.click();
                        }
                    }
                }
                break;
            }
            default:
                this.dirListingHandleEvent.call(this.directoryListing, event);
                break;
        }
    }
}
const showBrowseFileDialog = async (manager, options) => {
    const browseFileDialogBody = await BrowseFileDialog.init({
        manager: manager,
        filter: options.filter,
        multiselect: options.multiselect,
        includeDir: options.includeDir,
        rootPath: options.rootPath,
        startPath: options.startPath,
        acceptFileOnDblClick: Object.prototype.hasOwnProperty.call(options, 'acceptFileOnDblClick')
            ? options.acceptFileOnDblClick
            : true
    });
    const dialog = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog({
        title: 'Select a file',
        body: browseFileDialogBody,
        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Select' })]
    });
    dialog.addClass(BROWSE_FILE_CLASS);
    document.body.className += ` ${BROWSE_FILE_OPEN_CLASS}`;
    return dialog.launch().then((result) => {
        document.body.className = document.body.className
            .replace(BROWSE_FILE_OPEN_CLASS, '')
            .trim();
        if (options.rootPath && result.button.accept && result.value.length) {
            const relativeToPath = options.rootPath.endsWith('/')
                ? options.rootPath
                : options.rootPath + '/';
            result.value.forEach((val) => {
                val.path = val.path.replace(relativeToPath, '');
            });
        }
        return result;
    });
};


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   alertCircleFillIcon: () => (/* binding */ alertCircleFillIcon),
/* harmony export */   alertDiamondIcon: () => (/* binding */ alertDiamondIcon),
/* harmony export */   amphiLogo: () => (/* binding */ amphiLogo),
/* harmony export */   asteriskIcon: () => (/* binding */ asteriskIcon),
/* harmony export */   bugIcon: () => (/* binding */ bugIcon),
/* harmony export */   codeIcon: () => (/* binding */ codeIcon),
/* harmony export */   docsIcon: () => (/* binding */ docsIcon),
/* harmony export */   githubIcon: () => (/* binding */ githubIcon),
/* harmony export */   networkIcon: () => (/* binding */ networkIcon),
/* harmony export */   pipelineIcon: () => (/* binding */ pipelineIcon),
/* harmony export */   pipelineNegativeIcon: () => (/* binding */ pipelineNegativeIcon),
/* harmony export */   shieldCheckedIcon: () => (/* binding */ shieldCheckedIcon),
/* harmony export */   slackIcon: () => (/* binding */ slackIcon),
/* harmony export */   squareIcon: () => (/* binding */ squareIcon),
/* harmony export */   uploadIcon: () => (/* binding */ uploadIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_amphi_square_logo_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/icons/amphi-square-logo.svg */ "./style/icons/amphi-square-logo.svg");
/* harmony import */ var _style_icons_amphi_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/icons/amphi.svg */ "./style/icons/amphi.svg");
/* harmony import */ var _style_icons_pipeline_16_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/icons/pipeline-16.svg */ "./style/icons/pipeline-16.svg");
/* harmony import */ var _style_icons_shield_check_24_svg__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../style/icons/shield-check-24.svg */ "./style/icons/shield-check-24.svg");
/* harmony import */ var _style_icons_code_16_svg__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../style/icons/code-16.svg */ "./style/icons/code-16.svg");
/* harmony import */ var _style_icons_docs_16_svg__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../style/icons/docs-16.svg */ "./style/icons/docs-16.svg");
/* harmony import */ var _style_icons_upload_16_svg__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../style/icons/upload-16.svg */ "./style/icons/upload-16.svg");
/* harmony import */ var _style_icons_network_24_svg__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../style/icons/network-24.svg */ "./style/icons/network-24.svg");
/* harmony import */ var _style_icons_bug_16_svg__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../style/icons/bug-16.svg */ "./style/icons/bug-16.svg");
/* harmony import */ var _style_icons_github_svg__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../style/icons/github.svg */ "./style/icons/github.svg");
/* harmony import */ var _style_icons_slack_svg__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../style/icons/slack.svg */ "./style/icons/slack.svg");
/* harmony import */ var _style_icons_alert_circle_fill_24_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/icons/alert-circle-fill-24.svg */ "./style/icons/alert-circle-fill-24.svg");
/* harmony import */ var _style_icons_alert_diamond_24_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/icons/alert-diamond-24.svg */ "./style/icons/alert-diamond-24.svg");















const alertDiamondIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:alertDiamond-icon',
    svgstr: _style_icons_alert_diamond_24_svg__WEBPACK_IMPORTED_MODULE_1__
});
const alertCircleFillIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:alertCircleFill-icon',
    svgstr: _style_icons_alert_circle_fill_24_svg__WEBPACK_IMPORTED_MODULE_2__
});
const asteriskIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:asterisk-icon',
    svgstr: _style_icons_amphi_square_logo_svg__WEBPACK_IMPORTED_MODULE_3__
});
const squareIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:square-icon',
    svgstr: _style_icons_amphi_square_logo_svg__WEBPACK_IMPORTED_MODULE_3__
});
const amphiLogo = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:logo',
    svgstr: _style_icons_amphi_svg__WEBPACK_IMPORTED_MODULE_4__
});
const pipelineIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:pipeline-icon',
    svgstr: _style_icons_pipeline_16_svg__WEBPACK_IMPORTED_MODULE_5__
});
const pipelineNegativeIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:pipelinenegative-icon',
    svgstr: _style_icons_pipeline_16_svg__WEBPACK_IMPORTED_MODULE_5__
});
const shieldCheckedIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:shieldchecked-icon',
    svgstr: _style_icons_shield_check_24_svg__WEBPACK_IMPORTED_MODULE_6__
});
const codeIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:code-icon',
    svgstr: _style_icons_code_16_svg__WEBPACK_IMPORTED_MODULE_7__
});
const docsIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:docs-icon',
    svgstr: _style_icons_docs_16_svg__WEBPACK_IMPORTED_MODULE_8__
});
const uploadIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:upload-icon',
    svgstr: _style_icons_upload_16_svg__WEBPACK_IMPORTED_MODULE_9__
});
const networkIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:network-icon',
    svgstr: _style_icons_network_24_svg__WEBPACK_IMPORTED_MODULE_10__
});
const bugIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:bug-icon',
    svgstr: _style_icons_bug_16_svg__WEBPACK_IMPORTED_MODULE_11__
});
const githubIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:github-icon',
    svgstr: _style_icons_github_svg__WEBPACK_IMPORTED_MODULE_12__
});
const slackIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:slack-icon',
    svgstr: _style_icons_slack_svg__WEBPACK_IMPORTED_MODULE_13__
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   alertCircleFillIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.alertCircleFillIcon),
/* harmony export */   alertDiamondIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.alertDiamondIcon),
/* harmony export */   amphiLogo: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.amphiLogo),
/* harmony export */   asteriskIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.asteriskIcon),
/* harmony export */   bugIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.bugIcon),
/* harmony export */   codeIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.codeIcon),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   docsIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.docsIcon),
/* harmony export */   githubIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.githubIcon),
/* harmony export */   networkIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.networkIcon),
/* harmony export */   pipelineIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.pipelineIcon),
/* harmony export */   pipelineNegativeIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.pipelineNegativeIcon),
/* harmony export */   shieldCheckedIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.shieldCheckedIcon),
/* harmony export */   showBrowseFileDialog: () => (/* reexport safe */ _BrowseFileDialog__WEBPACK_IMPORTED_MODULE_8__.showBrowseFileDialog),
/* harmony export */   slackIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.slackIcon),
/* harmony export */   squareIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.squareIcon),
/* harmony export */   uploadIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.uploadIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _launcher__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./launcher */ "./lib/launcher.js");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _BrowseFileDialog__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./BrowseFileDialog */ "./lib/BrowseFileDialog.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");












/**
 * The main application icon.
 */
const logo = {
    id: '@amphi/ui-component:logo',
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    autoStart: true,
    activate: (app, labShell) => {
        let logo = null;
        if (labShell) {
            logo = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Widget();
            _icons__WEBPACK_IMPORTED_MODULE_10__.asteriskIcon.element({
                container: logo.node,
                elementPosition: 'center',
                margin: '2px 2px 2px 16px',
                height: '16px',
                width: '16px'
            });
        }
        if (logo) {
            logo.id = 'jp-MainLogo';
            app.shell.add(logo, 'top', { rank: 0 });
        }
    }
};
/**
 * The command IDs used by the launcher plugin.
 */
const CommandIDs = {
    create: 'launcher:create'
};
/**
 * The main launcher.
 */
const launcher = {
    id: '@amphi/ui-component:launcher',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1__.IMainMenu],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__.ICommandPalette],
    provides: _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.ILauncher,
    activate: (app, translator, labShell, mainMenu, manager, palette) => {
        console.log('Amphi - custom Launcher is activated!');
        /** */
        // Use custom Amphi launcher
        const { commands, shell } = app;
        const trans = translator.load('jupyterlab');
        const model = new _launcher__WEBPACK_IMPORTED_MODULE_11__.LauncherModel();
        console.log('Amphi - theme before adding launcher:create');
        commands.addCommand(CommandIDs.create, {
            label: trans.__('New'),
            execute: (args) => {
                const cwd = args['cwd'] ? String(args['cwd']) : '';
                const id = `launcher-${Private.id++}`;
                const callback = (item) => {
                    labShell.add(item, 'main', { ref: id });
                };
                const launcher = new _launcher__WEBPACK_IMPORTED_MODULE_11__.Launcher({
                    model,
                    cwd,
                    callback,
                    commands,
                    translator
                }, commands);
                launcher.model = model;
                launcher.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.homeIcon;
                launcher.title.label = trans.__('Homepage');
                const main = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__.MainAreaWidget({ content: launcher });
                // If there are any other widgets open, remove the launcher close icon.
                main.title.closable = !!(0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__.toArray)(labShell.widgets('main')).length;
                main.id = id;
                shell.add(main, 'main', {
                    activate: args['activate'],
                    ref: args['ref']
                });
                labShell.layoutModified.connect(() => {
                    // If there is only a launcher open, remove the close icon.
                    main.title.closable = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__.toArray)(labShell.widgets('main')).length > 1;
                }, main);
                return main;
            }
        });
        if (palette) {
            palette.addItem({
                command: CommandIDs.create,
                category: trans.__('Homepage')
            });
        }
        /**
         * This function seems to set up and handle the behavior of an "add" button within a JupyterLab-like environment.
         * When the button is clicked (or an "add" action is requested), the function determines
         * which tab or panel the action was requested from and then executes a command to handle the request,
         * either by creating a main launcher or by performing another default "create" action.
         */
        if (labShell) {
            labShell.addButtonEnabled = true;
            labShell.addRequested.connect((sender, arg) => {
                var _a;
                // Get the ref for the current tab of the tabbar which the add button was clicked
                const ref = ((_a = arg.currentTitle) === null || _a === void 0 ? void 0 : _a.owner.id) ||
                    arg.titles[arg.titles.length - 1].owner.id;
                if (commands.hasCommand('filebrowser:create-main-launcher')) {
                    // If a file browser is defined connect the launcher to it
                    return commands.execute('filebrowser:create-main-launcher', {
                        ref
                    });
                }
                return commands.execute(CommandIDs.create, { ref });
            });
        }
        return model;
    }
};
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * The incrementing id used for launcher widgets.
     */
    // eslint-disable-next-line
    Private.id = 0;
})(Private || (Private = {}));
const plugins = [logo, launcher];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);



/***/ }),

/***/ "./lib/launcher.js":
/*!*************************!*\
  !*** ./lib/launcher.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Launcher: () => (/* binding */ Launcher),
/* harmony export */   LauncherModel: () => (/* binding */ LauncherModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);




// Largely inspired by Elyra launcher https://github.com/elyra-ai/elyra
/**
 * The known categories of launcher items and their default ordering.
 */
const AMPHI_CATEGORY = 'Data Integration';
const CommandIDs = {
    newPipeline: 'pipeline-editor:create-new',
    newFile: 'fileeditor:create-new',
    createNewPythonEditor: 'script-editor:create-new-python-editor',
    createNewREditor: 'script-editor:create-new-r-editor'
};
// LauncherModel deals with the underlying data and logic of the launcher (what items are available, their order, etc.).
class LauncherModel extends _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_0__.LauncherModel {
    /**
     * Return an iterator of launcher items, but remove unnecessary items.
     */
    items() {
        const items = [];
        let pyEditorInstalled = false;
        let rEditorInstalled = false;
        this.itemsList.forEach(item => {
            if (item.command === CommandIDs.createNewPythonEditor) {
                pyEditorInstalled = true;
            }
            else if (item.command === CommandIDs.createNewREditor) {
                rEditorInstalled = true;
            }
        });
        if (!pyEditorInstalled && !rEditorInstalled) {
            return this.itemsList[Symbol.iterator]();
        }
        // Dont add tiles for new py and r files if their script editor is installed
        this.itemsList.forEach(item => {
            var _a, _b;
            if (!(item.command === CommandIDs.newFile &&
                ((pyEditorInstalled && ((_a = item.args) === null || _a === void 0 ? void 0 : _a.fileExt) === 'py') ||
                    (rEditorInstalled && ((_b = item.args) === null || _b === void 0 ? void 0 : _b.fileExt) === 'r')))) {
                items.push(item);
            }
        });
        return items[Symbol.iterator]();
    }
}
// Launcher deals with the visual representation and user interactions of the launcher
// (how items are displayed, icons, categories, etc.).
class Launcher extends _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_0__.Launcher {
    /**
     * Construct a new launcher widget.
     */
    constructor(options, commands) {
        super(options);
        this.myCommands = commands;
        // this._translator = this.translator.load('jupyterlab');
    }
    /**
    The replaceCategoryIcon function takes a category element and a new icon.
    It then goes through the children of the category to find the section header.
    Within the section header, it identifies the icon (by checking if it's not the section title)
    and replaces it with the new icon. The function then returns a cloned version of the original
    category with the icon replaced.
     */
    replaceCategoryIcon(category, icon) {
        const children = react__WEBPACK_IMPORTED_MODULE_2___default().Children.map(category.props.children, child => {
            if (child.props.className === 'jp-Launcher-sectionHeader') {
                const grandchildren = react__WEBPACK_IMPORTED_MODULE_2___default().Children.map(child.props.children, grandchild => {
                    if (grandchild.props.className !== 'jp-Launcher-sectionTitle') {
                        return react__WEBPACK_IMPORTED_MODULE_2___default().createElement(icon.react, { stylesheet: "launcherSection" });
                    }
                    else {
                        return grandchild;
                    }
                });
                return react__WEBPACK_IMPORTED_MODULE_2___default().cloneElement(child, child.props, grandchildren);
            }
            else {
                return child;
            }
        });
        return react__WEBPACK_IMPORTED_MODULE_2___default().cloneElement(category, category.props, children);
    }
    /**
     * Render the launcher to virtual DOM nodes.
     */
    render() {
        if (!this.model) {
            return null;
        }
        const launcherBody = super.render();
        const launcherContent = launcherBody === null || launcherBody === void 0 ? void 0 : launcherBody.props.children;
        const launcherCategories = launcherContent.props.children;
        const categories = [];
        const knownCategories = [
            AMPHI_CATEGORY,
            // this._translator.__('Console'),
            // this._translator.__('Other'),
            // this._translator.__('Notebook')
        ];
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.each)(knownCategories, (category, index) => {
            react__WEBPACK_IMPORTED_MODULE_2___default().Children.forEach(launcherCategories, (cat) => {
                if (cat.key === category) {
                    if (cat.key === AMPHI_CATEGORY) {
                        cat = this.replaceCategoryIcon(cat, _icons__WEBPACK_IMPORTED_MODULE_3__.pipelineIcon);
                    }
                    categories.push(cat);
                }
            });
        });
        const handleNewPipelineClick = () => {
            this.myCommands.execute('pipeline-editor:create-new');
        };
        const handleUploadFiles = () => {
            this.myCommands.execute('ui-components:file-upload');
        };
        const AlertBox = () => {
            const [isVisible, setIsVisible] = (0,react__WEBPACK_IMPORTED_MODULE_2__.useState)(false);
            (0,react__WEBPACK_IMPORTED_MODULE_2__.useEffect)(() => {
                const alertClosed = localStorage.getItem('alertClosed') === 'true';
                setIsVisible(!alertClosed);
            }, []);
            const closeAlert = () => {
                setIsVisible(false);
                localStorage.setItem('alertClosed', 'true');
            };
            if (!isVisible)
                return null;
            return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "alert-box" },
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "alert-content" },
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("span", { className: "alert-icon" },
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_3__.alertDiamondIcon.react, null)),
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "alert-text" },
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("h2", null, "About"),
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", null,
                            "Welcome to Amphi's demo playground! Explore Amphi ETL's capabilities and user experience here. ",
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("br", null),
                            "Note that ",
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("b", null, "executing pipelines is not supported in this environment."),
                            " For full functionality, install Amphi \u2014 it's free and open source.",
                            ' ',
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("a", { href: "https://github.com/amphi-ai/amphi-etl", target: "_blank" }, "Learn more."))),
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("button", { onClick: closeAlert, className: "alert-close-btn" },
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("span", { className: "sr-only" }, "Dismiss popup"),
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("svg", { xmlns: "http://www.w3.org/2000/svg", fill: "none", viewBox: "0 0 24 24", strokeWidth: "1.5", stroke: "currentColor" },
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", d: "M6 18L18 6M6 6l12 12" }))))));
        };
        return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "launcher-body" },
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "launcher-content" },
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("h1", { className: "launcher-title" }, "Amphi"),
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "launcher-grid" },
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "launcher-card" },
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "launcher-card-header" },
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("h3", null, "Start")),
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("ul", { className: "launcher-card-list" },
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("li", null,
                                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("a", { href: "#", onClick: handleNewPipelineClick, className: "launcher-card-item" },
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "launcher-icon" },
                                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_3__.pipelineIcon.react, { fill: "#5A8F7B" })),
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", null,
                                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("strong", null, "New pipeline"),
                                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", null, "Open a new untitled pipeline and drag and drop components to design and develop your data flow.")))))),
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "launcher-card" },
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "launcher-card-header" },
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("h3", null, "Resources")),
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("ul", { className: "launcher-card-list" },
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("li", null,
                                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("a", { href: "https://github.com/amphi-ai/amphi-etl", target: "_blank", className: "launcher-card-item" },
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "launcher-icon" },
                                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_3__.githubIcon.react, null)),
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", null,
                                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("strong", null, "Issues and feature requests"),
                                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", null, "Report issues and suggest features on GitHub. Don't hesitate to star the repository to watch the repository.")))),
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("li", null,
                                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("a", { href: "https://join.slack.com/t/amphi-ai/shared_invite/zt-2ci2ptvoy-FENw8AW4ISDXUmz8wcd3bw", target: "_blank", className: "launcher-card-item" },
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "launcher-icon" },
                                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_3__.slackIcon.react, null)),
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", null,
                                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("strong", null, "Join the Community"),
                                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", null, "Join Amphi's community on Slack: seek help, ask questions and share your experience."))))))))));
    }
}


/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "../../node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/insertBySelector.js */ "../../node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "../../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "../../node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "../../node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./index.css */ "../../node_modules/css-loader/dist/cjs.js!./style/index.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/icons/alert-circle-fill-24.svg":
/*!**********************************************!*\
  !*** ./style/icons/alert-circle-fill-24.svg ***!
  \**********************************************/
/***/ ((module) => {

module.exports = "<svg width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<g id=\"size=24\">\n<path id=\"Path\" fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M12 1C5.92487 1 1 5.92487 1 12C1 18.0751 5.92487 23 12 23C18.0751 23 23 18.0751 23 12C23 5.92487 18.0751 1 12 1ZM11.25 7.75C11.25 7.33579 11.5858 7 12 7C12.4142 7 12.75 7.33579 12.75 7.75V12.25C12.75 12.6642 12.4142 13 12 13C11.5858 13 11.25 12.6642 11.25 12.25V7.75ZM11 16C11 15.4477 11.4477 15 12 15H12.01C12.5623 15 13.01 15.4477 13.01 16C13.01 16.5523 12.5623 17 12.01 17H12C11.4477 17 11 16.5523 11 16Z\" fill=\"#000001\"/>\n</g>\n</svg>\n";

/***/ }),

/***/ "./style/icons/alert-diamond-24.svg":
/*!******************************************!*\
  !*** ./style/icons/alert-diamond-24.svg ***!
  \******************************************/
/***/ ((module) => {

module.exports = "<svg width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<g id=\"size=24\">\n<g id=\"Path\">\n<path d=\"M12 7C12.4143 7 12.75 7.33579 12.75 7.75V12.25C12.75 12.6642 12.4143 13 12 13C11.5858 13 11.25 12.6642 11.25 12.25V7.75C11.25 7.33579 11.5858 7 12 7Z\" fill=\"#000001\"/>\n<path d=\"M12 15C11.4478 15 11 15.4477 11 16C11 16.5523 11.4478 17 12 17H12.01C12.5623 17 13.01 16.5523 13.01 16C13.01 15.4477 12.5623 15 12.01 15H12Z\" fill=\"#000001\"/>\n<path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M1.88382 10.0558L10.0555 1.88415C11.1294 0.810196 12.8707 0.810205 13.9446 1.88417L22.1161 10.0558C23.19 11.1298 23.19 12.871 22.1161 13.9449L13.9446 22.1164C12.8706 23.1903 11.1295 23.1903 10.0555 22.1164L1.88385 13.9449C0.809886 12.871 0.809874 11.1298 1.88382 10.0558ZM11.1161 2.94481L2.94448 11.1165C2.45633 11.6046 2.45633 12.3961 2.9445 12.8842L11.1162 21.0557C11.6043 21.5439 12.3958 21.5439 12.8839 21.0557L21.0554 12.8842C21.5435 12.3961 21.5436 11.6046 21.0554 11.1165L12.8839 2.94482C12.3958 2.45665 11.6043 2.45665 11.1161 2.94481Z\" fill=\"#000001\"/>\n</g>\n</g>\n</svg>\n";

/***/ }),

/***/ "./style/icons/amphi-square-logo.svg":
/*!*******************************************!*\
  !*** ./style/icons/amphi-square-logo.svg ***!
  \*******************************************/
/***/ ((module) => {

module.exports = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   width=\"16\"\n   height=\"16\"\n   viewBox=\"0 0 4.2333334 4.2333334\"\n   version=\"1.1\"\n   id=\"svg1\"\n   inkscape:version=\"1.3 (0e150ed, 2023-07-21)\"\n   sodipodi:docname=\"amphi-square-logo.svg\"\n   inkscape:export-filename=\"../../../../../../../Desktop/ProductHunt/amphi-square-logo.png\"\n   inkscape:export-xdpi=\"1462.0128\"\n   inkscape:export-ydpi=\"1462.0128\"\n   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"\n   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"\n   xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   xmlns:svg=\"http://www.w3.org/2000/svg\">\n  <sodipodi:namedview\n     id=\"namedview1\"\n     pagecolor=\"#505050\"\n     bordercolor=\"#eeeeee\"\n     borderopacity=\"1\"\n     inkscape:showpageshadow=\"0\"\n     inkscape:pageopacity=\"0\"\n     inkscape:pagecheckerboard=\"0\"\n     inkscape:deskcolor=\"#505050\"\n     inkscape:document-units=\"mm\"\n     inkscape:zoom=\"23.064727\"\n     inkscape:cx=\"20.312401\"\n     inkscape:cy=\"13.700574\"\n     inkscape:window-width=\"1512\"\n     inkscape:window-height=\"875\"\n     inkscape:window-x=\"0\"\n     inkscape:window-y=\"639\"\n     inkscape:window-maximized=\"1\"\n     inkscape:current-layer=\"layer1\" />\n  <defs\n     id=\"defs1\">\n    <linearGradient\n       id=\"linearGradient14\"\n       inkscape:collect=\"always\">\n      <stop\n         style=\"stop-color:#000000;stop-opacity:1;\"\n         offset=\"0\"\n         id=\"stop14\" />\n      <stop\n         style=\"stop-color:#000000;stop-opacity:0;\"\n         offset=\"1\"\n         id=\"stop15\" />\n    </linearGradient>\n    <linearGradient\n       id=\"swatch12\"\n       inkscape:swatch=\"solid\">\n      <stop\n         style=\"stop-color:#000000;stop-opacity:1;\"\n         offset=\"0\"\n         id=\"stop13\" />\n    </linearGradient>\n    <rect\n       x=\"123.66742\"\n       y=\"261.60416\"\n       width=\"85.379112\"\n       height=\"35.370846\"\n       id=\"rect1\" />\n    <linearGradient\n       inkscape:collect=\"always\"\n       xlink:href=\"#linearGradient14\"\n       id=\"linearGradient15\"\n       x1=\"124.86797\"\n       y1=\"278.84354\"\n       x2=\"205.72131\"\n       y2=\"278.84354\"\n       gradientUnits=\"userSpaceOnUse\" />\n  </defs>\n  <g\n     inkscape:label=\"Layer 1\"\n     inkscape:groupmode=\"layer\"\n     id=\"layer1\"\n     transform=\"translate(-43.459922,-57.723277)\">\n    <path\n       d=\"M 47.661386,61.82914 H 47.06573 v -0.5883 q -0.654488,0.720669 -1.507527,0.720669 -0.853036,0 -1.4634,-0.625072 -0.603011,-0.632423 -0.603011,-1.500169 0,-0.8751 0.610365,-1.492817 0.610362,-0.625072 1.485463,-0.625072 0.882452,0 1.47811,0.713317 v -0.610364 h 0.595656 z m -2.05906,-0.43387 q 0.610365,0 1.051591,-0.441227 0.441227,-0.441229 0.441227,-1.095714 0,-0.661842 -0.433872,-1.103068 -0.433874,-0.448581 -1.066297,-0.448581 -0.625072,0 -1.058947,0.463291 -0.433871,0.455933 -0.433871,1.081003 0,0.625072 0.441226,1.08836 0.441226,0.455936 1.058943,0.455936 z\"\n       id=\"text1\"\n       style=\"font-size:26.6667px;font-family:'Heiti SC';-inkscape-font-specification:'Heiti SC, Normal';white-space:pre;fill:#5a8f7b;stroke-width:0.275766\"\n       aria-label=\"a\" />\n  </g>\n</svg>\n";

/***/ }),

/***/ "./style/icons/amphi.svg":
/*!*******************************!*\
  !*** ./style/icons/amphi.svg ***!
  \*******************************/
/***/ ((module) => {

module.exports = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   width=\"21.392445mm\"\n   height=\"6.6533971mm\"\n   viewBox=\"0 0 21.392445 6.6533971\"\n   version=\"1.1\"\n   id=\"svg1\"\n   inkscape:version=\"1.3 (0e150ed, 2023-07-21)\"\n   sodipodi:docname=\"amphi.svg\"\n   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"\n   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"\n   xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   xmlns:svg=\"http://www.w3.org/2000/svg\">\n  <sodipodi:namedview\n     id=\"namedview1\"\n     pagecolor=\"#505050\"\n     bordercolor=\"#eeeeee\"\n     borderopacity=\"1\"\n     inkscape:showpageshadow=\"0\"\n     inkscape:pageopacity=\"0\"\n     inkscape:pagecheckerboard=\"0\"\n     inkscape:deskcolor=\"#505050\"\n     inkscape:document-units=\"mm\"\n     inkscape:zoom=\"6.1387102\"\n     inkscape:cx=\"40.399366\"\n     inkscape:cy=\"10.751444\"\n     inkscape:window-width=\"1312\"\n     inkscape:window-height=\"713\"\n     inkscape:window-x=\"73\"\n     inkscape:window-y=\"186\"\n     inkscape:window-maximized=\"0\"\n     inkscape:current-layer=\"layer1\" />\n  <defs\n     id=\"defs1\">\n    <linearGradient\n       id=\"linearGradient14\"\n       inkscape:collect=\"always\">\n      <stop\n         style=\"stop-color:#000000;stop-opacity:1;\"\n         offset=\"0\"\n         id=\"stop14\" />\n      <stop\n         style=\"stop-color:#000000;stop-opacity:0;\"\n         offset=\"1\"\n         id=\"stop15\" />\n    </linearGradient>\n    <linearGradient\n       id=\"swatch12\"\n       inkscape:swatch=\"solid\">\n      <stop\n         style=\"stop-color:#000000;stop-opacity:1;\"\n         offset=\"0\"\n         id=\"stop13\" />\n    </linearGradient>\n    <rect\n       x=\"123.66742\"\n       y=\"261.60416\"\n       width=\"85.379112\"\n       height=\"35.370846\"\n       id=\"rect1\" />\n    <linearGradient\n       inkscape:collect=\"always\"\n       xlink:href=\"#linearGradient14\"\n       id=\"linearGradient15\"\n       x1=\"124.86797\"\n       y1=\"278.84354\"\n       x2=\"205.72131\"\n       y2=\"278.84354\"\n       gradientUnits=\"userSpaceOnUse\" />\n  </defs>\n  <g\n     inkscape:label=\"Layer 1\"\n     inkscape:groupmode=\"layer\"\n     id=\"layer1\"\n     transform=\"translate(-43.459922,-56.375664)\">\n    <text\n       xml:space=\"preserve\"\n       transform=\"matrix(0.26458333,0,0,0.26458333,10.421939,-14.074989)\"\n       id=\"text1\"\n       style=\"font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:26.6667px;font-family:'Heiti SC';-inkscape-font-specification:'Heiti SC, Normal';font-variant-ligatures:normal;font-variant-caps:normal;font-variant-numeric:normal;font-variant-east-asian:normal;white-space:pre;shape-inside:url(#rect1);fill:#5a8f7b;fill-opacity:1;fill-rule:nonzero\"><tspan\n         x=\"123.66797\"\n         y=\"287.87022\"\n         id=\"tspan1\">amphi</tspan></text>\n  </g>\n</svg>\n";

/***/ }),

/***/ "./style/icons/bug-16.svg":
/*!********************************!*\
  !*** ./style/icons/bug-16.svg ***!
  \********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M10.136.803a.75.75 0 011.061 1.06l-.415.416C11.525 2.932 12 3.853 12 4.909c0 .103-.005.205-.014.306.094.016.173.03.238.045a.973.973 0 01.776.951V6.6l1.571-.629a.75.75 0 01.557 1.393L13 8.214v1.13l1.849.246a.75.75 0 11-.198 1.487l-1.659-.221a3.935 3.935 0 01-.426 1.555l2.364.887a.75.75 0 01-.527 1.404l-2.667-1a.752.752 0 01-.12-.058C10.687 14.491 9.384 15 8 15s-2.687-.509-3.616-1.356a.752.752 0 01-.12.058l-2.667 1a.75.75 0 11-.527-1.404l2.364-.887a3.935 3.935 0 01-.426-1.555l-1.659.22a.75.75 0 01-.198-1.486L3 9.343V8.174L.971 7.363a.75.75 0 01.557-1.393L3 6.56V6.21c0-.474.334-.854.776-.95.065-.015.144-.03.238-.046C4.004 5.114 4 5.012 4 4.909c0-1.056.475-1.977 1.218-2.63l-.415-.415A.75.75 0 015.863.803l.695.694a4.318 4.318 0 012.884 0l.694-.694zm-4.63 4.26C6.133 5.026 6.946 5 8 5c1.054 0 1.867.026 2.494.063.004-.051.006-.102.006-.154C10.5 3.793 9.461 2.75 8 2.75S5.5 3.793 5.5 4.91c0 .05.002.102.006.153zM4.5 7.652v-.994C5.043 6.586 6.093 6.5 8 6.5s2.957.086 3.5.158v3.949c0 1.494-1.454 2.893-3.5 2.893-2.046 0-3.5-1.4-3.5-2.893v-.59-2.335-.03z\" clip-rule=\"evenodd\"/></svg>";

/***/ }),

/***/ "./style/icons/code-16.svg":
/*!*********************************!*\
  !*** ./style/icons/code-16.svg ***!
  \*********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><g fill=\"currentColor\"><path d=\"M9.424 2.02a.75.75 0 00-.904.556l-2.5 10.5a.75.75 0 001.46.348l2.5-10.5a.75.75 0 00-.556-.904zM11.2 4.24a.75.75 0 011.06-.04l3.5 3.25a.75.75 0 010 1.1l-3.5 3.25a.75.75 0 11-1.02-1.1L14.148 8 11.24 5.3a.75.75 0 01-.04-1.06zM4.76 5.3a.75.75 0 00-1.02-1.1L.24 7.45a.75.75 0 000 1.1l3.5 3.25a.75.75 0 101.02-1.1L1.852 8 4.76 5.3z\"/></g></svg>";

/***/ }),

/***/ "./style/icons/docs-16.svg":
/*!*********************************!*\
  !*** ./style/icons/docs-16.svg ***!
  \*********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M4.25 1A2.25 2.25 0 002 3.25v9.5A2.25 2.25 0 004.25 15h8.5c.69 0 1.25-.56 1.25-1.25V2.25C14 1.56 13.44 1 12.75 1h-8.5zM3.5 12.75c0 .414.336.75.75.75h8.25v-2H4.25a.75.75 0 00-.75.75v.5zm0-2.622c.235-.083.487-.128.75-.128h8.25V2.5H4.25a.75.75 0 00-.75.75v6.878z\" clip-rule=\"evenodd\"/></svg>";

/***/ }),

/***/ "./style/icons/github.svg":
/*!********************************!*\
  !*** ./style/icons/github.svg ***!
  \********************************/
/***/ ((module) => {

module.exports = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<svg\n   width=\"16\"\n   height=\"16\"\n   viewBox=\"0 0 16 16\"\n   fill=\"none\"\n   version=\"1.1\"\n   id=\"svg1\"\n   sodipodi:docname=\"github.svg\"\n   inkscape:version=\"1.3 (0e150ed, 2023-07-21)\"\n   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"\n   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   xmlns:svg=\"http://www.w3.org/2000/svg\">\n  <defs\n     id=\"defs1\" />\n  <sodipodi:namedview\n     id=\"namedview1\"\n     pagecolor=\"#505050\"\n     bordercolor=\"#eeeeee\"\n     borderopacity=\"1\"\n     inkscape:showpageshadow=\"0\"\n     inkscape:pageopacity=\"0\"\n     inkscape:pagecheckerboard=\"0\"\n     inkscape:deskcolor=\"#505050\"\n     inkscape:zoom=\"22.761807\"\n     inkscape:cx=\"9.6653136\"\n     inkscape:cy=\"3.0972937\"\n     inkscape:window-width=\"1512\"\n     inkscape:window-height=\"856\"\n     inkscape:window-x=\"0\"\n     inkscape:window-y=\"639\"\n     inkscape:window-maximized=\"1\"\n     inkscape:current-layer=\"svg1\" />\n  <path\n     fill-rule=\"evenodd\"\n     clip-rule=\"evenodd\"\n     d=\"M 8.012013,0.18564182 C 3.5853759,0.18564182 0,3.7710177 0,8.1976548 0,11.74297 2.2934387,14.737462 5.4782139,15.799053 c 0.4006007,0.07011 0.550826,-0.170255 0.550826,-0.380571 0,-0.190286 -0.01001,-0.821232 -0.01001,-1.492238 C 4.0060066,14.2968 3.4852256,13.435508 3.3249854,12.984833 3.2348499,12.754488 2.8442646,12.043421 2.5037541,11.853136 2.2233337,11.702911 1.8227329,11.332355 2.4937342,11.322339 c 0.630946,-0.01001 1.0816218,0.580873 1.2318471,0.821233 0.7210812,1.211817 1.872808,0.871305 2.3334988,0.660991 0.070106,-0.520782 0.2804203,-0.871307 0.5107657,-1.071607 -1.7826729,-0.200301 -3.6454659,-0.891337 -3.6454659,-3.9559319 0,-0.8713064 0.3104655,-1.5923875 0.8212313,-2.1532284 -0.08012,-0.2003004 -0.3605405,-1.0215317 0.08012,-2.1231835 0,0 0.6710061,-0.2103153 2.2033036,0.8212314 0.640961,-0.1802704 1.3219821,-0.2704055 2.0030033,-0.2704055 0.6810215,0 1.3620422,0.090136 2.0030029,0.2704055 1.532298,-1.0415618 2.203304,-0.8212314 2.203304,-0.8212314 0.440661,1.1016518 0.160241,1.9228831 0.08012,2.1231835 0.510765,0.5608409 0.82123,1.271907 0.82123,2.1532284 0,3.0746099 -1.872808,3.7556309 -3.6554799,3.9559319 0.2904354,0.250375 0.5408109,0.731096 0.5408109,1.482223 0,1.071606 -0.01002,1.932898 -0.01002,2.203303 0,0.210316 0.150226,0.460691 0.550826,0.380571 3.164749,-1.061591 5.458188,-4.066097 5.458188,-7.6013982 6e-6,-4.4266371 -3.585369,-8.01201298 -8.012007,-8.01201298 z\"\n     fill=\"#1b1f23\"\n     id=\"path1\"\n     style=\"stroke-width:1.0015\" />\n</svg>\n";

/***/ }),

/***/ "./style/icons/network-24.svg":
/*!************************************!*\
  !*** ./style/icons/network-24.svg ***!
  \************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M10.25 2.5A1.75 1.75 0 008.5 4.25v3.5c0 .966.784 1.75 1.75 1.75H11V11H3a.75.75 0 000 1.5h3.5v2H5.25a1.75 1.75 0 00-1.75 1.75v3.5c0 .966.784 1.75 1.75 1.75h3.5a1.75 1.75 0 001.75-1.75v-3.5a1.75 1.75 0 00-1.75-1.75H8v-2h8v2h-.75a1.75 1.75 0 00-1.75 1.75v3.5c0 .966.784 1.75 1.75 1.75h3.5a1.75 1.75 0 001.75-1.75v-3.5a1.75 1.75 0 00-1.75-1.75H17.5v-2H21a.75.75 0 000-1.5h-8.5V9.5h1.25a1.75 1.75 0 001.75-1.75v-3.5a1.75 1.75 0 00-1.75-1.75h-3.5zM10 4.25a.25.25 0 01.25-.25h3.5a.25.25 0 01.25.25v3.5a.25.25 0 01-.25.25h-3.5a.25.25 0 01-.25-.25v-3.5zm-5 12a.25.25 0 01.25-.25h3.5a.25.25 0 01.25.25v3.5a.25.25 0 01-.25.25h-3.5a.25.25 0 01-.25-.25v-3.5zM15.25 16a.25.25 0 00-.25.25v3.5c0 .138.112.25.25.25h3.5a.25.25 0 00.25-.25v-3.5a.25.25 0 00-.25-.25h-3.5z\" clip-rule=\"evenodd\"/></svg>";

/***/ }),

/***/ "./style/icons/pipeline-16.svg":
/*!*************************************!*\
  !*** ./style/icons/pipeline-16.svg ***!
  \*************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M2.75 2.5A1.75 1.75 0 001 4.25v1C1 6.216 1.784 7 2.75 7h1a1.75 1.75 0 001.732-1.5H6.5a.75.75 0 01.75.75v3.5A2.25 2.25 0 009.5 12h1.018c.121.848.85 1.5 1.732 1.5h1A1.75 1.75 0 0015 11.75v-1A1.75 1.75 0 0013.25 9h-1a1.75 1.75 0 00-1.732 1.5H9.5a.75.75 0 01-.75-.75v-3.5A2.25 2.25 0 006.5 4H5.482A1.75 1.75 0 003.75 2.5h-1zM2.5 4.25A.25.25 0 012.75 4h1a.25.25 0 01.25.25v1a.25.25 0 01-.25.25h-1a.25.25 0 01-.25-.25v-1zm9.75 6.25a.25.25 0 00-.25.25v1c0 .138.112.25.25.25h1a.25.25 0 00.25-.25v-1a.25.25 0 00-.25-.25h-1z\" clip-rule=\"evenodd\"/></svg>";

/***/ }),

/***/ "./style/icons/shield-check-24.svg":
/*!*****************************************!*\
  !*** ./style/icons/shield-check-24.svg ***!
  \*****************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><g fill=\"currentColor\"><path d=\"M16.78 8.22a.75.75 0 010 1.06l-5.499 5.5a.75.75 0 01-1.061 0l-2.5-2.5a.75.75 0 111.06-1.06l1.97 1.97 4.97-4.97a.75.75 0 011.06 0z\"/><path fill-rule=\"evenodd\" d=\"M11.04 1.307a2.75 2.75 0 011.92 0l6.25 2.33A2.75 2.75 0 0121 6.214V12c0 2.732-1.462 5.038-3.104 6.774-1.65 1.744-3.562 3-4.65 3.642a2.437 2.437 0 01-2.493 0c-1.087-.643-3-1.898-4.65-3.642C4.463 17.038 3 14.732 3 12V6.214a2.75 2.75 0 011.79-2.577l6.25-2.33zm1.397 1.406a1.25 1.25 0 00-.874 0l-6.25 2.33a1.25 1.25 0 00-.813 1.17V12c0 2.182 1.172 4.136 2.693 5.744 1.514 1.6 3.294 2.772 4.323 3.38.304.18.664.18.968 0 1.03-.608 2.809-1.78 4.323-3.38C18.327 16.136 19.5 14.182 19.5 12V6.214a1.25 1.25 0 00-.813-1.171l-6.25-2.33z\" clip-rule=\"evenodd\"/></g></svg>";

/***/ }),

/***/ "./style/icons/slack.svg":
/*!*******************************!*\
  !*** ./style/icons/slack.svg ***!
  \*******************************/
/***/ ((module) => {

module.exports = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<svg\n   enable-background=\"new 0 0 2447.6 2452.5\"\n   viewBox=\"0 0 15.999999 16\"\n   version=\"1.1\"\n   id=\"svg4\"\n   sodipodi:docname=\"slack.svg\"\n   width=\"16\"\n   height=\"16\"\n   inkscape:version=\"1.3 (0e150ed, 2023-07-21)\"\n   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"\n   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   xmlns:svg=\"http://www.w3.org/2000/svg\">\n  <defs\n     id=\"defs4\" />\n  <sodipodi:namedview\n     id=\"namedview4\"\n     pagecolor=\"#505050\"\n     bordercolor=\"#eeeeee\"\n     borderopacity=\"1\"\n     inkscape:showpageshadow=\"0\"\n     inkscape:pageopacity=\"0\"\n     inkscape:pagecheckerboard=\"0\"\n     inkscape:deskcolor=\"#505050\"\n     inkscape:zoom=\"38.974502\"\n     inkscape:cx=\"10.391409\"\n     inkscape:cy=\"12.277257\"\n     inkscape:window-width=\"1512\"\n     inkscape:window-height=\"856\"\n     inkscape:window-x=\"0\"\n     inkscape:window-y=\"639\"\n     inkscape:window-maximized=\"1\"\n     inkscape:current-layer=\"svg4\" />\n  <g\n     clip-rule=\"evenodd\"\n     fill-rule=\"evenodd\"\n     id=\"g4\"\n     transform=\"matrix(0.0065171,0,0,0.0065171,-2.7150657e-4,0)\">\n    <path\n       d=\"M 897.4,0 C 762.1,0.1 652.6,109.9 652.7,245.2 652.6,380.5 762.2,490.3 897.5,490.4 h 244.8 V 245.3 C 1142.4,110 1032.8,0.2 897.4,0 c 0.1,0 0.1,0 0,0 m 0,654 H 244.8 C 109.5,654.1 -0.1,763.9 0,899.2 c -0.2,135.3 109.4,245.1 244.7,245.3 h 652.7 c 135.3,-0.1 244.9,-109.9 244.8,-245.2 C 1142.3,763.9 1032.7,654.1 897.4,654 Z\"\n       fill=\"#36c5f0\"\n       id=\"path1\" />\n    <path\n       d=\"M 2447.6,899.2 C 2447.7,763.9 2338.1,654.1 2202.8,654 2067.5,654.1 1957.9,763.9 1958,899.2 v 245.3 h 244.8 c 135.3,-0.1 244.9,-109.9 244.8,-245.3 z m -652.7,0 v -654 C 1795,110 1685.5,0.2 1550.2,0 1414.9,0.1 1305.3,109.9 1305.4,245.2 v 654 c -0.2,135.3 109.4,245.1 244.7,245.3 135.3,-0.1 244.9,-109.9 244.8,-245.3 z\"\n       fill=\"#2eb67d\"\n       id=\"path2\" />\n    <path\n       d=\"m 1550.1,2452.5 c 135.3,-0.1 244.9,-109.9 244.8,-245.2 0.1,-135.3 -109.5,-245.1 -244.8,-245.2 h -244.8 v 245.2 c -0.1,135.2 109.5,245 244.8,245.2 z m 0,-654.1 h 652.7 c 135.3,-0.1 244.9,-109.9 244.8,-245.2 0.2,-135.3 -109.4,-245.1 -244.7,-245.3 h -652.7 c -135.3,0.1 -244.9,109.9 -244.8,245.2 -0.1,135.4 109.4,245.2 244.7,245.3 z\"\n       fill=\"#ecb22e\"\n       id=\"path3\" />\n    <path\n       d=\"m 0,1553.2 c -0.1,135.3 109.5,245.1 244.8,245.2 135.3,-0.1 244.9,-109.9 244.8,-245.2 V 1308 H 244.8 C 109.5,1308.1 -0.1,1417.9 0,1553.2 Z m 652.7,0 v 654 c -0.2,135.3 109.4,245.1 244.7,245.3 135.3,-0.1 244.9,-109.9 244.8,-245.2 v -653.9 c 0.2,-135.3 -109.4,-245.1 -244.7,-245.3 -135.4,0 -244.9,109.8 -244.8,245.1 0,0 0,0.1 0,0\"\n       fill=\"#e01e5a\"\n       id=\"path4\" />\n  </g>\n</svg>\n";

/***/ }),

/***/ "./style/icons/upload-16.svg":
/*!***********************************!*\
  !*** ./style/icons/upload-16.svg ***!
  \***********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><g fill=\"currentColor\"><path d=\"M4.24 5.8a.75.75 0 001.06-.04l1.95-2.1v6.59a.75.75 0 001.5 0V3.66l1.95 2.1a.75.75 0 101.1-1.02l-3.25-3.5a.75.75 0 00-1.101.001L4.2 4.74a.75.75 0 00.04 1.06z\"/><path d=\"M1.75 9a.75.75 0 01.75.75v3c0 .414.336.75.75.75h9.5a.75.75 0 00.75-.75v-3a.75.75 0 011.5 0v3A2.25 2.25 0 0112.75 15h-9.5A2.25 2.25 0 011 12.75v-3A.75.75 0 011.75 9z\"/></g></svg>";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.c54b237bb42e2695f487.js.map