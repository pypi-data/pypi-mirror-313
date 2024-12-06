# noinspection PyUnresolvedReferences
from .._core._c_uutils_base_random import _CRandomGenerator

__all__ = ['RandomGenerator']


class RandomGenerator:
    """
    A wrapper class for RandomGenerator to provide a more Pythonic interface.
    """

    def __init__(self):
        self._generator = _CRandomGenerator()

    @staticmethod
    def set_seed(seed: int):
        """
        Set globally shared random seed.

        :param seed: Seed value
        :type seed: int
        """
        _CRandomGenerator.set_seed(seed)

    def seed(self, seed: int):
        """
        Set random seed for this generator instance.

        :param seed: Seed value
        :type seed: int
        """
        self._generator.seed(seed)

    def uni(self, *args) -> int:
        """
        Generate a random integer based on provided arguments.

        :param args: Arguments for the uniform distribution
        :return: Random integer
        :rtype: int
        """
        return self._generator.uni(*args)

    def uni_1(self) -> float:
        """
        Generate a random double in the range [0, 1).

        :return: Random double
        :rtype: float
        """
        return self._generator.uni_1()

    def uni_r(self, *args) -> float:
        """
        Generate a random double based on provided arguments.

        :param args: Arguments for the uniform distribution
        :return: Random double
        :rtype: float
        """
        return self._generator.uni_r(*args)

    def exp(self, rate: float) -> float:
        """
        Generate a random double following an exponential distribution.

        :param rate: Rate parameter
        :type rate: float
        :return: Random double
        :rtype: float
        """
        return self._generator.exp(rate)

    def arcsine(self, minv: float, maxv: float) -> float:
        """
        Generate a random double following an arcsine distribution.

        :param minv: Minimum value
        :type minv: float
        :param maxv: Maximum value
        :type maxv: float
        :return: Random double
        :rtype: float
        """
        return self._generator.arcsine(minv, maxv)

    def beta(self, alpha: float, beta: float) -> float:
        """
        Generate a random double following a beta distribution.

        :param alpha: Alpha parameter
        :type alpha: float
        :param beta: Beta parameter
        :type beta: float
        :return: Random double
        :rtype: float
        """
        return self._generator.beta(alpha, beta)

    def gamma(self, shape: float, scale: float) -> float:
        """
        Generate a random double following a gamma distribution.

        :param shape: Shape parameter
        :type shape: float
        :param scale: Scale parameter
        :type scale: float
        :return: Random double
        :rtype: float
        """
        return self._generator.gamma(shape, scale)

    def normal(self, mean: float, stddev: float) -> float:
        """
        Generate a random double following a normal distribution.

        :param mean: Mean value
        :type mean: float
        :param stddev: Standard deviation
        :type stddev: float
        :return: Random double
        :rtype: float
        """
        return self._generator.normal(mean, stddev)

    def poisson(self, mean: float) -> float:
        """
        Generate a random double following a Poisson distribution.

        :param mean: Mean value
        :type mean: float
        :return: Random double
        :rtype: float
        """
        return self._generator.poisson(mean)

    def weibull(self, shape: float, scale: float) -> float:
        """
        Generate a random double following a Weibull distribution.

        :param shape: Shape parameter
        :type shape: float
        :param scale: Scale parameter
        :type scale: float
        :return: Random double
        :rtype: float
        """
        return self._generator.weibull(shape, scale)

    def tri(self, lower: float, mode: float, upper: float) -> float:
        """
        Generate a random double following a triangular distribution.

        :param lower: Lower bound
        :type lower: float
        :param mode: Mode value
        :type mode: float
        :param upper: Upper bound
        :type upper: float
        :return: Random double
        :rtype: float
        """
        return self._generator.tri(lower, mode, upper)
