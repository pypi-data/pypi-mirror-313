import torch
from torch import Tensor
from torchvision.ops import masks_to_boxes
import copy
import cv2
import numpy as np
from typing import Tuple


def mask2boxes(mask: Tensor) -> Tensor:
    """from stacked (id object = 1 ... N) mask (H, W) returns tensor of shape (N, 4)"""
    assert (
        mask.dim() == 2
    ), f"mask must be a stacked (id object = 1 ... N) mask of shape (H, W), got {mask.shape}"
    if torch.max(mask) == 0:
        return torch.empty((0, 4)).to(mask.device)
    objs = torch.arange(1, torch.max(mask) + 1)
    box_list = []
    for i in objs:
        m = copy.deepcopy(mask)
        m[mask != i] = 0
        m[mask == i] = 1
        box_list.append(masks_to_boxes(m[None, :]))
    return torch.cat(box_list, dim=0)


def reindex_mask_with_splitted_objects(mask: Tensor) -> Tuple[Tensor, Tensor]:
    """Function that reidex masks objects by creating new objects if they are disconnected.

    Args:
        mask (``Tensor``): Input mask tensor containing disconnected part of given objects.

    Returns:
        ``Tuple[Tensor, Tensor]``:
            - New mask indexed with 1 per object after separating disconnected objects, indexes of original common objects they belonged.

    Detailed explanation : Imagine a mask with 2 objects 0 and 1 and the first is separated in two parts disconnected.
    The new mask will contain 3 objects and the indices will be [0, 0, 1]

    """
    assert (
        mask.dim() == 2
    ), f"mask must be a stacked (id object = 1 ... N) mask of shape (H, W), got {mask.shape}"
    if torch.max(mask) == 0:
        return mask, torch.tensor([])

    objs = torch.arange(1, torch.max(mask) + 1)
    new_mask = torch.zeros(mask.shape).to(mask.device)
    split_count = 0
    new_labels_indices = []
    for i in objs:
        m = copy.deepcopy(mask)
        m[mask != i] = 0
        m[mask == i] = i
        np_mat = m.detach().cpu().numpy().astype(np.uint8)
        bool_mat = np_mat == 0
        contours, _ = cv2.findContours(
            np_mat,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_NONE,
        )
        mat = np.zeros(np_mat.shape)
        for j, c in enumerate(contours):
            split_count += j
            val = float(i + split_count)
            cv2.fillConvexPoly(mat, c, (val, val, val))
            new_labels_indices.append(i)
        mat[bool_mat] = 0
        add_mask = torch.tensor(mat).to(mask.device)
        new_mask, _ = torch.max(torch.stack([new_mask, add_mask]), dim=0)
    return new_mask, torch.tensor(new_labels_indices).to(new_mask.device)


def redefine_labels_scores(labs: Tensor, present: Tensor):
    new = labs[present.tolist()]
    return new
