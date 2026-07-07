import joblib
from sklearn.linear_model import LinearRegression
import numpy as np

# A very basic dummy model for sales forecasting
# In a real scenario, this would be a Prophet or XGBoost model
model = LinearRegression()

# Dummy training data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([100, 120, 150, 170, 200])
model.fit(X, y)

# Save the dummy model
joblib.dump(model, 'models/forecast_model.pkl')
print("Dummy model saved to models/forecast_model.pkl")
