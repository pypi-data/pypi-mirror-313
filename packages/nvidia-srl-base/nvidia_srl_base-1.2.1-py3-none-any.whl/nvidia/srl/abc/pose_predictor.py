# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Pose predictor classes and functions."""

# Standard Library
from abc import abstractmethod
from typing import Any, Dict, List, Optional, Tuple

# Third Party
import numpy as np

# NVIDIA
from nvidia.srl.abc.srl import SRL
from nvidia.srl.basics.types import Pose


class PosePredictor(SRL):
    """Base class to represent a model that predicts poses given camera data."""

    def __init__(self, params: Optional[dict] = None, **kwargs: Any):
        """Initialize a new :class:`PosePredictor` object.

        Args:
            params: Set of parameters needed to initialize the class.
            kwargs: Additional keyword arguments are passed to the parent class,
                :class:`~srl.abc.srl.SRL`.
        """
        # Initialize parent class
        super().__init__(**kwargs)

        # Initialize instance attributes
        self._params = params

    def params(self) -> Optional[dict]:
        """Return params."""
        return self._params

    @abstractmethod
    def predict_poses(
        self,
        point_cloud: Optional[np.ndarray] = None,
        point_features: Optional[np.ndarray] = None,
        images: Optional[List[np.ndarray]] = None,
        **model_kwargs: Any,
    ) -> Tuple[List[Pose], Optional[Dict[Any, Any]]]:
        """Predict poses given camera data.

        Args:
            point_cloud: Point cloud of the scene. P x 3 matrix of points.
            point_features: Set of features associated to each point in the point cloud. P x F
                matrix representing the feature data set, where F is the number features per point.
            images: Set of C input images. Each image is a M x N x 3 array of pixel values (RGB).
            model_kwargs: Additional keyword arguments to pass to the model.

        Returns:
            predicted_poses: A list of predicted poses (as a list of 4 x 4 transform matrices).
            output_data: Additional output data as a dictionary return by the model.
        """
