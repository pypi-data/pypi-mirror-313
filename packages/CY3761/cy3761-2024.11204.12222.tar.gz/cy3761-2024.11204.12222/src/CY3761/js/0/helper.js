// 当前模块使用 CommonJS 语法, PyExecJS2 可使用该模块
// 该目录下不能有 package.json 的 {"type": "module"}
// ----------------------------------------------------------------------------------------------------
const main_00 = (isExec, cb) => isExec && (typeof cb === 'function') && cb()
// ----------------------------------------------------------------------------------------------------
const main_01 = (isMain) => {
    // console.log(require.main === module)
    if (!isMain) return

    const [func, ...args] = process.argv.slice(2)

    // console.log(func, args)

    if (!func || func.trim().length === 0) return

    try {
        console.log(eval(func)(...args))
    } catch (e) {
        const data = [e.toString(), func, args]

        console.error(data)
    }
}
// ----------------------------------------------------------------------------------------------------
// 一个求和运算, 传入两个参数, 如果传入参数并非数字, 会转为 0 进行作为参数 | 此函数仅用于测试
const sum = (a, b) => {
    [a, b] = [a, b].map(v => Number(v)).map(v => isNaN(v) ? 0 : v)

    return a + b
}
// ----------------------------------------------------------------------------------------------------
module.exports = {
    main_00, main_01, sum
}
// ----------------------------------------------------------------------------------------------------
// 以下 <main_00>函数, 需 isExec==true 确定是否执行
main_00(0, () => {
    const [m, a] = [sum, [5, 7]]

    console.log(`${m.name}(${a})`, '=', m(...a))
})
// 以下 <main_01> 函数, 需 isMain==true, 且通过命令行传入 函数名 (函数存在), 才会执行打印结果
// node.exe I:\33008\项目\CY3761\src\CY3761\js\0\helper.js sum 3 5 | 这样的命令会执行, 默认运行不执行
main_01(require.main === module)