const fs = require('fs');
const expr = JSON.parse(fs.readFileSync('test_makeAff.json')).expression;

function search(e) {
    if (!e) return;
    if (e.type === 'Var') {
        console.log("Var:", e.value.identifier);
    }
    
    if (e.type === 'App') { search(e.abstraction); search(e.argument); }
    if (e.type === 'Let') { search(e.expression); e.binds.forEach(b => search(b.expression)); }
    if (e.type === 'Abs') { search(e.expression); }
    if (e.type === 'Case') { e.caseExpressions.forEach(search); e.caseAlternatives.forEach(a => search(a.expression)); }
    if (e.type === 'TypeApp') { search(e.expression); }
}

search(expr);
