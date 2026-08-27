const fs = require('fs');
const expr = JSON.parse(fs.readFileSync('test_makeAff.json')).expression;

function search(e) {
    if (!e) return;
    if (e.type === 'App' && e.abstraction && e.abstraction.type === 'TypeApp' && e.abstraction.expression && e.abstraction.expression.value && e.abstraction.expression.value.identifier === 'mempty') {
        console.log("FOUND APP OF MEMPTY!");
        console.log("Argument is:", e.argument.value.identifier);
    } else if (e.type === 'TypeApp' && e.expression && e.expression.value && e.expression.value.identifier === 'mempty') {
        console.log("FOUND TYPEAPP OF MEMPTY WITHOUT APP!");
    }
    
    if (e.type === 'App') { search(e.abstraction); search(e.argument); }
    if (e.type === 'Let') { search(e.expression); e.binds.forEach(b => search(b.expression)); }
    if (e.type === 'Abs') { search(e.expression); }
    if (e.type === 'Case') { e.caseExpressions.forEach(search); e.caseAlternatives.forEach(a => search(a.expression)); }
    if (e.type === 'TypeApp') { search(e.expression); }
}

search(expr);
