#!/bin/bash
sed -i '' '170,195s/func _MakeFiberNative(aff AffFn, _ interface{}) any {/func _MakeFiberNative(aff AffFn, _ interface{}) any {\n\t\/\/ STRIPPED CLOSURE/' src/Effect/Aff.go
sed -i '' 's/return func(_ any) any {//g' src/Effect/Aff.go
# Wait, this would leave extra closing braces!
# It's safer to use python or perl.
