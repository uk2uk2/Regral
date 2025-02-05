module Main where

import Regression
import Test.HUnit

-- A rudimentary test case: using a small dataset.
testRegression :: Test
testRegression = TestCase $ do
  let points = [(1, 2), (2, 3), (3, 5), (4, 4)]
      (m, b) = linearRegression points
      yPred  = predict (m, b) 5
  -- Check that the computed slope and intercept are within reasonable tolerance.
  assertBool "slope ~ 0.8" (abs (m - 0.8) < 0.1)
  assertBool "intercept ~ 1.3" (abs (b - 1.3) < 0.1)
  -- Also verify that the prediction is consistent.
  assertBool "prediction consistency" (abs (yPred - (m*5 + b)) < 0.001)

main :: IO ()
main = do
  counts <- runTestTT testRegression
  print counts
