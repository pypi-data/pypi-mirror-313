import numpy as np
import torch
from torch import nn
from torch import optim
from pathlib import Path
from typing import Union, List, Tuple, Collection
from sklearn.model_selection import train_test_split
from torch.nn import functional as F
from torch.optim.lr_scheduler import LRScheduler
from torch.utils.data import DataLoader, Dataset, TensorDataset
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    r2_score,
)

from . import log_utils
from model_wrapper.utils import convert_to_tensor, convert_data, acc_predict, get_device
from .training import (
    evaluate,
    Trainer,
    SimpleTrainer,
    EvalTrainer,
    SimpleEvalTrainer,
    acc_evaluate,
    ClassTrainer,
    SimpleClassTrainer,
    EvalClassTrainer,
    SimpleEvalClassTrainer,
    r2_evaluate,
    RegressTrainer,
    SimpleRegressTrainer,
    EvalRegressTrainer,
    SimpleEvalRegressTrainer,
)

__all__ = [
    "ModelWrapper",
    "SimpleModelWrapper",
    "ClassModelWrapper",
    "SimpleClassModelWrapper",
    "SplitClassModelWrapper",
    "RegressModelWrapper",
    "SimpleRegressModelWrapper",
    "SplitRegressModelWrapper",
]


class ModelWrapper:
    """
    Examples
    --------
    >>> model_wrapper = ModelWrapper(model)
    >>> model_wrapper.train(train_set, val_set, collate_fn)
    >>> model_wrapper.logits(X_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        self.device = get_device(device)
        if isinstance(model_or_path, nn.Module):
            model_or_path = model_or_path.to(self.device)
            self.model, self.best_model = model_or_path, model_or_path
        elif isinstance(model_or_path, (str, Path)):
            self.model = torch.load(model_or_path, map_location=device)
            self.best_model = self.model

    def train(
        self,
        train_set: Dataset,
        val_set: Dataset = None,
        collate_fn=None,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=64,
        eval_batch_size=128,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        if val_set:
            trainer = EvalTrainer(
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
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, val_set, collate_fn, show_progress, eps
            )
        else:
            trainer = Trainer(
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
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, collate_fn, show_progress, eps
            )
        return histories

    def logits(self, X: Union[torch.Tensor, np.ndarray, List]) -> torch.Tensor:
        self.best_model.eval()
        with torch.no_grad():
            return self.best_model(self._convert_X_to_tensor(X))

    def evaluate(
        self, val_set: Dataset, batch_size=64, num_workers=0, collate_fn=None
    ) -> float:
        """return loss"""
        val_loader = DataLoader(
            dataset=val_set,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate_fn,
        )
        return evaluate(self.best_model, val_loader, self.device)

    def save(
        self,
        best_model_path: Union[str, Path] = "./best_model.pt",
        last_model_path: Union[str, Path] = "./last_model.pt",
        save_mode: str = "both",
    ):
        """
        :param best_model_path:
        :param last_model_path:
        :param save_mode: "both" or "best" or "last"
        :return:
        """
        assert save_mode in ("both", "best", "last")
        if save_mode == "both":
            torch.save(self.model, last_model_path)
            torch.save(self.best_model, best_model_path)
        elif save_mode == "best":
            torch.save(self.best_model, best_model_path)
        elif save_mode == "last":
            torch.save(self.model, last_model_path)

    def load(self, model_path: Union[str, Path] = "./best_model.pt"):
        self.model = torch.load(model_path, map_location=self.device)
        self.best_model = self.model

    @staticmethod
    def _convert_X_to_tensor(X: Union[torch.Tensor, np.ndarray, List]) -> torch.Tensor:
        if isinstance(X, (List, np.ndarray)):
            return convert_to_tensor(X, 2)
        return X


class SimpleModelWrapper(ModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = SimpleModelWrapper(model)
    >>> model_wrapper.train(X, y, collate_fn)
    >>> model_wrapper.logits(X_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List],
        y: Union[torch.Tensor, np.ndarray, List],
        val_data: Tuple[
            Union[torch.Tensor, np.ndarray, List], Union[torch.Tensor, np.ndarray, List]
        ] = None,
        collate_fn=None,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=64,
        eval_batch_size=128,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        if val_data:
            trainer = SimpleEvalTrainer(
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
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, X, y, val_data, collate_fn, show_progress, eps
            )
        else:
            trainer = SimpleTrainer(
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
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, X, y, collate_fn, show_progress, eps
            )

    def evaluate(
        self,
        X: Union[torch.Tensor, np.ndarray, List],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size=64,
        num_workers=0,
        collate_fn=None,
    ) -> float:
        """return loss"""
        X, y = convert_data(X, y)
        val_set = TensorDataset(X, y)
        return super().evaluate(val_set, batch_size, num_workers, collate_fn)


class ClassModelWrapper(ModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = ClassModelWrapper(model, classes=classes)
    >>> model_wrapper.train(train_set, val_set, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(test_set, collate_fn=collate_fn)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)
        self.classes = classes

    def train(
        self,
        train_set: Dataset,
        val_set: Dataset = None,
        collate_fn=None,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=64,
        eval_batch_size=128,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        if val_set:
            trainer = EvalClassTrainer(
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
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, val_set, collate_fn, show_progress, eps
            )
        else:
            trainer = ClassTrainer(
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
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, collate_fn, show_progress, eps
            )
        return histories

    def predict(
        self, X: Union[torch.Tensor, np.ndarray, List], threshold: int = 0.5
    ) -> np.ndarray:
        """
        :param X:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        logits = self.logits(X)
        return acc_predict(logits, threshold)

    def predict_classes(
        self, X: Union[torch.Tensor, np.ndarray, List], threshold: int = 0.5
    ) -> list:
        """
        :param X:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        pred = self.predict(X, threshold)
        return self._predict_classes(pred.ravel())

    def _predict_classes(self, pred: np.ndarray) -> np.ndarray:
        if self.classes:
            return [self.classes[i] for i in pred]
        else:
            log_utils.warn("Warning: classes not be specified")
            return pred

    def predict_proba(
        self, X: Union[torch.Tensor, np.ndarray, List], threshold: int = 0.5
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        :param X:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        logits = self.logits(X)
        return self._proba(logits, threshold)

    @staticmethod
    def _proba(
        logits: torch.Tensor, threshold: int = 0.5
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        :param logits:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        shape = logits.shape
        shape_len = len(shape)
        if (shape_len == 2 and shape[1] > 1) or shape_len > 2:
            # 多分类
            result = F.softmax(logits, dim=-1).max(-1)
            return result.indices.numpy(), result.values.numpy()
        else:
            # 二分类
            logits = logits.numpy()
            if shape_len == 2:
                logits = logits.ravel()
            return np.where(logits >= threshold, 1, 0).astype(np.int64), np.where(
                logits >= 0.5, logits, 1 - logits
            )

    def predict_classes_proba(
        self, X: Union[torch.Tensor, np.ndarray, List], threshold: int = 0.5
    ) -> Tuple[list, np.ndarray]:
        """
        :param X:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        indices, values = self.predict_proba(X)
        return self._predict_classes(indices.ravel()), values

    def evaluate(
        self,
        val_set: Dataset,
        batch_size=64,
        num_workers=0,
        collate_fn=None,
        threshold: int = 0.5,
    ) -> float:
        """
        :param val_set:
        :param threshold: 二分类且模型输出为一维概率时生效
        :return accuracy
        """
        val_loader = DataLoader(
            dataset=val_set,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate_fn,
        )
        _, acc = acc_evaluate(self.best_model, val_loader, self.device, threshold)
        return acc


class SimpleClassModelWrapper(ClassModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = SimpleClassModelWrapper(model, classes=classes)
    >>> model_wrapper.train(X, y val_data, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(X_test, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, classes, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_data: Tuple[
            Union[torch.Tensor, np.ndarray, List],
            Union[torch.LongTensor, np.ndarray, List],
        ] = None,
        collate_fn=None,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=64,
        eval_batch_size=128,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        if val_data:
            trainer = SimpleEvalClassTrainer(
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
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, X, y, val_data, collate_fn, show_progress, eps
            )
        else:
            trainer = SimpleClassTrainer(
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
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, X, y, collate_fn, show_progress, eps
            )
        return histories

    def evaluate(
        self,
        X: Union[torch.Tensor, np.ndarray, List],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size=64,
        num_workers=0,
        collate_fn=None,
        threshold: int = 0.5,
    ):
        """return accuracy"""
        X, y = convert_data(X, y)
        data_set = TensorDataset(X, y)
        return super().evaluate(
            data_set, batch_size, num_workers, collate_fn, threshold
        )


class SplitClassModelWrapper(SimpleClassModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = SplitClassModelWrapper(model, classes=classes)
    >>> model_wrapper.train(X, y val_data, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(X_test, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, classes, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_size=0.2,
        random_state=None,
        collate_fn=None,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=64,
        eval_batch_size=128,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=val_size, random_state=random_state
        )
        trainer = SimpleEvalClassTrainer(
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
            self.device,
        )
        self.best_model, histories = trainer.train(
            self.model,
            X_train,
            y_train,
            (X_test, y_test),
            collate_fn,
            show_progress,
            eps,
        )
        return histories


class RegressModelWrapper(ModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = RegressModelWrapper(model)
    >>> model_wrapper.train(train_set, val_set, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(test_set, collate_fn=collate_fn)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)

    def train(
        self,
        train_set: Dataset,
        val_set: Dataset = None,
        collate_fn=None,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=64,
        eval_batch_size=128,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        if val_set:
            trainer = EvalRegressTrainer(
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
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, val_set, collate_fn, show_progress, eps
            )
        else:
            trainer = RegressTrainer(
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
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, collate_fn, show_progress, eps
            )
        return histories

    def predict(self, X: Union[torch.Tensor, np.ndarray, List[float]]) -> np.ndarray:
        return self.logits(self._convert_X_to_tensor(X)).cpu().numpy()

    def mae(
        self,
        X: Union[torch.Tensor, np.ndarray, List[float]],
        y: Union[torch.Tensor, np.ndarray, list[float]],
    ) -> float:
        if isinstance(y, list):
            y = np.array(y)
        elif torch.is_tensor(y):
            y = y.numpy()

        pred = self.predict(X)
        return mean_absolute_error(y.ravel(), pred.ravel())

    def mse(
        self,
        X: Union[torch.Tensor, np.ndarray, List[float]],
        y: Union[torch.Tensor, np.ndarray, list[float]],
    ) -> float:
        if isinstance(y, list):
            y = np.array(y)
        elif torch.is_tensor(y):
            y = y.numpy()

        pred = self.predict(X)
        return mean_squared_error(y.ravel(), pred.ravel())

    def rmse(
        self,
        X: Union[torch.Tensor, np.ndarray, List[float]],
        y: Union[torch.Tensor, np.ndarray, list[float]],
    ) -> float:
        if isinstance(y, list):
            y = np.array(y)
        elif torch.is_tensor(y):
            y = y.numpy()

        pred = self.predict(X)
        return root_mean_squared_error(y.ravel(), pred.ravel())

    def evaluate(
        self, val_set: Dataset, batch_size=64, num_workers=0, collate_fn=None
    ) -> float:
        """return r2_score"""
        val_loader = DataLoader(
            dataset=val_set,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate_fn,
        )
        _, r2 = r2_evaluate(self.best_model, val_loader, self.device)
        return r2


class SimpleRegressModelWrapper(RegressModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = SimpleRegressModelWrapper(model)
    >>> model_wrapper.train(train_set, val_set, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(test_set, collate_fn=collate_fn)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List],
        y: Union[torch.Tensor, np.ndarray, List],
        val_data: Tuple[
            Union[torch.Tensor, np.ndarray, List], Union[torch.Tensor, np.ndarray, List]
        ] = None,
        collate_fn=None,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=64,
        eval_batch_size=128,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        if val_data:
            trainer = SimpleEvalRegressTrainer(
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
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, X, y, val_data, collate_fn, show_progress, eps
            )
        else:
            trainer = SimpleRegressTrainer(
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
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, X, y, collate_fn, show_progress, eps
            )
        return histories

    def evaluate(
        self,
        X: Union[torch.Tensor, np.ndarray, List],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size=64,
        num_workers=0,
        collate_fn=None,
    ) -> float:
        """return loss"""
        if isinstance(y, list):
            y = np.array(y)
        elif torch.is_tensor(y):
            y = y.numpy()
        pred = self.predict(X)
        return r2_score(y.ravel(), pred.ravel())


class SplitRegressModelWrapper(SimpleRegressModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = SplitClassModelWrapper(model, classes=classes)
    >>> model_wrapper.train(X, y val_data, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(X_test, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_size=0.2,
        random_state=None,
        collate_fn=None,
        epochs=100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr=0.001,
        T_max: int = 0,
        batch_size=64,
        eval_batch_size=128,
        num_workers=0,
        num_eval_workers=0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=val_size, random_state=random_state
        )
        val_data = (X_test, y_test)
        trainer = SimpleEvalRegressTrainer(
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
            self.device,
        )
        self.best_model, histories = trainer.train(
            self.model, X, y, val_data, collate_fn, show_progress, eps
        )
        return histories
