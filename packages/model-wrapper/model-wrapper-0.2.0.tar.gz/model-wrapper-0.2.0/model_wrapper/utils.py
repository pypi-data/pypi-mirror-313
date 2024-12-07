import os
from typing import Collection, List, Tuple, Union
from functools import reduce
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset


def get_device(device: Union[str, int, torch.device] = "auto"):
    if isinstance(device, str):
        device = device.lower()
        assert device in {"auto", "cpu", "cuda"} or device.startswith("cuda:")
        if device == "auto":
            return torch.device("cuda" if torch.cuda.is_available() else "cpu")
        return torch.device(device)

    if isinstance(device, torch.device):
        return device

    if isinstance(device, int):
        torch.device(f"cuda:{device}")

    raise ValueError(f"device: {device} is not supported")


def is_gpu(device: torch.device) -> bool:
    return "cpu" != device.type.lower()


def get_workers(num_data: int, batch_size: int, train: bool = True) -> int:
    cpu_count = os.cpu_count()
    half_steps = round(num_data / batch_size / 2)
    if train:
        return max(2, min(8, half_steps, cpu_count // 2))  # 2 ~ 8
    return min(4, half_steps, cpu_count // 4)  # 0 ~ 4


def is_float(x) -> bool:
    if isinstance(x, (Collection, np.ndarray)):
        return is_float(x[0])
    return isinstance(
        x,
        (
            float,
            np.float_,
            np.float16,
            np.float16,
            np.float32,
            np.float64,
            np.float128,
            np.single,
            np.double,
        ),
    )


def convert_to_tensor(x, dim_start=1) -> torch.Tensor:
    if 1 == dim_start:
        return (
            torch.tensor(x, dtype=torch.float)
            if is_float(x[0])
            else torch.tensor(x, dtype=torch.long)
        )
    return (
        torch.tensor(x, dtype=torch.float)
        if is_float(x[0][0])
        else torch.tensor(x, dtype=torch.long)
    )


def convert_data(X, y) -> Tuple[torch.Tensor, torch.Tensor]:
    if isinstance(X, (List, np.ndarray)):
        X = convert_to_tensor(X, 2)
    if isinstance(y, (List, np.ndarray)):
        y = convert_to_tensor(y)
    return X, y


def convert_data_r2(X, y) -> Tuple[torch.Tensor, torch.FloatTensor]:
    if isinstance(X, (List, np.ndarray)):
        X = convert_to_tensor(X, 2)
    if isinstance(y, (List, np.ndarray)):
        y = torch.tensor(y, dtype=torch.float)
    return X, y


def cal_count(y) -> int:
    shape = y.shape
    if len(shape) == 1:
        return shape[0]
    return reduce(lambda x1, x2: x1 * x2, shape)


def acc_predict(logits: torch.Tensor, threshold: int = 0.5) -> np.ndarray:
    logits = logits.cpu().numpy()
    shape = logits.shape
    shape_len = len(shape)
    if (shape_len == 2 and shape[1] > 1) or shape_len > 2:
        # 多分类 logits：(N, num_classes) 或 (N, K, num_classes)
        return logits.argmax(-1)
    else:
        # 二分类
        if shape_len == 2:
            # (N, 1)
            logits = logits.ravel()  # (N,) 一维
        return np.where(logits >= threshold, 1, 0).astype(np.int64)


def cal_correct(
    logits: torch.Tensor, y: torch.Tensor, threshold: int = 0.5
) -> np.int64:
    return (acc_predict(logits, threshold) == y.numpy()).sum()


def predict_dataset(
    model: nn.Module,
    dataset: Dataset,
    batch_size: int = 64,
    device: Union[str, int, torch.device] = "auto",
) -> Tuple[np.ndarray, np.ndarray]:
    preds = []
    targets = []
    device = get_device(device)
    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=get_workers(len(dataset), batch_size, train=False),
    )
    model = model.to(device)
    model.eval()
    with torch.no_grad():
        for data, target in loader:
            data = data.to(device)
            output = model(data)
            preds.append(output.cpu().numpy())
            targets.append(target.numpy())
    return np.concatenate(preds), np.concatenate(targets)


def acc_predict_dataset(
    model: nn.Module,
    dataset: Dataset,
    batch_size: int = 64,
    threshold: float = 0.5,
    device: Union[str, int, torch.device] = "auto",
) -> Tuple[np.ndarray, np.ndarray]:
    preds = []
    targets = []
    device = get_device(device)
    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=get_workers(len(dataset), batch_size, train=False),
    )
    model = model.to(device)
    model.eval()
    with torch.no_grad():
        for data, target in loader:
            data = data.to(device)
            output = model(data)
            preds.append(acc_predict(output, threshold))
            targets.append(target.numpy())
    return np.concatenate(preds), np.concatenate(targets)
