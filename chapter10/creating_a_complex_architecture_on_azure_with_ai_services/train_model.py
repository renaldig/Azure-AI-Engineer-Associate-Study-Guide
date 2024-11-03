# Import necessary libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

# Load the Iris dataset
iris = load_iris()
X, y = iris.data, iris.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the classifier
clf.fit(X_train, y_train)

# Evaluate the model's accuracy
accuracy = clf.score(X_test, y_test)
print(f"Model accuracy: {accuracy:.2f}")

# Save the trained model to a file
dump(clf, 'model.joblib')

# Register the model in Azure Machine Learning
from azureml.core import Workspace, Model

# Connect to your Azure ML workspace
ws = Workspace.from_config()  # Assumes the config.json file is in the same directory

# Register the model
model = Model.register(
    workspace=ws,
    model_name='iris-classifier',
    model_path='model.joblib',
    description='A simple RandomForest model for classifying Iris species.',
    tags={'data': 'Iris', 'model': 'RandomForest'},
    model_framework=Model.Framework.SCIKITLEARN,
    model_framework_version='0.24.1'
)
