const fs = require('fs');
function hashString(s) {
  let hash = 0;
  for (let i = 0; i < s.length; i++) {
    const char = s.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash = hash & hash;
  }
  return (hash >>> 0).toString();
}

function traverse(obj) {
  if (typeof obj === 'string') {
    if (hashString(obj) === '193435443') {
      console.log("MATCH:", obj);
    }
  } else if (Array.isArray(obj)) {
    obj.forEach(traverse);
  } else if (obj !== null && typeof obj === 'object') {
    Object.values(obj).forEach(traverse);
  }
}
// check common types
const types = [
  "Effect.Aff.Canceler",
  "Prim.String",
  "Prim.Unit",
  "Prim.Boolean",
  "Data.Unit.Unit",
  "Prim.Array",
  "(ADT [\"Data\",\"Unit\",\"Unit\"] [])"
];
types.forEach(t => {
  if (hashString(t) === '193435443') console.log("MATCHED:", t);
});
