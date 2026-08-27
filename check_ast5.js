const fs = require('fs');
const expr = JSON.parse(fs.readFileSync('test_makeAff.json')).expression;

function search(e) {
    if (!e) return;
    if (e.type === 'Var') console.log("Var:", e.value.identifier);
    else if (e.type === 'App') { search(e.abstraction); search(e.argument); }
    else if (e.type === 'Let') { search(e.expression); e.binds.forEach(b => search(b.expression)); }
    else if (e.type === 'Abs') { search(e.expression); }
    else if (e.type === 'Case') { e.caseExpressions.forEach(search); e.caseAlternatives.forEach(a => search(a.expression)); }
    else if (e.type === 'TypeApp') { search(e.expression); }
    else if (e.type === 'Constructor') { console.log("Constructor:", e.constructorName.identifier); }
    else if (e.type === 'Literal') {}
    else console.log("UNKNOWN TYPE:", e.type);
}

search(expr);
