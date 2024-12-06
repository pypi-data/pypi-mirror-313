import cv2
import numpy as np
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator
from scipy.ndimage import map_coordinates
import skimage.transform as sktf
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from ._unit import RYScaler,inv_RYScaler
def _sparse_sd(data_instance,
			   of_params={'st_pars': dict(maxCorners = 200,
										  qualityLevel = 0.2,
										  minDistance = 7,
										  blockSize = 21),
						  'lk_pars': dict(winSize = (20, 20),
										  maxLevel = 2,
										  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0))},
			   lead_steps=12):
	penult_frame = data_instance[-2]
	last_frame = data_instance[-1]
	old_corners = cv2.goodFeaturesToTrack(data_instance[0], mask=None,
										  **of_params['st_pars'])
	new_corners, st, err = cv2.calcOpticalFlowPyrLK(prevImg=penult_frame,
													nextImg=last_frame,
													prevPts=old_corners,
													nextPts=None,
													**of_params['lk_pars'])
	success = st.ravel() == 1
	new_corners = new_corners[success].copy()
	old_corners = old_corners[success].copy()
	delta = new_corners.reshape(-1, 2) - old_corners.reshape(-1, 2)
	pts_source = new_corners.reshape(-1, 2)
	pts_target_container = []
	for lead_step in range(lead_steps):
		pts_target_container.append(pts_source + delta * (lead_step + 1))
	return pts_source, pts_target_container
class Sparse:
	def __init__(self,lead_steps=2):
		self.of_params = {'st_pars': dict(maxCorners=200, qualityLevel=0.2,
										  minDistance=7, blockSize=21),
						  'lk_pars': dict(winSize=(20, 20), maxLevel=2,
										  criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0))}
		self.warper = "affine"
		self.input_data = None
		self.scaler = RYScaler
		self.inverse_scaler = inv_RYScaler
		self.lead_steps = lead_steps
	def run(self):
		transformations = {'euclidean': sktf.EuclideanTransform(),
						   'similarity': sktf.SimilarityTransform(),
						   'affine': sktf.AffineTransform(),
						   'projective': sktf.ProjectiveTransform()}
		data_scaled, c1, c2 = self.scaler(self.input_data)
		trf = transformations[self.warper]
		pts_source, pts_target_container = _sparse_sd(data_instance=data_scaled,
													  of_params=self.of_params,
													  lead_steps=self.lead_steps)
		last_frame = data_scaled[-1]
		nowcst_frames = []
		for lead_step, pts_target in enumerate(pts_target_container):
			trf.estimate(pts_source, pts_target)
			nowcst_frame = sktf.warp(last_frame/255, trf.inverse)
			nowcst_frame = (nowcst_frame*255).astype('uint8')
			nowcst_frames.append(nowcst_frame)
		nowcst_frames = np.stack(nowcst_frames, axis=0)
		nowcst_frames = self.inverse_scaler(nowcst_frames, c1, c2)
		return nowcst_frames
