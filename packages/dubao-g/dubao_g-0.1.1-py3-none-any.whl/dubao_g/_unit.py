import numpy as np
def RYScaler(X_dbz):
	X_dbz[X_dbz < 0] = 0
	c1 = X_dbz.min()
	c2 = X_dbz.max()
	return ((X_dbz - c1) / (c2 - c1) * 255).astype(np.uint8), c1, c2
def inv_RYScaler(X_scl, c1, c2):
	X_scl = (X_scl / 255)*(c2 - c1) + c1
	return X_scl