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
console.log(hashString("(ConstrainedType [(App (TypeConstructor (Qualified (Just \"Data.Monoid\") \"Monoid\")) (TypeConstructor (Qualified (Just \"Effect.Aff\") \"Canceler\")))] (TypeConstructor (Qualified (Just \"Effect.Aff\") \"Canceler\")))"));
