const errors = {
    invalidSelectorType: "Error: Invalid selector type",
    elementNotDefined: "Error: element was not defined",
    elementTypeError: "Error: Element is not of type NodeList"
}

class __Executor {
    constructor(element, node=false) {
        this.element = null;

        if(element instanceof Object)
            this.element = element;
        else {
            this.element = !node 
            ? document.querySelector(element)
            : document.querySelectorAll(element)
        } 
        this.this = this.element
        this.node = node
        if(!element) throw errors.elementNotDefined
    }

    addClass(className) {
        this.this.classList.add(className);
    }

    removeClass(className) {
        this.this.classList.remove(className);
    }

    toggleClass(className) {
        this.this.classList.toggle(className);
    }

    get(element, callback = null) {
        if (callback) {
            return callback($(this.element.querySelector(element)))
        }else {
            return this.this.querySelector(element);
        }
    }

    getAll(elements, callback = null) {
        if (callback) {
            return callback($(this.element.querySelectorAll(elements)))
        } else {
            return [...this.this.querySelectorAll(elements)];
        }
    }

    text() {
        return this.this.textContent;
    }

    setText(text) {
        this.this.textContent = text;
    }

    removeSelf() {
        this.this.remove();
    }

    remove(item) {
        this.this.remove(item)
    }

    containClass(className) {
        return this.this.classList.contains(className)
    }

    for(callback){
        if(this.node) return this.element.forEach(callback)
        throw  errors.elementTypeError
    }

    filter(callback){
        if(this.node) return [...this.element].filter(callback)
        throw `${errors.invalidSelectorType} \n ${errors.elementTypeError}`
    }

    map(callback){
        if(this.node) return [...this.element].map(callback)
        throw  `${errors.invalidSelectorType} \n ${errors.elementTypeError}`
    }

    on(event, callback) {
        this.element && this.node
        && this.element.forEach(el => 
            el.addEventListener(event, callback)
        );
        this.element && !this.node
        && this.element.addEventListener(event, callback);
    }
}

const _$$ = (element) => new  __Executor(element, true).this;
const _$ = (element) => new  __Executor(element).this;

const $$ = (element) => new  __Executor(element, true);
const $ = (element) => new  __Executor(element);