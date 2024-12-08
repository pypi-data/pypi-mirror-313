import inspect
import numpy as np
from tqdm import tqdm
from sklearn.metrics import r2_score
import torch
from torch.optim.lr_scheduler import LRScheduler
from torch.nn import functional as F

from model_wrapper.utils import cal_count, cal_correct


def _forward(model, batch, device):
    batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
    return model(*batch)


def _forward_dict(model, batch, device):
    batch = {
        key: value.to(device) if torch.is_tensor(value) else value
        for key, value in batch.items()
    }
    return model(**batch)


def _fit(model, batch, device):
    batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
    return model.fit(*batch)


def _fit_dict(model, batch, device):
    batch = {
        key: value.to(device) if torch.is_tensor(value) else value
        for key, value in batch.items()
    }
    return model.fit(**batch)


def _forward_y(model, batch, device):
    same_params = len(batch) == len(
        inspect.signature(model.forward).parameters
    )  # 判断所传参数个数是否与方法一致
    batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
    if same_params:
        return model(*batch), batch[-1]
    # 参数个数不一致，去掉最后一个
    return model(*(batch[:-1])), batch[-1]


def _forward_y_dict(model, batch, device):
    same_params = len(batch) == len(
        inspect.signature(model.forward).parameters
    )  # 判断所传参数个数是否与方法一致
    batch = {
        key: value.to(device) if torch.is_tensor(value) else value
        for key, value in batch.items()
    }
    if same_params:
        y = batch["labels"] if "labels" in batch else batch["targets"]
    else:  # 参数个数不一致，要把 'labels' 或 'targets' 从参数里剔除
        y = batch.pop("labels") if "labels" in batch else batch.pop("targets")
    return model(**batch), y


def _fit_y(model, batch, device):
    batch = [x.to(device) if torch.is_tensor(x) else x for x in batch]
    return model.fit(*batch), batch[-1]


def _fit_y_dict(model, batch, device):
    batch = {
        key: value.to(device) if torch.is_tensor(value) else value
        for key, value in batch.items()
    }
    return model.fit(**batch), (
        batch["labels"] if "labels" in batch else batch["targets"]
    )


#   ----------------------------------------------------------------


def evaluate(model, val_loader, device, is_tuple_params: bool = None) -> float:
    total_loss = torch.Tensor([0.0]).to(device)
    is_tuple_params = (
        is_tuple_params
        if is_tuple_params is not None
        else isinstance(next(iter(val_loader)), (list, tuple))
    )
    model.eval()
    with torch.no_grad():
        if hasattr(model, "fit"):
            if is_tuple_params:
                for batch in val_loader:
                    loss, logits = _fit(model, batch, device)
                    total_loss += loss
            else:
                for batch in val_loader:
                    loss, logits = _fit_dict(model, batch, device)
                    total_loss += loss
        else:
            if is_tuple_params:
                for batch in val_loader:
                    loss, logits = _forward(model, batch, device)
                    total_loss += loss
            else:
                for batch in val_loader:
                    loss, logits = _forward_dict(model, batch, device)
                    total_loss += loss
    return total_loss.item() / len(val_loader)


def evaluate_progress(
    model, val_loader, device, epoch, epochs, is_tuple_params: bool = None
) -> float:
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    is_tuple_params = (
        is_tuple_params
        if is_tuple_params is not None
        else isinstance(next(iter(val_loader)), (list, tuple))
    )
    model.eval()
    with torch.no_grad():
        loop = tqdm(
            val_loader,
            desc=f"[Epoch-{epoch}/{epochs} Valid]",
            total=len(val_loader),
            colour="green",
        )
        if hasattr(model, "fit"):
            if is_tuple_params:
                for batch in loop:
                    loss, logits = _fit(model, batch, device)
                    total_loss += loss
                    steps += 1
                    loop.set_postfix(Loss=f"{total_loss.item() / steps:.4f}")
            else:
                for batch in loop:
                    loss, logits = _fit_dict(model, batch, device)
                    total_loss += loss
                    steps += 1
                    loop.set_postfix(Loss=f"{total_loss.item() / steps:.4f}")
        else:
            if is_tuple_params:
                for batch in loop:
                    loss, logits = _forward(model, batch, device)
                    total_loss += loss
                    steps += 1
                    loop.set_postfix(Loss=f"{total_loss.item() / steps:.4f}")
            else:
                for batch in loop:
                    loss, logits = _forward_dict(model, batch, device)
                    total_loss += loss
                    steps += 1
                    loop.set_postfix(Loss=f"{total_loss.item() / steps:.4f}")

        loop.close()

    return total_loss.item() / steps


def evaluate_epoch(
    model, val_loader, device, epoch, epochs, show_progress, is_tuple_params
):
    if show_progress:
        return evaluate_progress(
            model, val_loader, device, epoch, epochs, is_tuple_params=is_tuple_params
        )
    else:
        return evaluate(model, val_loader, device, is_tuple_params=is_tuple_params)


def do_train(model, batch, optimizer, device):
    loss, logits = _forward(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss


def do_train_dict(model, batch, optimizer, device):
    loss, logits = _forward_dict(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss


def do_fit(model, batch, optimizer, device):
    loss, logits = _fit(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss


def do_fit_dict(model, batch, optimizer, device):
    loss, logits = _fit_dict(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss


def do_train_scheduler(model, batch, optimizer, device, scheduler: LRScheduler):
    loss, logits = _forward(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss


def do_train_scheduler_dict(model, batch, optimizer, device, scheduler: LRScheduler):
    loss, logits = _forward_dict(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss


def do_fit_scheduler(model, batch, optimizer, device, scheduler: LRScheduler):
    loss, logits = _fit(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss


def do_fit_scheduler_dict(model, batch, optimizer, device, scheduler: LRScheduler):
    loss, logits = _fit_dict(model, batch, device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss


def train_epoch_base(model, train_loader, optimizer, device, is_tuple_params):
    total_loss = torch.Tensor([0.0]).to(device)
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in train_loader:
                loss = do_fit(model, batch, optimizer, device)
                total_loss += loss
        else:
            for batch in train_loader:
                loss = do_fit_dict(model, batch, optimizer, device)
                total_loss += loss
    else:
        if is_tuple_params:
            for batch in train_loader:
                loss = do_train(model, batch, optimizer, device)
                total_loss += loss
        else:
            for batch in train_loader:
                loss = do_train_dict(model, batch, optimizer, device)
                total_loss += loss

    return total_loss.item() / len(train_loader)


def train_epoch_progress(
    model, train_loader, optimizer, device, epoch, epochs, is_tuple_params
):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in loop:
                loss = do_fit(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                loop.set_postfix(
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
        else:
            for batch in loop:
                loss = do_fit_dict(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                loop.set_postfix(
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
    else:
        if is_tuple_params:
            for batch in loop:
                loss = do_train(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                loop.set_postfix(
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
        else:
            for batch in loop:
                loss = do_train_dict(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                loop.set_postfix(
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
    loop.close()
    return total_loss.item() / steps


def train_epoch_scheduler(
    model, train_loader, optimizer, device, scheduler: LRScheduler, is_tuple_params
):
    total_loss = torch.Tensor([0.0]).to(device)
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in train_loader:
                loss = do_fit_scheduler(model, batch, optimizer, device, scheduler)
                total_loss += loss
        else:
            for batch in train_loader:
                loss = do_fit_scheduler_dict(model, batch, optimizer, device, scheduler)
                total_loss += loss
    else:
        if is_tuple_params:
            for batch in train_loader:
                loss = do_train_scheduler(model, batch, optimizer, device, scheduler)
                total_loss += loss
        else:
            for batch in train_loader:
                loss = do_train_scheduler_dict(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
    return total_loss.item() / len(train_loader)


def train_epoch_scheduler_progress(
    model, train_loader, optimizer, device, scheduler, epoch, epochs, is_tuple_params
):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in loop:
                loss = do_fit_scheduler(model, batch, optimizer, device, scheduler)
                total_loss += loss
                steps += 1
                loop.set_postfix(
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
        else:
            for batch in loop:
                loss = do_fit_scheduler_dict(model, batch, optimizer, device, scheduler)
                total_loss += loss
                steps += 1
                loop.set_postfix(
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
    else:
        if is_tuple_params:
            for batch in loop:
                loss = do_train_scheduler(model, batch, optimizer, device, scheduler)
                total_loss += loss
                steps += 1
                loop.set_postfix(
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
        else:
            for batch in loop:
                loss = do_train_scheduler_dict(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                steps += 1
                loop.set_postfix(
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
    loop.close()
    return total_loss.item() / steps


def train_epoch(
    model,
    train_loader,
    optimizer,
    device,
    scheduler,
    epoch,
    epochs,
    show_progress,
    is_tuple_params,
):
    if show_progress:
        if scheduler is None:
            return train_epoch_progress(
                model, train_loader, optimizer, device, epoch, epochs, is_tuple_params
            )
        return train_epoch_scheduler_progress(
            model,
            train_loader,
            optimizer,
            device,
            scheduler,
            epoch,
            epochs,
            is_tuple_params,
        )
    else:
        if scheduler is None:
            return train_epoch_base(
                model, train_loader, optimizer, device, is_tuple_params
            )
        return train_epoch_scheduler(
            model, train_loader, optimizer, device, scheduler, is_tuple_params
        )


#  ----------------------------------------------------------------


def acc_loss_logits(outputs, targets):
    if isinstance(outputs, tuple):
        loss, logits = outputs
    else:
        logits = outputs
        shape = logits.size()
        shape_len = len(shape)
        if shape_len == 2 and shape[1] > 1:
            # 多分类 logits: (N, num_classes), targets: (N,) 一维
            loss = F.cross_entropy(logits, targets)
        elif shape_len > 2:
            # 多分类 logits: (N, K, num_classes), targets: (N, K)
            targets = targets.view(-1)  # (N * K,) 一维
            logits = logits.reshape(targets.size(0))  # (N * K, num_classes)
            loss = F.cross_entropy(logits, targets)
        else:
            # 二分类 targets: (N,) 一维
            if shape_len == 2:
                # (N, 1)
                logits = logits.ravel()  # (N,) 一维
            loss = F.binary_cross_entropy(logits, targets)

    return loss, logits


def acc_evaluate(
    model, val_loader, device, threshold: int = 0.5, is_tuple_params: bool = None
):
    total, correct = 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    is_tuple_params = (
        is_tuple_params
        if is_tuple_params is not None
        else isinstance(next(iter(val_loader)), (list, tuple))
    )
    model.eval()
    with torch.no_grad():
        if hasattr(model, "fit"):
            if is_tuple_params:
                for batch in val_loader:
                    outputs, y = _fit_y(model, batch, device)
                    loss, logits = acc_loss_logits(outputs, y)
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)
            else:
                for batch in val_loader:
                    outputs, y = _fit_y_dict(model, batch, device)
                    loss, logits = acc_loss_logits(outputs, y)
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)
        else:
            if is_tuple_params:
                for batch in val_loader:
                    outputs, y = _forward_y(model, batch, device)
                    loss, logits = acc_loss_logits(outputs, y)
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)
            else:
                for batch in val_loader:
                    outputs, y = _forward_y_dict(model, batch, device)
                    loss, logits = acc_loss_logits(outputs, y)
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)

    return (total_loss.item() / len(val_loader)), (correct / total)


def acc_evaluate_progress(
    model,
    val_loader,
    device,
    epoch,
    epochs,
    threshold: int = 0.5,
    is_tuple_params: bool = None,
):
    total, correct, steps = 0, 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    is_tuple_params = (
        is_tuple_params
        if is_tuple_params is not None
        else isinstance(next(iter(val_loader)), (list, tuple))
    )
    model.eval()
    with torch.no_grad():
        loop = tqdm(
            val_loader,
            desc=f"[Epoch-{epoch}/{epochs} Valid]",
            total=len(val_loader),
            colour="green",
        )
        if hasattr(model, "fit"):
            if is_tuple_params:
                for batch in loop:
                    outputs, y = _fit_y(model, batch, device)
                    loss, logits = acc_loss_logits(outputs, y)
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)
                    steps += 1
                    loop.set_postfix(
                        Acc=f"{correct / total:.4f}",
                        Loss=f"{total_loss.item() / steps:.4f}",
                    )
            else:
                for batch in loop:
                    outputs, y = _fit_y_dict(model, batch, device)
                    loss, logits = acc_loss_logits(outputs, y)
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)
                    steps += 1
                    loop.set_postfix(
                        Acc=f"{correct / total:.4f}",
                        Loss=f"{total_loss.item() / steps:.4f}",
                    )
        else:
            if is_tuple_params:
                for batch in loop:
                    outputs, y = _forward_y(model, batch, device)
                    loss, logits = acc_loss_logits(outputs, y)
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)
                    steps += 1
                    loop.set_postfix(
                        Acc=f"{correct / total:.4f}",
                        Loss=f"{total_loss.item() / steps:.4f}",
                    )
            else:
                for batch in loop:
                    outputs, y = _forward_y_dict(model, batch, device)
                    loss, logits = acc_loss_logits(outputs, y)
                    total_loss += loss
                    total += cal_count(y)
                    correct += cal_correct(logits, y, threshold)
                    steps += 1
                    loop.set_postfix(
                        Acc=f"{correct / total:.4f}",
                        Loss=f"{total_loss.item() / steps:.4f}",
                    )

        loop.close()

    return (total_loss.item() / steps), (correct / total)


def acc_evaluate_epoch(
    model, val_loader, device, epoch, epochs, show_progress, is_tuple_params
):
    if show_progress:
        return acc_evaluate_progress(
            model, val_loader, device, epoch, epochs, is_tuple_params=is_tuple_params
        )
    else:
        return acc_evaluate(model, val_loader, device, is_tuple_params=is_tuple_params)


def do_train_acc(model, batch, optimizer, device):
    outputs, y = _forward_y(model, batch, device)
    loss, logits = acc_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def do_train_acc_dict(model, batch, optimizer, device):
    outputs, y = _forward_y_dict(model, batch, device)
    loss, logits = acc_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def do_fit_acc(model, batch, optimizer, device):
    outputs, y = _fit_y(model, batch, device)
    loss, logits = acc_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def do_fit_acc_dict(model, batch, optimizer, device):
    outputs, y = _fit_y_dict(model, batch, device)
    loss, logits = acc_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def do_train_scheduler_acc(model, batch, optimizer, device, scheduler: LRScheduler):
    outputs, y = _forward_y(model, batch, device)
    loss, logits = acc_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def do_train_scheduler_acc_dict(
    model, batch, optimizer, device, scheduler: LRScheduler
):
    outputs, y = _forward_y_dict(model, batch, device)
    loss, logits = acc_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def do_fit_scheduler_acc(model, batch, optimizer, device, scheduler: LRScheduler):
    outputs, y = _fit_y(model, batch, device)
    loss, logits = acc_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def do_fit_scheduler_acc_dict(model, batch, optimizer, device, scheduler: LRScheduler):
    outputs, y = _fit_y_dict(model, batch, device)
    loss, logits = acc_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, cal_count(y), cal_correct(logits.detach(), y)


def train_epoch_base_acc(model, train_loader, optimizer, device, is_tuple_params):
    total, total_correct = 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in train_loader:
                loss, count, correct = do_fit_acc(model, batch, optimizer, device)
                total_loss += loss
                total += count
                total_correct += correct
        else:
            for batch in train_loader:
                loss, count, correct = do_fit_acc_dict(model, batch, optimizer, device)
                total_loss += loss
                total += count
                total_correct += correct
    else:
        if is_tuple_params:
            for batch in train_loader:
                loss, count, correct = do_train_acc(model, batch, optimizer, device)
                total_loss += loss
                total += count
                total_correct += correct
        else:
            for batch in train_loader:
                loss, count, correct = do_train_acc_dict(
                    model, batch, optimizer, device
                )
                total_loss += loss
                total += count
                total_correct += correct
    return total_correct / total, total_loss.item() / len(train_loader)


def train_epoch_progress_acc(
    model, train_loader, optimizer, device, epoch, epochs, is_tuple_params
):
    total, steps, total_correct = 0, 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in loop:
                loss, count, correct = do_fit_acc(model, batch, optimizer, device)
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix(
                    Acc=f"{total_correct.item() / total:.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
        else:
            for batch in loop:
                loss, count, correct = do_fit_acc_dict(model, batch, optimizer, device)
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix(
                    Acc=f"{total_correct.item() / total:.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
    else:
        if is_tuple_params:
            for batch in loop:
                loss, count, correct = do_train_acc(model, batch, optimizer, device)
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix(
                    Acc=f"{total_correct.item() / total:.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
        else:
            for batch in loop:
                loss, count, correct = do_train_acc_dict(
                    model, batch, optimizer, device
                )
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix(
                    Acc=f"{total_correct.item() / total:.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
    loop.close()

    return total_correct / total, total_loss.item() / steps


def train_epoch_scheduler_acc(
    model, train_loader, optimizer, device, scheduler: LRScheduler, is_tuple_params
):
    total, total_correct = 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in train_loader:
                loss, count, correct = do_fit_scheduler_acc(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                total += count
                total_correct += correct
        else:
            for batch in train_loader:
                loss, count, correct = do_fit_scheduler_acc_dict(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                total += count
                total_correct += correct
    else:
        if is_tuple_params:
            for batch in train_loader:
                loss, count, correct = do_train_scheduler_acc(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                total += count
                total_correct += correct
        else:
            for batch in train_loader:
                loss, count, correct = do_train_scheduler_acc_dict(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                total += count
                total_correct += correct
    return total_correct / total, total_loss.item() / len(train_loader)


def train_epoch_scheduler_progress_acc(
    model, train_loader, optimizer, device, scheduler, epoch, epochs, is_tuple_params
):
    total, steps, total_correct = 0, 0, 0
    total_loss = torch.Tensor([0.0]).to(device)
    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in loop:
                loss, count, correct = do_fit_scheduler_acc(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix(
                    Acc=f"{total_correct.item() / total:.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
        else:
            for batch in loop:
                loss, count, correct = do_fit_scheduler_acc_dict(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix(
                    Acc=f"{total_correct.item() / total:.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
    else:
        if is_tuple_params:
            for batch in loop:
                loss, count, correct = do_train_scheduler_acc(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix(
                    Acc=f"{total_correct.item() / total:.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
        else:
            for batch in loop:
                loss, count, correct = do_train_scheduler_acc_dict(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                total += count
                total_correct += correct
                steps += 1
                loop.set_postfix(
                    Acc=f"{total_correct.item() / total:.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
    loop.close()

    return total_correct / total, total_loss.item() / steps


def train_epoch_acc(
    model,
    train_loader,
    optimizer,
    device,
    scheduler,
    epoch,
    epochs,
    show_progress,
    is_tuple_params,
):
    if show_progress:
        if scheduler is None:
            return train_epoch_progress_acc(
                model, train_loader, optimizer, device, epoch, epochs, is_tuple_params
            )
        return train_epoch_scheduler_progress_acc(
            model,
            train_loader,
            optimizer,
            device,
            scheduler,
            epoch,
            epochs,
            is_tuple_params,
        )
    else:
        if scheduler is None:
            return train_epoch_base_acc(
                model, train_loader, optimizer, device, is_tuple_params
            )
        return train_epoch_scheduler_acc(
            model, train_loader, optimizer, device, scheduler, is_tuple_params
        )


#   ----------------------------------------------------------------


def r2_loss_logits(outputs, targets):
    if isinstance(outputs, tuple):
        loss, logits = outputs
    else:
        logits = outputs
        loss = F.mse_loss(logits, targets.view(logits.size()))
    return loss, logits


def _r2_score(y_true: list[np.ndarray], y_pred: list[np.ndarray]):
    y_true = np.concatenate(y_true, axis=0).ravel()
    y_pred = np.concatenate(y_pred, axis=0).ravel()
    return r2_score(y_true, y_pred)


def r2_evaluate(model, val_loader, device, is_tuple_params: bool = None):
    labels, preds = [], []
    total_loss = torch.Tensor([0.0]).to(device)
    is_tuple_params = (
        is_tuple_params
        if is_tuple_params is not None
        else isinstance(next(iter(val_loader)), (list, tuple))
    )
    model.eval()
    with torch.no_grad():
        if hasattr(model, "fit"):
            if is_tuple_params:
                for batch in val_loader:
                    outputs, y = _fit_y(model, batch, device)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())
            else:
                for batch in val_loader:
                    outputs, y = _fit_y_dict(model, batch, device)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())
        else:
            if is_tuple_params:
                for batch in val_loader:
                    outputs, y = _forward_y(model, batch, device)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())
            else:
                for batch in val_loader:
                    outputs, y = _forward_y_dict(model, batch, device)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())

    return total_loss.item() / len(val_loader), _r2_score(labels, preds)


def r2_evaluate_progress(
    model, val_loader, device, epoch, epochs, is_tuple_params: bool = None
):
    steps = 0
    labels, preds = [], []
    total_loss = torch.Tensor([0.0]).to(device)
    is_tuple_params = (
        is_tuple_params
        if is_tuple_params is not None
        else isinstance(next(iter(val_loader)), (list, tuple))
    )
    model.eval()
    with torch.no_grad():
        loop = tqdm(
            val_loader,
            desc=f"[Epoch-{epoch}/{epochs} Valid]",
            total=len(val_loader),
            colour="green",
        )
        if hasattr(model, "fit"):
            if is_tuple_params:
                for batch in loop:
                    outputs, y = _fit_y(model, batch, device)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())
                    steps += 1
                    loop.set_postfix(
                        R2=f"{_r2_score(labels, preds):.4f}",
                        Loss=f"{total_loss.item() / steps:.4f}",
                    )
            else:
                for batch in loop:
                    outputs, y = _fit_y_dict(model, batch, device)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())
                    steps += 1
                    loop.set_postfix(
                        R2=f"{_r2_score(labels, preds):.4f}",
                        Loss=f"{total_loss.item() / steps:.4f}",
                    )
        else:
            if is_tuple_params:
                for batch in loop:
                    outputs, y = _forward_y(model, batch, device)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())
                    steps += 1
                    loop.set_postfix(
                        R2=f"{_r2_score(labels, preds):.4f}",
                        Loss=f"{total_loss.item() / steps:.4f}",
                    )
            else:
                for batch in loop:
                    outputs, y = _forward_y_dict(model, batch, device)
                    loss, logits = r2_loss_logits(outputs, y)
                    total_loss += loss
                    labels.append(y.cpu().numpy().ravel())
                    preds.append(logits.cpu().numpy().ravel())
                    steps += 1
                    loop.set_postfix(
                        R2=f"{_r2_score(labels, preds):.4f}",
                        Loss=f"{total_loss.item() / steps:.4f}",
                    )

        loop.close()

    return total_loss.item() / steps, _r2_score(labels, preds)


def r2_evaluate_epoch(
    model, val_loader, device, epoch, epochs, show_progress, is_tuple_params
):
    if show_progress:
        return r2_evaluate_progress(
            model, val_loader, device, epoch, epochs, is_tuple_params=is_tuple_params
        )
    else:
        return r2_evaluate(model, val_loader, device, is_tuple_params=is_tuple_params)


def train_epoch_r2(
    model,
    train_loader,
    optimizer,
    device,
    scheduler,
    epoch,
    epochs,
    show_progress,
    is_tuple_params,
):
    if show_progress:
        if scheduler is None:
            return train_epoch_progress_r2(
                model, train_loader, optimizer, device, epoch, epochs, is_tuple_params
            )
        return train_epoch_scheduler_progress_r2(
            model,
            train_loader,
            optimizer,
            device,
            scheduler,
            epoch,
            epochs,
            is_tuple_params,
        )
    else:
        if scheduler is None:
            return train_epoch_base_r2(
                model, train_loader, optimizer, device, is_tuple_params
            )
        return train_epoch_scheduler_r2(
            model, train_loader, optimizer, device, scheduler, is_tuple_params
        )


def train_epoch_base_r2(model, train_loader, optimizer, device, is_tuple_params):
    total_loss = torch.Tensor([0.0]).to(device)
    labels, preds = [], []
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in train_loader:
                loss, label, pred = do_fit_r2(model, batch, optimizer, device)
                total_loss += loss
                labels.append(label.ravel())
                preds.append(pred.ravel())
        else:
            for batch in train_loader:
                loss, label, pred = do_fit_r2_dict(model, batch, optimizer, device)
                total_loss += loss
                labels.append(label.ravel())
                preds.append(pred.ravel())
    else:
        if is_tuple_params:
            for batch in train_loader:
                loss, label, pred = do_train_r2(model, batch, optimizer, device)
                total_loss += loss
                labels.append(label.ravel())
                preds.append(pred.ravel())
        else:
            for batch in train_loader:
                loss, label, pred = do_train_r2_dict(model, batch, optimizer, device)
                total_loss += loss
                labels.append(label.ravel())
                preds.append(pred.ravel())
    return _r2_score(labels, preds), total_loss.item() / len(train_loader)


def train_epoch_progress_r2(
    model, train_loader, optimizer, device, epoch, epochs, is_tuple_params
):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    labels, preds = [], []
    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in loop:
                loss, label, pred = do_fit_r2(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix(
                    R2=f"{_r2_score(labels, preds):.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
        else:
            for batch in loop:
                loss, label, pred = do_fit_r2_dict(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix(
                    R2=f"{_r2_score(labels, preds):.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
    else:
        if is_tuple_params:
            for batch in loop:
                loss, label, pred = do_train_r2(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix(
                    R2=f"{_r2_score(labels, preds):.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
        else:
            for batch in loop:
                loss, label, pred = do_train_r2_dict(model, batch, optimizer, device)
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix(
                    R2=f"{_r2_score(labels, preds):.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
    loop.close()

    return _r2_score(labels, preds), total_loss.item() / steps


def train_epoch_scheduler_r2(
    model, train_loader, optimizer, device, scheduler: LRScheduler, is_tuple_params
):
    total_loss = torch.Tensor([0.0]).to(device)
    labels, preds = [], []
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in train_loader:
                loss, label, pred = do_fit_scheduler_r2(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                labels.append(label.ravel())
                preds.append(pred.ravel())
        else:
            for batch in train_loader:
                loss, label, pred = do_fit_scheduler_r2_dict(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                labels.append(label.ravel())
                preds.append(pred.ravel())
    else:
        if is_tuple_params:
            for batch in train_loader:
                loss, label, pred = do_train_scheduler_r2(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                labels.append(label.ravel())
                preds.append(pred.ravel())
        else:
            for batch in train_loader:
                loss, label, pred = do_train_scheduler_r2_dict(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                labels.append(label.ravel())
                preds.append(pred.ravel())
    return _r2_score(labels, preds), total_loss.item() / len(train_loader)


def train_epoch_scheduler_progress_r2(
    model, train_loader, optimizer, device, scheduler, epoch, epochs, is_tuple_params
):
    steps = 0
    total_loss = torch.Tensor([0.0]).to(device)
    labels, preds = [], []
    loop = tqdm(
        train_loader,
        desc=f"[Epoch-{epoch}/{epochs} Train]",
        total=len(train_loader),
        colour="green",
    )
    if hasattr(model, "fit"):
        if is_tuple_params:
            for batch in loop:
                loss, label, pred = do_fit_scheduler_r2(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix(
                    R2=f"{_r2_score(labels, preds):.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
        else:
            for batch in loop:
                loss, label, pred = do_fit_scheduler_r2_dict(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix(
                    R2=f"{_r2_score(labels, preds):.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
    else:
        if is_tuple_params:
            for batch in loop:
                loss, label, pred = do_train_scheduler_r2(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix(
                    R2=f"{_r2_score(labels, preds):.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
        else:
            for batch in loop:
                loss, label, pred = do_train_scheduler_r2_dict(
                    model, batch, optimizer, device, scheduler
                )
                total_loss += loss
                steps += 1
                labels.append(label.ravel())
                preds.append(pred.ravel())
                loop.set_postfix(
                    R2=f"{_r2_score(labels, preds):.4f}",
                    Loss=f"{total_loss.item() / steps:.4f}",
                    lr=f'{optimizer.param_groups[0]["lr"]:.6f}',
                )
    loop.close()

    return _r2_score(labels, preds), total_loss.item() / steps


def do_train_r2(model, batch, optimizer, device):
    outputs, y = _forward_y(model, batch, device)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def do_train_r2_dict(model, batch, optimizer, device):
    outputs, y = _forward_y_dict(model, batch, device)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def do_fit_r2(model, batch, optimizer, device):
    outputs, y = _fit_y(model, batch, device)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def do_fit_r2_dict(model, batch, optimizer, device):
    outputs, y = _fit_y_dict(model, batch, device)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def do_train_scheduler_r2(model, batch, optimizer, device, scheduler: LRScheduler):
    outputs, y = _forward_y(model, batch, device)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def do_train_scheduler_r2_dict(model, batch, optimizer, device, scheduler: LRScheduler):
    outputs, y = _forward_y_dict(model, batch, device)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def do_fit_scheduler_r2(model, batch, optimizer, device, scheduler: LRScheduler):
    outputs, y = _fit_y(model, batch, device)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()


def do_fit_scheduler_r2_dict(model, batch, optimizer, device, scheduler: LRScheduler):
    outputs, y = _fit_y_dict(model, batch, device)
    loss, logits = r2_loss_logits(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()
    return loss, y.cpu().numpy(), logits.detach().cpu().numpy()
