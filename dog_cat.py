import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Conv2D, MaxPooling2D, Flatten, Dropout
from keras import optimizers
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator
import os, sys

class DogCat(object):
    # write a classifier object
    def __init__(self, im_size):
        self.im_size = im_size
        self.net = Sequential([
            # feature extractor
            Conv2D(filters=32, kernel_size=3, strides=1, padding='same', activation='relu', input_shape=(*im_size, 3)),
            MaxPooling2D(pool_size=2),
            Conv2D(filters=32, kernel_size=3, strides=1, padding='same', activation='relu'),
            MaxPooling2D(pool_size=2),
            Conv2D(filters=64, kernel_size=3, strides=1, padding='same', activation='relu'),
            MaxPooling2D(pool_size=2),
            # classifier
            Flatten(),
            Dense(64, activation='relu'),
            Dropout(0.5),
            Dense(2, activation='softmax'),
        ])
        self.optim = optimizers.SGD(lr=1e-3, decay=1e-6, momentum=0.9, nesterov=True)

    def _fit(self, generator, nb_epochs=10, batch_size=32, nb_images=25000):
        # train network
        self.net.compile(optimizer=self.optim, loss='binary_crossentropy', metrics=['accuracy'])
        self.net.fit_generator(generator, steps_per_epoch=nb_images // batch_size, epochs=nb_epochs)

    def _predict(self, image):
        # predict image's class
        im = Image.open(image)
        im = im.resize(self.im_size)
        im_arr = np.array(im) / 255.
        im_arr = im_arr[np.newaxis]
        return np.argmax(self.net.predict(im_arr), axis=1)


def train(dir: str, im_size: tuple, pretrained_checkpoint=None, **kwargs):
    """Create a Dog Cat Classifier

    Parameters
    ----------
    dir : str
        The dir path where is located downloaded data
    im_size : tuple
        Input imsize for the neural net. Every img in the dataset will be
        rescaled to this size
    pretrained_checkpoint : str or None
        If not None, it must be a str that indicates path to pretrained checkpoint,
        then the neural net will load pretrained weights before training
    **kwargs : dict
        arguments for _fit method of neural net

    Returns
    -------
    DogCat
        a DogCat trained object

    """

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')
    train_generator = train_datagen.flow_from_directory(
        dir,  # data directory
        target_size=im_size,
        batch_size=batch_size,
        class_mode='binary')
    print(train_generator.class_indices)
    model = DogCat(im_size)
    if pretrained_checkpoint:
        assert isinstance(pretrained_checkpoint, str)
        model.net.load_weights(pretrained_checkpoint)
    model._fit(train_generator, **kwargs)
    model.net.save_weights('checkpoint_{}.h5'.format(nb_epochs))
    return model


def classify(model, image_fn: str):
    pred = model._predict(image_fn)
    print('Your object is made of {}.'.format('cat' if pred == 0 else 'dog'))


if __name__ == '__main__':
    # demo how to use my code
    # please remove this part if you find it unnecessary
    train_dir = os.path.join('data', 'dogcat', 'train')
    batch_size = 128
    nb_epochs = 10
    im_size = (32, 32)
    model = train(train_dir, im_size=(28, 28), nb_epochs=nb_epochs, batch_size=batch_size, nb_images=25000)
    image_fn = '' # enter your image filename here
    classify(model, image_fn) # this will print the class our model assign to this image
