{-# LANGUAGE ScopedTypeVariables #-}
module Regression
  ( linearRegression
  , predict
  ) where

-- | Given a list of (x, y) points, compute the linear regression coefficients.
-- Returns (slope, intercept).
linearRegression :: [(Double, Double)] -> (Double, Double)
linearRegression points =
  let n      = fromIntegral (length points)
      sumX   = sum (map fst points)
      sumY   = sum (map snd points)
      sumXY  = sum [ x * y | (x,y) <- points ]
      sumXX  = sum [ x * x | (x,_) <- points ]
      denom  = n * sumXX - sumX * sumX
      slope  = if denom == 0 then error "Denom zero" else (n * sumXY - sumX * sumY) / denom
      intercept = (sumY - slope * sumX) / n
  in (slope, intercept)

-- | Given regression coefficients (slope, intercept) and an x value,
-- return the predicted y value.
predict :: (Double, Double) -> Double -> Double
predict (slope, intercept) x = slope * x + intercept
