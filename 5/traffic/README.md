# Traffic

The final model uses two convolution and max-pooling stages. The first stage
has 32 3-by-3 filters and the second has 64 3-by-3 filters. Their output is
flattened and passed to a 128-unit dense layer, followed by 50% dropout and a
43-unit softmax output layer. It is trained with Adam and categorical
cross-entropy.

I began with one convolutional layer and one dense layer. That learned the
training set, but its validation accuracy was less consistent because a single
stage did not capture enough of the signs' small shapes and symbols. Adding a
second convolutional stage improved feature extraction while keeping the
network compact. A larger dense layer made training slower without a useful
gain, while no dropout produced a widening gap between training and validation
accuracy. Dropout at 0.5 gave the best balance in my experiments. The final
architecture therefore favors two small convolutional stages and moderate
regularization over a much larger network.
