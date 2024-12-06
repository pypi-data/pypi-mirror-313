import time
import sys

import numpy as np
from matplotlib import pyplot as plt

import pytrans

np.random.seed(5)
data = np.random.gamma(3,1, size=500)
lcens = 0.0

data[data<=lcens]=lcens
scale = 5.0/np.max(data)

transform = pytrans.PyLogSinh(1.0, 1.0, scale)

# transform = pytrans.PyYJT(1.0, np.std(data), -np.mean(data))

rescaled_data = transform.rescale_many(data)
# rescaled_lcens = transform.rescale_one(lcens)
# opt_params = transform.optim_params(rescaled_data, rescaled_lcens, False, True)
# trans_data = transform.transform_many(rescaled_data)
#
transform.optim_params(data, lcens, True, False)
opt_params = transform.get_optimised_params()
trans_data = transform.transform_many(transform.rescale_many(data))

back_trans_data = transform.inv_rescale_many(transform.inv_transform_many(trans_data))

print(transform.get_scale_shift())
print(transform.get_transformation_params())
print(transform.get_distribution_params())
print(np.array(transform.get_optimised_params()))

lsh = transform.get_distribution_params()
plt.hist(np.random.normal(lsh[2], lsh[3], size=5000), bins=200, density=True, alpha=0.5, label='trans_new')

rand_norm_samples = np.random.normal(mean,stdev, size=50000)
back_trans_samples = transform.inv_transform_many(rand_norm_samples)
back_rescaled_samples = transform.inv_rescale_many(back_trans_samples)

plt.hist(trans_data, bins=50, density=True, alpha=0.5, label='trans_orig')
plt.hist(data, bins=50, density=True, alpha=0.5, label='orig')
plt.hist(rescaled_data, bins=50, density=True, alpha=0.5, label='rescaled_orig')
plt.hist(back_trans_samples, bins=200, density=True, alpha=0.5, label='inv_trans_new')
plt.hist(back_rescaled_samples, bins=200, density=True, alpha=0.5, label='inv_rescaled_new')

shift = 0.0
x = 4.0
x_rs = scale*(x+shift)
lcens_rs = scale*(lcens+shift)

print(opt_params)
log_dens = transform.log_density(opt_params, x, lcens, True)
print(x_rs, log_dens, np.exp(log_dens))

log_dens = transform.log_density(opt_params, x_rs, lcens_rs, False)
print(x_rs, log_dens, np.exp(log_dens))

plt.axvline(x_rs)
plt.legend(loc='best')

plt.show()





