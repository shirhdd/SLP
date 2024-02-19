import json
import tensorflow as tf
import matplotlib.pyplot as plt
def deserialize_element_spec(serializable_spec):
    def deserialize_tensor_spec(spec_dict):
        return tf.TensorSpec(shape=spec_dict["shape"], dtype=spec_dict["dtype"])

    if isinstance(serializable_spec, list):
        return tuple(deserialize_tensor_spec(spec) for spec in serializable_spec)
    else:  # Similarly, assuming it's either a list (tuple) or a single spec.
        return deserialize_tensor_spec(serializable_spec)

with open('element_spec_saved_r_w_s_sh.json', 'r') as f:
    loaded_spec_dict = json.load(f)

element_spec = deserialize_element_spec(loaded_spec_dict)
data = tf.data.experimental.load("S:\\data_saved_r_w_s_sh", element_spec=element_spec)

print("Total data size:", len(list(data.as_numpy_iterator())))

data = data.take(18000)
data = data.cache()
data = data.shuffle(buffer_size=9000)
data = data.batch(50)
# data = data.prefetch(8)

train = data.take(250)
test = data.skip(250).take(50)

from keras import layers
from keras import models

model = models.Sequential()
# todo: change shape!
model.add(layers.Conv2D(16, (3, 3), activation='relu', input_shape=(191, 65, 1)))
model.add(layers.Conv2D(16, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile('Adam', loss='BinaryCrossentropy', metrics=[tf.keras.metrics.Recall(), tf.keras.metrics.Precision()])
hist = model.fit(train, epochs=4, validation_data=test)
plt.title('Loss')
plt.plot(hist.history['loss'], 'r')
plt.plot(hist.history['val_loss'], 'b')
plt.show()
plt.title('Precision')
plt.plot(hist.history['precision'], 'r')
plt.plot(hist.history['val_precision'], 'b')
plt.show()
plt.title('Recall')
plt.plot(hist.history['recall'], 'r')
plt.plot(hist.history['val_recall'], 'b')
plt.show()

X_test, y_test = test.as_numpy_iterator().next()
yhat = model.predict(X_test)
yhat = [1 if prediction > 0.5 else 0 for prediction in yhat]
print(yhat)
print(y_test)

