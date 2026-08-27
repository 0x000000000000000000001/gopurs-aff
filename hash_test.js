function hs(str) {
  let hash = 5381;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) + hash) + str.charCodeAt(i);
  }
  return (hash >>> 0).toString();
}

console.log(hs("Data.Monoid.MonoidRecord"));
console.log(hs("String"));
console.log(hs("Array"));
console.log(hs("Data.Unit.Unit"));
console.log(hs("Record"));
console.log(hs("Data.Ordering.Ordering"));
console.log(hs("Any"));
