module Scratch8 where

import Prelude
import Data.Maybe

foo :: forall a. Eq a => a -> Maybe a -> Boolean
foo a_2 m = isJust (map (eq a_2) m)
