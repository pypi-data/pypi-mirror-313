from scipy import stats
import numpy
from sklearn.metrics import r2_score

def linear_regression(x: int, data_x: list = [5,7,8,7,2,17,2,9,4,11,12,9,6], data_y: list = [99,86,87,88,111,86,103,87,94,78,77,85,86]):
  slope, intercept, r, p, std_err = stats.linregress(data_x, data_y)
  def predict(x):
    return slope * x + intercept
  prediction = predict(x)
  return {
    "prediction":prediction,
    "r":r,
    }
def polynomial_regression(x: int, data_x: list = [1,2,3,5,6,7,8,9,10,12,13,14,15,16,18,19,21,22], data_y: list = [100, 90,80,60,60,55,60,65,70,70,75,76,78,79,90,99,99,100]):
    data_x.sort()
    data_y.sort()
    model = numpy.poly1d(numpy.polyfit(data_x, data_y, 3))
    prediction = model(x)
    predictions = model(data_x)
    r = r2_score(data_y, predictions)
    return {
        "prediction": prediction,
        "r": r,
    }

print(f"{linear_regression(10)['prediction']}")
print(f"{polynomial_regression(10)['prediction']}")