import numpy as np
from scipy.stats import norm


class BlackScholes:
    def __init__(self, S, K, T, r, sigma):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def d1(self):
        return (np.log(self.S/self.K) + (self.r + 0.5*self.sigma**2)*self.T) / (self.sigma*np.sqrt(self.T))

    def d2(self):
        return self.d1() - self.sigma*np.sqrt(self.T)

    def call_price(self):
        return self.S * norm.cdf(self.d1()) - self.K * np.exp(-self.r*self.T) * norm.cdf(self.d2())

    def put_price(self):
        return self.K * np.exp(-self.r*self.T) * norm.cdf(-self.d2()) - self.S * norm.cdf(-self.d1())

    def delta(self, option='call'):
        return norm.cdf(self.d1()) if option=='call' else norm.cdf(self.d1()) - 1

    def gamma(self):
        return norm.pdf(self.d1()) / (self.S*self.sigma*np.sqrt(self.T))

    def vega(self):
        return self.S * norm.pdf(self.d1()) * np.sqrt(self.T) / 100

    def theta(self, option='call'):
        if option=='call':
            return (-self.S*norm.pdf(self.d1())*self.sigma/(2*np.sqrt(self.T)) -
                    self.r*self.K*np.exp(-self.r*self.T)*norm.cdf(self.d2()))/365
        return (-self.S*norm.pdf(self.d1())*self.sigma/(2*np.sqrt(self.T)) +
                self.r*self.K*np.exp(-self.r*self.T)*norm.cdf(-self.d2()))/365

    def rho(self, option='call'):
        if option=='call':
            return self.K*self.T*np.exp(-self.r*self.T)*norm.cdf(self.d2())/100
        return -self.K*self.T*np.exp(-self.r*self.T)*norm.cdf(-self.d2())/100