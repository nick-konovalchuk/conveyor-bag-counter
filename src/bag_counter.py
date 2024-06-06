import numpy as np


class BagCounter:
    def __init__(self, p1, p2):
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
        theta = np.arctan(m)
        self._rotation_matrix = np.array(
            [[np.cos(-theta), -np.sin(-theta)], [np.sin(-theta), np.cos(-theta)]]
        )
        self._thr_y = (p1 @ self._rotation_matrix.T)[0]
        self._state = {}
        self.count = 0

    def update(self, predictions):
        ids = predictions.boxes.id.int().tolist()
        centers = predictions.boxes.xywh[:, :2].numpy().astype(int)
        rotated_centers = centers @ self._rotation_matrix.T
        above_line = (rotated_centers[:, 1] < self._thr_y).astype(int)
        missing = self._state.keys() - ids
        for k, v in zip(ids, above_line):
            if k in self._state:
                self.count += v - self._state[k]
            self._state[k] = v
        for k in missing:
            self._state.pop(k)
