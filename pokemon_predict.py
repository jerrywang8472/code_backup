import pandas
import numpy
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam, Nadam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler

scaler = StandardScaler()

training_file_path = "train.csv"
testing_file_path = "test.csv"
df = pandas.read_csv(training_file_path)
# for column_type, column_name in zip(df.dtypes, df.columns):
#     print(column_type, column_name)
test_df = pandas.read_csv(testing_file_path)

df = df.drop(['ID'], axis=1)
y_train = df["class"]
class_weight = dict(y_train.value_counts())

df = df.drop(['class'], axis=1)

ids = test_df["id"]
test_df = test_df.drop(['id'], axis=1)

training_set_length = len(df)

combined_df = df.append(test_df)
combined_df = combined_df.astype({"terrainType":"object"})
# drop_list = []
# for column_name in combined_df.columns:
#     if "city" in column_name:
#         drop_list.append(column_name)
# combined_df = combined_df.drop(drop_list, axis=1)

combined_df = pandas.get_dummies(combined_df)
scaler.fit(combined_df.to_numpy())
df = combined_df.iloc[:training_set_length, :]
test_df = combined_df.iloc[training_set_length:, :]

x_train = df.to_numpy()
y_train = pandas.get_dummies(y_train)
y_train = y_train.to_numpy()
x_train = x_train.astype(numpy.float32)
x_train = scaler.transform(x_train)

# x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.2, random_state=42)


x_test = test_df.to_numpy()
x_test = x_test.astype(numpy.float32)
x_test = scaler.transform(x_test)

feature_num = len(x_train[0])

model = Sequential()
model.add(Dense(512, activation='elu', input_shape=(feature_num,)))
model.add(BatchNormalization())
model.add(Dropout(0.3))
model.add(Dense(256, activation='elu'))
model.add(BatchNormalization())
model.add(Dropout(0.3))
model.add(Dense(256, activation='elu'))
model.add(BatchNormalization())
model.add(Dropout(0.3))
model.add(Dense(128, activation='elu'))
model.add(BatchNormalization())
model.add(Dropout(0.3))
model.add(Dense(128, activation='elu'))
model.add(BatchNormalization())
model.add(Dropout(0.3))
model.add(Dense(64, activation='elu'))
model.add(BatchNormalization())
model.add(Dropout(0.3))
model.add(Dense(6, activation='softmax'))

nadam = Nadam(learning_rate=0.001)
model.compile(optimizer=nadam, loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=100, batch_size=32, class_weight=class_weight)
y_test = model.predict(x_test)
y_test = numpy.argmax(y_test, axis=1)
output_df = pandas.DataFrame({"ID":ids, "class":y_test})
output_df.to_csv("submission.csv", index = False)