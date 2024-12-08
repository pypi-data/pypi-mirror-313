from copy import deepcopy
from typing import Tuple, Union
import torch
from torch import nn
from torch import optim
from torch.utils.data import DataLoader, TensorDataset, Dataset
from torch.optim.lr_scheduler import LRScheduler, CosineAnnealingLR

from model_wrapper import log_utils
from model_wrapper.utils import convert_data, convert_data_r2, get_device, is_gpu, get_workers
from ._support import (
    evaluate_epoch,
    acc_evaluate_epoch,
    r2_evaluate_epoch,
    train_epoch,
    train_epoch_acc,
    train_epoch_r2,
)


def get_early_stopping_rounds(epochs):
    if epochs <= 10:
        return max(2, int(0.2 * epochs))
    if epochs <= 50:
        return min(10, int(0.2 * epochs))
    return max(10, int(0.1 * epochs))


class Trainer:

    def __init__(
        self,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=32,
        num_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        self.epochs = epochs
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.lr = lr
        self.T_max = T_max
        self.batch_size = batch_size
        self.device = get_device(device)
        self.num_workers = num_workers
        self.pin_memory = pin_memory
        self.pin_memory_device = pin_memory_device
        self.persistent_workers = persistent_workers
        self.early_stopping_rounds = early_stopping_rounds or get_early_stopping_rounds(
            epochs
        )
        self.print_per_rounds = print_per_rounds
        self.checkpoint_per_rounds = checkpoint_per_rounds
        self.checkpoint_name = checkpoint_name

    def _begin_train(self):
        log_utils.info(f"Use {self.device} training...\n")

    def _get_workers(
        self, num_workers: int, dataset: Dataset, batch_size: int, train: bool = True
    ) -> int:
        if is_gpu(self.device):
            return (
                num_workers
                if num_workers > 0
                else get_workers(len(dataset), batch_size, train)
            )
        else:
            return (
                num_workers
                if num_workers >= 0
                else get_workers(len(dataset), batch_size, train)
            )

    def _get_pin_persistent(self, num_workers: int) -> Tuple[bool, bool]:
        pin_memory = self.pin_memory or (num_workers > 0 and is_gpu(self.device))
        persistent_workers = self.persistent_workers or (
            num_workers > 0 and is_gpu(self.device)
        )
        return pin_memory, persistent_workers

    def _build_train_loader(self, train_set: Dataset, collate_fn=None) -> DataLoader:
        num_workers = self._get_workers(self.num_workers, train_set, self.batch_size)
        pin_memory, persistent_workers = self._get_pin_persistent(num_workers)
        return DataLoader(
            dataset=train_set,
            batch_size=self.batch_size,
            pin_memory=pin_memory,
            pin_memory_device=self.pin_memory_device,
            persistent_workers=persistent_workers,
            num_workers=num_workers,
            shuffle=True,
            collate_fn=collate_fn,
        )

    def _build_val_loader(self, val_set: Dataset, eval_batch_size: int, num_eval_workers: int, collate_fn=None):
        num_eval_workers = self._get_workers(num_eval_workers, val_set, eval_batch_size, False)
        return DataLoader(
            dataset=val_set,
            batch_size=eval_batch_size,
            num_workers=num_eval_workers,
            collate_fn=collate_fn,
        )
    
    def train(
        self, model, train_set: Dataset, collate_fn=None, show_progress=False, eps=1e-5
    ) -> Tuple[nn.Module, dict]:
        train_loader = self._build_train_loader(train_set, collate_fn)
        self._begin_train()
        cnt = 0
        min_loss = float("inf")
        best_model = None
        train_losses = []
        if next(model.parameters()).device != self.device:
            model = model.to(self.device)
        optimizer, scheduler = self.get_optimizer_scheduler(model)
        is_tuple_params = isinstance(next(iter(train_loader)), (tuple, list))

        model.train()
        for epoch in range(1, self.epochs + 1):
            avg_loss = train_epoch(
                model,
                train_loader,
                optimizer,
                self.device,
                scheduler,
                epoch,
                self.epochs,
                show_progress,
                is_tuple_params,
            )
            train_losses.append(avg_loss)
            self.try_print(
                self.print,
                show_progress,
                epoch,
                optimizer.param_groups[0]["lr"],
                avg_loss,
            )
            self.try_checkpoint(model, epoch)

            if min_loss - avg_loss > eps:
                cnt = 0
                best_model = deepcopy(model)
                min_loss = avg_loss
                continue

            # x次epoch的val_acc不提升或x次epoch的val_acc不变化
            if (
                epoch >= min(3, self.early_stopping_rounds)
                and cnt >= self.early_stopping_rounds
            ):
                log_utils.info(f"Early stopping at Epoch-{epoch}")
                break

            cnt += 1

        log_utils.info(f"Min loss: {min_loss:.4f}\n")
        return best_model, {"train_losses": train_losses}

    def get_optimizer_scheduler(self, model):
        scheduler = None
        if self.scheduler is not None:
            scheduler = self.scheduler
            optimizer = scheduler.optimizer
        elif self.optimizer is None:
            optimizer = optim.AdamW(model.parameters(), lr=self.lr)
        elif isinstance(self.optimizer, type):
            optimizer = self.optimizer(model.parameters(), lr=self.lr)
        else:
            optimizer = self.optimizer

        if scheduler is None and self.T_max and self.T_max > 0:
            scheduler = CosineAnnealingLR(optimizer, T_max=self.T_max)

        return optimizer, scheduler

    def try_checkpoint(self, model, epoch):
        if self.checkpoint_per_rounds <= 0:
            return

        if self.checkpoint_per_rounds == 1 or epoch % self.checkpoint_per_rounds == 0:
            torch.save(model, self.checkpoint_name)

    def try_print(self, do_print, show_progress, epoch, lr, loss, **kwargs):
        if self.print_per_rounds == 1 or epoch % self.print_per_rounds == 0:
            do_print(show_progress, epoch, lr, loss, **kwargs)

    def print(self, show_progress, epoch, lr, loss):
        if show_progress:
            log_utils.info("")
        else:
            log_utils.info(
                f"Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}"
            )


class SimpleTrainer(Trainer):

    def __init__(
        self,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=32,
        num_workers=1,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
            epochs,
            optimizer,
            scheduler,
            lr,
            T_max,
            batch_size,
            num_workers,
            pin_memory,
            pin_memory_device,
            persistent_workers,
            early_stopping_rounds,
            print_per_rounds,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )

    def train(
        self, model, X, y, collate_fn=None, show_progress=False, eps=1e-5
    ) -> Tuple[nn.Module, dict]:
        X, y = convert_data(X, y)
        return super().train(
            model, TensorDataset(X, y), collate_fn, show_progress, eps=eps
        )


class EvalTrainer(Trainer):

    def __init__(
        self,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=32,
        eval_batch_size=64,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
            epochs,
            optimizer,
            scheduler,
            lr,
            T_max,
            batch_size,
            num_workers,
            pin_memory,
            pin_memory_device,
            persistent_workers,
            early_stopping_rounds,
            print_per_rounds,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )
        self.eval_batch_size = eval_batch_size
        self.num_eval_workers = num_eval_workers


    def train(
        self,
        model,
        train_set: Dataset,
        val_set: Dataset,
        collate_fn=None,
        show_progress=False,
        eps=1e-5,
    ) -> Tuple[nn.Module, dict]:
        train_loader = self._build_train_loader(train_set, collate_fn)
        val_loader = self._build_val_loader(val_set, self.eval_batch_size, self.num_eval_workers, collate_fn)
        self._begin_train()
        cnt = 0
        best_model = None
        min_loss = float("inf")
        train_losses, val_losses = [], []
        if next(model.parameters()).device != self.device:
            model = model.to(self.device)
        optimizer, scheduler = self.get_optimizer_scheduler(model)
        is_tuple_params = isinstance(next(iter(train_loader)), (tuple, list))

        for epoch in range(1, self.epochs + 1):
            model.train()
            avg_loss = train_epoch(
                model,
                train_loader,
                optimizer,
                self.device,
                scheduler,
                epoch,
                self.epochs,
                show_progress,
                is_tuple_params,
            )
            val_loss = evaluate_epoch(
                model,
                val_loader,
                self.device,
                epoch,
                self.epochs,
                show_progress,
                is_tuple_params,
            )
            train_losses.append(avg_loss)
            val_losses.append(val_loss)
            self.try_print(
                self.print,
                show_progress,
                epoch,
                optimizer.param_groups[0]["lr"],
                avg_loss,
                val_loss=val_loss,
            )
            self.try_checkpoint(model, epoch)

            if min_loss - val_loss > eps:
                cnt = 0
                best_model = deepcopy(model)
                min_loss = val_loss
                continue

            # x次epoch的val_acc不提升或x次epoch的val_acc不变化
            if (
                epoch >= min(3, self.early_stopping_rounds)
                and cnt >= self.early_stopping_rounds
            ):
                log_utils.info(f"Early stopping at Epoch-{epoch}")
                break

            cnt += 1

        log_utils.info(f"Min loss: {min_loss:.4f}\n")
        return best_model, {"train_losses": train_losses, "val_losses": val_losses}

    def print(self, show_progress, epoch, lr, loss, val_loss):
        if show_progress:
            log_utils.info("")
        else:
            log_utils.info(
                f"Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}, val_loss: {val_loss:.4f}"
            )


class SimpleEvalTrainer(EvalTrainer):

    def __init__(
        self,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=32,
        eval_batch_size=64,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
            epochs,
            optimizer,
            scheduler,
            lr,
            T_max,
            batch_size,
            eval_batch_size,
            num_workers,
            num_eval_workers,
            pin_memory,
            pin_memory_device,
            persistent_workers,
            early_stopping_rounds,
            print_per_rounds,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )

    def train(
        self,
        model,
        X,
        y,
        val_data: Tuple,
        collate_fn=None,
        show_progress=False,
        eps=1e-5,
    ) -> Tuple[nn.Module, dict]:
        X, y = convert_data(X, y)
        X_val, y_val = convert_data(val_data[0], val_data[1])
        return super().train(
            model,
            TensorDataset(X, y),
            TensorDataset(X_val, y_val),
            collate_fn,
            show_progress,
            eps,
        )


class ClassTrainer(Trainer):

    def __init__(
        self,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=32,
        num_workers=1,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
            epochs,
            optimizer,
            scheduler,
            lr,
            T_max,
            batch_size,
            num_workers,
            pin_memory,
            pin_memory_device,
            persistent_workers,
            early_stopping_rounds,
            print_per_rounds,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )

    def train(
        self, model, train_set: Dataset, collate_fn=None, show_progress=False, eps=1e-5
    ):
        train_loader = self._build_train_loader(train_set, collate_fn)
        self._begin_train()
        best_model = None
        min_loss = float("inf")
        cnt, cnt2, best_acc, last_acc = 0, 0, 0.0, 0.0
        train_losses, train_accs = [], []
        if next(model.parameters()).device != self.device:
            model = model.to(self.device)
        optimizer, scheduler = self.get_optimizer_scheduler(model)
        is_tuple_params = isinstance(next(iter(train_loader)), (tuple, list))

        model.train()
        for epoch in range(1, self.epochs + 1):
            acc, avg_loss = train_epoch_acc(
                model,
                train_loader,
                optimizer,
                self.device,
                scheduler,
                epoch,
                self.epochs,
                show_progress,
                is_tuple_params,
            )
            train_accs.append(acc)
            train_losses.append(avg_loss)
            self.try_print(
                self.print,
                show_progress,
                epoch,
                optimizer.param_groups[0]["lr"],
                avg_loss,
                acc=acc,
            )
            self.try_checkpoint(model, epoch)

            if acc > best_acc or (acc == best_acc and min_loss - avg_loss > eps):
                cnt, cnt2 = 0, 0
                best_acc, best_model = acc, deepcopy(model)
                last_acc, min_loss = acc, min(min_loss, avg_loss)
                continue

            # x次epoch的val_acc不提升或x次epoch的val_acc不变化
            if (
                epoch >= min(5, self.early_stopping_rounds)
                and max(cnt, cnt2) >= self.early_stopping_rounds
            ):
                log_utils.info(f"Early stopping at Epoch-{epoch}")
                break

            if abs(last_acc - acc) < eps:  # val_acc不在变化
                cnt2 += 1
            else:
                cnt2 = 0

            cnt += 1
            last_acc = acc
            best_acc = max(best_acc, acc)
            min_loss = min(min_loss, avg_loss)

        log_utils.info(f"Best acc: {best_acc:.4f}, min loss: {min_loss:.4f}\n")
        return best_model, {"train_losses": train_losses, "train_accs": train_accs}

    def print(self, show_progress, epoch, lr, loss, acc):
        if show_progress:
            log_utils.info("")
        else:
            log_utils.info(
                f"Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_acc: {acc:.4f}, train_loss: {loss:.4f}"
            )


class SimpleClassTrainer(ClassTrainer):

    def __init__(
        self,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=32,
        num_workers=1,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
            epochs,
            optimizer,
            scheduler,
            lr,
            T_max,
            batch_size,
            num_workers,
            pin_memory,
            pin_memory_device,
            persistent_workers,
            early_stopping_rounds,
            print_per_rounds,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )

    def train(
        self, model, X, y, collate_fn=None, show_progress=False, eps=1e-5
    ) -> Tuple[nn.Module, dict]:
        X, y = convert_data(X, y)
        return super().train(
            model, TensorDataset(X, y), collate_fn, show_progress, eps=eps
        )


class EvalClassTrainer(EvalTrainer):

    def __init__(
        self,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=32,
        eval_batch_size=64,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
            epochs,
            optimizer,
            scheduler,
            lr,
            T_max,
            batch_size,
            eval_batch_size,
            num_workers,
            num_eval_workers,
            pin_memory,
            pin_memory_device,
            persistent_workers,
            early_stopping_rounds,
            print_per_rounds,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )

    def train(
        self,
        model,
        train_set: Dataset,
        val_set: Dataset,
        collate_fn=None,
        show_progress=False,
        eps=1e-5,
    ) -> Tuple[nn.Module, dict]:
        train_loader = self._build_train_loader(train_set, collate_fn)
        val_loader = self._build_val_loader(val_set, self.eval_batch_size, self.num_eval_workers, collate_fn)
        self._begin_train()
        best_model = None
        min_loss = float("inf")
        cnt, cnt2, best_acc, last_acc = 0, 0, 0.0, 0.0
        train_losses, train_accs, val_losses, val_accs = [], [], [], []
        if next(model.parameters()).device != self.device:
            model = model.to(self.device)
        optimizer, scheduler = self.get_optimizer_scheduler(model)
        is_tuple_params = isinstance(next(iter(train_loader)), (tuple, list))

        for epoch in range(1, self.epochs + 1):
            model.train()
            acc, avg_loss = train_epoch_acc(
                model,
                train_loader,
                optimizer,
                self.device,
                scheduler,
                epoch,
                self.epochs,
                show_progress,
                is_tuple_params,
            )
            val_loss, val_acc = acc_evaluate_epoch(
                model,
                val_loader,
                self.device,
                epoch,
                self.epochs,
                show_progress,
                is_tuple_params,
            )
            train_accs.append(acc)
            train_losses.append(avg_loss)
            val_accs.append(val_acc)
            val_losses.append(val_loss)
            self.try_print(
                self.print,
                show_progress,
                epoch,
                optimizer.param_groups[0]["lr"],
                avg_loss,
                acc=acc,
                val_loss=val_loss,
                val_acc=val_acc,
            )
            self.try_checkpoint(model, epoch)

            if val_acc > best_acc or (
                val_acc == best_acc and min_loss - val_loss > eps
            ):
                cnt, cnt2 = 0, 0
                best_acc, best_model = val_acc, deepcopy(model)
                last_acc, min_loss = val_acc, min(min_loss, val_loss)
                continue

            # x次epoch的val_acc不提升或x次epoch的val_acc不变化
            if (
                epoch >= min(5, self.early_stopping_rounds)
                and max(cnt, cnt2) >= self.early_stopping_rounds
            ):
                log_utils.info(f"Early stopping at Epoch-{epoch}")
                break

            if abs(last_acc - val_acc) < eps:  # val_acc不在变化
                cnt2 += 1
            else:
                cnt2 = 0

            cnt += 1
            last_acc = val_acc
            best_acc = max(best_acc, val_acc)
            min_loss = min(min_loss, val_loss)

        log_utils.info(f"Best acc: {best_acc:.4f}, min loss: {min_loss:.4f}\n")
        return best_model, {
            "train_losses": train_losses,
            "train_accs": train_accs,
            "val_losses": val_losses,
            "val_accs": val_accs,
        }

    def print(self, show_progress, epoch, lr, loss, acc, val_loss, val_acc):
        if show_progress:
            log_utils.info("")
        else:
            log_utils.info(
                f"Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_acc: {acc:.4f}, train_loss: {loss:.4f}, "
                f"val_acc: {val_acc:.4f}, val_loss: {val_loss:.4f}"
            )


class SimpleEvalClassTrainer(EvalClassTrainer):

    def __init__(
        self,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=32,
        eval_batch_size=64,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
            epochs,
            optimizer,
            scheduler,
            lr,
            T_max,
            batch_size,
            eval_batch_size,
            num_workers,
            num_eval_workers,
            pin_memory,
            pin_memory_device,
            persistent_workers,
            early_stopping_rounds,
            print_per_rounds,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )

    def train(
        self,
        model,
        X,
        y,
        val_data: Tuple,
        collate_fn=None,
        show_progress=False,
        eps=1e-5,
    ) -> Tuple[nn.Module, dict]:
        X, y = convert_data(X, y)
        X_val, y_val = convert_data(val_data[0], val_data[1])
        return super().train(
            model,
            TensorDataset(X, y),
            TensorDataset(X_val, y_val),
            collate_fn,
            show_progress,
            eps,
        )


class RegressTrainer(Trainer):

    def __init__(
        self,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=32,
        num_workers=1,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
            epochs,
            optimizer,
            scheduler,
            lr,
            T_max,
            batch_size,
            num_workers,
            pin_memory,
            pin_memory_device,
            persistent_workers,
            early_stopping_rounds,
            print_per_rounds,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )

    def train(
        self, model, train_set: Dataset, collate_fn=None, show_progress=False, eps=1e-5
    ):
        train_loader = self._build_train_loader(train_set, collate_fn)
        self._begin_train()
        best_model = model
        min_loss = float("inf")
        cnt, cnt2, best_r2, last_r2 = 0, 0, -1.0, -1.0
        train_losses, train_r2s = [], []
        if next(model.parameters()).device != self.device:
            model = model.to(self.device)
        optimizer, scheduler = self.get_optimizer_scheduler(model)
        is_tuple_params = isinstance(next(iter(train_loader)), (tuple, list))

        model.train()
        for epoch in range(1, self.epochs + 1):
            r2, avg_loss = train_epoch_r2(
                model,
                train_loader,
                optimizer,
                self.device,
                scheduler,
                epoch,
                self.epochs,
                show_progress,
                is_tuple_params,
            )
            train_r2s.append(r2)
            train_losses.append(avg_loss)
            self.try_print(
                self.print,
                show_progress,
                epoch,
                optimizer.param_groups[0]["lr"],
                avg_loss,
                r2=r2,
            )
            self.try_checkpoint(model, epoch)

            if r2 > best_r2 or (r2 == best_r2 and min_loss - avg_loss > eps):
                cnt, cnt2 = 0, 0
                best_r2, best_model = r2, deepcopy(model)
                last_r2, min_loss = r2, min(min_loss, avg_loss)
                continue

            # x次epoch的val_r2不提升或x次epoch的val_r2不变化
            if (
                epoch >= min(5, self.early_stopping_rounds)
                and max(cnt, cnt2) >= self.early_stopping_rounds
            ):
                log_utils.info(f"Early stopping at Epoch-{epoch}")
                break

            if abs(last_r2 - r2) < eps:  # val_r2不在变化
                cnt2 += 1
            else:
                cnt2 = 0

            cnt += 1
            last_r2 = r2
            best_r2 = max(best_r2, r2)
            min_loss = min(min_loss, avg_loss)

        log_utils.info(f"Best r2 score: {best_r2:.4f}, min loss: {min_loss:.4f}\n")
        return best_model, {"train_losses": train_losses, "train_r2s": train_r2s}

    def print(self, show_progress, epoch, lr, loss, r2):
        if show_progress:
            log_utils.info("")
        else:
            log_utils.info(
                f"Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}, train_r2: {r2:.4f}"
            )


class SimpleRegressTrainer(RegressTrainer):

    def __init__(
        self,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=32,
        num_workers=1,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
            epochs,
            optimizer,
            scheduler,
            lr,
            T_max,
            batch_size,
            num_workers,
            pin_memory,
            pin_memory_device,
            persistent_workers,
            early_stopping_rounds,
            print_per_rounds,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )

    def train(
        self, model, X, y, collate_fn=None, show_progress=False, eps=1e-5
    ) -> Tuple[nn.Module, dict]:
        X, y = convert_data_r2(X, y)
        return super().train(
            model, TensorDataset(X, y), collate_fn, show_progress, eps=eps
        )


class EvalRegressTrainer(Trainer):

    def __init__(
        self,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=32,
        eval_batch_size=64,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
            epochs,
            optimizer,
            scheduler,
            lr,
            T_max,
            batch_size,
            num_workers,
            pin_memory,
            pin_memory_device,
            persistent_workers,
            early_stopping_rounds,
            print_per_rounds,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )
        self.eval_batch_size = eval_batch_size
        self.num_eval_workers = num_eval_workers

    def train(
        self,
        model,
        train_set: Dataset,
        val_set: Dataset,
        collate_fn=None,
        show_progress=False,
        eps=1e-5,
    ) -> Tuple[nn.Module, dict]:
        train_loader = self._build_train_loader(train_set, collate_fn)
        val_loader = self._build_val_loader(val_set, self.eval_batch_size, self.num_eval_workers, collate_fn)
        self._begin_train()
        best_model = model
        min_loss = float("inf")
        cnt, cnt2, best_r2, last_r2 = 0, 0, -1.0, -1.0
        train_losses, train_r2s, val_losses, val_r2s = [], [], [], []
        if next(model.parameters()).device != self.device:
            model = model.to(self.device)
        optimizer, scheduler = self.get_optimizer_scheduler(model)
        is_tuple_params = isinstance(next(iter(train_loader)), (tuple, list))

        for epoch in range(1, self.epochs + 1):
            model.train()
            r2, avg_loss = train_epoch_r2(
                model,
                train_loader,
                optimizer,
                self.device,
                scheduler,
                epoch,
                self.epochs,
                show_progress,
                is_tuple_params,
            )
            val_loss, val_r2 = r2_evaluate_epoch(
                model,
                val_loader,
                self.device,
                epoch,
                self.epochs,
                show_progress,
                is_tuple_params,
            )
            train_r2s.append(r2)
            train_losses.append(avg_loss)
            val_r2s.append(val_r2)
            val_losses.append(val_loss)

            self.try_print(
                self.print,
                show_progress,
                epoch,
                optimizer.param_groups[0]["lr"],
                avg_loss,
                r2=r2,
                val_loss=val_loss,
                val_r2=val_r2,
            )
            self.try_checkpoint(model, epoch)

            if val_r2 > best_r2 or (val_r2 == best_r2 and min_loss - val_loss > eps):
                cnt, cnt2 = 0, 0
                best_r2, best_model = val_r2, deepcopy(model)
                last_r2, min_loss = val_r2, min(min_loss, val_loss)
                continue

            # x次epoch的val_r2不提升或x次epoch的val_r2不变化
            if (
                epoch >= min(5, self.early_stopping_rounds)
                and max(cnt, cnt2) >= self.early_stopping_rounds
            ):
                log_utils.info(f"Early stopping at Epoch-{epoch}")
                break

            if abs(last_r2 - val_r2) < eps:  # val_r2不在变化
                cnt2 += 1
            else:
                cnt2 = 0

            cnt += 1
            last_r2 = val_r2
            best_r2 = max(best_r2, val_r2)
            min_loss = min(min_loss, val_loss)

        log_utils.info(f"Best r2 score: {best_r2:.4f}, min loss: {min_loss:.4f}\n")
        return best_model, {
            "train_losses": train_losses,
            "train_r2s": train_r2s,
            "val_losses": val_losses,
            "val_r2s": val_r2s,
        }

    def print(self, show_progress, epoch, lr, loss, r2, val_loss, val_r2):
        if show_progress:
            log_utils.info("")
        else:
            log_utils.info(
                f"Epoch-{epoch}/{self.epochs}  lr: {lr:.6f}, train_loss: {loss:.4f}, train_r2: {r2:.4f}, "
                f"val_loss: {val_loss:.4f}, val_r2: {val_r2:.4f}"
            )


class SimpleEvalRegressTrainer(EvalRegressTrainer):

    def __init__(
        self,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=32,
        eval_batch_size=64,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,  # 早停，等10轮决策，评价指标不在变化，停止
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(
            epochs,
            optimizer,
            scheduler,
            lr,
            T_max,
            batch_size,
            eval_batch_size,
            num_workers,
            num_eval_workers,
            pin_memory,
            pin_memory_device,
            persistent_workers,
            early_stopping_rounds,
            print_per_rounds,
            checkpoint_per_rounds,
            checkpoint_name,
            device,
        )

    def train(
        self,
        model,
        X,
        y,
        val_data: Tuple,
        collate_fn=None,
        show_progress=False,
        eps=1e-5,
    ) -> Tuple[nn.Module, dict]:
        X, y = convert_data_r2(X, y)
        X_val, y_val = convert_data_r2(val_data[0], val_data[1])
        return super().train(
            model,
            TensorDataset(X, y),
            TensorDataset(X_val, y_val),
            collate_fn,
            show_progress,
            eps,
        )
