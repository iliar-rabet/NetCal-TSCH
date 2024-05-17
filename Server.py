from abc import abstractmethod, ABC
import ParameterOutOfBounds
import math 
from Arrival import Poisson

def MMO(theta, Pon, r):
    x=Pon * math.exp(-theta *r) + 1 - Pon
    # print(f"x is {x} and theta is {theta} and math.exp is {math.exp(-theta *r)} pon is {Pon} r is {r}")
    if x <= 0:
        # print(theta,x, math.exp(theta * self.B))
        return 0.000000001
        # raise ParameterOutOfBounds(f"x = {x} must be > 0")

    rho = (math.log(x))/(-theta)
    return rho

class Server(ABC):
    """Abstract Server class"""

    @abstractmethod
    def sigma(self, theta: float) -> float:
        """Sigma method"""
        pass

    @abstractmethod
    def rho(self, theta: float) -> float:
        """Rho method"""
        pass


class ConstantRateServer(Server):
    """Constant-rate service"""

    def __init__(self, rate: float) -> None:
        self.rate = rate

    def sigma(self, theta=0.0) -> float:
        return 0.0

    def rho(self, theta: float) -> float:
        if theta <= 0:
            raise ParameterOutOfBounds(f"theta = {theta} must be > 0")
        return self.rate
    
class MarkovOnOff(Server):
    def __init__(self, Pon: float, LUC, B=100) -> None:
        self.Pon = Pon
        self.B=B
        self.r=B*100/LUC
        self.LUC=LUC

    def sigma(self, theta=0.0) -> float:
        # return self.LUC * 0.01
        return 0

    def rho(self, theta: float) -> float:
        rho = MMO(theta, self.Pon, self.r)
        return rho

class MSF(Server):
    def __init__(self, Pon: float, LUC, B=100) -> None:
        self.Pon = Pon
        self.B=B
        self.r=B*100/LUC
        self.LUC=LUC

    def sigma(self, theta=0.0) -> float:
        # return self.LUC * 0.01
        return 0

    def rho(self, theta: float) -> float:
        rho = MMO(theta, self.Pon, self.r)

        DIO_interval = 1.028
        collision_rate = self.B /DIO_interval  + 2*self.B /DIO_interval 
        # collision_rate=0.5
        # print(f"rho {rho} collision {collision_rate}")
        return rho - collision_rate
        


class Orchestra(Server):
    def __init__(self, Pon: float, LUC, LBC, LEB, B=100) -> None:
        self.Pon = Pon
        self.B=B
        self.r=B*100/LUC
        self.LEB=LEB*10
        self.LBC=LBC*10
        self.LUC=LUC
    def sigma(self, theta=0.0) -> float:
        # return self.LUC * 0.01
        # return self.B
        return 0

    def rho(self, theta: float) -> float:
        rho = MMO(theta, self.Pon, self.r)
        collision = self.B*100/self.LBC + self.B*100/self.LEB -self.B*100/(self.LBC*self.LEB)
        # print(f"rho {rho} collision {collision}")
        return rho - self.B * collision


class RB_Net(Server):
    def __init__(self, Pon: float, LUC, LBC, LEB, Cross, B=1) -> None:
        self.Pon = Pon
        self.B=B
        self.r=B*100/LUC
        self.LEB=LEB*10
        self.LBC=LBC*10
        self.LUC=LUC
        self.Cross=Cross

    def sigma(self, theta=0.0) -> float:
        # return self.LUC * 0.01
        # return self.B
        return self.Cross.sigma(theta)
        # return 0

    def rho(self, theta: float) -> float:
        rho = MMO(theta, self.Pon, self.r)
        collision = self.B*100/self.LBC + self.B*100/self.LEB -self.B*100/(self.LBC*self.LEB)
        # print(f"rho {rho} collision {collision}")
        total= rho - self.B * collision
        return total - self.Cross.rho(theta)

class MSF_Net(Server):
    def __init__(self, Pon: float, LUC, NBRs, B=1) -> None:
        self.Pon = Pon
        self.B=B
        self.r=B*100/LUC
        self.LUC=LUC
        self.NBRs=NBRs

    def sigma(self, theta=0.0) -> float:
        # return self.LUC * 0.01
        return 0

    def rho(self, theta: float) -> float:
        rho = MMO(theta, self.Pon, self.r)

        DIO_interval = 1.028
        collision_rate = self.B /DIO_interval # + 2*self.B /DIO_interval 
        collision_rate=1 + self.NBRs*1.5

        # print(f"rho {rho} collision {collision_rate}")
        return rho - collision_rate
        