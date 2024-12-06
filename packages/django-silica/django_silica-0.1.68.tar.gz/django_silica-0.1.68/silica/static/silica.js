/*jshint esversion: 6 */
let silica_components = {};

class Silica {
    components = []

    static initComponents() {
        let componentEls = document.querySelectorAll("[silica\\:initial-data], [silica\\:lazy]");

        componentEls.forEach((componentEl) => {
            let component_id = componentEl.getAttribute("silica:id");

            if (!silica_components.hasOwnProperty(component_id)) {
                silica_components[component_id] = new SilicaComponent(componentEl);
            }
        });

        Silica.createAlpineMagics();
    }

    static getNearestComponent(elem) {
        for (; elem && elem !== document; elem = elem.parentNode) {
            if (elem.getAttribute("silica:id")) {
                return {
                    el: elem,
                    id: elem.getAttribute("silica:id"),
                    name: elem.getAttribute("silica:name"),
                    component: silica_components[elem.getAttribute("silica:id")]
                };
            }
        }
        return false;
    }

    static broadcastEvent() {
    }

    static createAlpineMagics() {
        window.Alpine.magic('set', (el, {Alpine}) => (key, value) => {
            try {
                const {component} = Silica.getNearestComponent(el)
                if (component) {
                    component.setProperty(key, value)
                }
            } catch (e) {
                console.error("Error calling $set Alpine magic method", e)
            }
        })
        window.Alpine.magic('call', (el, {Alpine}) => (method, args) => {
            try {
                const {component} = Silica.getNearestComponent(el)
                if (component) {
                    component.callMethod(method, args)
                }
            } catch (e) {
                console.error("Error calling $call Alpine magic method", e)
            }
        })

        Alpine.magic('silica', (el, {cleanup}) => {
            return new Proxy({}, {
                get(target, property) {
                    let {component} = Silica.getNearestComponent(el)
                    if (component) {
                        return component['data'][property]
                    }
                },
                set(target, property, value) {
                    let {component} = Silica.getNearestComponent(el)
                    if (component) {
                        component.setProperty(property, value)
                    }
                    return true
                },
            })
        })
    }

    static data_get(data, path) {
        return path.split('.').reduce((o, i) => o?.[i], data);
    }

    static data_key_exists(data, key) {
        return key.split('.').every(i => (data = data[i]) !== undefined);
    }
}

document.addEventListener('alpine:init', () => {
    Silica.initComponents();
})

class SilicaComponent {
    el;
    id;
    name;
    // data = {};
    state = {};

    last_request_timestamp = null;

    ACTION_TYPE_CALL_METHOD = "call_method";
    ACTION_TYPE_SET_PROPERTY = "set_property";
    ACTION_TYPE_EVENT = "event";

    constructor(componentEl) {
        const encodedData = componentEl.getAttribute("silica:initial-data");
        const decodedData = decodeURIComponent(encodedData);
        const snapshot = JSON.parse(decodedData);

        this.el = componentEl
        this.id = componentEl.getAttribute("silica:id");
        this.name = componentEl.getAttribute("silica:name");

        if (componentEl.hasAttribute("silica:lazy")) {
            this.activateLazy()
            componentEl.removeAttribute("silica:lazy")
            return
        }

        this.data = snapshot.data;

        if (this.processRedirections(snapshot.js_calls)) {
            return;
        }

        componentEl.removeAttribute("silica:initial-data");

        // Bind methods
        this.boundEvents = new Map();
        this.boundMethods = {
            handleModelInputEvent: this.handleModelInputEvent.bind(this),
            handleClickEvent: this.handleClickEvent.bind(this),
        };

        this.updateModelValues(snapshot.data);
        this.setQueryParams(snapshot);
        this.processJsCalls(snapshot?.js_calls);
        this.processEvents(snapshot?.event_calls);
        this.setListeners()
        this.processInitCalls()
    }

    updateModelValues(data) {
        let mthis = this
        this.findElementsByPartialAttributeName("silica:model").forEach((el) => {
            let modelName = this.getAttributeFromPartialName("silica:model", el)
            let modelValue = Silica.data_get(data, modelName);

            if (Silica.data_key_exists(data, modelName)) {
                if (el.type === 'checkbox') {
                    if (Array.isArray(modelValue)) {
                        el.checked = modelValue.includes(el.value);
                    } else {
                        el.checked = modelValue;
                    }
                } else {
                    el.value = mthis._data_get(data, modelName);
                }
            }
        });
    }

    setQueryParams(snapshot) {
        if (snapshot["query_params"] && snapshot["query_params"].length > 0) {
            snapshot["query_params"].forEach((param) => {
                if (snapshot.data?.[param.key] !== undefined) {

                    const url_key = param?.as || param.key

                    if (param.visible) {
                        this.setQueryParam(url_key, snapshot.data[param.key]);
                    } else {
                        this.removeQueryParam(url_key);
                    }
                }
            });
        }
    }

    setQueryParam(paramKey, paramValue) {
        const url = new URL(window.location);

        if (Array.isArray(paramValue)) {
            url.searchParams.delete(paramKey);
            paramValue.forEach(value => {
                url.searchParams.append(paramKey, value);
            });
        } else {
            url.searchParams.set(paramKey, paramValue);
        }

        window.history.pushState({}, "", url);
    }

    removeQueryParam(paramKey) {
        const url = new URL(window.location);
        url.searchParams.delete(paramKey)
        window.history.pushState({}, "", url);
    }

    processJsCalls(calls = []) {
        calls.forEach((call) => {
            const fn = call.fn;
            const args = call?.args;

            if (fn === '_silicaDispatchBrowserEvent') {
                this._silicaDispatchBrowserEvent(...args);
                return;
            }
            window[fn](...args);
        });
    }

    _silicaDispatchBrowserEvent(name, payload) {
        window.dispatchEvent(
            new CustomEvent(name, {
                detail: payload,
                bubbles: true,
                // Allows events to pass the shadow DOM barrier.
                composed: true,
                cancelable: true,
            })
        )
    }

    processEvents(events = []) {
        events.forEach((event) => {
            if (event.type === "emit") {
                // emit to all silica_components on page
                Object.values(silica_components).forEach((component) => {
                    const action = {
                        type: this.ACTION_TYPE_EVENT,
                        event_name: event.name,
                        payload: event.payload
                    };

                    component.sendMessage(action);
                });
            } else if (event.type === "emit_to") {
                // emit to all silica_components on page
                Object.values(silica_components)
                    .filter((component) => component.name === event.component_name)
                    .forEach((component) => {
                        const action = {
                            type: this.ACTION_TYPE_EVENT,
                            event_name: event.name,
                            payload: event.payload
                        };

                        component.sendMessage(action);
                    });
            }
        });
    }

    processInitCalls() {
        const isInitiating = true

        this.querySelectorAll("[silica\\:init]").forEach((el) => {
            const methodOrExpressionString = el.getAttribute("silica:init");
            this.callMethodOrSetProperty(methodOrExpressionString, isInitiating);
        });

        // include the case where silica:init is defined on the root element
        const methodOrExpressionString = this.el.getAttribute("silica:init");

        if (methodOrExpressionString) {
            this.callMethodOrSetProperty(methodOrExpressionString, isInitiating);
        }
    }

    callMethod(name, args, isInitiating) {
        const action = {
            type: this.ACTION_TYPE_CALL_METHOD,
            method_name: name,
            args: args
        };

        this.sendMessage(action, isInitiating);
    }

    activateLazy() {
        const action = {
            type: "activate_lazy"
        };

        this.sendMessage(action);
    }

    setProperty(name, value, isInitiating) {
        // If we have a dictionary path as the name, check the property exists
        if (name.includes('.')) {
            let parts = name.split('.')
            let obj = this.data
            let i
            for (i = 0; i < parts.length - 1; i++) {
                if (obj.hasOwnProperty(parts[i])) {
                    obj = obj[parts[i]]
                } else {
                    console.error(`Property ${parts[i]} does not exist on component data`)
                    return
                }
            }
        }

        const action = {
            type: this.ACTION_TYPE_SET_PROPERTY,
            name: name,
            value: value
        };

        this.sendMessage(action, isInitiating);
    }

    sendMessage(action, isInitiating) {
        if (!this.id || !this.name) {
            console.error(
                "No Silica component element found when processing silica:click"
            );
            return;
        }

        // Initiate request concurrency checking
        this.last_request_timestamp = new Date().getTime();
        let current_request_timestamp = this.last_request_timestamp;

        // Show any silica:loading elements
        this.showLoaders(action, isInitiating);

        const params = {
            name: this.name,
            id: this.id,
            actions: [action]
        };

        // Send the POST request using fetch
        fetch("/silica/message", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(params)
        })
            .then((response) => {
                if (response.ok) {
                    return response.json()
                }
                console.log('ERROR')
                response.text().then(text => this.showErrorModal(text))
                throw new Error("Network response was not ok");
            })
            .then((response) => {
                if (this.last_request_timestamp > current_request_timestamp) {
                    console.debug('Request was superseded by a newer request')
                    return;
                }

                let snapshot = response.snapshot;

                if (this.processRedirections(snapshot?.js_calls)) {
                    return;
                }

                this.updateDomWithAlpineMorph(response.html);

                Silica.initComponents();

                this.data = snapshot.data
                this.updateModelValues(snapshot.data);
                this.setQueryParams(snapshot);
                this.processJsCalls(snapshot.js_calls);
                this.processEvents(snapshot.event_calls);

                this.hideLoaders();
            })
            .catch((error) => {
                this.hideLoaders();
                // this.showErrorModal(error.message);

                // console.error("Error:", error);
            });
    }

    // Performance TODO list
    // - In an init function, cache silica:models in the component

    /*
    find lazy silica_components
    call the activation
     */
    initLazyComponents() {
        const lazyComponentEls = this.querySelectorAll("[silica\\:lazy]");

        lazyComponentEls.forEach((componentEl) => {
            let component = silica_components.find(c => c.id === componentEl.getAttribute('silica:id'))

            if (!component) {
                console.error('Component for lazy activation not found in silica_components array')
                return
            }

            component.activateLazy()
        });
    }

    // Todo... refactor so that if we detect parentheses, we send the whole string to the backend for
    // Todo... parsing and execution
    callMethodOrSetProperty(methodOrExpressionString, isInitiating) {
        if (methodOrExpressionString.includes("(")) {
            // Check if string looks like function call and extract args
            const methodNameParts = methodOrExpressionString.split("(");
            const methodName = methodNameParts[0];

            // also remove any quotes from left or right of each arg
            const args = methodNameParts[1]
                .replace(")", "")
                .split(",")
                .map((arg) => arg.trim().replace(/^['"]+|['"]+$/g, ''))
                .filter(arg => arg !== '');
            this.callMethod(methodName, args, isInitiating);
        } else if (methodOrExpressionString.includes("=")) {
            // Checked if it's a property update (e.g., "something=2")
            const [propertyName, value] = methodOrExpressionString.split("=");

            this.setProperty(propertyName.trim(), value.trim().replace(/^['"]+|['"]+$/g, ''), isInitiating);
        } else {
            // Assumed the string is a function without parentheses
            this.callMethod(methodOrExpressionString, undefined, isInitiating);
        }
    }

    handleModelInputEvent(event) {
        const el = event.target || event.currentTarget

        // const modelName = el.getAttribute("silica:model");
        const modelName = this.getAttributeFromPartialName("silica:model", el)
        let currentValue = Silica.data_get(this.data, modelName);

        if (el.type === 'checkbox') {
            // Check if we have a multi-value checkbox
            if (Array.isArray(currentValue)) {

                if (!el.hasAttribute('value') || el.getAttribute('value') === '') {
                    console.error(`silica:model for checkbox ${modelName} is set to an array but the checkbox does not have a valid value attribute`)
                    return
                }

                let value = el.checked ? el.getAttribute('value') : false;

                if (value) {
                    currentValue.push(value)
                } else {
                    let valueToRemove = el.getAttribute('value') || true
                    currentValue = currentValue.filter(v => v !== valueToRemove)
                }

                this.setProperty(modelName, currentValue);
            } else {
                let value = el.checked ? (el.getAttribute('value') || true) : false;
                this.setProperty(modelName, value);
            }
        } else {
            this.setProperty(modelName, el.value);
        }
    }

    handleClickEvent(event) {
        const el = event.currentTarget;

        let instance = this

        /**
         * Handle a silica:click event
         * methodOrExpressionString can be a method name or a string expression, i.e. something = 1
         * @param event
         * @param methodOrExpressionString
         * @param prevent
         */
        function silicaClick(event, methodOrExpressionString, prevent = false) {
            if (prevent) {
                event.preventDefault();
            }

            instance.callMethodOrSetProperty(methodOrExpressionString);
        }

        if (el.hasAttribute("silica:click")) {
            const methodOrExpressionString = el.getAttribute("silica:click");
            silicaClick(event, methodOrExpressionString);
        } else if (el.hasAttribute("silica:click.prevent")) {
            const methodOrExpressionString = el.getAttribute("silica:click.prevent");
            silicaClick(event, methodOrExpressionString);
        }
    }

    setListeners() {
        const models = this.findElementsByPartialAttributeName("silica:model")

        models.forEach((element) => {
            // let handler = this.boundMethods.handleModelInputEvent

            let handler = this.boundMethods.handleModelInputEvent

            const attribute = this.getAttributeInfoFromPartialName("silica:model", element)

            // Check debounce
            if (attribute && attribute.name.includes("debounce")) {
                const debounceTime = parseInt(attribute.name.replace(/[^\d]/g, ''), 10) || 300;
                handler = this.debounce(handler, debounceTime)
            }

            this.boundEvents.set(element, handler);

            if (element.type === "checkbox") {
                element.addEventListener("change", handler);
            } else {
                element.addEventListener("input", handler);
            }
        });

        // Should move to the above way for clickables too when we also deal with more click modifiers
        const clickables = this.querySelectorAll("[silica\\:click\\.prevent], [silica\\:click]");
        clickables.forEach((element) => {
            element.addEventListener("click", this.boundMethods.handleClickEvent);
        });
    }

    removeListeners() {
        const models = this.findElementsByPartialAttributeName("silica:model")

        models.forEach((element) => {
            const handler = this.boundEvents.get(element);
            if (handler) {
                if (element.type === "checkbox") {
                    element.removeEventListener("change", handler);
                } else {
                    element.removeEventListener("input", handler);
                }
                this.boundEvents.delete(element);
            }
            element.removeEventListener("input", this.boundMethods.handleModelInputEvent);
        });

        // Should move to the above way for clickables too when we also deal with more click modifiers
        const clickables = this.querySelectorAll("[silica\\:click\\.prevent]");
        clickables.forEach((element) => {
            element.removeEventListener("click", this.boundMethods.handleClickEvent);
        });
    }

    updateDomWithAlpineMorph(html) {

        function isntElement(el) {
            return typeof el.hasAttribute !== 'function'
        }

        const targetElement = document.querySelector('[silica\\:id="' + this.id + '"]');

        if (!targetElement) {
            console.warn(`Element with id="${this.id}" and name ${this.name} not found.`);
            return
        }

        Alpine.morph(targetElement, html, {
            updating: (el, toEl, childrenOnly, skip) => {
                if (isntElement(el)) return

                if (el.hasAttribute('silica:glued')) return skip()

                // Children will update themselves.
                // if (el.hasAttribute('silica:id') && el.getAttribute('silica:id') !== this.id) return skip()
            },

            updated: (el) => {
                if (isntElement(el)) return
            },

            removing: (el, skip) => {
                if (isntElement(el)) return
            },

            removed: (el) => {
                if (isntElement(el)) return
            },

            adding: (el) => {
                if (isntElement(el)) return
            },

            added: (el) => {
                if (isntElement(el)) return

                if (el.nodeName === 'SCRIPT') {
                    var script = document.createElement('script');
                    //copy over the attributes
                    [...el.attributes].forEach(attr => {
                        script.setAttribute(attr.nodeName, attr.nodeValue)
                    })

                    script.innerHTML = el.innerHTML;
                    el.replaceWith(script)
                }
            },

            key: (el) => {
                if (isntElement(el)) return

                // return el.hasAttribute(`silica:key`)
                //     ? el.getAttribute(`silica:key`)
                //     : // If no "key", then first check for "silica:id", then "id"
                //     el.hasAttribute(`silica:id`)
                //         ? el.getAttribute(`silica:id`)
                //         : el.id
            },

            lookahead: false,
        })

        this.removeListeners();
        this.setListeners();
    }

    updateDomWithMorphdom(html) {
        const targetElement = document.querySelector('[silica\\:id="' + this.id + '"]');

        if (targetElement) {
            // Create a temporary div to hold the new HTML content
            let tempDiv = document.createElement("div");
            tempDiv.innerHTML = html;

            // Use morphdom to update the target element with the new content
            morphdom(targetElement, tempDiv.firstChild, {
                getNodeKey: function (node) {
                    if (typeof node.hasAttribute !== 'function') {
                        return
                    }

                    return node.hasAttribute('silica:key')
                        ? node.getAttribute('silica:key')
                        : node.id
                },
                onNodeAdded: function (node) {
                    if (node.nodeName === 'SCRIPT') {
                        var script = document.createElement('script');
                        //copy over the attributes
                        [...node.attributes].forEach(attr => {
                            script.setAttribute(attr.nodeName, attr.nodeValue)
                        })

                        script.innerHTML = node.innerHTML;
                        node.replaceWith(script)
                    }
                },
                onBeforeElUpdated: (fromEl, toEl) => {
                    // If the element being updated is an input, ignore it
                    // if (fromEl.tagName === "INPUT" && toEl.tagName === "INPUT") {
                    //     return false;
                    // }

                    // Ignore glued items
                    if (
                        fromEl.hasAttribute("silica:glued") &&
                        toEl.hasAttribute("silica:glued")
                    ) {
                        return false;
                    }

                    // Ignore child components
                    if (fromEl.hasAttribute("silica:id") && toEl.hasAttribute("silica:id") && fromEl.getAttribute("silica:id") !== this.id) {
                        return false;
                    }

                    if (fromEl.nodeName === "SCRIPT" && toEl.nodeName === "SCRIPT") {
                        var script = document.createElement('script');
                        //copy over the attributes
                        [...toEl.attributes].forEach(attr => {
                            script.setAttribute(attr.nodeName, attr.nodeValue)
                        })

                        script.innerHTML = toEl.innerHTML;
                        fromEl.replaceWith(script)
                        return false;
                    }
                    return true; // Continue with the update for other elements
                }
            });

            this.removeListeners();
            this.setListeners();
        } else {
            console.warn(`Element with id="${this.id}" and name ${this.name} not found.`);
        }
    }

    processRedirections(jsCalls = []) {
        // Check if we have a redirect
        const redirectFn = jsCalls.find((call) => call.fn === "_silicaRedirect");
        if (redirectFn) {
            window.location.href = redirectFn.args[0];
            return true;
        }
        return false;
    }

    /**
     * Get all elements that match a query, but only if they are inside the subject component
     * @param query
     * @returns []
     */
    querySelectorAll(query) {
        let nodes = [];
        const nodeList = Array.from(this.el.querySelectorAll(query));

        for (let i = 0; i < nodeList.length; i++) {
            if (
                Silica.getNearestComponent(nodeList[i])?.name === this.name
            ) {
                nodes.push(nodeList[i]);
            }
        }


        return nodes;
    }

    /**
     * Get all elements with attribute names that start with a provided string that match a query,
     * and scoped to the current component.
     * "silica:model" will match all:
     * - silica:model
     * - silica:model:debounce
     * - silica:model:debounce.200ms
     * - silica:model:debounce.500ms
     * @param attributeName
     * @returns {*[]}
     */
    findElementsByPartialAttributeName(attributeName) {
        const nodes = document.evaluate(
            `.//*[@*[starts-with(name(), "${attributeName}")]]`,
            this.el,
            null,
            XPathResult.UNORDERED_NODE_ITERATOR_TYPE,
            null
        )

        let els = []
        let el = nodes.iterateNext()
        while (el) {
            els.push(el)
            el = nodes.iterateNext()
        }

        return els
    }

    /**
     * Mimics getAttribute but for partial attribute name and return the attribute's value
     * @param attributeName
     * @returns {*[]}
     */
    getAttributeFromPartialName(attributeName, el) {
        const attribute = document.evaluate(
            `@*[starts-with(name(), "${attributeName}")]`,
            el,
            null,
            XPathResult.STRING_TYPE,
            null
        )

        return attribute.stringValue !== ""
            ? attribute.stringValue
            : null
    }

    getAttributeInfoFromPartialName(attributeName, el) {
        const attribute = document.evaluate(
            `@*[starts-with(name(), "${attributeName}")]`,
            el,
            null,
            XPathResult.ANY_UNORDERED_NODE_TYPE,
            null
        ).singleNodeValue

        return attribute?.value ? {
            value: attribute.value,
            name: attribute.name
        } : null
    }

    /**
     * Show or hide silica:loading elements based on the loading state,
     * including handling elements that should be hidden during loading.
     * @param action The action that initiated the loading
     * @param isInitiating Whether the loading is for a deferred load silica:init
     */
    showLoaders(action, isInitiating) {
        let method_or_property = null;

        if (action?.type === this.ACTION_TYPE_CALL_METHOD) {
            method_or_property = action?.method_name;
        } else if (action?.type === this.ACTION_TYPE_SET_PROPERTY) {
            method_or_property = action?.name;
        }

        // Define selectors for elements to show during loading
        const loadingSelectors = [
            "[silica\\:loading]",
            isInitiating ? "[silica\\:loading\\.init]" : "[silica\\:loading\\.proceeding]",
        ];

        const classSelectors = [
            "[silica\\:loading\\.class]",
            isInitiating ? "[silica\\:loading\\.init\\.class]" : "[silica\\:loading\\.proceeding\\.class]"
        ];

        // Define selectors for elements to hide during loading
        const hiddenSelectors = [
            "[silica\\:loading\\.hidden]",
            isInitiating ? "[silica\\:loading\\.init\\.hidden]" : "[silica\\:loading\\.proceeding\\.hidden]",
        ];

        // Elements to be shown during loading
        this.querySelectorAll(loadingSelectors.join(", ")).forEach(el => {
            if (this.canSetLoadingState(el, method_or_property)) {
                el.style.display = 'block';
            }
        });

        // Elements with a class modifier to show/add during loading
        this.querySelectorAll(classSelectors.join(", ")).forEach(el => {
            if (this.canSetLoadingState(el, method_or_property)) {
                const classToAdd = el.getAttribute("silica:loading.class") ||
                    el.getAttribute("silica:loading.init.class") ||
                    el.getAttribute("silica:loading.proceeding.class");
                if (classToAdd) {
                    el.classList.add(classToAdd);
                }
            }
        });

        // Elements to be hidden during loading
        this.querySelectorAll(hiddenSelectors.join(", ")).forEach(el => {
            if (this.canSetLoadingState(el, method_or_property)) {
                el.style.display = 'none';
            }
        });
    }

    /**
     * Determines if an element should be processed based on the target action.
     * @param el The element to check.
     * @param method_or_property The target method or property name, if any.
     * @returns {boolean} True if the element should be processed, false otherwise.
     */
    canSetLoadingState(el, method_or_property) {
        if(el.hasAttribute("silica:target.except")) {
            const exceptTargets = el.getAttribute("silica:target.except").split(",");
            return !exceptTargets.includes(method_or_property);
        }

        if (el.hasAttribute("silica:target")) {
            const targets = el.getAttribute("silica:target").split(",");
            return targets.includes(method_or_property);
        }

        return true;
    }

    hideLoaders(action) {
        let method_or_property = null;

        if (action?.type === this.ACTION_TYPE_CALL_METHOD) {
            method_or_property = action?.method_name;
        } else if (action?.type === this.ACTION_TYPE_SET_PROPERTY) {
            method_or_property = action?.name;
        }

        const loadingSelectors = [
            "[silica\\:loading]",
            "[silica\\:loading\\.init]",
            "[silica\\:loading\\.proceeding]",
        ];

        const classSelectors = [
            "[silica\\:loading\\.class]",
            "[silica\\:loading\\.init\\.class]",
            "[silica\\:loading\\.proceeding\\.class]"
        ];

        // Define selectors for elements to hide during loading
        const hiddenSelectors = [
            "[silica\\:loading\\.hidden]",
            "[silica\\:init\\.hidden]",
            "[silica\\:proceeding\\.hidden]",
        ];

        // Reverse visibility for elements directly manipulated during loading
        this.querySelectorAll("[silica\\:loading], [silica\\:loading\\.init], [silica\\:loading\\.proceeding]").forEach(el => {
            if (this.canSetLoadingState(el, method_or_property)) {
                el.style.display = '';
            }
        });

        // Reverse class modifications for elements modified during loading
        this.querySelectorAll("[silica\\:loading\\.class], [silica\\:loading\\.init\\.class], [silica\\:loading\\.proceeding\\.class]").forEach(el => {
            if (this.canSetLoadingState(el, method_or_property)) {
                const classToRemove = el.getAttribute("silica:loading.class") ||
                    el.getAttribute("silica:loading.init.class") ||
                    el.getAttribute("silica:loading.proceeding.class");
                if (classToRemove) {
                    el.classList.remove(classToRemove);
                }
            }
        });

        // Show elements that were hidden during loading
        this.querySelectorAll("[silica\\:loading\\.hidden], [silica\\:loading\\.init\\.hidden], [silica\\:loading\\.proceeding\\.hidden]").forEach(el => {
            if (this.canSetLoadingState(el, method_or_property)) {
                el.style.display = '';
            }
        });
    }

    applyClassesToEl(el, classes = "") {
        if (classes) {
            // Split by space to support multiple classes
            const classes_arr = classes.split(" ");
            el.classList.add(...classes_arr);
        }
    }

    removeClassesFromEl(el, classes = "") {
        if (classes) {
            // Split by space to support multiple classes
            const classes_arr = classes.split(" ");
            el.classList.remove(...classes_arr);
        }
    }

    debounce(func, timeout = 300) {
        let timer;
        return (...args) => {
            clearTimeout(timer);
            timer = setTimeout(() => {
                func.apply(this, args);
            }, timeout);
        };
    }

    // Here be _helper methods

    _data_get(obj, path, defaultValue = undefined) {
        // Convert paths like 'a.b.c' into an array ['a', 'b', 'c']
        const keys = path.replace(/\[(\w+)\]/g, '.$1').split('.');

        let result = obj;
        for (const key of keys) {
            // Check if result is null or undefined before trying to access the key
            if (result === null || result === undefined) {
                return defaultValue;
            }
            result = result[key];
        }

        return result === undefined ? defaultValue : result;
    }


    showErrorModal(message) {
        // Remove any existing error modal
        const existingModal = document.querySelector('.error-modal');
        if (existingModal) {
            existingModal.remove();
        }

        const modal = document.createElement('div');
        modal.className = 'error-modal';

        // Apply styles for the modal container (dark background)
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            padding: 1rem 0;
          `;

        modal.innerHTML = `
            <div class="error-content" style="
              background-color: white;
              border-radius: 5px;
              box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
              width: 80%;

              margin: 0 auto;
              overflow-y: auto;
            ">
                <iframe id="error-content-frame" style="width: 100%; height:100%; border: none;"></iframe>
                <svg class="close-error-modal" 
                    style="
                        color: white;
                        cursor: pointer;
                        position: absolute;
                        top: 10px;
                        right: 10px;                   
                        width: 3rem; 
                        height: 3rem 
                    "
                    xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                </svg>       
            </div>
        `;

        // Function to remove the modal
        function removeModal() {
            modal.remove();
            document.removeEventListener('keydown', handleEscapeKey);
        }

        // Close modal when clicking the close button
        const closeButton = modal.querySelector('.close-error-modal');
        closeButton.addEventListener('click', removeModal);

        // Function to handle Escape key press
        function handleEscapeKey(event) {
            if (event.key === 'Escape') {
                removeModal();
            }
        }

        // Add event listeners
        document.addEventListener('keydown', handleEscapeKey);

        // Add modal to the DOM
        document.body.appendChild(modal);

        // Populate the iframe with the HTML content
        const iframe = document.getElementById('error-content-frame');

        const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        iframeDoc.open();
        iframeDoc.write(message);
        iframeDoc.close();
    }

}