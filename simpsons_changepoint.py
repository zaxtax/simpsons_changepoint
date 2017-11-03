import pymc3 as pm
import theano.tensor as tt
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("simpsons_ratings.csv")
index = data.index

with pm.Model() as model:
    switch = pm.DiscreteUniform('switch', lower=index.min(), upper=index.max())
    early_mean = pm.Normal('early_mean', mu=5., sd=1.)
    late_mean = pm.Normal('late_mean', mu=5., sd=1.)
    mean = tt.switch(switch >= index.values, early_mean, late_mean)
    ratings = pm.Normal('ratings', mu=mean, sd=1.,
                        observed=data["UserRating"].values)

    tr = pm.sample(10000, tune=500)
    pm.traceplot(tr)

plt.savefig("trace.png")

print("{}: {}".format(data["EpisodeID"][220], data["Episode"][220]))
