import sympy as sp

# !!!!!!!
# 30OCT2024: started implementing schwarzschild solver in xyz coordinates proper. This does not work well! See notebook
# !!!!!!!
def get_schwarzschild_xyz(r_s):
	# See notebook ConvertingSchwarzschildSphericalCoordinateMetricToCartisian.ipynb

	x, y, z = sp.symbols(" x y z ")

	r = sp.sqrt(x**2+y**2+z**2)
	th = sp.acos(z/r)
	phi = sp.atan(y/x)


	n_sph = sp.Matrix([\
	                   [-(1-r_s/r), 0, 0, 0],\
	                   [0, (1-r_s/r)**-1, 0, 0],\
	                   [0, 0, r**2, 0],\
	                   [0, 0, 0, r**2 * sp.sin(th)**2]\
	                  ])

	M_xyz_to_sph = sp.Matrix([[1, 0, 0, 0],\
	                          [0, r.diff(x), r.diff(y), r.diff(z)],\
	                          [0, th.diff(x), th.diff(y), th.diff(z)],\
	                          [0, phi.diff(x), phi.diff(y), phi.diff(z)],\
	                         ])

	M_xyz_to_sph.simplify()

	n_xyz = M_xyz_to_sph.T * n_sph * M_xyz_to_sph

	n_xyz.simplify()

	return n_xyz
