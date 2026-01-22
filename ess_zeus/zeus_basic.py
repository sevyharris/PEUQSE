import numpy as np
from sklearn.datasets import make_spd_matrix
import matplotlib.pyplot as plt
import zeus
import mpi4py.MPI as MPI

ndim = 10
nwalkers = 30
nsteps= 5000

C = make_spd_matrix(ndim)

icov = np.linalg.inv(C)

mu = np.random.rand(ndim)

def log_prob(x, mu, icov):
    return -0.5 * np.dot(np.dot((x-mu).T,icov),(x-mu))

start = np.random.randn(nwalkers, ndim)

sampler = zeus.EnsembleSampler(nwalkers, ndim, log_prob, args=[mu, icov])
sampler.run_mcmc(start, nsteps)


print('Samples: ', sampler.samples.flatten(discard = 0).shape)

rank = MPI.COMM_WORLD.Get_rank()
np.save(f'chain_{rank}.npy', sampler.samples.flatten(discard = 0))

