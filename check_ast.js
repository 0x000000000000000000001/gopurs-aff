const fs = require('fs');
const corefn = JSON.parse(fs.readFileSync('output/Test.Main/corefn.json'));

function findMakeAff(expr) {
    if (!expr) return null;
    if (expr.type === 'Let') {
        return findMakeAff(expr.expression);
    }
    if (expr.type === 'App') {
        if (expr.abstraction && expr.abstraction.value && expr.abstraction.value.identifier === 'makeAff') {
            return expr.argument;
        }
        return findMakeAff(expr.abstraction) || findMakeAff(expr.argument);
    }
    if (expr.type === 'Abs') {
        return findMakeAff(expr.expression);
    }
    if (expr.type === 'Case') {
        for (let alt of expr.caseAlternatives) {
            let res = findMakeAff(alt.expression);
            if (res) return res;
        }
    }
    return null;
}

let decl = corefn.decls.find(d => d.identifier === 'test_makeAff');
let arg = findMakeAff(decl.expression);
console.log(JSON.stringify(arg, null, 2));
