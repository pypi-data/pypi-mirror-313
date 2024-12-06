from detectools.formats import (
    BaseFormat,
    InstanceMaskData,
    BboxData,
    InstanceMaskFormat,
    BboxFormat,
)
from torch import Tensor
from typing import Dict, List, Tuple, Literal, Union, Sequence
from detectools import Configuration
import copy
from torchvision.utils import draw_bounding_boxes, draw_segmentation_masks
from torch.nn.functional import one_hot
import torch
from PIL import Image, ImageDraw, ImageFont
from torchvision.transforms.v2.functional import to_pil_image, pil_to_tensor
from pathlib import Path
from detectools.preprocessing.image import save_image
from torchvision.transforms.v2 import Resize
import matplotlib.pyplot as plt
import colorcet as cc
import cv2
import numpy as np
import detectools.utils.errors as er
import math


def visualization(
    image: Tensor,
    target: BaseFormat,
    categories: Dict[int, str] = None,
    save_path: str = "",
    class_colors: List[Sequence[float]] = cc.glasbey_bw,
    instance_colors: List[Sequence[float]] = cc.glasbey_hv,
    desired_min_size: int = 1200,
    show: bool = False,
    window_mode: Literal["dual", "single"] = "dual",
) -> Tensor:
    """From image and target generates a visualization image as Tensor.

    Args:
        image (``Tensor``): Original image
        target (``BaseFormat``): Target to visualize
        categories (``Dict[int, str]``, **optional**): Categories to be used as labels as Dict[int, str]. If set to None will use label indexes. Defaults to None.
        save_path (``str``, **optional**): Path to save visualization, if set to "" will not save the visualization. Defaults to "".
        class_colors (``List[Sequence[float]]``, **optional**): Colors to be used for classes. Needs to be RGB normalized (divided by 255). Defaults to cc.glasbey_bw.
        instance_colors (``List[Sequence[float]]``, **optional**): Colors to be used for instances. Defaults to cc.glasbey_hv.
        desired_min_size (``int``, **optional**): Resize to this specific min size value (preserving shape). Defaults to 1200.
        show (``bool``, **optional**): Either to display it on the flight or not. Defaults to False.
        window_mode (``Literal[&quot;dual&quot;, &quot;single&quot;]``, **optional**): if dual : provide a combination of image + visu, otherwise will provide only visu. Defaults to "dual".

    Returns:
        ``Tensor``:
            - visualization Tensor
    """
    visualizer = Visualizer(
        image,
        target,
        categories,
        save_path,
        class_colors,
        instance_colors,
        desired_min_size,
        show,
        window_mode,
    )
    visualizer.visualize()
    return visualizer.visu


class Visualizer:
    """From image and target generates a visualization image as Tensor.

    Args:
        image (``Tensor``): Original image
        target (``BaseFormat``): Target to visualize
        categories (``Dict[int, str]``, **optional**): Categories to be used as labels as Dict[int, str]. If set to None will use label indexes. Defaults to None.
        save_path (``str``, **optional**): Path to save visualization, if set to "" will not save the visualization. Defaults to "".
        class_colors (``List[Sequence[float]]``, **optional**): Colors to be used for classes. Needs to be RGB normalized (divided by 255). Defaults to cc.glasbey_bw.
        instance_colors (``List[Sequence[float]]``, **optional**): Colors to be used for instances (see class colors constraints). Defaults to cc.glasbey_hv.
        desired_min_size (``int``, **optional**): Resize to this specific min size value (preserving shape). Defaults to 1200.
        show (``bool``, **optional**): Either to display it on the flight or not. Defaults to False.
        window_mode (``Literal[&quot;dual&quot;, &quot;single&quot;]``, **optional**): if dual : provide a combination of image + visu, otherwise will provide only visu. Defaults to "dual".
    """

    def __init__(
        self,
        image: Tensor,
        target: BaseFormat,
        categories: Dict[int, str] = None,
        save_path: str = "",
        class_colors: List[Sequence[float]] = cc.glasbey_bw,
        instance_colors: List[Sequence[float]] = cc.glasbey_hv,
        desired_min_size: int = 1200,
        show: bool = False,
        window_mode: Literal["dual", "single"] = "dual",
    ):
        # Multiply colors to be sure to fit nb objects / classes (default in colorcet is 256 colors)
        instance_colors = instance_colors * (math.floor(target.nb_object / 255) + 1)
        if target.labels.nelement() != 0:
            class_colors = class_colors * (
                math.ceil(torch.max(target.labels).item() / 255) + 1
            )
        # store attributes
        self.image = copy.deepcopy(image)
        self.target = copy.deepcopy(target)
        if save_path:
            self.save_path = (
                save_path if isinstance(save_path, Path) else Path(save_path)
            )
        else:
            self.save_path = None
        self.class_colors = [class_colors[l.item()] for l in self.target.labels]
        if self.target.nb_object != 0:
            if isinstance(self.class_colors[0][0], float) or isinstance(
                self.class_colors[0], list
            ):
                self.class_colors = [
                    tuple(int(i * 255) for i in t) for t in self.class_colors
                ]
            self.instance_colors = [
                instance_colors[i] for i in range(self.target.nb_object)
            ]
            if isinstance(self.instance_colors[0][0], float) or isinstance(
                self.instance_colors[0], list
            ):
                self.instance_colors = [
                    tuple(int(i * 255) for i in t) for t in self.instance_colors
                ]
        else:
            self.instance_colors = []
            self.class_colors = []
        self.categories = categories
        self.show_visu = show
        self.desired_min_size = desired_min_size
        self.window_mode = window_mode
        self.visu = copy.deepcopy(image)
        # Change device
        self.image = self.image.to("cpu")
        self.visu = self.visu.to("cpu")
        self.target.device = "cpu"
        # store text coordinates for label / scores as bounding box format [N, 4]. Done dynamically during visualize process
        self.coord_labels_scores: Union[Tensor, None] = None

    def _apply_visualization(self):
        # apply all visualizations funcs
        if isinstance(self.target, InstanceMaskFormat):
            self._mask_update_visu()
        if isinstance(self.target, BboxFormat):
            self._box_update_visu()
        self._resize_visu_img()
        self._add_label_scores()
        if self.window_mode == "dual":
            self.visu = torch.cat([self.image, self.visu], dim=2)

    def visualize(self):
        # Handles empty targets
        if self.target.nb_object != 0:
            self._apply_visualization()
        else:
            self._resize_visu_img()
        if self.show_visu:
            self._show()
        if self.save_path:
            save_image(self.visu, self.save_path)

    def _mask_update_visu(self):
        # draw class colored instance masks

        one_hots = one_hot(self.target.data.value.long()).permute(2, 0, 1)[1:]
        self.visu = draw_segmentation_masks(
            self.visu, one_hots.bool(), alpha=0.4, colors=self.class_colors
        )
        # find and draw instance colored contours
        np_one_hots = one_hots.numpy()
        contours_masks = []
        for i in range(np_one_hots.shape[0]):
            m = np.zeros((np_one_hots.shape[-2], np_one_hots.shape[-1], 3))
            c, _ = cv2.findContours(
                np_one_hots[i].astype(np.uint8),
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_NONE,
            )
            cv2.drawContours(m, c, -1, color=(1), thickness=2)
            contours_masks.append(torch.tensor(m))

        contours = torch.stack(contours_masks)
        self.visu = draw_segmentation_masks(
            self.visu,
            contours[:, :, :, 0].bool(),
            alpha=0.9,
            colors=self.instance_colors,
        )
        bboxes: BboxFormat = BboxFormat.from_instance_mask(self.target)
        bboxes.device = "cpu"
        bboxes.data.format = "XYXY"
        self.coord_labels_scores = bboxes.data.value

    def _box_update_visu(self):
        self.target.data.format = "XYXY"
        boxes = self.target.data.value
        self.visu = draw_bounding_boxes(
            self.visu, boxes, width=3, colors=self.class_colors
        )
        self.coord_labels_scores = boxes

    def _resize_visu_img(self):
        original_size = self.target.canvas_size
        factor = self.desired_min_size / min(original_size)
        new_size = (int(original_size[0] * factor), int(original_size[1] * factor))
        resizer = Resize(new_size)
        self.image = resizer(self.image)
        self.visu = resizer(self.visu)
        self.coord_labels_scores = resizer(self.coord_labels_scores)

    def _add_label_scores(self):
        labels = self.target.labels.tolist()
        if self.categories:
            labels = [self.categories[l] for l in labels]
        else:
            labels = [str(l) for l in labels]
        if self.target.scores != None:
            scores = self.target.scores.tolist()
            scores = [str(round(s, 2)) for s in scores]
        else:
            scores = ["" for l in labels]
        visu: Image = to_pil_image(copy.deepcopy(self.visu))
        graph = ImageDraw.Draw(visu)
        fnt_size = int(min(self.visu.shape[1], self.visu.shape[2]) / 55)
        font_lab = ImageFont.load_default()
        cls_coords = [
            (coord[0].item(), coord[1].item() - fnt_size)
            for coord in self.coord_labels_scores
        ]
        scores_coord = [
            (coord[0].item() + 5, coord[3].item() - fnt_size)
            for coord in self.coord_labels_scores
        ]
        for i, cls_c in enumerate(cls_coords):
            graph.text(
                cls_c,
                labels[i],
                font=font_lab,
                fill=self.class_colors[i],
                stroke_width=2,
                stroke_fill="white",
            )
            graph.text(
                scores_coord[i],
                scores[i],
                font=font_lab,
                fill=self.class_colors[i],
                stroke_width=2,
                stroke_fill="white",
            )
        self.visu = pil_to_tensor(visu)

    def _show(self):
        plt.imshow(self.visu.permute(1, 2, 0).numpy())
        plt.axis("off")
        plt.tight_layout()
        plt.show(block=True)
        plt.close()
