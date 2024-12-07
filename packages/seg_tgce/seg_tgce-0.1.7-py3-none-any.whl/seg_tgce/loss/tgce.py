from typing import Any

import tensorflow as tf
from keras.losses import Loss
from tensorflow import Tensor, cast
from tensorflow import float32 as tf_float32

TARGET_DATA_TYPE = tf_float32


def safe_divide(
    numerator: Tensor, denominator: Tensor, epsilon: float = 1e-8
) -> Tensor:
    """Safely divide two tensors, avoiding division by zero."""
    return tf.math.divide(
        numerator, tf.clip_by_value(denominator, epsilon, tf.reduce_max(denominator))
    )


def stable_pow(x: Tensor, p: Tensor, epsilon: float = 1e-8) -> Tensor:
    """Compute x^p safely by ensuring x is within a valid range."""
    return tf.pow(tf.clip_by_value(x, epsilon, 1.0 - epsilon), p)


class TcgeSs(Loss):
    """
    Truncated generalized cross entropy
    for semantic segmentation loss.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        train_annotators: int,
        val_annotators: int,
        num_classes: int,
        name: str = "TGCE_SS",
        q: float = 0.1,
        gamma: float = 0.1,
    ) -> None:
        self.q = q
        self.train_annotators = train_annotators
        self.val_annotators = val_annotators
        self.num_classes = num_classes
        self.gamma = gamma
        self.stage = "train"
        super().__init__(name=name)

    def call(self, y_true: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
        # A stateless approach here would be much more desirable
        # but the stage is a mutable attribute and cannot be passed to the call method
        # since the heritable methods are not called with the stage argument.
        # Future research should be done to find a better way to handle this.

        match self.stage:
            case "train":
                num_scorers = self.train_annotators
            case "val":
                num_scorers = self.val_annotators
            case _:
                raise ValueError(f"Invalid stage: {self.stage}")
        y_true = cast(y_true, TARGET_DATA_TYPE)
        y_pred = cast(y_pred, TARGET_DATA_TYPE)

        y_pred = y_pred[..., : self.num_classes + num_scorers]

        y_true_shape = tf.shape(y_true)

        new_shape = tf.concat(
            [y_true_shape[:-2], [self.num_classes, num_scorers]], axis=0
        )
        y_true = tf.reshape(y_true, new_shape)

        lambda_r = y_pred[..., self.num_classes :]
        y_pred_ = y_pred[..., : self.num_classes]

        n_samples = tf.shape(y_pred_)[0]
        width = tf.shape(y_pred_)[1]
        height = tf.shape(y_pred_)[2]

        y_pred_ = y_pred_[..., tf.newaxis]
        y_pred_ = tf.repeat(y_pred_, repeats=[num_scorers], axis=-1)

        epsilon = 1e-8
        y_pred_ = tf.clip_by_value(y_pred_, epsilon, 1.0 - epsilon)

        term_r = tf.math.reduce_mean(
            tf.math.multiply(
                y_true,
                safe_divide(
                    (
                        tf.ones(
                            [n_samples, width, height, self.num_classes, num_scorers]
                        )
                        - stable_pow(y_pred_, self.q)
                    ),
                    (self.q + epsilon),
                ),
            ),
            axis=-2,
        )

        term_c = tf.math.multiply(
            tf.ones([n_samples, width, height, num_scorers]) - lambda_r,
            safe_divide(
                (
                    tf.ones([n_samples, width, height, num_scorers])
                    - stable_pow(
                        (1 / self.num_classes)
                        * tf.ones([n_samples, width, height, num_scorers]),
                        self.q,
                    )
                ),
                (self.q + epsilon),
            ),
        )

        loss = tf.math.reduce_mean(tf.math.multiply(lambda_r, term_r) + term_c)
        loss = tf.where(tf.math.is_nan(loss), tf.constant(1e-8), loss)

        return loss

    def get_config(
        self,
    ) -> Any:
        """
        Retrieves loss configuration.
        """
        base_config = super().get_config()
        return {**base_config, "q": self.q}
