import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score

# Load the dataset
file_path = 'output.csv'  # Update with your actual path
data = pd.read_csv(file_path)

# Split the data into features and target
X = data.drop(columns=['A'])
y = data['A']

# Encode the target labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Initialize the classifiers
# 1. Naive Bayes
naive_bayes = GaussianNB(var_smoothing=1e-3)

# 2. Decision Tree
decision_tree = DecisionTreeClassifier(
    criterion='entropy', 
    max_depth=8, 
    min_samples_split=7, 
    min_samples_leaf=3, 
    random_state=42
)

# 3. K-Nearest Neighbors
knn = KNeighborsClassifier(
    n_neighbors=7, 
    weights='distance', 
    metric='manhattan'
)


# Train and test Naive Bayes
nb_scores = cross_val_score(naive_bayes, X_train, y_train, cv=10)
naive_bayes.fit(X_train, y_train)
nb_predictions = naive_bayes.predict(X_test)
nb_accuracy = accuracy_score(y_test, nb_predictions)
nb_report = classification_report(y_test, nb_predictions, target_names=label_encoder.classes_)

# Train and test Decision Tree
dt_scores = cross_val_score(decision_tree, X_train, y_train, cv=10)
decision_tree.fit(X_train, y_train)
dt_predictions = decision_tree.predict(X_test)
dt_accuracy = accuracy_score(y_test, dt_predictions)
dt_report = classification_report(y_test, dt_predictions, target_names=label_encoder.classes_)

# Train and test KNN
knn_scores = cross_val_score(knn, X_train, y_train, cv=10)
knn.fit(X_train, y_train)
knn_predictions = knn.predict(X_test)
knn_accuracy = accuracy_score(y_test, knn_predictions)
knn_report = classification_report(y_test, knn_predictions, target_names=label_encoder.classes_)


print("Naive Bayes Accuracy:", nb_accuracy)
print("Naive Bayes Score:", np.mean(nb_scores))
print("Naive Bayes Report:\n", nb_report)
print("Naive Bayes Crosstab:\n", pd.crosstab(y_test, nb_predictions, rownames=['True'], colnames=['Predicted'], margins=True))

print("Decision Tree Accuracy:", dt_accuracy)
print("Decision Tree Score:", np.mean(dt_scores))
print("Decision Tree Report:\n", dt_report)
print("Decision Tree Crosstab:\n", pd.crosstab(y_test, dt_predictions, rownames=['True'], colnames=['Predicted'], margins=True))

print("KNN Accuracy:", knn_accuracy)
print("KNN Score:", np.mean(knn_scores))
print("KNN Report:\n", knn_report)
print("KNN Crosstab:\n", pd.crosstab(y_test, knn_predictions, rownames=['True'], colnames=['Predicted'], margins=True))
