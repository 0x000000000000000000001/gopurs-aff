const crypto = require('crypto');
function hashString(s) {
  let hash = 0;
  for (let i = 0; i < s.length; i++) {
    const char = s.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash = hash & hash;
  }
  return (hash >>> 0).toString();
}
console.log(hashString("Canceler"));
console.log(hashString("Effect.Aff.Canceler"));
