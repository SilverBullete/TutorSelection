module.exports = {
    root: true,
    
    //解析器，这里我们使用babel-eslint
    // parser: '',
    parserOptions: {
        sourceType: 'module',
        parser: 'babel-eslint',
    },

    env: {
        browser: true,
    },

    // https://github.com/feross/standard/blob/master/RULES.md#javascript-standard-style
    //扩展，可以通过字符串或者一个数组来扩展规则
    extends: ["standard", 'plugin:vue/recommended'],

    // required to lint *.vue files
    plugins: [
        'html',
        'standard',
        'promise'
    ],

    // add your custom rules here
    'rules': 'plugin:vue/recommended',

    rules: {
        'arrow-parens': 0,
        'generator-star-spacing': 0,
        'no-debugger': 0,
        'no-tabs': 0,
        'no-mixed-spaces-and-tabs': 0,
        'indent': ["off", "tab"],
        'no-trailing-spaces': 0,
    }
}