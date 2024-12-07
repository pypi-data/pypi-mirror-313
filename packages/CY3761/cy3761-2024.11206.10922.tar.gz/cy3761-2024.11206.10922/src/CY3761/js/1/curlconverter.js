// https://www.npmjs.com/package/curlconverter
// https://github.com/curlconverter/curlconverter
// https://curlconverter.com/
// npm i curlconverter
// ----------------------------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------------------------
import * as curlconverter from 'curlconverter'
import {read} from './helper.js'
// ----------------------------------------------------------------------------------------------------
const getCode = (sn) => curlconverter.toPython(read(sn))

// ----------------------------------------------------------------------------------------------------
const a00 = process.argv
const u00 = decodeURIComponent(import.meta.url.slice('file:///'.length))
const u01 = a00[1].replaceAll('\\', '/')
const a03 = a00[3]
// ----------------------------------------------------------------------------------------------------
// console.log(u00 === u01, a03)
u00 === u01 && a03 && console.log(getCode(a03))