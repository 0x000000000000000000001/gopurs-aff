module Scratch where

import Prelude
import Data.Array as Array

test :: Array String -> Boolean
test arr = Array.length (Array.filter (_ == "foo") arr) > 0
