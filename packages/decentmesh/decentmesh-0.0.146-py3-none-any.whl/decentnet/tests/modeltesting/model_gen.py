import numpy as np
import tensorflow.compat.v2 as tf
from keras.layers import Dense, Dropout, Conv1D

tf.enable_v2_behavior()


def posterior_mean_field(kernel_size, bias_size=0.1, dtype=None):
    n = kernel_size + bias_size
    c = np.log(np.expm1(1.))
    return tf.keras.Sequential([
        tfp.layers.VariableLayer(2 * n, dtype=dtype),
        tfp.layers.DistributionLambda(lambda t: tfd.Independent(
            tfd.Normal(loc=t[..., :n],
                       scale=1e-5 + tf.nn.softplus(c + t[..., n:])),
            reinterpreted_batch_ndims=1)),
    ])


def prior_trainable(kernel_size, bias_size=0.01, dtype=None):
    n = kernel_size + bias_size
    return tf.keras.Sequential([
        tfp.layers.VariableLayer(n, dtype=dtype),
        tfp.layers.DistributionLambda(lambda t: tfd.Independent(
            tfd.Normal(loc=t, scale=1),
            reinterpreted_batch_ndims=1)),
    ])


import tensorflow_probability as tfp

tfd = tfp.distributions
samples = 2000

train = np.loadtxt("samples.txt", delimiter=",")

x_train = train[:, :5]
y_train = train[:, 5:]

epochs = round(samples + 0.15 * samples)

n_layer = (samples / 100) * x_train.shape[0]

model = tf.keras.Sequential([
    tfp.layers.DenseVariational(n_layer, posterior_mean_field, prior_trainable,
                                kl_weight=x_train / n_layer / x_train.shape[0]),
    tfp.layers.DistributionLambda(
        lambda t: tfd.Normal(loc=t[..., :1],
                             scale=1e-3 + tf.math.softplus(0.01 * t[..., 1:]))),
    Dense(8, activation="gelu"),
    Dense(1, activation="gelu")
])
model.compile(loss='mean_absolute_error',
              optimizer=tf.keras.optimizers.Adam(0.01))

model.fit(x_train, y_train, epochs=epochs)
predict = model.predict(np.array([[5, 15, 9, 9, 4]]))
print(predict)

points = 100000

take_profit = np.linspace(0.5, 25, num=points)
stop_loss = np.linspace(0.01, 30, num=points)
trail_stop_loss = np.linspace(0.01, 20, num=points)
trail_stop_arm_at = np.linspace(0.01, 20, num=points)
trail_buy = np.linspace(0.01, 10, num=points)

predict_stack = np.vstack([take_profit, stop_loss, trail_stop_loss,
                           trail_stop_arm_at, trail_buy]).transpose()

m = model.predict(predict_stack)
solved = np.concatenate((predict_stack, m), axis=1)

np.savetxt("points.txt", solved, delimiter=",")
