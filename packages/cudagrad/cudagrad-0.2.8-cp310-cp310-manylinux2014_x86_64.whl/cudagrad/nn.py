# So the magic is that there's this relatively simple algorithm called
# backpropagation that takes the error in the output and sends that
# error backwards through the network and computes through all the
# connections how you should change them to improve the behavior, and
# then you change them all a tiny bit and you just keep going with
# another example. And surprisingly that actually works. For many years
# people thought that would just get jammed up — it would get stuck
# somewhere — but no it doesn't, it actually works very well.
#
# Geoffrey Hinton

from cudagrad.tensor import Tensor


def mse(predicted: Tensor, actual: Tensor) -> Tensor:
    # TODO this assumes column tensor
    difference = predicted - actual
    squared = difference * difference
    summed = squared.sum()
    mean = summed / Tensor([1], [summed.size[0]])
    return mean


class Module:
    def parameters(self) -> list[Tensor]:
        params = []
        for x in self.__dict__:
            param = getattr(self, x)
            if type(param) is Tensor:
                params.append(param)
        return params

    def zero_grad(self) -> None:
        for parameter in self.parameters():
            assert type(parameter) is Tensor
            parameter.zero_grad()


def sgd(model: Module, lr: float) -> None:
    for parameter in model.parameters():
        parameter.data[:] = parameter + (
            Tensor.explode(parameter.size, -lr) * parameter.grad()
        )


def softmax(t: Tensor) -> Tensor:
    D = Tensor([1], [-1]) * t.max()
    e = (t + D).exp()
    return e / e.sum()


def cross_entropy(inputs: Tensor, target: Tensor) -> Tensor:
    probs = softmax(inputs)

    one_hot_target = Tensor.zeros(inputs.size)
    one_hot_target.data[0, int(target.data[0, 0].item())] = (
        1.0  # TODO 0 index is wrong?
    )

    log_probs = Tensor.log(probs)

    loss = (
        Tensor([1], [-1.0])
        * (one_hot_target * log_probs).sum()
        / Tensor([1], [inputs.size[0]])
    )
    return loss
