import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_digits
from tensorflow.keras.datasets import mnist
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Flatten, Dropout

from sklearn.preprocessing import minmax_scale, OneHotEncoder

def sourceANN(type):

    match(type):

        case 'cat':
            print(
"""
Example:

# Load the diabetes dataset
breast_cancer = load_breast_cancer()
X, y = breast_cancer.data, breast_cancer.target

print(breast_cancer.DESCR)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Build the model
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(32, activation='relu'),
    #Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train_scaled, y_train, validation_split=0.2, epochs=20, batch_size=32, verbose=1)

# Evaluate the model
y_pred_proba = model.predict(X_test_scaled)
y_pred = (y_pred_proba > 0.5).astype(int)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Model Accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'])
plt.show()

# Model Loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'])
plt.show()
""")
        case 'imgCat':
            print(
"""
def load_data():

    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = x_train.astype('float32') / 255
    x_test = x_test.astype('float32') / 255

    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)
    
    return x_train, y_train, x_test, y_test

def create_model():
    model = Sequential([
        Flatten(input_shape=(28, 28)),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def train_and_evaluate(model, x_train, y_train, x_test, y_test, epochs=10):
    model.fit(x_train, y_train, epochs=epochs, validation_split=0.1, verbose=0)
    _, accuracy = model.evaluate(x_test, y_test, verbose=0)
    return accuracy

def apply_overfitting_prevention(method):
    model = create_model()
    
    if method == 'dropout':
        model.add(Dropout(0.5))
    elif method == 'early_stopping':
        from keras.callbacks import EarlyStopping
        early_stopping = EarlyStopping(monitor='val_loss', patience=3)
        return model, early_stopping
#    elif method == 'data_augmentation':
#        from tensorflow.keras.preprocessing.image import ImageDataGenerator
#        datagen = ImageDataGenerator(rotation_range=10, zoom_range=0.1, width_shift_range=0.1, height_shift_range=0.1)
#        return model, datagen
    
    return model, None

def main():
    x_train, y_train, x_test, y_test = load_data()
    
    # Base model
    base_model = create_model()
    base_accuracy = train_and_evaluate(base_model, x_train, y_train, x_test, y_test)
    print(f"Base model accuracy: {base_accuracy:.4f}")
    
    # Models with overfitting prevention
    methods = ['dropout', 'early_stopping']#, 'data_augmentation']
    
    for method in methods:
        model, extra = apply_overfitting_prevention(method)
        
        if method == 'early_stopping':
            accuracy = train_and_evaluate(model, x_train, y_train, x_test, y_test, epochs=50)
        else:
            accuracy = train_and_evaluate(model, x_train, y_train, x_test, y_test)
        
        print(f"{method.capitalize()} model accuracy: {accuracy:.4f}")

if __name__ == "__main__":
    main()
""")
        case 'reg':
            print(
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# Load and preprocess the data
california = fetch_california_housing()
X, y = california.data, california.target

# Feature engineering
X = np.column_stack((X, X[:, 0]**2, X[:, 1]**2, X[:, 0]*X[:, 1], np.log1p(X[:, 0])))

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test) 

# Define the model
def create_model(input_dim):
    model = Sequential([
        Dense(128, activation='relu', input_shape=(input_dim,)),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error', metrics=['mae'])
    return model

# Callbacks
early_stopping = EarlyStopping(patience=20, restore_best_weights=True)
lr_reducer = ReduceLROnPlateau(factor=0.5, patience=10)

# K-fold Cross-validation
n_splits = 5
kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
r2_scores = []

for fold, (train_index, val_index) in enumerate(kf.split(X_train_scaled), 1):
    print(f"Fold {fold}")
    X_train_fold, X_val_fold = X_train_scaled[train_index], X_train_scaled[val_index]
    y_train_fold, y_val_fold = y_train[train_index], y_train[val_index]

    model = create_model(X_train_scaled.shape[1])
    history = model.fit(X_train_fold, y_train_fold, validation_data=(X_val_fold, y_val_fold),
                        epochs=200, batch_size=32, verbose=0, callbacks=[early_stopping, lr_reducer])

    y_pred = model.predict(X_val_fold)
    r2 = r2_score(y_val_fold, y_pred)
    r2_scores.append(r2)
    print(f"R² score: {r2:.4f}")

print(f"\nMean R² score: {np.mean(r2_scores):.4f}")

# Train the final model on all training data
final_model = create_model(X_train_scaled.shape[1])
history = final_model.fit(X_train_scaled, y_train, validation_split=0.2,
                          epochs=200, batch_size=32, verbose=0, callbacks=[early_stopping, lr_reducer])

# Evaluate on test set
y_pred = final_model.predict(X_test_scaled)
final_r2 = r2_score(y_test, y_pred)
print(f"Final R² score on test set: {final_r2:.4f}")

# Model Loss
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Mean Squared Error')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper right')

plt.tight_layout()
plt.show()
""")
    return None

def sourceCNN():

    print(
"""
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import cifar10
import matplotlib.pyplot as plt

def load_data():
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0  # norm pixel values
    return (x_train, y_train), (x_test, y_test)

def build_model(num_filters, kernel_size, num_layers):
    model = models.Sequential()
    model.add(layers.Conv2D(num_filters, kernel_size, activation='relu', input_shape=(32, 32, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    
    for _ in range(num_layers - 1):
        model.add(layers.Conv2D(num_filters * 2, kernel_size, activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
    
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))
    return model

def train_model(model, x_train, y_train, x_test, y_test, learning_rate, batch_size):
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    history = model.fit(x_train, y_train,
                        epochs=10,
                        batch_size=batch_size,
                        validation_data=(x_test, y_test))
    
    return history

def plot_history(history):
    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

hyperparams = [
    {'num_filters': 32, 'kernel_size': (3, 3), 'num_layers': 3, 'learning_rate': 0.01, 'batch_size': 32},
    {'num_filters': 64, 'kernel_size': (3, 3), 'num_layers': 3, 'learning_rate': 0.001, 'batch_size': 64},
    {'num_filters': 128, 'kernel_size': (3, 3), 'num_layers': 3, 'learning_rate': 0.0001, 'batch_size': 128}
]

(x_train, y_train), (x_test, y_test) = load_data()

for params in hyperparams:
    print(f"Training with: {params}")
    
    # building and train the model
    model = build_model(params['num_filters'], params['kernel_size'], params['num_layers'])
    history = train_model(model, x_train, y_train, x_test, y_test,
                          params['learning_rate'], params['batch_size'])
    
    # plotting the results
    plot_history(history)
""")
    return None

def sourceRNN():

    print(
"""
import numpy as np
import pandas as pd
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Embedding, SimpleRNN, Dense
from keras.preprocessing.sequence import pad_sequences

def load_data(num_words = 10000, maxlen = 500):

    (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=num_words)
    
    # Pad sequences to ensure uniform input size
    x_train = pad_sequences(x_train, maxlen = maxlen)
    x_test = pad_sequences(x_test, maxlen = maxlen)
    
    return (x_train, y_train), (x_test, y_test)

def build_model(input_length):
    model = Sequential()
    model.add(Embedding(input_dim = 10000, output_dim = 128, input_length = input_length))
    model.add(SimpleRNN(128))
    model.add(Dense(1, activation = 'sigmoid'))
    
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model

def train_model(model, train_data):
    history = model.fit(train_data[0], train_data[1], epochs = 5, batch_size = 32)
    
    return history

def evaluate_model(model, test_data):
    loss, accuracy = model.evaluate(test_data[0], test_data[1])
    
    print(f"Test Loss: {loss}, Test Accuracy: {accuracy}")

if __name__ == "__main__":
    # Load data
    train_data, test_data = load_data()
    
    # Build and compile the model
    model = build_model(input_length=train_data[0].shape[1])
    
    # Train the model
    train_model(model, train_data)
    
    # Evaluate the model
    evaluate_model(model, test_data)
""")
    return None

def sourceTransLearn():

    print(
"""
import tensorflow as tf
import tensorflow_datasets as tfds

from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50

(train_data, test_data), info = tfds.load('caltech101', split = ['train', 'test'], with_info = True, as_supervised = True)

def preprocessImage(image, label):
    image = tf.image.resize(image, (224, 224))
    image = image / 255.0 # normalize the pixel values
    label = tf.math.maximum(label - 1, 0) # shifting the range of the labels to 0-100
    
    return image, label

train_data = train_data.map(preprocessImage).batch(64)
test_data = test_data.map(preprocessImage).batch(64)

base_model = ResNet50(weights = 'imagenet', include_top = False, input_shape = (224, 224, 3))

 # freezing the layers in the base layer excluding the last 10

for layer in base_model.layers[:-10]:
    layer.trainable = False

model_resnet = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),

    layers.Dense(512, activation = 'relu'),
    layers.Dropout(0.5),
    
    layers.Dense(101, activation = 'softmax')  # 101 categories in Caltech101
])

model_resnet.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])

history_resnet = model_resnet.fit(train_data, validation_data = test_data, epochs = 10)

# WITHOUT TRANSFER LEARNING

model_cnn = models.Sequential([
    layers.Conv2D(32, (3, 3), activation = 'relu', input_shape = (224, 224, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation = 'relu'),
    layers.MaxPooling2D((2, 2)),

    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),

    layers.Dense(512, activation = 'relu'),
    layers.Dropout(0.5),

    layers.Dense(101, activation = 'softmax')
])

model_cnn.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])

history_cnn = model_cnn.fit(train_data, validation_data = test_data, epochs = 10)

""")
    return None

def sourceLSTM():

    print(
"""
import numpy as np
import pandas as pd
from keras.layers import LSTM
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Embedding, SimpleRNN, Dense
from keras.preprocessing.sequence import pad_sequences

def load_data(num_words = 10000, maxlen = 500):

    (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=num_words)
    
    # Pad sequences to ensure uniform input size
    x_train = pad_sequences(x_train, maxlen = maxlen)
    x_test = pad_sequences(x_test, maxlen = maxlen)
    
    return (x_train, y_train), (x_test, y_test) 

def build_rnn_model(input_length):
    model = Sequential()
    model.add(Embedding(input_dim = 10000, output_dim = 128, input_length = input_length))
    model.add(SimpleRNN(128))
    model.add(Dense(1, activation = 'sigmoid'))
    
    model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
    
    return model

def build_lstm_model(input_length):
    model = Sequential()
    model.add(Embedding(input_dim = 10000, output_dim = 128, input_length = input_length))
    model.add(LSTM(128))
    model.add(Dense(1, activation = 'sigmoid'))
    
    model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
    
    return model

def train_model(model, train_data):
    history = model.fit(train_data[0], train_data[1], epochs = 5, batch_size = 32)
    
    return history

def evaluate_model(model, test_data):
    loss, accuracy = model.evaluate(test_data[0], test_data[1])
    
    print(f"Test Loss: {loss}, Test Accuracy: {accuracy}")

if __name__ == "__main__":
    # Load data
    train_data, test_data = load_data()
    
    print('\n RNN: ')
    # Build and compile the RNN model
    rnn_model = build_rnn_model(input_length=train_data[0].shape[1])
    
    # Train the model
    train_model(rnn_model, train_data)
    
    # Evaluate the model
    evaluate_model(rnn_model, test_data)

    print('\n LSTM: ')
    # Build and compile the RNN model
    lstm_model = build_lstm_model(input_length=train_data[0].shape[1])
    
    # Train the model
    train_model(lstm_model, train_data)
    
    # Evaluate the model
    evaluate_model(lstm_model, test_data)

""")
    return None

def sourceRBM():
    print(
"""
from sklearn.datasets import load_digits
from sklearn.preprocessing import minmax_scale, OneHotEncoder
from sklearn.model_selection import train_test_split

d = load_digits()
x=d.data
print(x)
y=d.target
print(y)

print("The size of the train dataset",x.shape)
print("the data type of the dataset ",x.dtype)

# Min-max scaling
x_scaled = minmax_scale(x, feature_range=(0, 1))
x_scaled

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x_scaled, y,
                                            test_size=0.2, random_state=42)

                                            
print("The size of the train dataset",x_train.shape)
print("The size of the test dataset",y_train.shape )

from sklearn.neural_network import BernoulliRBM
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Create an RBM model
rbm = BernoulliRBM(n_components=100, learning_rate=0.02, n_iter=15,
                   random_state=42, verbose=True)

# Create a classifier
classifier = LogisticRegression(max_iter=500)

# Create a pipeline combining RBM and classifier
pipeline = Pipeline(steps=[('rbm', rbm), ('classifier', classifier)])

# Train the model
history=pipeline.fit(x_train, y_train)

# Make predictions on the test set
y_pred = pipeline.predict(x_test)
y_pred

from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(6, 6)) # Set Figure

Y_pred = np.argmax(y_pred, axis=0) # Decode Predicted labels
Y_test = np.argmax(y_test, axis=0) # Decode labels

mat = confusion_matrix(y_test, y_pred) # Confusion matrix

# Plot Confusion matrix
sns.heatmap(mat.T, square=True, annot=True, cbar=False, cmap=plt.cm.Blues)
plt.xlabel('Predicted Values')
plt.ylabel('True Values');
plt.show();

# Evaluate the model
from sklearn.metrics import classification_report
print('\nClassification Report :\n',classification_report(y_test, y_pred))

"""
    )
    return None

def sourceAutoEncoder():
    print(
"""
import numpy as np
import pandas as pd
import numpy.random as nr
import tensorflow as tf
import matplotlib.pyplot as plt
import keras
from keras.datasets import mnist
import keras.models as models
import keras.layers as layers
from keras import regularizers
from keras.layers import Dropout
from keras.layers import Dense, Conv2D,  Flatten,  Reshape,BatchNormalization
from keras.layers import Conv2DTranspose, MaxPooling2D, UpSampling2D, Input
from tensorflow.keras import optimizers
from tensorflow.keras.optimizers import RMSprop, Adam
%matplotlib inline

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

train_images = train_images.reshape((60000, 28, 28, 1)).astype('float')/255
print("The size of the train dataset",train_images.shape)
print("the data type of the dataset ",train_images.dtype)

print(test_images.shape, test_labels.shape)
test_images = test_images.reshape((10000, 28, 28, 1)).astype('float')/255
print(test_images.shape)

plt.imshow(train_images[1].reshape(28, 28))

from imgaug import augmenters
noise = augmenters.SaltAndPepper(0.1)
seq_object = augmenters.Sequential([noise])

train_x_n = seq_object.augment_images(train_images * 255) / 255
val_x_n = seq_object.augment_images(test_images * 255) / 255

data =np.append(train_x_n,val_x_n)

data.reshape((70000, 28, 28, 1))

label=np.append(train_labels,test_labels)
label.shape

data = np.append(train_x_n,val_x_n)
data = data.reshape((70000, 28, 28, 1)) # Assign the reshaped array back to data
label = np.append(train_labels,test_labels)
df = pd.DataFrame({'data': data.tolist(), 'labels': label}) # Create a DataFrame with image data and labels

image_index = 0
image_to_display = data[image_index]

# Reshape the selected image to (28, 28) for display
reshaped_image = image_to_display.reshape(28, 28)

# Display the image
plt.imshow(reshaped_image)
plt.show()

#encoder
nn = models.Sequential()
nn.add(Conv2D(32, kernel_size=(3,3), activation='relu', input_shape = (28,28,1 )))
nn.add(MaxPooling2D(pool_size=(2, 2)))
nn.add(Conv2D(64, kernel_size=(3,3), activation='relu'))
nn.add(MaxPooling2D(pool_size=(2, 2)))
nn.add(Conv2D(64, kernel_size=(3,3), activation='relu'))
nn.add(Flatten()) # Flattening the 2D arrays for fully connected layers
nn.add(Dense(49, activation='softmax'))

#decoder
nn.add(Reshape((7,7,1)))
nn.add(Conv2DTranspose(64, kernel_size=(3,3), strides=2,activation='relu',padding='same'))
nn.add(BatchNormalization())
nn.add(Conv2DTranspose(64,kernel_size=(3,3),strides=2,activation='relu' , padding='same'))
nn.add(BatchNormalization())
nn.add(Conv2DTranspose(32,kernel_size=(3,3),activation='relu',padding='same'))
nn.add(Conv2D(1,kernel_size=(3,3),activation='sigmoid',padding='same'))
nn.summary()
nn.compile(optimizer="adam", loss="mse")

history =nn.fit(train_images, train_images, epochs=2)

#original image
plt.imshow(train_images[1].reshape(28, 28))

prediction = nn.predict(train_images, verbose=1, batch_size=100)
# you can now display an image to see it is reconstructed well
x =prediction[1].reshape(28,28)
plt.imshow(x)

"""
    )
    return None

def help():
    print("""This section of the module still has to be written, the functions are essentially placeholders for the code to come. However the blueprint is still available for reference:
Functions:
    1. sourceANN(type='cat', 'imgCat', 'reg')
    2. sourceCNN()
    3. sourceRNN()
    4. sourceTransLearn()
    5. sourceLSTM()
    6. sourceRBM()
    7. sourceAutoEncoder()
    8. help()
""")