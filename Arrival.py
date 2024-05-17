from abc import abstractmethod, ABC
import math
import ParameterOutOfBounds
import numpy as np

class Arrival(ABC):
    """Abstract Arrival class."""

    @abstractmethod
    def sigma(self, theta: float) -> float:
        """
        sigma(theta)
        :param theta: mgf parameter
        """
        pass

    @abstractmethod
    def rho(self, theta: float) -> float:
        """
        rho(theta)
        :param theta: mgf parameter
        """
        pass

class ExponentialDist(Arrival):
    """Exponential distribution."""

    def __init__(self, lamb: float, n=1) -> None:
        self.lamb = lamb
        self.n = n

    def sigma(self, theta=0.0) -> float:
        """

        :param theta: mgf parameter
        :return:      sigma(theta)
        """
        return 0.0

    def rho(self, theta: float) -> float:
        """
        rho(theta)
        :param theta: mgf parameter
        """
        if theta <= 0:
            raise ParameterOutOfBounds(f"theta = {theta} must be > 0")

        if theta >= self.lamb:
            # raise ParameterOutOfBounds(f"theta = {theta} must be < lambda = {self.lamb}")
            return np.inf

        return (self.n / theta) * math.log(self.lamb / (self.lamb - theta))
    

class RateLatency(Arrival):
    """Exponential distribution."""

    def __init__(self, rate: float, n=1) -> None:
        self.rate = rate
        self.n = n

    def sigma(self, theta=0.0) -> float:
        """

        :param theta: mgf parameter
        :return:      sigma(theta)
        """
        return 0.0

    def rho(self, theta: float) -> float:
        """
        rho(theta)
        :param theta: mgf parameter
        """
        return self.rate

class Periodic(Arrival):
    def __init__(self, interval, size):
        self.size=size
        self.interval=interval

    def sigma(self, theta=0.0) -> float:
        """

        :param theta: mgf parameter
        :return:      sigma(theta)
        """
        # return 0
        return self.size

    def rho(self, theta: float) -> float:
        """
        rho(theta)
        :param theta: mgf parameter
        """
        return self.size/self.interval

class Poisson(Arrival):
    def __init__(self,rate,size):
        self.rate=rate
        self.size=size

    def sigma(self, theta=0.0) -> float:
        """

        :param theta: mgf parameter
        :return:      sigma(theta)
        """
        return self.size

    def rho(self, theta: float) -> float:
        """
        rho(theta)
        :param theta: mgf parameter
        """
        return self.rate * (math.exp(theta*self.size)-1)/theta
