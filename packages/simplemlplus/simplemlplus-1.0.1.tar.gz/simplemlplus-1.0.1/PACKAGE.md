# simplemlplus
> Version: 1.0.1

Simple machine learning one-liners.
## Headless Mode
All functions create plots, useful for seeing how they work. To use a headless version (no plot), just import them from `simplemlplus.headless` instead of `simplemlplus`.
## Plot Only
If you just want to see the visual representation, simply call the function without assigning it to a variable.
```python
import simplemlplus
linear_regression(6, [5, 2, 7, 8], [4, 2, 4, 8])
```

## Linear Regression
```python
linear_regression(x: int, x_data: list, y_data: list)

Returns:

{
    "prediction": predicted value,
    "r", relationship, how well this regression fits the model
}
```
Both `x_data` and `y_data` have default values if you want to play around with existing data.
### Example Use
```python
import simplemlplus
data = linear_regression(10, [1, 2, 3, 4], [1, 2, 3, 4])
```

## Polynomial Regression
```python
import simplemlplus
data = polynomial_regression(x: int, x_data: list, y_data: list)

Returns:

{
    "prediction": predicted value,
    "r", relationship^2, how well this regression fits the model
}
```
Both `x_data` and `y_data` have default values if you want to play around with existing data.
### Example Use
```python
polynomial_regression(10, [1, 2, 3, 4], [1, 2, 3, 4])
```

## Contribuiting
The repo is `XenonPy/ai`. Feel free to open an issue/PR for any changes.

