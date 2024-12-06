import math
import os
import numpy as np
import pandas as pd

current_dir = os.path.dirname(os.path.realpath(__file__))


class GumbelDistribution:
    """

Gumbel Distribution represents the distribution of extreme values either maximum or minimum
of samples used in various distributions. It is used to model distribution of peak levels.
For example, to show the distribution of peak temperatures of the year if there is a list of maximum temperatures of 10 years
    """

    def __init__(self, df: pd.DataFrame, event_col: str, extract_yearly_data: bool = True):
        """
        :param df: dataframe with index year and in datetime formapt using pd.to_datetime
        :param event_col: value of events, it could be discharge or rainfall
        :param extract_yearly_data: to extract yearly informaiton and calculating rank
         if already calculated set it False
        """
        if extract_yearly_data:
            self.df = self.extract_yearly_data(df)
        else:
            self.df = df
        # rank of value
        self.no_of_events = self.df.shape[0]
        self.event_col_name = event_col
        self.mean = np.mean(self.df[self.event_col_name].values)
        self.std = np.std(self.df[self.event_col_name].values)
        self.calculate_rank_of_event()
        self.estimate_gumbel_distribution()

        # self.std_s = stdev(self.df[self.q_col].values.tolist())
        # print(self.std, self.std_s)

    def calculate_rank_of_event(self):
        self.df = self.df.sort_values(by=[self.event_col_name], ascending=False)
        self.df['rank'] = [i + 1 for i in range(self.no_of_events)]

    def get_data(self) -> pd.DataFrame:
        return self.df

    @staticmethod
    def extract_yearly_data(df: pd.DataFrame):
        df = df.resample(rule="A", kind="period").max()
        df = df.dropna()
        df["year"] = df.index.year
        df.reset_index(inplace=True, drop=True)
        df.dropna()
        return df

    @staticmethod
    def get_mean_std_variate(no_of_years: int):
        df = pd.read_excel(os.path.join(current_dir, "gumbel-variate.xlsx"))
        row = df[df.n == no_of_years]
        return row.mean_n.values[0], row.std_n.values[0]

    @staticmethod
    def get_reduced_variate(rp: float):
        """
        calculate reduce variate of Gumble Distribution
        The reduced variate of the normal distribution is defined as Z = (x - )/. The properties
        of the reduced variate are mean = 0, standard deviation z = 1, and coefficient of skewness = 0.
        :param rp: is return period
        :return:
        """
        ln = lambda x: math.log(x)
        yr = -ln(ln(rp / (rp - 1)))
        return yr

    @staticmethod
    def calculate_cdf(yr: float):
        """
        :param yr:
        :return:
        """
        e = lambda x: math.exp(x)
        cdf = e(-e(-yr))
        return round(cdf,3)

    def calculate_event_value(self, rps):
        """
        calculate event value against return period
        :param rps:
        :return:
        """
        # 2. Find reduce mean yn and reduce Standard deviatio sn using Tables
        yn, sn = self.get_mean_std_variate(self.no_of_events)

        # 3. Find reduced variate yr for a given return period T using the equation -(ln.ln T/(T-1))
        yr = [self.get_reduced_variate(t) for t in rps]
        # print("reduce variate", yr)

        # 4. Find frequency factor K using equation K = (yr -yn)/sn
        Ks = [(y - yn) / sn for y in yr]
        # print("frequency factor", Ks)

        # 5. Determined required value of event  using equation Xt = mean + K * std.s (standard deviation of sample)
        qs = [self.mean + K * self.std for K in Ks]
        # print("discharges", qs)
        return qs

    def calculate_event_probability(self, qs: list) -> list:
        """
        :param q: value in float
        :return: 
        """
        # 1. Find reduce mean yn and reduce Standard deviatio sn using Tables
        yn, sn = self.get_mean_std_variate(self.no_of_events)
        # 2. Find  z-score using equation z = (x-μ)/σ
        Zs = [(v - self.mean) / self.std for v in qs]
        # 3. find reduce factor using reduce mean and std
        yrs = [yn + z * sn for z in Zs]
        # 4. calculate return period using cumulative distribution function
        rp = [self.calculate_cdf(yr) if yr != 0 else 0 for yr in yrs]
        return rp

    def estimate_gumbel_distribution(self):
        # value deviation from mean
        self.df["deviation"] = self.df[self.event_col_name].apply(lambda v: math.pow(v - self.mean, 2))
        # return period calculation
        self.df["rp"] = self.df['rank'].apply(lambda m: (self.no_of_events + 1) / m)
        # reduce variate (Z)
        self.df["Yr"] = self.df['rp'].apply(lambda rp: self.get_reduced_variate(rp))
        # print(self.df.head())
        # return self.df[["rp","Yr"]]


if __name__ == "__main__":
    media_dir = os.path.join(os.path.dirname(__file__), 'sample_data')

    file_path = os.path.join(media_dir, 'flood_rp_testdata.xlsx')
    df = pd.read_excel(file_path, header=2)
    gdrp = GumbelDistribution(df, 'q', False)
    # gdrp.calculate_rp()
    rps = [2, 10, 50, 100, 150, 200, 300, 500]
    gdrp.calculate_event_value(rps)
