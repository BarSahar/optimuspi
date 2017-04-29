import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor


def polyGetDidt(pixelDist):
    dataset = pd.read_csv('Pixcel_Data.csv')
    x = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, 1]

    poly_req = PolynomialFeatures(degree=5)
    x_poly = poly_req.fit_transform(x)
    poly_req.fit(x_poly, y)
    lin_reg2 = LinearRegression()
    lin_reg2.fit(x_poly, y)

    return lin_reg2.predict(poly_req.fit_transform(pixelDist))


def randomForestGetDist(pixelDist):
    dataset = pd.read_csv('Salary_Data.csv')
    x = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, 1]
    regressor = RandomForestRegressor(n_estimators=300, random_state=0)
    regressor.fit(x, y)
    return regressor.predict(pixelDist)


def average(pixelDist):
    return (polyGetDidt(pixelDist) + randomForestGetDist(pixelDist)) / 2


def printRes(pixelDist):
    print("Poly predict: " + str(polyGetDidt(pixelDist)))
    print("Random Forest predict: " + str(randomForestGetDist(pixelDist)))
    print("average: " + str(average(pixelDist)))


if __name__=="__main__":
    printRes(7)

