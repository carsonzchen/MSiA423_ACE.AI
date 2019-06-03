import train_model
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.ensemble.partial_dependence import partial_dependence, plot_partial_dependence

new_model = train_model.newmodel

# predict on train and test
preds_train = new_model.predict(train_model.train_features)
print('train misclassification rate: ', np.sum(preds_train != train_model.train_labels) / train_model.train_features.shape[0])

preds_test = new_model.predict(train_model.test_features)
print('test misclassification rate: ', np.sum(preds_test != train_model.test_labels) / train_model.test_features.shape[0])

feature_importance = pd.DataFrame(new_model.feature_importances_, index = train_model.feature_list, columns=['importance']).sort_values('importance',ascending=False)
print(feature_importance)
print(sum(feature_importance['importance']))

y_actu = pd.Series(train_model.test_labels, name='Actual')
y_pred = pd.Series(preds_test, name='Predicted')
df_confusion = pd.crosstab(y_actu, y_pred)
df_confusion