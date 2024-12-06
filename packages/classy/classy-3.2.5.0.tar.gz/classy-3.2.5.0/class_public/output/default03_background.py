import matplotlib.pyplot as plt
import numpy as np
import itertools

files = ['/home/nilsor/codes/class_public/class_public/output/default03_background.dat']
data = []
for data_file in files:
    data.append(np.loadtxt(data_file))
roots = ['default03_background']

fig, ax = plt.subplots()

index, curve = 0, data[0]
y_axis = ['rho_g', 'rho_b', 'rho_cdm', 'rho_lambda', 'rho_ur', 'rho_crit', 'rho_tot']
tex_names = ['(8\\pi G/3)rho_g', '(8\\pi G/3)rho_b', '(8\\pi G/3)rho_cdm', '(8\\pi G/3)rho_lambda', '(8\\pi G/3)rho_ur', '(8\\pi G/3)rho_crit', '(8\\pi G/3)rho_tot']
x_axis = 'z'
ylim = []
xlim = []
ax.plot(curve[:, 0], curve[:, 8])
ax.plot(curve[:, 0], curve[:, 9])
ax.plot(curve[:, 0], curve[:, 10])
ax.plot(curve[:, 0], curve[:, 11])
ax.plot(curve[:, 0], curve[:, 12])
ax.plot(curve[:, 0], curve[:, 13])
ax.plot(curve[:, 0], curve[:, 14])

ax.legend([root+': '+elem for (root, elem) in
    itertools.product(roots, y_axis)], loc='best')

ax.set_xlabel('z', fontsize=16)
plt.show()