// modules are defined as an array
// [ module function, map of requires ]
//
// map of requires is short require name -> numeric require
//
// anything defined in a previous bundle is accessed via the
// orig method which is the require for previous bundles

(function (modules, entry, mainEntry, parcelRequireName, globalName) {
  /* eslint-disable no-undef */
  var globalObject =
    typeof globalThis !== 'undefined'
      ? globalThis
      : typeof self !== 'undefined'
      ? self
      : typeof window !== 'undefined'
      ? window
      : typeof global !== 'undefined'
      ? global
      : {};
  /* eslint-enable no-undef */

  // Save the require from previous bundle to this closure if any
  var previousRequire =
    typeof globalObject[parcelRequireName] === 'function' &&
    globalObject[parcelRequireName];

  var cache = previousRequire.cache || {};
  // Do not use `require` to prevent Webpack from trying to bundle this call
  var nodeRequire =
    typeof module !== 'undefined' &&
    typeof module.require === 'function' &&
    module.require.bind(module);

  function newRequire(name, jumped) {
    if (!cache[name]) {
      if (!modules[name]) {
        // if we cannot find the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire =
          typeof globalObject[parcelRequireName] === 'function' &&
          globalObject[parcelRequireName];
        if (!jumped && currentRequire) {
          return currentRequire(name, true);
        }

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) {
          return previousRequire(name, true);
        }

        // Try the node require function if it exists.
        if (nodeRequire && typeof name === 'string') {
          return nodeRequire(name);
        }

        var err = new Error("Cannot find module '" + name + "'");
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }

      localRequire.resolve = resolve;
      localRequire.cache = {};

      var module = (cache[name] = new newRequire.Module(name));

      modules[name][0].call(
        module.exports,
        localRequire,
        module,
        module.exports,
        globalObject
      );
    }

    return cache[name].exports;

    function localRequire(x) {
      var res = localRequire.resolve(x);
      return res === false ? {} : newRequire(res);
    }

    function resolve(x) {
      var id = modules[name][1][x];
      return id != null ? id : x;
    }
  }

  function Module(moduleName) {
    this.id = moduleName;
    this.bundle = newRequire;
    this.exports = {};
  }

  newRequire.isParcelRequire = true;
  newRequire.Module = Module;
  newRequire.modules = modules;
  newRequire.cache = cache;
  newRequire.parent = previousRequire;
  newRequire.register = function (id, exports) {
    modules[id] = [
      function (require, module) {
        module.exports = exports;
      },
      {},
    ];
  };

  Object.defineProperty(newRequire, 'root', {
    get: function () {
      return globalObject[parcelRequireName];
    },
  });

  globalObject[parcelRequireName] = newRequire;

  for (var i = 0; i < entry.length; i++) {
    newRequire(entry[i]);
  }

  if (mainEntry) {
    // Expose entry point to Node, AMD or browser globals
    // Based on https://github.com/ForbesLindesay/umd/blob/master/template.js
    var mainExports = newRequire(mainEntry);

    // CommonJS
    if (typeof exports === 'object' && typeof module !== 'undefined') {
      module.exports = mainExports;

      // RequireJS
    } else if (typeof define === 'function' && define.amd) {
      define(function () {
        return mainExports;
      });

      // <script>
    } else if (globalName) {
      this[globalName] = mainExports;
    }
  }
})({"kK1tq":[function(require,module,exports,__globalThis) {
var global = arguments[3];
var HMR_HOST = null;
var HMR_PORT = 1234;
var HMR_SECURE = false;
var HMR_ENV_HASH = "d6ea1d42532a7575";
var HMR_USE_SSE = false;
module.bundle.HMR_BUNDLE_ID = "42377f4a529f7c98";
"use strict";
/* global HMR_HOST, HMR_PORT, HMR_ENV_HASH, HMR_SECURE, HMR_USE_SSE, chrome, browser, __parcel__import__, __parcel__importScripts__, ServiceWorkerGlobalScope */ /*::
import type {
  HMRAsset,
  HMRMessage,
} from '@parcel/reporter-dev-server/src/HMRServer.js';
interface ParcelRequire {
  (string): mixed;
  cache: {|[string]: ParcelModule|};
  hotData: {|[string]: mixed|};
  Module: any;
  parent: ?ParcelRequire;
  isParcelRequire: true;
  modules: {|[string]: [Function, {|[string]: string|}]|};
  HMR_BUNDLE_ID: string;
  root: ParcelRequire;
}
interface ParcelModule {
  hot: {|
    data: mixed,
    accept(cb: (Function) => void): void,
    dispose(cb: (mixed) => void): void,
    // accept(deps: Array<string> | string, cb: (Function) => void): void,
    // decline(): void,
    _acceptCallbacks: Array<(Function) => void>,
    _disposeCallbacks: Array<(mixed) => void>,
  |};
}
interface ExtensionContext {
  runtime: {|
    reload(): void,
    getURL(url: string): string;
    getManifest(): {manifest_version: number, ...};
  |};
}
declare var module: {bundle: ParcelRequire, ...};
declare var HMR_HOST: string;
declare var HMR_PORT: string;
declare var HMR_ENV_HASH: string;
declare var HMR_SECURE: boolean;
declare var HMR_USE_SSE: boolean;
declare var chrome: ExtensionContext;
declare var browser: ExtensionContext;
declare var __parcel__import__: (string) => Promise<void>;
declare var __parcel__importScripts__: (string) => Promise<void>;
declare var globalThis: typeof self;
declare var ServiceWorkerGlobalScope: Object;
*/ var OVERLAY_ID = '__parcel__error__overlay__';
var OldModule = module.bundle.Module;
function Module(moduleName) {
    OldModule.call(this, moduleName);
    this.hot = {
        data: module.bundle.hotData[moduleName],
        _acceptCallbacks: [],
        _disposeCallbacks: [],
        accept: function(fn) {
            this._acceptCallbacks.push(fn || function() {});
        },
        dispose: function(fn) {
            this._disposeCallbacks.push(fn);
        }
    };
    module.bundle.hotData[moduleName] = undefined;
}
module.bundle.Module = Module;
module.bundle.hotData = {};
var checkedAssets /*: {|[string]: boolean|} */ , disposedAssets /*: {|[string]: boolean|} */ , assetsToDispose /*: Array<[ParcelRequire, string]> */ , assetsToAccept /*: Array<[ParcelRequire, string]> */ ;
function getHostname() {
    return HMR_HOST || (location.protocol.indexOf('http') === 0 ? location.hostname : 'localhost');
}
function getPort() {
    return HMR_PORT || location.port;
}
// eslint-disable-next-line no-redeclare
var parent = module.bundle.parent;
if ((!parent || !parent.isParcelRequire) && typeof WebSocket !== 'undefined') {
    var hostname = getHostname();
    var port = getPort();
    var protocol = HMR_SECURE || location.protocol == 'https:' && ![
        'localhost',
        '127.0.0.1',
        '0.0.0.0'
    ].includes(hostname) ? 'wss' : 'ws';
    var ws;
    if (HMR_USE_SSE) ws = new EventSource('/__parcel_hmr');
    else try {
        ws = new WebSocket(protocol + '://' + hostname + (port ? ':' + port : '') + '/');
    } catch (err) {
        if (err.message) console.error(err.message);
        ws = {};
    }
    // Web extension context
    var extCtx = typeof browser === 'undefined' ? typeof chrome === 'undefined' ? null : chrome : browser;
    // Safari doesn't support sourceURL in error stacks.
    // eval may also be disabled via CSP, so do a quick check.
    var supportsSourceURL = false;
    try {
        (0, eval)('throw new Error("test"); //# sourceURL=test.js');
    } catch (err) {
        supportsSourceURL = err.stack.includes('test.js');
    }
    // $FlowFixMe
    ws.onmessage = async function(event /*: {data: string, ...} */ ) {
        checkedAssets = {} /*: {|[string]: boolean|} */ ;
        disposedAssets = {} /*: {|[string]: boolean|} */ ;
        assetsToAccept = [];
        assetsToDispose = [];
        var data /*: HMRMessage */  = JSON.parse(event.data);
        if (data.type === 'reload') fullReload();
        else if (data.type === 'update') {
            // Remove error overlay if there is one
            if (typeof document !== 'undefined') removeErrorOverlay();
            let assets = data.assets.filter((asset)=>asset.envHash === HMR_ENV_HASH);
            // Handle HMR Update
            let handled = assets.every((asset)=>{
                return asset.type === 'css' || asset.type === 'js' && hmrAcceptCheck(module.bundle.root, asset.id, asset.depsByBundle);
            });
            if (handled) {
                console.clear();
                // Dispatch custom event so other runtimes (e.g React Refresh) are aware.
                if (typeof window !== 'undefined' && typeof CustomEvent !== 'undefined') window.dispatchEvent(new CustomEvent('parcelhmraccept'));
                await hmrApplyUpdates(assets);
                hmrDisposeQueue();
                // Run accept callbacks. This will also re-execute other disposed assets in topological order.
                let processedAssets = {};
                for(let i = 0; i < assetsToAccept.length; i++){
                    let id = assetsToAccept[i][1];
                    if (!processedAssets[id]) {
                        hmrAccept(assetsToAccept[i][0], id);
                        processedAssets[id] = true;
                    }
                }
            } else fullReload();
        }
        if (data.type === 'error') {
            // Log parcel errors to console
            for (let ansiDiagnostic of data.diagnostics.ansi){
                let stack = ansiDiagnostic.codeframe ? ansiDiagnostic.codeframe : ansiDiagnostic.stack;
                console.error("\uD83D\uDEA8 [parcel]: " + ansiDiagnostic.message + '\n' + stack + '\n\n' + ansiDiagnostic.hints.join('\n'));
            }
            if (typeof document !== 'undefined') {
                // Render the fancy html overlay
                removeErrorOverlay();
                var overlay = createErrorOverlay(data.diagnostics.html);
                // $FlowFixMe
                document.body.appendChild(overlay);
            }
        }
    };
    if (ws instanceof WebSocket) {
        ws.onerror = function(e) {
            if (e.message) console.error(e.message);
        };
        ws.onclose = function() {
            console.warn("[parcel] \uD83D\uDEA8 Connection to the HMR server was lost");
        };
    }
}
function removeErrorOverlay() {
    var overlay = document.getElementById(OVERLAY_ID);
    if (overlay) {
        overlay.remove();
        console.log("[parcel] \u2728 Error resolved");
    }
}
function createErrorOverlay(diagnostics) {
    var overlay = document.createElement('div');
    overlay.id = OVERLAY_ID;
    let errorHTML = '<div style="background: black; opacity: 0.85; font-size: 16px; color: white; position: fixed; height: 100%; width: 100%; top: 0px; left: 0px; padding: 30px; font-family: Menlo, Consolas, monospace; z-index: 9999;">';
    for (let diagnostic of diagnostics){
        let stack = diagnostic.frames.length ? diagnostic.frames.reduce((p, frame)=>{
            return `${p}
<a href="/__parcel_launch_editor?file=${encodeURIComponent(frame.location)}" style="text-decoration: underline; color: #888" onclick="fetch(this.href); return false">${frame.location}</a>
${frame.code}`;
        }, '') : diagnostic.stack;
        errorHTML += `
      <div>
        <div style="font-size: 18px; font-weight: bold; margin-top: 20px;">
          \u{1F6A8} ${diagnostic.message}
        </div>
        <pre>${stack}</pre>
        <div>
          ${diagnostic.hints.map((hint)=>"<div>\uD83D\uDCA1 " + hint + '</div>').join('')}
        </div>
        ${diagnostic.documentation ? `<div>\u{1F4DD} <a style="color: violet" href="${diagnostic.documentation}" target="_blank">Learn more</a></div>` : ''}
      </div>
    `;
    }
    errorHTML += '</div>';
    overlay.innerHTML = errorHTML;
    return overlay;
}
function fullReload() {
    if ('reload' in location) location.reload();
    else if (extCtx && extCtx.runtime && extCtx.runtime.reload) extCtx.runtime.reload();
}
function getParents(bundle, id) /*: Array<[ParcelRequire, string]> */ {
    var modules = bundle.modules;
    if (!modules) return [];
    var parents = [];
    var k, d, dep;
    for(k in modules)for(d in modules[k][1]){
        dep = modules[k][1][d];
        if (dep === id || Array.isArray(dep) && dep[dep.length - 1] === id) parents.push([
            bundle,
            k
        ]);
    }
    if (bundle.parent) parents = parents.concat(getParents(bundle.parent, id));
    return parents;
}
function updateLink(link) {
    var href = link.getAttribute('href');
    if (!href) return;
    var newLink = link.cloneNode();
    newLink.onload = function() {
        if (link.parentNode !== null) // $FlowFixMe
        link.parentNode.removeChild(link);
    };
    newLink.setAttribute('href', // $FlowFixMe
    href.split('?')[0] + '?' + Date.now());
    // $FlowFixMe
    link.parentNode.insertBefore(newLink, link.nextSibling);
}
var cssTimeout = null;
function reloadCSS() {
    if (cssTimeout) return;
    cssTimeout = setTimeout(function() {
        var links = document.querySelectorAll('link[rel="stylesheet"]');
        for(var i = 0; i < links.length; i++){
            // $FlowFixMe[incompatible-type]
            var href /*: string */  = links[i].getAttribute('href');
            var hostname = getHostname();
            var servedFromHMRServer = hostname === 'localhost' ? new RegExp('^(https?:\\/\\/(0.0.0.0|127.0.0.1)|localhost):' + getPort()).test(href) : href.indexOf(hostname + ':' + getPort());
            var absolute = /^https?:\/\//i.test(href) && href.indexOf(location.origin) !== 0 && !servedFromHMRServer;
            if (!absolute) updateLink(links[i]);
        }
        cssTimeout = null;
    }, 50);
}
function hmrDownload(asset) {
    if (asset.type === 'js') {
        if (typeof document !== 'undefined') {
            let script = document.createElement('script');
            script.src = asset.url + '?t=' + Date.now();
            if (asset.outputFormat === 'esmodule') script.type = 'module';
            return new Promise((resolve, reject)=>{
                var _document$head;
                script.onload = ()=>resolve(script);
                script.onerror = reject;
                (_document$head = document.head) === null || _document$head === void 0 || _document$head.appendChild(script);
            });
        } else if (typeof importScripts === 'function') {
            // Worker scripts
            if (asset.outputFormat === 'esmodule') return import(asset.url + '?t=' + Date.now());
            else return new Promise((resolve, reject)=>{
                try {
                    importScripts(asset.url + '?t=' + Date.now());
                    resolve();
                } catch (err) {
                    reject(err);
                }
            });
        }
    }
}
async function hmrApplyUpdates(assets) {
    global.parcelHotUpdate = Object.create(null);
    let scriptsToRemove;
    try {
        // If sourceURL comments aren't supported in eval, we need to load
        // the update from the dev server over HTTP so that stack traces
        // are correct in errors/logs. This is much slower than eval, so
        // we only do it if needed (currently just Safari).
        // https://bugs.webkit.org/show_bug.cgi?id=137297
        // This path is also taken if a CSP disallows eval.
        if (!supportsSourceURL) {
            let promises = assets.map((asset)=>{
                var _hmrDownload;
                return (_hmrDownload = hmrDownload(asset)) === null || _hmrDownload === void 0 ? void 0 : _hmrDownload.catch((err)=>{
                    // Web extension fix
                    if (extCtx && extCtx.runtime && extCtx.runtime.getManifest().manifest_version == 3 && typeof ServiceWorkerGlobalScope != 'undefined' && global instanceof ServiceWorkerGlobalScope) {
                        extCtx.runtime.reload();
                        return;
                    }
                    throw err;
                });
            });
            scriptsToRemove = await Promise.all(promises);
        }
        assets.forEach(function(asset) {
            hmrApply(module.bundle.root, asset);
        });
    } finally{
        delete global.parcelHotUpdate;
        if (scriptsToRemove) scriptsToRemove.forEach((script)=>{
            if (script) {
                var _document$head2;
                (_document$head2 = document.head) === null || _document$head2 === void 0 || _document$head2.removeChild(script);
            }
        });
    }
}
function hmrApply(bundle /*: ParcelRequire */ , asset /*:  HMRAsset */ ) {
    var modules = bundle.modules;
    if (!modules) return;
    if (asset.type === 'css') reloadCSS();
    else if (asset.type === 'js') {
        let deps = asset.depsByBundle[bundle.HMR_BUNDLE_ID];
        if (deps) {
            if (modules[asset.id]) {
                // Remove dependencies that are removed and will become orphaned.
                // This is necessary so that if the asset is added back again, the cache is gone, and we prevent a full page reload.
                let oldDeps = modules[asset.id][1];
                for(let dep in oldDeps)if (!deps[dep] || deps[dep] !== oldDeps[dep]) {
                    let id = oldDeps[dep];
                    let parents = getParents(module.bundle.root, id);
                    if (parents.length === 1) hmrDelete(module.bundle.root, id);
                }
            }
            if (supportsSourceURL) // Global eval. We would use `new Function` here but browser
            // support for source maps is better with eval.
            (0, eval)(asset.output);
            // $FlowFixMe
            let fn = global.parcelHotUpdate[asset.id];
            modules[asset.id] = [
                fn,
                deps
            ];
        }
        // Always traverse to the parent bundle, even if we already replaced the asset in this bundle.
        // This is required in case modules are duplicated. We need to ensure all instances have the updated code.
        if (bundle.parent) hmrApply(bundle.parent, asset);
    }
}
function hmrDelete(bundle, id) {
    let modules = bundle.modules;
    if (!modules) return;
    if (modules[id]) {
        // Collect dependencies that will become orphaned when this module is deleted.
        let deps = modules[id][1];
        let orphans = [];
        for(let dep in deps){
            let parents = getParents(module.bundle.root, deps[dep]);
            if (parents.length === 1) orphans.push(deps[dep]);
        }
        // Delete the module. This must be done before deleting dependencies in case of circular dependencies.
        delete modules[id];
        delete bundle.cache[id];
        // Now delete the orphans.
        orphans.forEach((id)=>{
            hmrDelete(module.bundle.root, id);
        });
    } else if (bundle.parent) hmrDelete(bundle.parent, id);
}
function hmrAcceptCheck(bundle /*: ParcelRequire */ , id /*: string */ , depsByBundle /*: ?{ [string]: { [string]: string } }*/ ) {
    if (hmrAcceptCheckOne(bundle, id, depsByBundle)) return true;
    // Traverse parents breadth first. All possible ancestries must accept the HMR update, or we'll reload.
    let parents = getParents(module.bundle.root, id);
    let accepted = false;
    while(parents.length > 0){
        let v = parents.shift();
        let a = hmrAcceptCheckOne(v[0], v[1], null);
        if (a) // If this parent accepts, stop traversing upward, but still consider siblings.
        accepted = true;
        else {
            // Otherwise, queue the parents in the next level upward.
            let p = getParents(module.bundle.root, v[1]);
            if (p.length === 0) {
                // If there are no parents, then we've reached an entry without accepting. Reload.
                accepted = false;
                break;
            }
            parents.push(...p);
        }
    }
    return accepted;
}
function hmrAcceptCheckOne(bundle /*: ParcelRequire */ , id /*: string */ , depsByBundle /*: ?{ [string]: { [string]: string } }*/ ) {
    var modules = bundle.modules;
    if (!modules) return;
    if (depsByBundle && !depsByBundle[bundle.HMR_BUNDLE_ID]) {
        // If we reached the root bundle without finding where the asset should go,
        // there's nothing to do. Mark as "accepted" so we don't reload the page.
        if (!bundle.parent) return true;
        return hmrAcceptCheck(bundle.parent, id, depsByBundle);
    }
    if (checkedAssets[id]) return true;
    checkedAssets[id] = true;
    var cached = bundle.cache[id];
    assetsToDispose.push([
        bundle,
        id
    ]);
    if (!cached || cached.hot && cached.hot._acceptCallbacks.length) {
        assetsToAccept.push([
            bundle,
            id
        ]);
        return true;
    }
}
function hmrDisposeQueue() {
    // Dispose all old assets.
    for(let i = 0; i < assetsToDispose.length; i++){
        let id = assetsToDispose[i][1];
        if (!disposedAssets[id]) {
            hmrDispose(assetsToDispose[i][0], id);
            disposedAssets[id] = true;
        }
    }
    assetsToDispose = [];
}
function hmrDispose(bundle /*: ParcelRequire */ , id /*: string */ ) {
    var cached = bundle.cache[id];
    bundle.hotData[id] = {};
    if (cached && cached.hot) cached.hot.data = bundle.hotData[id];
    if (cached && cached.hot && cached.hot._disposeCallbacks.length) cached.hot._disposeCallbacks.forEach(function(cb) {
        cb(bundle.hotData[id]);
    });
    delete bundle.cache[id];
}
function hmrAccept(bundle /*: ParcelRequire */ , id /*: string */ ) {
    // Execute the module.
    bundle(id);
    // Run the accept callbacks in the new version of the module.
    var cached = bundle.cache[id];
    if (cached && cached.hot && cached.hot._acceptCallbacks.length) {
        let assetsToAlsoAccept = [];
        cached.hot._acceptCallbacks.forEach(function(cb) {
            let additionalAssets = cb(function() {
                return getParents(module.bundle.root, id);
            });
            if (Array.isArray(additionalAssets) && additionalAssets.length) assetsToAlsoAccept.push(...additionalAssets);
        });
        if (assetsToAlsoAccept.length) {
            let handled = assetsToAlsoAccept.every(function(a) {
                return hmrAcceptCheck(a[0], a[1]);
            });
            if (!handled) return fullReload();
            hmrDisposeQueue();
        }
    }
}

},{}],"bn71D":[function(require,module,exports,__globalThis) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "shuffle_array", ()=>shuffle_array);
parcelHelpers.export(exports, "initial_seating", ()=>initial_seating);
var RULE = /*#__PURE__*/ function(RULE) {
    RULE[RULE["R1_PREDATOR_PREY"] = 0] = "R1_PREDATOR_PREY";
    RULE[RULE["R2_OPPONENT_ALWAYS"] = 1] = "R2_OPPONENT_ALWAYS";
    RULE[RULE["R3_AVAILABLE_VPS"] = 2] = "R3_AVAILABLE_VPS";
    RULE[RULE["R4_OPPONENT_TWICE"] = 3] = "R4_OPPONENT_TWICE";
    RULE[RULE["R5_FIFTH_SEAT"] = 4] = "R5_FIFTH_SEAT";
    RULE[RULE["R6_SAME_POSITION"] = 5] = "R6_SAME_POSITION";
    RULE[RULE["R7_SAME_SEAT"] = 6] = "R7_SAME_SEAT";
    RULE[RULE["R8_STARTING_TRANSFERS"] = 7] = "R8_STARTING_TRANSFERS";
    RULE[RULE["R9_SAME_POSITION_GROUP"] = 8] = "R9_SAME_POSITION_GROUP";
    return RULE;
}(RULE || {});
var IDX = /*#__PURE__*/ function(IDX) {
    // relationship
    IDX[IDX["OPPONENT"] = 0] = "OPPONENT";
    IDX[IDX["PREY"] = 1] = "PREY";
    IDX[IDX["PREDATOR"] = 2] = "PREDATOR";
    IDX[IDX["GRAND_PREY"] = 3] = "GRAND_PREY";
    IDX[IDX["GRAND_PREDATOR"] = 4] = "GRAND_PREDATOR";
    IDX[IDX["CROSS_TABLE"] = 5] = "CROSS_TABLE";
    IDX[IDX["NEIGHBOUR"] = 6] = "NEIGHBOUR";
    IDX[IDX["NON_NEIGHBOUR"] = 7] = "NON_NEIGHBOUR";
    // position (own index)
    IDX[IDX["ROUNDS_PLAYED"] = 0] = "ROUNDS_PLAYED";
    IDX[IDX["VPS"] = 1] = "VPS";
    IDX[IDX["TRS"] = 2] = "TRS";
    IDX[IDX["SEAT_1"] = 3] = "SEAT_1";
    IDX[IDX["SEAT_2"] = 4] = "SEAT_2";
    IDX[IDX["SEAT_3"] = 5] = "SEAT_3";
    IDX[IDX["SEAT_4"] = 6] = "SEAT_4";
    IDX[IDX["SEAT_5"] = 7] = "SEAT_5";
    return IDX;
}(IDX || {});
// Measure
// To measure a seating "value", we use an N x N x 8 triangular matrix of integers, N being the number of players.
// For each couple of players, it records their successive relationships,
// A value of zero means they've never been in that position, otherwise it's the number of time it happened
// as per the IDX enum above:
// [opponent, prey, grand_prey, grand_pred, pred, cross, neighbour, non_neighbour]
// Because of the symmetry in relationships, we need only a triangular matrix and don't set half the values.
//
// The [i][i] diagonal of the matrix is special: a player has no relationship with themsleves,
// so instead it records their successive positions, again as per the IDX enum above: 
// [rounds_played, vps_available, first_turn_transfers, seat_1, seat2, seat3, seat4, seat5]
//
// The beauty of it is we can compute a round's matrix very quickly by copying the standard vectors below,
// and we can simply add the rounds matrixes successively to get our final matrix.
// Computing a "score" vector counting the seating rules "violations" from the matrix is relatively straightforward.
const OPPONENTS = new Map(// for each pair of players
// 0: opponents
// 1: prey
// 2: grand-prey (5 seats only)
// 3: grand-predator (5 seats only)
// 4: predator
// 5: cross-table (4 seats only)
// 6: neighbours
// 7: non-neighbours
[
    [
        4,
        [
            [],
            [
                1,
                1,
                0,
                0,
                0,
                0,
                1,
                0
            ],
            [
                1,
                0,
                0,
                0,
                0,
                1,
                0,
                1
            ],
            [
                1,
                0,
                1,
                0,
                0,
                0,
                1,
                0
            ]
        ]
    ],
    [
        5,
        [
            [],
            [
                1,
                1,
                0,
                0,
                0,
                0,
                1,
                0
            ],
            [
                1,
                0,
                0,
                1,
                0,
                0,
                0,
                1
            ],
            [
                1,
                0,
                0,
                0,
                1,
                0,
                0,
                1
            ],
            [
                1,
                0,
                1,
                0,
                0,
                0,
                1,
                0
            ]
        ]
    ]
]);
const POSITIONS = new Map(// for each player
// 0: playing
// 1: vps opportunity 
// 2: first turn transfers
// 3: seat 1
// 4: seat 2
// 5: seat 3
// 6: seat 4
// 7: seat 5
[
    [
        4,
        [
            [
                1,
                4,
                1,
                1,
                0,
                0,
                0,
                0
            ],
            [
                1,
                4,
                2,
                0,
                1,
                0,
                0,
                0
            ],
            [
                1,
                4,
                3,
                0,
                0,
                1,
                0,
                0
            ],
            [
                1,
                4,
                4,
                0,
                0,
                0,
                1,
                0
            ]
        ]
    ],
    [
        5,
        [
            [
                1,
                5,
                1,
                1,
                0,
                0,
                0,
                0
            ],
            [
                1,
                5,
                2,
                0,
                1,
                0,
                0,
                0
            ],
            [
                1,
                5,
                3,
                0,
                0,
                1,
                0,
                0
            ],
            [
                1,
                5,
                4,
                0,
                0,
                0,
                1,
                0
            ],
            [
                1,
                5,
                4,
                0,
                0,
                0,
                0,
                1
            ]
        ]
    ]
]);
// function add1(lhs: number[], rhs: number[]): number[] {
//     return lhs.map((x, i) => x + rhs[i])
// }
// function add2(lhs: number[][], rhs: number[][]): number[][] {
//     return lhs.map((x, i) => x.map((y, j) => y + rhs[i][j]))
// }
function add3(lhs, rhs) {
    // add two 3D measures together
    return lhs.map((x, i)=>x.map((y, j)=>y.map((z, k)=>z + rhs[i][j][k])));
}
class Evaluator {
    mapping = new Map();
    reverse = new Map();
    constructor(ids){
        var i = 0;
        for (const uid of ids)if (!this.mapping.has(uid)) {
            this.reverse.set(i, uid);
            this.mapping.set(uid, i++);
        }
    }
    measure(round_, hints) {
        // careful on the init, we need distinct arrays (no fill() with Array instances)
        const measure = Array.from({
            length: this.mapping.size
        }, (e)=>Array.from({
                length: this.mapping.size
            }, (e)=>new Array(8).fill(0)));
        for (const [idx_t, table] of round_.entries()){
            if (hints && !hints.includes(idx_t)) continue;
            for (const [idx_p, player] of table.entries()){
                const index = this.mapping.get(player);
                console.log("measure", table.length, idx_p);
                measure[index][index] = POSITIONS.get(table.length)[idx_p].slice();
                for(var idx_r = 1; idx_r < table.length; idx_r++){
                    // We skip when opponent index > player index to do 1/2 less copies (symmetry)
                    const opponent_index = this.mapping.get(table[(idx_p + idx_r) % table.length]);
                    if (opponent_index > index) continue;
                    measure[index][opponent_index] = OPPONENTS.get(table.length)[idx_r].slice();
                }
            }
        }
        return measure;
    }
    measure_rounds(rounds) {
        var result = undefined;
        for (const round of rounds){
            const M = this.measure(round);
            if (result) result = add3(result, M);
            else result = M;
        }
        return result;
    }
    issues(M) {
        // returns the faulty indexes for each rule
        const result = Array.from({
            length: 9
        }, (e)=>new Array());
        // compute some global values
        var mean_vps = 0 // average possible vp per round overall
        ;
        var mean_trs = 0 // average first-turn transfers per round overall
        ;
        var playing = 0 // number of players playing in total
        ;
        var rounds = 0 // rounds played (the max number of rounds played by a player)
        ;
        for (const [i, measure] of M.entries()){
            const position = measure[i];
            const rounds_played = position[0];
            if (rounds_played > 0) {
                mean_vps += position[1] / rounds_played;
                mean_trs += position[2] / rounds_played;
                playing++;
                rounds = rounds < rounds_played ? rounds_played : rounds;
            }
        }
        mean_vps = mean_vps / playing;
        mean_trs = mean_trs / playing;
        for (const [i, measure] of M.entries())for (const [j, relationship] of measure.entries()){
            if (j > i) break;
            if (j === i) {
                // vps and tps outliers
                // the base is 1 for vps (4 or 5) and 2 for transfers (1, 2, 3 or 4)
                // this "allowed" deviation is *divided* by the number of rounds: 
                // more rounds played by a player, more opportunities to fix it
                const rounds_played = relationship[0];
                if (Math.abs(mean_vps - relationship[1] / rounds_played) > 1 / rounds_played) result[2].push([
                    this.reverse.get(i)
                ]);
                if (Math.abs(mean_vps - relationship[2] / rounds_played) > 2 / rounds_played) result[7].push([
                    this.reverse.get(i)
                ]);
                if (relationship[3] > 1) result[6].push([
                    this.reverse.get(i)
                ]);
                if (relationship[4] > 1) result[6].push([
                    this.reverse.get(i)
                ]);
                if (relationship[5] > 1) result[6].push([
                    this.reverse.get(i)
                ]);
                if (relationship[6] > 1) result[6].push([
                    this.reverse.get(i)
                ]);
                if (relationship[7] > 1) {
                    result[6].push([
                        this.reverse.get(i)
                    ]);
                    result[4].push([
                        this.reverse.get(i)
                    ]);
                }
            } else {
                for (const [k, value] of relationship.entries())if (value > 1) {
                    if (k == 0) {
                        result[3].push([
                            this.reverse.get(i),
                            this.reverse.get(j)
                        ]);
                        if (value >= rounds) result[1].push([
                            this.reverse.get(i),
                            this.reverse.get(j)
                        ]);
                    } else if (k <= 2) {
                        result[0].push([
                            this.reverse.get(i),
                            this.reverse.get(j)
                        ]);
                        result[5].push([
                            this.reverse.get(i),
                            this.reverse.get(j)
                        ]);
                    } else if (k <= 5) result[5].push([
                        this.reverse.get(i),
                        this.reverse.get(j)
                    ]);
                    else result[8].push([
                        this.reverse.get(i),
                        this.reverse.get(j)
                    ]);
                }
            }
        }
        return result;
    }
    fast_score(M) {
        // A score vector indicating the number of issues per rule
        const result = new Array(9).fill(0);
        var mean_vps = 0;
        var mean_trs = 0;
        var playing = 0;
        var rounds = 0;
        for (const [i, measure] of M.entries()){
            const position = measure[i];
            const rounds_played = position[0];
            if (rounds_played > 0) {
                mean_vps += position[1] / rounds_played;
                mean_trs += position[2] / rounds_played;
                playing++;
                rounds = rounds < rounds_played ? rounds_played : rounds;
            }
        }
        mean_vps = mean_vps / playing;
        mean_trs = mean_trs / playing;
        for (const [i, measure] of M.entries())for (const [j, relationship] of measure.entries()){
            if (j > i) break;
            if (j === i) {
                const rounds_played = relationship[0];
                if (Math.abs(mean_vps - relationship[1] / rounds_played) > 1 / rounds_played) result[2]++;
                if (Math.abs(mean_vps - relationship[2] / rounds_played) > 2 / rounds_played) result[7]++;
                if (relationship[3] > 1) result[6]++;
                if (relationship[4] > 1) result[6]++;
                if (relationship[5] > 1) result[6]++;
                if (relationship[6] > 1) result[6]++;
                if (relationship[7] > 1) {
                    result[6]++;
                    result[4]++;
                }
            } else {
                for (const [k, value] of relationship.entries())if (value > 1) {
                    if (k == 0) {
                        result[3]++;
                        if (value >= rounds) result[1]++;
                    } else if (k <= 2) {
                        result[0]++;
                        result[5]++;
                    } else if (k <= 5) result[5]++;
                    else result[8]++;
                }
            }
        }
        return result;
    }
}
function shuffle_array(array) {
    for(let i = array.length - 1; i >= 0; i--){
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [
            array[j],
            array[i]
        ];
    }
}
function default_seating(players) {
    const seat_in_fives = players.length - 4 * (5 - (players.length % 5 | 5));
    var seated = 0;
    const res = [];
    while(seated < players.length){
        const seats = seated < seat_in_fives ? 5 : 4;
        res.push(players.slice(seated, seated + seats));
        seated += seats;
    }
    return res;
}
function compare_issues(lhs, rhs) {
    const length = lhs.length < rhs.length ? lhs.length : rhs.length;
    for(var i = 0; i < length; i++){
        const cmp_l = lhs[i].length;
        const cmp_r = rhs[i].length;
        if (cmp_l < cmp_r) return -1;
        if (cmp_l > cmp_r) return 1;
    }
    return 0;
}
function zero_issues(issues) {
    return !issues.some((x)=>x.length > 0);
}
function initial_seating(previous_rounds, players) {
    players = players.slice();
    if (previous_rounds.length <= 0) {
        shuffle_array(players);
        return default_seating(players);
    }
    const all_players = new Set(players);
    for (const round_ of previous_rounds){
        for (const table of round_)for (const player of table)all_players.add(player);
    }
    const E = new Evaluator(all_players);
    const base_measure = E.measure_rounds(previous_rounds);
    shuffle_array(players);
    var best_seating = new Seating(default_seating(players));
    var best_issues = E.issues(add3(base_measure, E.measure(best_seating.seating)));
    // keep it simple, guided monte-carlo
    // TODO: use online API when not offline for better seating? May not be necessary
    for(var it = 0; it < 1000; it++){
        var seating = new Seating(best_seating.seating);
        const players_to_switch = new Set();
        for (const rule of best_issues){
            for (const players of rule)if (players.length < 2) players_to_switch.add(players[0]);
            else players_to_switch.add(players[Math.floor(Math.random() * players.length)]);
        }
        for (const player of players_to_switch)seating.random_swap(player);
        const new_issues = E.issues(add3(base_measure, E.measure(seating.seating)));
        if (compare_issues(new_issues, best_issues) < 0) {
            best_issues = new_issues;
            best_seating = seating;
        }
        if (zero_issues(best_issues)) break;
    }
    console.log("best seating found", best_seating.seating, best_issues);
    return best_seating.seating;
}
class Seating {
    seat_index = new Map() // seat number to [table, seat] indexes
    ;
    player_index = new Map() // player string to seat number
    ;
    seating;
    constructor(seating){
        this.seating = seating.map((s)=>s.slice()) // copy seating
        ;
        var x = 0;
        for (const [i, table] of seating.entries())for (const [j, player] of table.entries()){
            this.player_index.set(player, x);
            this.seat_index.set(x, [
                i,
                j
            ]);
            x++;
        }
    }
    random_swap(player) {
        const x = this.player_index.get(player);
        var y = x;
        while(y == x)y = Math.floor(Math.random() * this.seat_index.size);
        this.swap(x, y);
    }
    shuffle() {
        for(var i = this.seat_index.size - 1; i >= 0; i--){
            const a = i;
            const b = Math.floor(Math.random() * (i + 1));
            this.swap(a, b);
        }
    }
    swap(a, b) {
        const [x, y] = [
            this.seat_index.get(a),
            this.seat_index.get(b)
        ];
        const [player_a, player_b] = [
            this.seating[x[0]][x[1]],
            this.seating[y[0]][y[1]]
        ];
        this.seating[x[0]][x[1]] = player_b;
        this.seating[y[0]][y[1]] = player_a;
        this.player_index.set(player_a, b);
        this.player_index.set(player_b, a);
    }
}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"gkKU3":[function(require,module,exports,__globalThis) {
exports.interopDefault = function(a) {
    return a && a.__esModule ? a : {
        default: a
    };
};
exports.defineInteropFlag = function(a) {
    Object.defineProperty(a, '__esModule', {
        value: true
    });
};
exports.exportAll = function(source, dest) {
    Object.keys(source).forEach(function(key) {
        if (key === 'default' || key === '__esModule' || Object.prototype.hasOwnProperty.call(dest, key)) return;
        Object.defineProperty(dest, key, {
            enumerable: true,
            get: function() {
                return source[key];
            }
        });
    });
    return dest;
};
exports.export = function(dest, destName, get) {
    Object.defineProperty(dest, destName, {
        enumerable: true,
        get: get
    });
};

},{}]},["kK1tq","bn71D"], "bn71D", "parcelRequire94c2")

//# sourceMappingURL=seating.js.map
