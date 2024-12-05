"""This script contains different model architectures

Functions
---------
init_weights
    initializes the weights of the linear layers in a model using the xavier initialization

Classes
---------
class_MLP_base
    Base class for the binary classification Multilayer Perceptron (MLP), provides methods for training, evaluation, and analysis of an MLP model for binary classification tasks.

class_PMLP_base
    Base class for the binary classification parametrized MLP (PMLP), provides methods for training, evaluation, and analysis of a PMLP model for binary classification tasks.

class_MLP_reg
    Class that sets the architecture for a Regularized MLP (including BN, Dropout etc.)

class_PMLP_reg
    Class that sets the architecture for a Regularized PMLP (including BN, Dropout etc.)

ResMLP
    Architecture for a deep (P)MLP using residual connections

self_attn_mlp
    MLP that utilizes self attention blocks to encode the input

class_CNN_Base
    Base class for the binary classification Convolutional Neural Network (CNN), provides methods for training, evaluation, and analysis of an MLP model for binary classification tasks.

FCN
    Architecture for a fully connected convolutional neural network (FCN)

ResNet
    Architecture for a deep fully connected convolutional neural network (FCN) utilizing residual connections

Autoencoder_test (OLD)
    autoencoder used for classification via the reconstruction loss

VAE (OLD)
    Variational autoencoder
"""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import torch
from tqdm.notebook import trange

# from dataset import *
# from model_eval import *
# from model_pipeline import colored_line

from .dataset import *
from .model_eval import *
from .model_pipeline import colored_line


class RunningAverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self, momentum=0.99, update_frequency=1):
        self.momentum = momentum ** (1 / update_frequency)
        self.reset()

    def reset(self):
        self.val = None
        self.avg = 0

    def update(self, val):
        if self.val is None:
            self.avg = val
        else:
            self.avg = self.avg * self.momentum + val * (1 - self.momentum)
        self.val = val


def init_weights(m, bias=False):
    """
    Initializes the models weights for all linear layers using the xavier initialization
                                   for all Convolutional Layers using kaiming initialization
    """
    if isinstance(m, torch.nn.Linear):
        torch.nn.init.xavier_uniform(m.weight)
        if bias:
            torch.nn.init.zeros_(m.bias)

    if isinstance(m, torch.nn.Conv1d):
        torch.nn.init.kaiming_normal_(m.weight, nonlinearity="relu")


# ===========================================================================================================================================================
# ===========================================================================================================================================================
# ===========================================================================================================================================================
# (Binary) Classification MLPs ==============================================================================================================================
# ===========================================================================================================================================================
# ===========================================================================================================================================================
# ===========================================================================================================================================================


class class_MLP_Base:
    """
    Simple binary classification Multilayer Perceptron (MLP) Base Class.

    This class provides methods for training, evaluation, and analysis of an MLP model for binary classification tasks.

    Methods:
        train_simple(X_train, y_train, X_validation, y_validation, epochs, scheduler=None, weight_decay=None, gradient_flow=False, lr=1e-3, batch_size=32, device="cpu", verbose=1, val_loss_update_freq=100, seed=42):
            Trains the MLP model using a specified dataset and training configurations.

        eval_simple(losses_training, losses_validation, X_validation, y_validation, threshold_pred=0.5, plot=("epochs", 100), device="cpu"):
            Evaluates the trained MLP model on validation data and calculates metrics such as accuracy, precision, recall, etc.

        model_out(x_sterile_test=None, y_sterile_test=None, x_ref_test=None, y_ref_test=None, mode="Both", device="cpu", random_state=42):
            Computes and returns model predictions for given test datasets in specified mode.

        integrated_gradients(x_data, y_data, baseline=None, steps=50, device="cpu"):
            Calculates Integrated Gradients to understand feature importance for the given input.

        eval_full(x_sterile_test=None, y_sterile_test=None, x_ref_test=None, y_ref_test=None, losses_training=None, losses_validation=None, X_validation=None, y_validation=None, grads=None, threshold_pred=0.5, device="cpu", plot=("all", {"epochs": 100, "int_grad_spec": 100})):
            Provides a comprehensive evaluation of the model including training loss, gradients, model outputs, and integrated gradients visualizations.

        eval_by_threshold(threshold_list, X_val, y_val, device="cpu", fraction=1.0):
            Evaluates model performance across a range of prediction thresholds and returns metrics for each threshold.

        saliency(x_data, device="cpu", show_plot=True, **plot_kwargs):
            Generates a saliency map to visualize the importance of input features for predictions.
    """

    def train_simple(
        self,
        X_train,
        y_train,
        X_validation,
        y_validation,
        epochs,
        scheduler=None,
        weight_decay=None,
        gradient_flow=False,
        lr=1e-3,
        batch_size=32,
        device="cpu",
        verbose=1,
        val_loss_update_freq=100,
        seed=42,
    ):
        """
        Trains the MLP model.

        Args:
            X_train (torch.Tensor): Training input data.
            y_train (torch.Tensor): Training target labels.
            X_validation (torch.Tensor): Validation input data.
            y_validation (torch.Tensor): Validation target labels.
            epochs (int): Number of training epochs.
            scheduler (dict, optional): Configuration for learning rate scheduler. Defaults to None.
            weight_decay (float, optional): Weight decay (L2 regularization). Defaults to None.
            gradient_flow (bool, optional): Whether to compute and return gradients. Defaults to False.
            lr (float, optional): Learning rate for optimization. Defaults to 1e-3.
            batch_size (int, optional): Size of batches for training. Defaults to 32.
            device (str, optional): Device to perform computations on ("cpu" or "cuda"). Defaults to "cpu".
            verbose (int, optional): Verbosity level of training progress. Defaults to 1.
            val_loss_update_freq (int, optional): Frequency of validation loss updates (in steps). Defaults to 100.
            seed (int, optional): Seed for reproducibility. Defaults to 42.

        Returns:
            tuple: Training losses, validation losses, and gradients (if `gradient_flow=True`).
        """

        assert (
            self.bins == X_train[0].shape[0]
        ), f"Model input dimension ({self.bins}) doesnt match data ({X_train[0].shape[0]})!"

        if weight_decay is not None:
            optim = torch.optim.Adam(self.parameters(), lr, weight_decay=weight_decay)
        else:
            optim = torch.optim.Adam(self.parameters(), lr)
        if scheduler is not None:
            sched = torch.optim.lr_scheduler.ReduceLROnPlateau(
                optim, "min", **scheduler
            )  # def: 'patience': 10, 'factor': 0.5

        loss_meter_tr = RunningAverageMeter()
        # loss_meter_val = RunningAverageMeter(update_frequency=val_loss_update_freq)

        train_data = Dataset(X_train, y_train, seed=seed)
        train_dl = DataLoader(train_data, batch_size=batch_size, device=device)
        val_data = Dataset(X_validation, y_validation, seed=seed)
        val_dl = DataLoader(val_data, batch_size=batch_size, device=device)
        losses = []
        validation_losses = []
        gradients = {"lin1.weight": [], "lin2.weight": [], "out.weight": []}
        with trange(epochs, unit="epochs") as iterable:
            for count in iterable:
                if count > 0:
                    train_data.shuffle()
                    train_dl = DataLoader(
                        train_data, batch_size=batch_size, device=device
                    )
                for count_batch, (x_b, y_b) in enumerate(train_dl):
                    optim.zero_grad()
                    p = self(x_b)
                    loss = torch.nn.functional.binary_cross_entropy(p, y_b)
                    # losses.append(loss.cpu().detach().numpy())
                    loss.backward()
                    if gradient_flow:
                        for n, p in self.named_parameters():
                            if (p.requires_grad) and ("bias" not in n):
                                avg_grad = p.grad.abs().mean()
                                gradients[n].append(avg_grad.cpu().detach().numpy())
                    optim.step()
                    loss_meter_tr.update(loss.cpu().detach().numpy())
                    losses.append(loss_meter_tr.avg)
                    if count_batch % val_loss_update_freq == 0:
                        x_b_val, y_b_val = iter(val_dl).__next__()
                        x_b_val = x_b_val.to(device)
                        y_b_val = y_b_val.to(device)
                        with torch.no_grad():
                            pred = self(x_b_val)
                        loss_val = torch.nn.functional.binary_cross_entropy(
                            pred, y_b_val
                        )
                        # loss_meter_val.update(loss_val.cpu().detach().numpy())
                        # validation_losses.append(loss_meter_val.avg)
                        validation_losses.append(loss_val.cpu().detach().numpy())
                        if scheduler is not None:
                            sched.step(
                                loss_val
                            )  # could be problematic that is is evaluated only every 100 batches
                        # validation_losses.append(loss_val.cpu().detach().numpy())
                        if verbose == 1:
                            iterable.set_description("Training")
                            iterable.set_postfix(
                                tr_loss=f"{float(losses[-1]):.4f}",
                                val_loss=f"{float(validation_losses[-1]):.4f}",
                            )

        if gradient_flow:
            return losses, validation_losses, pd.DataFrame(gradients)

        return losses, validation_losses

    def eval_simple(
        self,
        losses_training,
        losses_validation,
        X_validation,
        y_validation,
        threshold_pred=0.5,
        plot=("epochs", 100),
        device="cpu",
    ):
        self.eval()
        """
        Evaluates the performance of the trained model.

        Args:
            losses_training (list): Training losses recorded during training.
            losses_validation (list): Validation losses recorded during training.
            X_validation (torch.Tensor): Validation input data.
            y_validation (torch.Tensor): Validation target labels.
            threshold_pred (float, optional): Threshold for binary classification predictions. Defaults to 0.5.
            plot (tuple, optional): Tuple specifying plotting options, e.g., ("epochs", 100). Defaults to ("epochs", 100).
            device (str, optional): Device for computations ("cpu", "cuda" or "mps"). Defaults to "cpu".

        Returns:
            dict: Dictionary of evaluation metrics including accuracy, precision, recall, F1-score, etc.
        """

        val_data = Dataset(X_validation, y_validation, seed=self.random_state)
        val_dl = DataLoader(val_data, batch_size=len(val_data), device=device)
        x_val, y_val = iter(val_dl).__next__()
        y_val = y_val.cpu()
        with torch.no_grad():
            pred = self(x_val)
            pred = pred.cpu()
        sterile_pred = np.where(pred > threshold_pred, 1, 0)
        gt = y_val.detach().numpy()

        if plot is not False:
            if plot[0] == "epochs":
                r = int(len(losses_training) / len(losses_validation))
                e = int(len(losses_training) / plot[1])
                x_ax_val = []
                x_ax_epochs = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                    if i % e == 0:
                        x_ax_epochs.append(i)

                fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                if len(x_ax_val) == len(losses_validation):
                    ax.plot(
                        x_ax_val,
                        losses_validation,
                        linewidth=3,
                        label="validation loss",
                    )
                else:
                    ax.plot(
                        x_ax_val[:-1],
                        losses_validation,
                        linewidth=3,
                        label="validation loss",
                    )
                for c, epoch in enumerate(x_ax_epochs):
                    if c % 5 == 0:
                        ax.axvline(
                            epoch,
                            ymin=0,
                            ymax=1,
                            color="grey",
                            linestyle="--",
                            linewidth=0.5,
                        )

                ax.axvline(
                    x_ax_epochs[-1],
                    ymin=0,
                    ymax=1,
                    color="grey",
                    linestyle="--",
                    linewidth=0.5,
                    label="every fifth training epoch",
                )

                # ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

            if plot[0] == "grid":
                r = int(len(losses_training) / len(losses_validation))
                x_ax_val = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                fig, ax = plt.subplots(figsize=(12, 8))
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                ax.plot(
                    x_ax_val, losses_validation, linewidth=3, label="validation loss"
                )
                ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

        score_dict = {
            "accuracy": accuracy(gt, sterile_pred),
            "precision": precision(gt, sterile_pred),
            "recall": recall(gt, sterile_pred),
            "fall-out": fallout(gt, sterile_pred),
            "f1": f1(gt, sterile_pred),
            "threshold_roc": threshold_pred,
        }
        # accuracy(gt, sterile_pred), recall(gt, sterile_pred), precision(gt, sterile_pred), f1(gt, sterile_pred)
        return score_dict

    def model_out(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        mode="Both",
        device="cpu",
        random_state=42,
    ):
        """
        Computes model outputs for specified test datasets.

        Args:
            x_sterile_test (numpy.ndarray, optional): Test input data for "sterile" class. Defaults to None.
            y_sterile_test (numpy.ndarray, optional): Test target labels for "sterile" class. Defaults to None.
            x_ref_test (numpy.ndarray, optional): Test input data for reference class. Defaults to None.
            y_ref_test (numpy.ndarray, optional): Test target labels for reference class. Defaults to None.
            mode (str, optional): Specifies which outputs to compute: ("Both", "ref", "ster"). Defaults to "Both".
            device (str, optional): Device for computations ("cpu" or "cuda"). Defaults to "cpu".
            random_state (int, optional): Random seed for reproducibility. Defaults to 42.

        Returns:
            numpy.ndarray or tuple: Model outputs corresponding to the specified mode.
        """
        self.eval()

        if mode == "Both":
            data_s = Dataset(x_sterile_test, y_sterile_test, seed=self.random_state)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            data_r = Dataset(x_ref_test, y_ref_test, seed=self.random_state)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                out_s = self(x_s)
                out_r = self(x_r)

            return out_s.cpu().detach().numpy(), out_r.cpu().detach().numpy()

        if mode == "ref":
            data_r = Dataset(x_ref_test, y_ref_test, seed=self.random_state)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                out_r = self(x_r)

            return out_r.cpu().detach().numpy()

        if mode == "ster":
            data_s = Dataset(x_sterile_test, y_sterile_test, seed=self.random_state)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            with torch.no_grad():
                out_s = self(x_s)

            return out_s.cpu().detach().numpy()

    def integrated_gradients(
        self, x_data, y_data, baseline=None, steps=50, device="cpu"
    ):
        """
        Computes Integrated Gradients for feature attribution.

        Args:
            x_data (numpy.ndarray): Input data for which attributions are calculated.
            y_data (numpy.ndarray): Target label associated with the input.
            baseline (numpy.ndarray, optional): Baseline input for integration. Defaults to zeros of the same shape as `x_data`.
            steps (int, optional): Number of steps for Riemann approximation. Defaults to 50.
            device (str, optional): Device for computations ("cpu" or "cuda"). Defaults to "cpu".

        Returns:
            numpy.ndarray: Integrated gradients for the given input.
        """

        self.eval()
        if baseline is None:
            baseline = np.zeros_like(x_data)

        gradients = []

        y_arr = np.zeros(steps + 1) + y_data
        scaled_inputs = np.array(
            [
                baseline + (float(i) / steps) * (x_data - baseline)
                for i in range(steps + 1)
            ]
        )
        ds = Dataset(scaled_inputs, y_arr, 42)
        dl = DataLoader(ds, batch_size=1, device=device)

        for c, (scaled_input, y) in enumerate(dl):
            scaled_input.requires_grad_(True)
            output = self(scaled_input)
            loss = output
            loss.backward(retain_graph=True)
            gradients.append(scaled_input.grad.cpu().detach().clone())

        avg_gradients = torch.mean(torch.stack(gradients), dim=0)
        approx_int_grad = (
            torch.Tensor(x_data) - torch.Tensor(baseline)
        ) * avg_gradients

        return approx_int_grad.detach().numpy()

    def eval_full(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        losses_training=None,
        losses_validation=None,
        X_validation=None,
        y_validation=None,
        grads=None,
        threshold_pred=0.5,
        device="cpu",
        plot=("all", {"epochs": 100, "int_grad_spec": 100}),
    ):
        """
        Comprehensive evaluation of the model.

        Args:
            x_sterile_test (numpy.ndarray, optional): Test input data for "sterile" class. Defaults to None.
            y_sterile_test (numpy.ndarray, optional): Test target labels for "sterile" class. Defaults to None.
            x_ref_test (numpy.ndarray, optional): Test input data for reference class. Defaults to None.
            y_ref_test (numpy.ndarray, optional): Test target labels for reference class. Defaults to None.
            losses_training (list, optional): Training losses recorded during training. Defaults to None.
            losses_validation (list, optional): Validation losses recorded during training. Defaults to None.
            X_validation (torch.Tensor, optional): Validation input data. Defaults to None.
            y_validation (torch.Tensor, optional): Validation target labels. Defaults to None.
            grads (pandas.DataFrame, optional): Dataframe of gradients recorded during training. Defaults to None.
            threshold_pred (float, optional): Threshold for binary classification predictions. Defaults to 0.5.
            device (str, optional): Device for computations ("cpu" or "cuda"). Defaults to "cpu".
            plot (tuple, optional): Specifies evaluation plots. Defaults to ("all", {"epochs": 100, "int_grad_spec": 100}).

        Returns:
            None: Displays evaluation plots and metrics.
        """

        self.eval()
        score = self.eval_simple(
            losses_training,
            losses_validation,
            X_validation,
            y_validation,
            threshold_pred,
            plot=False,
            device=device,
        )
        out_s, out_r = self.model_out(
            x_sterile_test, y_sterile_test, x_ref_test, y_ref_test, device=device
        )
        int_grad_ster = self.integrated_gradients(
            x_sterile_test[plot[1]["int_grad_spec"]],
            y_sterile_test[plot[1]["int_grad_spec"]],
            device=device,
        )[0]
        int_grad_ref = self.integrated_gradients(
            x_ref_test[0], y_ref_test[0], device=device
        )[0]

        if plot[0] == "all":
            fig, (l_ax, g_ax, o_ax, i_g_ax) = plt.subplots(4, 1, figsize=(15, 30))

            # l_ax

            r = int(len(losses_training) / len(losses_validation))
            e = int(len(losses_training) / plot[1]["epochs"])
            x_ax_val = []
            x_ax_epochs = []
            for i in np.arange(len(losses_training)):
                if i % r == 0:
                    x_ax_val.append(i)
                if i % e == 0:
                    x_ax_epochs.append(i)

            l_ax.plot(
                np.arange(len(losses_training)),
                losses_training,
                label="training loss",
            )
            l_ax.set_yscale("log")
            l_ax.set_xlabel("training iterations")
            l_ax.set_ylabel("Loss value")
            l_ax.set_title("BCE Loss", weight="bold")
            l_ax.plot(x_ax_val, losses_validation, linewidth=3, label="validation loss")
            for c, epoch in enumerate(x_ax_epochs):
                if c % 5 == 0:
                    l_ax.axvline(
                        epoch,
                        ymin=0,
                        ymax=1,
                        color="grey",
                        linestyle="--",
                        linewidth=0.5,
                    )

            l_ax.axvline(
                x_ax_epochs[-1],
                ymin=0,
                ymax=1,
                color="grey",
                linestyle="--",
                linewidth=0.5,
                label="every fifth training epoch",
            )

            l_ax.legend()

            l_ax.table(
                cellText=[[k, v] for k, v in zip(score.keys(), score.values())],
                cellLoc="left",
                edges="open",
                bbox=[0.05, 0.05, 0.3, 0.3],
            )

            # g_ax
            g_ax.plot(list(grads.index.values), grads["lin1.weight"], label="lin1")
            g_ax.plot(list(grads.index.values), grads["lin2.weight"], label="lin2")
            g_ax.plot(list(grads.index.values), grads["out.weight"], label="out")
            g_ax.legend()
            g_ax.set_xlabel("training iterations")
            g_ax.set_ylabel("avg gradient")

            # o_ax
            ul = 1
            o_ax.hist(
                out_s,
                bins=100,
                range=(out_r.min(), ul),
                fill=True,
                color="r",
                alpha=0.3,
                label="Model Output w/ sterile",
            )
            o_ax.hist(
                out_r,
                bins=100,
                range=(out_r.min(), ul),
                fill=True,
                color="g",
                alpha=0.3,
                label="Reference",
            )
            o_ax.set_yscale("log")
            o_ax.set_xlabel("Model Output")
            o_ax.set_ylabel("Counts")
            o_ax.set_title("Histogram of Model Outputs", weight="bold")
            o_ax.legend()

            # i_g_ax
            i_g_ax.plot(
                int_grad_ster,
                marker="o",
                linestyle="-",
                color="b",
                markersize=8,
                linewidth=2,
                alpha=0.75,
                label="Sterile Spectrum",
            )
            i_g_ax.plot(
                int_grad_ref,
                marker="o",
                linestyle="-",
                color="g",
                markersize=8,
                linewidth=2,
                alpha=0.75,
                label="Reference Spectrum",
            )

            i_g_ax.set_title("Integrated Gradients Attributions", weight="bold")
            i_g_ax.set_xlabel("Energy Bin")
            i_g_ax.set_ylabel("Attribution Value")
            i_g_ax.grid(True, which="both", linestyle="--", linewidth=0.5)
            i_g_ax.axhline(0, color="grey", linewidth=0.8)

            i_g_ax.legend()

            fig.tight_layout()
            fig.show()

    def eval_by_threshold(
        self, threshold_list, X_val, y_val, device="cpu", fraction=1.0
    ):
        """
        Evaluates model performance for various classification thresholds.

        Args:
            threshold_list (list): List of thresholds to evaluate.
            X_val (torch.Tensor): Validation input data.
            y_val (torch.Tensor): Validation target labels.
            device (str, optional): Device for computations ("cpu" or "cuda"). Defaults to "cpu".
            fraction (float, optional): Fraction of data to use for evaluation. Defaults to 1.0.

        Returns:
            pandas.DataFrame: Dataframe containing evaluation metrics for each threshold.
        """

        dataset_size = int(X_val.shape[0] * fraction)
        idxs = np.random.choice(
            np.linspace(1, X_val.shape[0], X_val.shape[0], dtype=int),
            size=dataset_size,
            replace=False,
        )
        score_df_list = []

        with trange(len(threshold_list), unit="treshold") as iterable:
            for count in iterable:
                threshold = threshold_list[count]
                score = self.eval_simple(
                    threshold_pred=threshold,
                    X_validation=X_val[idxs],
                    y_validation=y_val[idxs],
                    plot=False,
                    losses_training=False,
                    losses_validation=False,
                    device=device,
                )
                score_df = pd.DataFrame(score, index=[count])
                score_df_list.append(score_df)

        return pd.concat(score_df_list)

    def saliency(
        self,
        x_data,
        device="cpu",
        show_plot=True,
        **plot_kwargs,
    ):
        """
        Generates saliency maps to visualize feature importance.

        Args:
            x_data (numpy.ndarray): Input data for saliency analysis.
            device (str, optional): Device for computations ("cpu" or "cuda"). Defaults to "cpu".
            show_plot (bool, optional): Whether to display the saliency plot. Defaults to True.
            **plot_kwargs: Additional keyword arguments for plot configuration.

        Returns:
            numpy.ndarray: Saliency map for the input data.
        """

        self.eval()
        sample = torch.FloatTensor(x_data.astype(np.float64)).to(device)
        inp = sample.unsqueeze(0)
        inp.requires_grad = True
        o = self(inp)
        o.backward()
        grads = inp.grad.data
        saliency = grads.abs().cpu().numpy()

        # plot
        if show_plot:
            x_vals = np.linspace(0, x_data.shape[0], x_data.shape[0])
            fig, ax = plt.subplots(**plot_kwargs)
            saliency_map = colored_line(
                x_vals, x_data, c=saliency.squeeze(), ax=ax, linewidth=8
            )
            fig.colorbar(saliency_map)
            ax.set_xlim(0, x_vals.max())
            ax.set_ylim(x_data.min() - 0.1, x_data.max() + 0.1)
            fig.show()

        return saliency


class class_PMLP_Base:
    """
    Simple binary classification Parametrized Multilayer Perceptron (PMLP) Base Class.

    This class provides methods for training, evaluation, and analysis of an MLP model for binary classification tasks.

    Methods:
        train_simple(X_train, y_train, m_train, s_train, X_validation, y_validation, m_validation, s_validation, epochs, scheduler=None, weight_decay=None, gradient_flow=False, lr=1e-3, batch_size=32, device="cpu", verbose=1, val_loss_update_freq=100, seed=42):
            Trains the MLP model using a specified dataset and training configurations.

        eval_simple(losses_training, losses_validation, X_validation, y_validation, m_validation, s_validation, threshold_pred=0.5, plot=("epochs", 100), device="cpu"):
            Evaluates the trained MLP model on validation data and calculates metrics such as accuracy, precision, recall, etc.

        model_out(x_sterile_test=None, y_sterile_test=None, x_ref_test=None, y_ref_test=None, mode="Both", device="cpu", random_state=42):
            Computes and returns model predictions for given test datasets in specified mode.

        integrated_gradients(x_data, y_data, baseline=None, steps=50, device="cpu"):
            Calculates Integrated Gradients to understand feature importance for the given input.

        eval_full(x_sterile_test=None, y_sterile_test=None, x_ref_test=None, y_ref_test=None, losses_training=None, losses_validation=None, X_validation=None, y_validation=None, grads=None, threshold_pred=0.5, device="cpu", plot=("all", {"epochs": 100, "int_grad_spec": 100})):
            Provides a comprehensive evaluation of the model including training loss, gradients, model outputs, and integrated gradients visualizations.

        eval_by_threshold(threshold_list, X_val, y_val, device="cpu", fraction=1.0):
            Evaluates model performance across a range of prediction thresholds and returns metrics for each threshold.

        saliency(x_data, device="cpu", show_plot=True, **plot_kwargs):
            Generates a saliency map to visualize the importance of input features for predictions.
    """

    def train_simple(
        self,
        X_train,
        y_train,
        m_train,
        s_train,
        X_validation,
        y_validation,
        m_validation,
        s_validation,
        epochs,
        scheduler=None,
        weight_decay=None,
        # gradient_flow=False,
        lr=1e-3,
        batch_size=32,
        device="cpu",
        verbose=1,
        val_loss_update_freq=100,
        seed=42,
    ):
        """
        Trains the PMLP model.

        Args:
            epochs (int): Number of training epochs.
            X_train (torch.Tensor): Training input data.
            y_train (torch.Tensor): Training target labels.
            m_train (torch.Tensor): Training mass parametrization values.
            s_train (torch.Tensor): Training mixing angle parametrization values.
            X_validation (torch.Tensor): Validation input data.
            y_validation (torch.Tensor): Validation target labels.
            m_validation (torch.Tensor): Validation mass parametrization values.
            s_validation (torch.Tensor): Validation mixing angle parametrization values.
            gradient_flow (bool, optional): Whether to compute and return gradients. Defaults to False.
            lr (float, optional): Learning rate for optimization. Defaults to 1e-3.
            batch_size (int, optional): Size of batches for training. Defaults to 32.
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            tuple: Tuple containing training losses, validation losses, and gradients if gradient_flow=True.
        """

        assert (
            self.bins == X_train[0].shape[0]
        ), f"Model input dimension ({self.bins}) doesnt match data ({X_train[0].shape[0]})!"

        if weight_decay is not None:
            optim = torch.optim.Adam(self.parameters(), lr, weight_decay=weight_decay)
        else:
            optim = torch.optim.Adam(self.parameters(), lr)
        if scheduler is not None:
            sched = torch.optim.lr_scheduler.ReduceLROnPlateau(
                optim, "min", **scheduler
            )  # def: 'patience': 10, 'factor': 0.5

        # loss_meter_tr = RunningAverageMeter()

        train_data = Dataset_Parametrized(
            X_train,
            y_train,
            m_train,
            s_train,
            seed=seed,
        )
        train_dl = DataLoader_Parametrized(
            train_data, batch_size=batch_size, device=device
        )
        val_data = Dataset_Parametrized(
            X_validation,
            y_validation,
            m_validation,
            s_validation,
            seed=seed,
        )
        val_dl = DataLoader_Parametrized(val_data, batch_size=batch_size, device=device)
        losses = []
        validation_losses = []
        # gradients = {"lin1.weight": [], "lin2.weight": [], "out.weight": []}
        with trange(epochs, unit="epochs") as iterable:
            for count in iterable:
                if count > 0:
                    train_data.shuffle()
                    train_dl = DataLoader_Parametrized(
                        train_data, batch_size=batch_size, device=device
                    )
                for count_batch, (x_b, y_b, m_b, s_b) in enumerate(train_dl):
                    optim.zero_grad()
                    p = self(x_b, m_b, s_b)
                    loss = torch.nn.functional.binary_cross_entropy(p, y_b)
                    losses.append(loss.cpu().detach().numpy())
                    loss.backward()
                    # if gradient_flow:
                    #     for n, p in self.named_parameters():
                    #         if (p.requires_grad) and ("bias" not in n):
                    #             avg_grad = p.grad.abs().mean()
                    #             gradients[n].append(avg_grad.cpu().detach().numpy())
                    optim.step()
                    # loss_meter_tr.update(loss.cpu().detach().numpy())
                    # losses.append(loss_meter_tr.avg)
                    losses.append(loss.cpu().detach().numpy())
                    if count_batch % val_loss_update_freq == 0:
                        x_b_val, y_b_val, m_b_val, s_b_val = iter(val_dl).__next__()
                        x_b_val = x_b_val.to(device)
                        y_b_val = y_b_val.to(device)
                        m_b_val = m_b_val.to(device)
                        s_b_val = s_b_val.to(device)
                        with torch.no_grad():
                            pred = self(
                                x_b_val, m_b_val, s_b_val
                            )  # reshape not really necessary anymore
                        loss_val = torch.nn.functional.binary_cross_entropy(
                            pred, y_b_val
                        )
                        if scheduler is not None:
                            sched.step(
                                loss_val
                            )  # could be problematic that is is evaluated only every 100 batches
                        validation_losses.append(loss_val.cpu().detach().numpy())
                        if verbose == 1:
                            iterable.set_description("Training")
                            iterable.set_postfix(
                                tr_loss=f"{float(losses[-1]):.4f}",
                                val_loss=f"{float(validation_losses[-1]):.4f}",
                            )

        # if gradient_flow:
        #     return losses, validation_losses, pd.DataFrame(gradients)

        return losses, validation_losses

    def eval_simple(
        self,
        losses_training,
        losses_validation,
        X_validation,
        y_validation,
        m_validation,
        s_validation,
        threshold_pred=0.5,
        plot=("epochs", 100),
        device="cpu",
    ):
        self.eval()
        """
        Evaluates the performance of the trained model.

        Args:
            losses_training (list): Training losses.
            losses_validation (list): Validation losses.
            X_validation (torch.Tensor): Validation input data.
            y_validation (torch.Tensor): Validation target labels.
            m_validation (torch.Tensor): Validation mass parametrization values.
            s_validation (torch.Tensor): Validation mixing angle parametrization values.
            Nsamples (int, optional): Number of samples. Defaults to 1000.
            threshold_pred (float, optional): Prediction threshold. Defaults to 0.5.
            plot (tuple, optional): In which mode to plot the loss curve. Defaults to True.
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            dict: Dictionary containing evaluation metrics.
        """

        val_data = Dataset_Parametrized(
            X_validation,
            y_validation,
            m_validation,
            s_validation,
            seed=self.random_state,
        )
        val_dl = DataLoader_Parametrized(
            val_data, batch_size=len(val_data), device=device
        )
        x_val, y_val, m_val, s_val = iter(val_dl).__next__()
        y_val = y_val.cpu()
        with torch.no_grad():
            pred = self(x_val, m_val, s_val)
            pred = pred.cpu()
        sterile_pred = np.where(pred > threshold_pred, 1, 0)
        gt = y_val.detach().numpy()

        if plot is not False:
            if plot[0] == "epochs":
                r = int(len(losses_training) / len(losses_validation))
                e = int(len(losses_training) / plot[1])
                x_ax_val = []
                x_ax_epochs = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                    if i % e == 0:
                        x_ax_epochs.append(i)

                fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                if len(x_ax_val) == len(losses_validation):
                    ax.plot(
                        x_ax_val,
                        losses_validation,
                        linewidth=3,
                        label="validation loss",
                    )
                else:
                    ax.plot(
                        x_ax_val[:-1],
                        losses_validation,
                        linewidth=3,
                        label="validation loss",
                    )
                for c, epoch in enumerate(x_ax_epochs):
                    if c % 5 == 0:
                        ax.axvline(
                            epoch,
                            ymin=0,
                            ymax=1,
                            color="grey",
                            linestyle="--",
                            linewidth=0.5,
                        )

                ax.axvline(
                    x_ax_epochs[-1],
                    ymin=0,
                    ymax=1,
                    color="grey",
                    linestyle="--",
                    linewidth=0.5,
                    label="every fifth training epoch",
                )

                # ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

            if plot[0] == "grid":
                r = int(len(losses_training) / len(losses_validation))
                x_ax_val = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                fig, ax = plt.subplots(figsize=(12, 8))
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                ax.plot(
                    x_ax_val, losses_validation, linewidth=3, label="validation loss"
                )
                ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

        score_dict = {
            "accuracy": accuracy(gt, sterile_pred),
            "precision": precision(gt, sterile_pred),
            "recall": recall(gt, sterile_pred),
            "fall-out": fallout(gt, sterile_pred),
            "f1": f1(gt, sterile_pred),
            "threshold_roc": threshold_pred,
        }
        # accuracy(gt, sterile_pred), recall(gt, sterile_pred), precision(gt, sterile_pred), f1(gt, sterile_pred)
        return score_dict

    def model_out(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        m_sterile_test=None,
        s_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        m_ref_test=None,
        s_ref_test=None,
        mode="Both",
        device="cpu",
        random_state=42,
    ):
        self.eval()
        """
        Computes the model output for given test data.

        Args:
            x_sterile_test (numpy.ndarray, optional): Test input data for sterile class. Defaults to None.
            y_sterile_test (numpy.ndarray, optional): Test target labels for sterile class. Defaults to None.
            m_sterile_test (numpy.ndarray, optional): Additional parameters for sterile test data (sterile mass). Defaults to None.
            s_sterile_test (numpy.ndarray, optional): Additional parameters for sterile test data (mixing angle). Defaults to None.
            x_ref_test (numpy.ndarray, optional): Test input data for reference class. Defaults to None.
            y_ref_test (numpy.ndarray, optional): Test target labels for reference class. Defaults to None.
            m_ref_test (numpy.ndarray, optional): Additional parameters for reference test data (sterile mass). Defaults to None.
            s_ref_test (numpy.ndarray, optional): Additional parameters for reference test data (mixing angle). Defaults to None.
            mode (str, optional): Kind of spectra for which the output is calculated, possible modes: ("Both", "ref", or "ster"). Defaults to "Both".
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            numpy.ndarray: Model outputs for the specified mode.
        """

        if mode == "Both":
            data_s = Dataset_Parametrized(
                x_sterile_test,
                y_sterile_test,
                m_sterile_test,
                s_sterile_test,
                seed=self.random_state,
            )
            x_s, y_s, m_s, s_s = data_s[:]
            x_s, y_s, m_s, s_s = (
                torch.FloatTensor(x_s.astype(np.float64)),
                torch.FloatTensor(y_s.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(m_s.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(s_s.astype(np.float64)).unsqueeze(-1),
            )
            x_s, y_s, m_s, s_s = (
                x_s.to(device),
                y_s.to(device),
                m_s.to(device),
                s_s.to(device),
            )

            data_r = Dataset_Parametrized(
                x_ref_test,
                y_ref_test,
                m_ref_test,
                s_ref_test,
                self.random_state,
            )
            x_r, y_r, m_r, s_r = data_r[:]
            x_r, y_r, m_r, s_r = (
                torch.FloatTensor(x_r.astype(np.float64)),
                torch.FloatTensor(y_r.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(m_r.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(s_r.astype(np.float64)).unsqueeze(-1),
            )
            x_r, y_r, m_r, s_r = (
                x_r.to(device),
                y_r.to(device),
                m_r.to(device),
                s_r.to(device),
            )

            with torch.no_grad():
                out_s = self(x_s, m_s, s_s)
                out_r = self(x_r, m_r, s_r)

            return out_s.cpu().detach().numpy(), out_r.cpu().detach().numpy()

        if mode == "ref":
            data_r = Dataset_Parametrized(
                x_ref_test,
                y_ref_test,
                m_ref_test,
                s_ref_test,
                seed=self.random_state,
            )
            x_r, y_r, m_r, s_r = data_r[:]
            x_r, y_r, m_r, s_r = (
                torch.FloatTensor(x_r.astype(np.float64)),
                torch.FloatTensor(y_r.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(m_r.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(s_r.astype(np.float64)).unsqueeze(-1),
            )
            x_r, y_r, m_r, s_r = (
                x_r.to(device),
                y_r.to(device),
                m_r.to(device),
                s_r.to(device),
            )

            with torch.no_grad():
                out_r = self(x_r, m_r, s_r)

            return out_r.cpu().detach().numpy()

        if mode == "ster":
            data_s = Dataset_Parametrized(
                x_sterile_test,
                y_sterile_test,
                m_sterile_test,
                s_sterile_test,
                seed=self.random_state,
            )
            x_s, y_s, m_s, s_s = data_s[:]
            x_s, y_s, m_s, s_s = (
                torch.FloatTensor(x_s.astype(np.float64)),
                torch.FloatTensor(y_s.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(m_s.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(s_s.astype(np.float64)).unsqueeze(-1),
            )
            x_s, y_s, m_s, s_s = (
                x_s.to(device),
                y_s.to(device),
                m_s.to(device),
                s_s.to(device),
            )

            with torch.no_grad():
                out_s = self(x_s, m_s, s_s)

            return out_s.cpu().detach().numpy()

    def integrated_gradients(
        self, x_data, y_data, m_data, s_data, baseline=None, steps=50, device="cpu"
    ):
        self.eval()
        if baseline is None:
            baseline = np.zeros_like(x_data)

        gradients = []

        y_arr = np.zeros(steps + 1) + y_data
        m_data = np.zeros(steps + 1) + m_data
        s_data = np.zeros(steps + 1) + s_data

        scaled_inputs = np.array(
            [
                baseline + (float(i) / steps) * (x_data - baseline)
                for i in range(steps + 1)
            ]
        )
        ds = Dataset_Parametrized(scaled_inputs, y_arr, m_data, s_data, 42)
        dl = DataLoader_Parametrized(ds, batch_size=1, device=device)

        for c, (scaled_input, y, m, s) in enumerate(dl):
            scaled_input.requires_grad_(True)
            output = self(scaled_input, m, s)
            loss = output
            loss.backward(retain_graph=True)
            gradients.append(scaled_input.grad.cpu().detach().clone())

        avg_gradients = torch.mean(torch.stack(gradients), dim=0)
        approx_int_grad = (
            torch.Tensor(x_data) - torch.Tensor(baseline)
        ) * avg_gradients

        return approx_int_grad.detach().numpy()

    def eval_full(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        m_sterile_test=None,
        s_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        m_ref_test=None,
        s_ref_test=None,
        losses_training=None,
        losses_validation=None,
        X_validation=None,
        y_validation=None,
        m_validation=None,
        s_validation=None,
        grads=None,
        threshold_pred=0.5,
        device="cpu",
        plot=("all", {"epochs": 100, "int_grad_spec": 100}),
    ):
        self.eval()
        score = self.eval_simple(
            losses_training,
            losses_validation,
            X_validation,
            y_validation,
            m_validation,
            s_validation,
            threshold_pred,
            plot=False,
            device=device,
        )
        out_s, out_r = self.model_out(
            x_sterile_test,
            y_sterile_test,
            m_sterile_test,
            s_sterile_test,
            x_ref_test,
            y_ref_test,
            m_ref_test,
            s_ref_test,
            device=device,
        )
        int_grad_ster = self.integrated_gradients(
            x_sterile_test[plot[1]["int_grad_spec"]],
            y_sterile_test[plot[1]["int_grad_spec"]],
            m_sterile_test[plot[1]["int_grad_spec"]],
            s_sterile_test[plot[1]["int_grad_spec"]],
            device=device,
        )[0]
        int_grad_ref = self.integrated_gradients(
            x_ref_test[0], y_ref_test[0], m_ref_test[0], s_ref_test[0], device=device
        )[0]

        if plot[0] == "all":
            fig, (l_ax, g_ax, o_ax, i_g_ax) = plt.subplots(4, 1, figsize=(15, 30))

            # l_ax

            r = int(len(losses_training) / len(losses_validation))
            e = int(len(losses_training) / plot[1]["epochs"])
            x_ax_val = []
            x_ax_epochs = []
            for i in np.arange(len(losses_training)):
                if i % r == 0:
                    x_ax_val.append(i)
                if i % e == 0:
                    x_ax_epochs.append(i)

            l_ax.plot(
                np.arange(len(losses_training)),
                losses_training,
                label="training loss",
            )
            l_ax.set_yscale("log")
            l_ax.set_xlabel("training iterations")
            l_ax.set_ylabel("Loss value")
            l_ax.set_title("BCE Loss", weight="bold")
            l_ax.plot(x_ax_val, losses_validation, linewidth=3, label="validation loss")
            for c, epoch in enumerate(x_ax_epochs):
                if c % 5 == 0:
                    l_ax.axvline(
                        epoch,
                        ymin=0,
                        ymax=1,
                        color="grey",
                        linestyle="--",
                        linewidth=0.5,
                    )

            l_ax.axvline(
                x_ax_epochs[-1],
                ymin=0,
                ymax=1,
                color="grey",
                linestyle="--",
                linewidth=0.5,
                label="every fifth training epoch",
            )

            l_ax.legend()

            l_ax.table(
                cellText=[[k, v] for k, v in zip(score.keys(), score.values())],
                cellLoc="left",
                edges="open",
                bbox=[0.05, 0.05, 0.3, 0.3],
            )

            # g_ax
            g_ax.plot(list(grads.index.values), grads["lin1.weight"], label="lin1")
            g_ax.plot(list(grads.index.values), grads["lin2.weight"], label="lin2")
            g_ax.plot(list(grads.index.values), grads["out.weight"], label="out")
            g_ax.legend()
            g_ax.set_xlabel("training iterations")
            g_ax.set_ylabel("avg gradient")

            # o_ax
            ul = 1
            o_ax.hist(
                out_s,
                bins=100,
                range=(out_r.min(), ul),
                fill=True,
                color="r",
                alpha=0.3,
                label="Model Output w/ sterile",
            )
            o_ax.hist(
                out_r,
                bins=100,
                range=(out_r.min(), ul),
                fill=True,
                color="g",
                alpha=0.3,
                label="Reference",
            )
            o_ax.set_yscale("log")
            o_ax.set_xlabel("Model Output")
            o_ax.set_ylabel("Counts")
            o_ax.set_title("Histogram of Model Outputs", weight="bold")
            o_ax.legend()

            # i_g_ax
            i_g_ax.plot(
                int_grad_ster,
                marker="o",
                linestyle="-",
                color="b",
                markersize=8,
                linewidth=2,
                alpha=0.75,
                label="Sterile Spectrum",
            )
            i_g_ax.plot(
                int_grad_ref,
                marker="o",
                linestyle="-",
                color="g",
                markersize=8,
                linewidth=2,
                alpha=0.75,
                label="Reference Spectrum",
            )

            i_g_ax.set_title("Integrated Gradients Attributions", weight="bold")
            i_g_ax.set_xlabel("Energy Bin")
            i_g_ax.set_ylabel("Attribution Value")
            i_g_ax.grid(True, which="both", linestyle="--", linewidth=0.5)
            i_g_ax.axhline(0, color="grey", linewidth=0.8)

            i_g_ax.legend()

            fig.tight_layout()
            fig.show()

    def saliency(
        self,
        x_data,
        m_data,
        s_data,
        device="cpu",
        show_plot=True,
        **plot_kwargs,
    ):
        """outputs saliency map for input beta spectrum and label"""
        self.eval()
        sample = torch.FloatTensor(x_data.astype(np.float64)).to(device)
        m_data = np.expand_dims(m_data, 0)
        s_data = np.expand_dims(s_data, 0)
        m_sample = torch.FloatTensor(m_data.astype(np.float64)).unsqueeze(-1).to(device)
        s_sample = torch.FloatTensor(s_data.astype(np.float64)).unsqueeze(-1).to(device)
        inp = sample.unsqueeze(0)
        inp.requires_grad = True
        o = self(inp, m_sample, s_sample)
        o.backward()
        grads = inp.grad.data
        saliency = grads.abs().cpu().numpy()

        # plot
        if show_plot:
            x_vals = np.linspace(0, x_data.shape[0], x_data.shape[0])
            fig, ax = plt.subplots(**plot_kwargs)
            saliency_map = colored_line(
                x_vals, x_data, c=saliency.squeeze(), ax=ax, linewidth=8
            )
            fig.colorbar(saliency_map)
            ax.set_xlim(0, x_vals.max())
            ax.set_ylim(x_data.min() - 0.1, x_data.max() + 0.1)
            fig.show()

        return saliency


# ==============================================================================
# ==============================================================================
# Example subclass for a MLP with a certain architecture
# ==============================================================================
# ==============================================================================


class MLPBlock(torch.nn.Module):
    def __init__(
        self,
        batch_size,
        dropout,
        batch_norm,
        dims,
        incl_ReLU=True,
        parametrized=False,
        num_params=0,
    ):
        super(MLPBlock, self).__init__()
        self.parametrized = parametrized
        self.batch_size = batch_size
        self.batch_norm = batch_norm
        self.dropout_prob = dropout
        self.incl_ReLU = incl_ReLU
        self.dims = dims
        if parametrized:
            self.lin = torch.nn.Linear(dims[0] + num_params, dims[1] + num_params)
        else:
            self.lin = torch.nn.Linear(dims[0], dims[1])
        if self.batch_norm:
            self.bn = torch.nn.BatchNorm1d(dims[1])
        if self.dropout_prob is not None:
            self.do = torch.nn.Dropout(self.dropout_prob)
        if incl_ReLU:
            self.relu = torch.nn.ReLU()

    def forward(self, x, *params):
        if self.parametrized:
            i = torch.cat((x, *params), 1)
        else:
            i = x

        out = self.lin(i)

        if self.batch_norm:
            out = self.bn(out)
        if self.dropout_prob is not None:
            out = self.do(out)
        if self.incl_ReLU:
            out = self.relu(out)
        return out


class ResMLPBlock(torch.nn.Module):
    def __init__(self, batch_size, parametrized=False, num_params=0, **layer_kwargs):
        super(ResMLPBlock, self).__init__()
        self.parametrized = parametrized
        self.batch_size = batch_size
        self.mlp_blocks = torch.nn.ModuleList(
            [
                MLPBlock(
                    batch_size=self.batch_size,
                    parametrized=self.parametrized,
                    num_params=num_params,
                    **layer_kwargs[str(i)],
                )
                for i in range(len(layer_kwargs) - 1)
            ]
        )
        self.mlp_blocks.append(
            MLPBlock(
                batch_size=self.batch_size,
                incl_ReLU=False,
                parametrized=self.parametrized,
                num_params=num_params,
                **layer_kwargs[str(len(layer_kwargs) - 1)],
            )
        )
        self.relu = torch.nn.ReLU()

    def forward(self, x, *params):
        if self.parametrized:
            i = torch.cat((x, *params), 1)
        else:
            i = x

        inp = i

        for block in self.mlp_blocks:
            i = block(i)

        return self.relu(i + inp)


class ResMLP(
    torch.nn.Module, class_MLP_Base
):  # TODO: Eanble flexible picking of class_MLP base and class_PMLP base if parametrized, else training wont work
    """Initialization with the following dictionary for 3 blocks with each three layers
    dropouts = [0.5, 0.5, 0.5]
    block0 = {
        "0": {"dims": [186, 128], "dropout": dropouts[0], "batch_norm": True,},
        "1": {"dims": [128, 128], "dropout": dropouts[1], "batch_norm": True,},
        "2": {"dims": [128, 186], "dropout": dropouts[2], "batch_norm": True,}
    }
    block1 = {
        "0": {"dims": [186, 128], "dropout": dropouts[0], "batch_norm": True,},
        "1": {"dims": [128, 128], "dropout": dropouts[1], "batch_norm": True,},
        "2": {"dims": [128, 186], "dropout": dropouts[2], "batch_norm": True,}
    }

    block2 = {
        "0": {"dims": [186, 128], "dropout": dropouts[0], "batch_norm": True,},
        "1": {"dims": [128, 128], "dropout": dropouts[1], "batch_norm": True,},
        "2": {"dims": [128, 186], "dropout": dropouts[2], "batch_norm": True,}
    }
    resmlp_dict = {"0": block0, "1": block1, "2": block2}
    """

    def __init__(
        self,
        bins,
        batch_size=30000,
        lr=1e-3,
        random_state=42,
        parametrized=False,
        num_params=0,
        **resmlp_kwargs,
    ):
        super(ResMLP, self).__init__()

        self.bins = bins
        self.batch_size = batch_size
        self.learning_rate = lr
        self.resmlp_kwargs = resmlp_kwargs
        self.random_state = random_state
        self.parametrized = parametrized
        self.num_params = num_params

        self.resmlp_blocks = torch.nn.ModuleList(
            [
                ResMLPBlock(
                    self.batch_size,
                    self.parametrized,
                    self.num_params,
                    **self.resmlp_kwargs[str(i)],
                )
                for i in range(len(self.resmlp_kwargs))
            ]
        )

        self.sigmoid = torch.nn.Sigmoid()

        if self.parametrized:
            self.ff = torch.nn.Linear(
                self.resmlp_kwargs[str(len(self.resmlp_kwargs) - 1)][
                    str(len(self.resmlp_kwargs[str(len(self.resmlp_kwargs) - 1)]) - 1)
                ]["dims"][1]
                + self.num_params,
                1,
            )
        else:
            self.ff = torch.nn.Linear(
                self.resmlp_kwargs[str(len(self.resmlp_kwargs) - 1)][
                    str(len(self.resmlp_kwargs[str(len(self.resmlp_kwargs) - 1)]) - 1)
                ]["dims"][1],
                1,
            )

    def forward(self, x, *params):
        if self.parametrized:
            i = torch.cat((x, *params), 1)
        else:
            i = x

        for block in self.resmlp_blocks:
            i = block(i)
        i = self.ff(i)
        i = self.sigmoid(i)
        return i


class class_MLP_reg(torch.nn.Module, class_MLP_Base):
    def __init__(
        self,
        bins,
        hidden_dims=[256, 256],
        batch_size=30000,
        learning_rate=1e-3,
        scheduler=None,
        dropout=[None, None],
        weight_decay=1e-6,
        random_state=42,
    ):
        super(class_MLP_reg, self).__init__()
        self.bins = bins
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.dropout = dropout
        self.weight_decay = weight_decay
        self.random_state = random_state
        self.hidden_dims = hidden_dims
        self.scheduler = scheduler

        layers = []
        dims = [self.bins] + self.hidden_dims + [1]

        for i in range(len(dims) - 1):
            layers.append(torch.nn.Linear(dims[i], dims[i + 1]))
            if i < len(dims) - 2:
                layers.append(torch.nn.BatchNorm1d(dims[i + 1]))
                layers.append(torch.nn.ReLU())
                if dropout[i] is not None:
                    layers.append(torch.nn.Dropout(dropout[i]))

        layers.append(torch.nn.Sigmoid())

        self.layers = torch.nn.Sequential(*layers)

    def forward(self, x):
        out = self.layers(x)
        return out

    # def __getstate__(self):
    #     state = self.__dict__.copy()
    #     state["state_dict"] = self.state_dict()
    #     return state

    # def __setstate__(self, state):
    #     self.__init__(
    #         bins=state["bins"],
    #         hidden_dims=state["hidden_dims"],
    #         batch_size=state["batch_size"],
    #         learning_rate=state["learning_rate"],
    #         scheduler=state["scheduler"],
    #         dropout=state["dropout"],
    #         weight_decay=state["weight_decay"],
    #         random_state=state["random_state"],
    #     )
    #     self.load_state_dict(state["state_dict"])


class class_PMLP_reg(torch.nn.Module, class_PMLP_Base):
    """Regularized and parametrized binary classification MLP
    can be initialized e.g. with
    reg_dict = {"hidden_dims": [256, 256], "learning_rate": 1e-3, "dropout": [0.5, 0.5], "weight_decay": 1e-6, "scheduler": {'patience': 10, 'factor': 0.5}}
    """

    def __init__(
        self,
        bins,
        hidden_dims=[256, 256],
        batch_size=30000,
        learning_rate=1e-3,
        scheduler=None,
        dropout=[None, None],
        weight_decay=1e-6,
        random_state=42,
    ):
        super(class_PMLP_reg, self).__init__()
        self.bins = bins
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.dropout = dropout
        self.weight_decay = weight_decay
        self.random_state = random_state
        self.hidden_dims = hidden_dims
        self.scheduler = scheduler

        layers = []
        dims = [self.bins + 2] + self.hidden_dims + [1]

        for i in range(len(dims) - 1):
            layers.append(torch.nn.Linear(dims[i], dims[i + 1]))
            if i < len(dims) - 2:
                layers.append(torch.nn.BatchNorm1d(dims[i + 1]))
                layers.append(torch.nn.ReLU())
                if dropout[i] is not None:
                    layers.append(torch.nn.Dropout(dropout[i]))

        layers.append(torch.nn.Sigmoid())

        self.layers = torch.nn.Sequential(*layers)

    def forward(self, x, m_s, sin2theta):
        i = torch.cat((x, m_s, sin2theta), 1)
        out = self.layers(i)
        return out


class class_MLP_2hidden(torch.nn.Module, class_MLP_Base):
    """
    Simple binary classification multilayer perceptron (MLP).

    Args:
        bins (int): Dimensionality of input features.
        hidden_dim (int): Number of dimensions used in the hidden layers.
        batch_size (int): Size of batches for training.
        learning_rate (float): Learning rate for the adam optimizer.
        random_state (int, optional): Random seed for reproducibility. Defaults to 42.

    Attributes:
        bins (int): Dimensionality of input features.
        lin1 (torch.nn.Linear): First linear transformation layer.
        lin2 (torch.nn.Linear): Second linear transformation layer.
        out (torch.nn.Linear): Output layer.
        ReLU (torch.nn.ReLU): Rectified Linear Unit activation function.
        sigmoid (torch.nn.Sigmoid): Sigmoid activation function.
        batch_size (int): Size of batches for training.
        learning_rate (float): Learning rate for optimization.
        random_state (int): Random seed for reproducibility.

    Methods:
        forward(x): Forward pass through the MLP.
    """

    def __init__(
        self,
        bins,
        hidden_dim,
        batch_size,
        learning_rate,
        scheduler=None,
        random_state=42,
    ):
        super(class_MLP_2hidden, self).__init__()
        self.bins = bins
        self.lin1 = torch.nn.Linear(self.bins, hidden_dim)
        self.lin2 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.out = torch.nn.Linear(hidden_dim, 1)
        self.ReLU = torch.nn.ReLU()
        self.sigmoid = torch.nn.Sigmoid()

        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.scheduler = scheduler

        self.random_state = random_state

    def forward(self, x):
        h1 = self.ReLU(self.lin1(x))
        h2 = self.ReLU(self.lin2(h1))
        out = self.sigmoid(self.out(h2))
        return out


#
# 2 Hidden Layer Original MLP
#


class class_MLP(torch.nn.Module):
    """
    Simple binary classification multilayer perceptron (MLP).

    Args:
        bins (int): Dimensionality of input features.
        hidden_dim (int): Number of dimensions used in the hidden layers.
        batch_size (int): Size of batches for training.
        learning_rate (float): Learning rate for the adam optimizer.
        random_state (int, optional): Random seed for reproducibility. Defaults to 42.

    Attributes:
        bins (int): Dimensionality of input features.
        lin1 (torch.nn.Linear): First linear transformation layer.
        lin2 (torch.nn.Linear): Second linear transformation layer.
        out (torch.nn.Linear): Output layer.
        ReLU (torch.nn.ReLU): Rectified Linear Unit activation function.
        sigmoid (torch.nn.Sigmoid): Sigmoid activation function.
        batch_size (int): Size of batches for training.
        learning_rate (float): Learning rate for optimization.
        random_state (int): Random seed for reproducibility.

    Methods:
        forward(x): Forward pass through the MLP.
        train_simple(epochs, X_train, y_train, X_validation, y_validation, gradient_flow=False, lr=1e-3, batch_size=32, device="cpu"): Trains the MLP model.
        eval_simple(losses_training, losses_validation, X_validation, y_validation, Nsamples=1000, threshold_pred=0.5, plot=True, device="cpu"): Evaluates the performance of the trained model.
        model_out(x_sterile_test=None, y_sterile_test=None, x_ref_test=None, y_ref_test=None, mode="Both", device="cpu", random_state=42): Computes the model output for given test data.
    """

    def __init__(
        self,
        bins,
        hidden_dim,
        batch_size,
        learning_rate,
        scheduler=None,
        random_state=42,
    ):
        super(class_MLP, self).__init__()
        self.bins = bins
        self.lin1 = torch.nn.Linear(self.bins, hidden_dim)
        self.lin2 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.out = torch.nn.Linear(hidden_dim, 1)
        self.ReLU = torch.nn.ReLU()
        self.sigmoid = torch.nn.Sigmoid()

        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.scheduler = scheduler

        self.random_state = random_state

    def forward(self, x):
        h1 = self.ReLU(self.lin1(x))
        h2 = self.ReLU(self.lin2(h1))
        out = self.sigmoid(self.out(h2))
        return out

    def train_simple(
        self,
        X_train,
        y_train,
        X_validation,
        y_validation,
        epochs,
        scheduler=None,
        gradient_flow=False,
        lr=1e-3,
        batch_size=32,
        device="cpu",
        verbose=1,
    ):
        """
        Trains the MLP model.

        Args:
            epochs (int): Number of training epochs.
            X_train (torch.Tensor): Training input data.
            y_train (torch.Tensor): Training target labels.
            X_validation (torch.Tensor): Validation input data.
            y_validation (torch.Tensor): Validation target labels.
            gradient_flow (bool, optional): Whether to compute and return gradients. Defaults to False.
            lr (float, optional): Learning rate for optimization. Defaults to 1e-3.
            batch_size (int, optional): Size of batches for training. Defaults to 32.
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            tuple: Tuple containing training losses, validation losses, and gradients if gradient_flow=True.
        """

        assert (
            self.bins == X_train[0].shape[0]
        ), f"Model input dimension ({self.bins}) doesnt match data ({X_train[0].shape[0]})!"

        optim = torch.optim.Adam(self.parameters(), lr)
        if scheduler is not None:
            sched = torch.optim.lr_scheduler.ReduceLROnPlateau(
                optim, "min", **scheduler
            )  # def: {'patience': 10, 'factor': 0.5}

        train_data = Dataset(X_train, y_train, seed=self.random_state)
        train_dl = DataLoader(train_data, batch_size=batch_size, device=device)
        val_data = Dataset(X_validation, y_validation, seed=self.random_state)
        val_dl = DataLoader(val_data, batch_size=batch_size, device=device)
        losses = []
        validation_losses = []
        gradients = {"lin1.weight": [], "lin2.weight": [], "out.weight": []}
        with trange(epochs, unit="epochs") as iterable:
            for count in iterable:
                if count > 0:
                    train_data.shuffle()
                    train_dl = DataLoader(
                        train_data, batch_size=batch_size, device=device
                    )
                for count_batch, (x_b, y_b) in enumerate(train_dl):
                    optim.zero_grad()
                    p = self(x_b)
                    loss = torch.nn.functional.binary_cross_entropy(p, y_b)
                    losses.append(loss.cpu().detach().numpy())
                    loss.backward()
                    if gradient_flow:
                        for n, p in self.named_parameters():
                            if (p.requires_grad) and ("bias" not in n):
                                avg_grad = p.grad.abs().mean()
                                gradients[n].append(avg_grad.cpu().detach().numpy())
                    optim.step()
                    if count_batch % 100 == 0:
                        x_b_val, y_b_val = iter(val_dl).__next__()
                        x_b_val = x_b_val.to(device)
                        y_b_val = y_b_val.to(device)
                        with torch.no_grad():
                            pred = self(x_b_val)  # reshape not really necessary anymore
                        loss_val = torch.nn.functional.binary_cross_entropy(
                            pred, y_b_val
                        )
                        if scheduler is not None:
                            sched.step(loss_val)
                        validation_losses.append(loss_val.cpu().detach().numpy())
                        if verbose == 1:
                            iterable.set_description("Training")
                            iterable.set_postfix(
                                tr_loss=f"{float(losses[-1]):.4f}",
                                val_loss=f"{float(validation_losses[-1]):.4f}",
                            )

        if gradient_flow:
            return losses, validation_losses, pd.DataFrame(gradients)

        return losses, validation_losses

    def eval_simple(
        self,
        losses_training,
        losses_validation,
        X_validation,
        y_validation,
        threshold_pred=0.5,
        plot=("epochs", 100),
        device="cpu",
    ):
        self.eval()
        """
        Evaluates the performance of the trained model.

        Args:
            losses_training (list): Training losses.
            losses_validation (list): Validation losses.
            X_validation (torch.Tensor): Validation input data.
            y_validation (torch.Tensor): Validation target labels.
            Nsamples (int, optional): Number of samples. Defaults to 1000.
            threshold_pred (float, optional): Prediction threshold. Defaults to 0.5.
            plot (tuple, optional): In which mode to plot the loss curve. Defaults to True.
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            dict: Dictionary containing evaluation metrics.
        """

        val_data = Dataset(X_validation, y_validation, seed=self.random_state)
        val_dl = DataLoader(val_data, batch_size=len(val_data), device=device)
        x_val, y_val = iter(val_dl).__next__()
        y_val = y_val.cpu()
        with torch.no_grad():
            pred = self(x_val)
            pred = pred.cpu()
        sterile_pred = np.where(pred > threshold_pred, 1, 0)
        gt = y_val.detach().numpy()

        if plot is not False:
            if plot[0] == "epochs":
                r = int(len(losses_training) / len(losses_validation))
                e = int(len(losses_training) / plot[1])
                x_ax_val = []
                x_ax_epochs = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                    if i % e == 0:
                        x_ax_epochs.append(i)

                fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                if len(x_ax_val) == len(losses_validation):
                    ax.plot(
                        x_ax_val,
                        losses_validation,
                        linewidth=3,
                        label="validation loss",
                    )
                else:
                    ax.plot(
                        x_ax_val[:-1],
                        losses_validation,
                        linewidth=3,
                        label="validation loss",
                    )
                for c, epoch in enumerate(x_ax_epochs):
                    if c % 5 == 0:
                        ax.axvline(
                            epoch,
                            ymin=0,
                            ymax=1,
                            color="grey",
                            linestyle="--",
                            linewidth=0.5,
                        )

                ax.axvline(
                    x_ax_epochs[-1],
                    ymin=0,
                    ymax=1,
                    color="grey",
                    linestyle="--",
                    linewidth=0.5,
                    label="every fifth training epoch",
                )

                # ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

            if plot[0] == "grid":
                r = int(len(losses_training) / len(losses_validation))
                x_ax_val = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                fig, ax = plt.subplots(figsize=(12, 8))
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                ax.plot(
                    x_ax_val, losses_validation, linewidth=3, label="validation loss"
                )
                ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

        score_dict = {
            "accuracy": accuracy(gt, sterile_pred),
            "precision": precision(gt, sterile_pred),
            "recall": recall(gt, sterile_pred),
            "fall-out": fallout(gt, sterile_pred),
            "f1": f1(gt, sterile_pred),
            "threshold_roc": threshold_pred,
        }
        # accuracy(gt, sterile_pred), recall(gt, sterile_pred), precision(gt, sterile_pred), f1(gt, sterile_pred)
        return score_dict

    def model_out(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        mode="Both",
        device="cpu",
        random_state=42,
    ):
        self.eval()
        """
        Computes the model output for given test data.

        Args:
            x_sterile_test (numpy.ndarray, optional): Test input data for sterile class. Defaults to None.
            y_sterile_test (numpy.ndarray, optional): Test target labels for sterile class. Defaults to None.
            x_ref_test (numpy.ndarray, optional): Test input data for reference class. Defaults to None.
            y_ref_test (numpy.ndarray, optional): Test target labels for reference class. Defaults to None.
            mode (str, optional): Kind of spectra for which the output is calculated, possible modes: ("Both", "ref", or "ster"). Defaults to "Both".
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".
            random_state (int, optional): Random seed for reproducibility. Defaults to 42.

        Returns:
            numpy.ndarray: Model outputs for the specified mode.
        """

        if mode == "Both":
            data_s = Dataset(x_sterile_test, y_sterile_test, seed=self.random_state)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            data_r = Dataset(x_ref_test, y_ref_test, seed=self.random_state)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                out_s = self(x_s)
                out_r = self(x_r)

            return out_s.cpu().detach().numpy(), out_r.cpu().detach().numpy()

        if mode == "ref":
            data_r = Dataset(x_ref_test, y_ref_test, seed=self.random_state)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                out_r = self(x_r)

            return out_r.cpu().detach().numpy()

        if mode == "ster":
            data_s = Dataset(x_sterile_test, y_sterile_test, seed=self.random_state)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            with torch.no_grad():
                out_s = self(x_s)

            return out_s.cpu().detach().numpy()

    def integrated_gradients(
        self, x_data, y_data, baseline=None, steps=50, device="cpu"
    ):
        self.eval()
        if baseline is None:
            baseline = np.zeros_like(x_data)

        gradients = []

        y_arr = np.zeros(steps + 1) + y_data
        scaled_inputs = np.array(
            [
                baseline + (float(i) / steps) * (x_data - baseline)
                for i in range(steps + 1)
            ]
        )
        ds = Dataset(scaled_inputs, y_arr, 42)
        dl = DataLoader(ds, batch_size=1, device=device)

        for c, (scaled_input, y) in enumerate(dl):
            scaled_input.requires_grad_(True)
            output = self(scaled_input)
            loss = output
            loss.backward(retain_graph=True)
            gradients.append(scaled_input.grad.cpu().detach().clone())

        avg_gradients = torch.mean(torch.stack(gradients), dim=0)
        approx_int_grad = (
            torch.Tensor(x_data) - torch.Tensor(baseline)
        ) * avg_gradients

        return approx_int_grad.detach().numpy()

    def eval_full(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        losses_training=None,
        losses_validation=None,
        X_validation=None,
        y_validation=None,
        grads=None,
        threshold_pred=0.5,
        device="cpu",
        plot=("all", {"epochs": 100, "int_grad_spec": 100}),
    ):
        self.eval()
        score = self.eval_simple(
            losses_training,
            losses_validation,
            X_validation,
            y_validation,
            threshold_pred,
            plot=False,
            device=device,
        )
        out_s, out_r = self.model_out(
            x_sterile_test, y_sterile_test, x_ref_test, y_ref_test, device=device
        )
        int_grad_ster = self.integrated_gradients(
            x_sterile_test[plot[1]["int_grad_spec"]],
            y_sterile_test[plot[1]["int_grad_spec"]],
            device=device,
        )[0]
        int_grad_ref = self.integrated_gradients(
            x_ref_test[0], y_ref_test[0], device=device
        )[0]

        if plot[0] == "all":
            fig, (l_ax, g_ax, o_ax, i_g_ax) = plt.subplots(4, 1, figsize=(15, 30))

            # l_ax

            r = int(len(losses_training) / len(losses_validation))
            e = int(len(losses_training) / plot[1]["epochs"])
            x_ax_val = []
            x_ax_epochs = []
            for i in np.arange(len(losses_training)):
                if i % r == 0:
                    x_ax_val.append(i)
                if i % e == 0:
                    x_ax_epochs.append(i)

            l_ax.plot(
                np.arange(len(losses_training)),
                losses_training,
                label="training loss",
            )
            l_ax.set_yscale("log")
            l_ax.set_xlabel("training iterations")
            l_ax.set_ylabel("Loss value")
            l_ax.set_title("BCE Loss", weight="bold")
            l_ax.plot(x_ax_val, losses_validation, linewidth=3, label="validation loss")
            for c, epoch in enumerate(x_ax_epochs):
                if c % 5 == 0:
                    l_ax.axvline(
                        epoch,
                        ymin=0,
                        ymax=1,
                        color="grey",
                        linestyle="--",
                        linewidth=0.5,
                    )

            l_ax.axvline(
                x_ax_epochs[-1],
                ymin=0,
                ymax=1,
                color="grey",
                linestyle="--",
                linewidth=0.5,
                label="every fifth training epoch",
            )

            l_ax.legend()

            l_ax.table(
                cellText=[[k, v] for k, v in zip(score.keys(), score.values())],
                cellLoc="left",
                edges="open",
                bbox=[0.05, 0.05, 0.3, 0.3],
            )

            # g_ax
            g_ax.plot(list(grads.index.values), grads["lin1.weight"], label="lin1")
            g_ax.plot(list(grads.index.values), grads["lin2.weight"], label="lin2")
            g_ax.plot(list(grads.index.values), grads["out.weight"], label="out")
            g_ax.legend()
            g_ax.set_xlabel("training iterations")
            g_ax.set_ylabel("avg gradient")

            # o_ax
            ul = 1
            o_ax.hist(
                out_s,
                bins=100,
                range=(out_r.min(), ul),
                fill=True,
                color="r",
                alpha=0.3,
                label="Model Output w/ sterile",
            )
            o_ax.hist(
                out_r,
                bins=100,
                range=(out_r.min(), ul),
                fill=True,
                color="g",
                alpha=0.3,
                label="Reference",
            )
            o_ax.set_yscale("log")
            o_ax.set_xlabel("Model Output")
            o_ax.set_ylabel("Counts")
            o_ax.set_title("Histogram of Model Outputs", weight="bold")
            o_ax.legend()

            # i_g_ax
            i_g_ax.plot(
                int_grad_ster,
                marker="o",
                linestyle="-",
                color="b",
                markersize=8,
                linewidth=2,
                alpha=0.75,
                label="Sterile Spectrum",
            )
            i_g_ax.plot(
                int_grad_ref,
                marker="o",
                linestyle="-",
                color="g",
                markersize=8,
                linewidth=2,
                alpha=0.75,
                label="Reference Spectrum",
            )

            i_g_ax.set_title("Integrated Gradients Attributions", weight="bold")
            i_g_ax.set_xlabel("Energy Bin")
            i_g_ax.set_ylabel("Attribution Value")
            i_g_ax.grid(True, which="both", linestyle="--", linewidth=0.5)
            i_g_ax.axhline(0, color="grey", linewidth=0.8)

            i_g_ax.legend()

            fig.tight_layout()
            fig.show()


#
# 2 Hidden Layer Original Parametrized MLP
#


class class_MLP_parametrized(torch.nn.Module):
    """
    Parametrized multilayer perceptron (MLP) for binary classification.

    Args:
        bins (int): Dimensionality of input features.
        params (int): Number of additional parameters.
        hidden_dim (int): Number of units in the hidden layer.
        batch_size (int): Size of batches for training.
        learning_rate (float): Learning rate for optimization.
        random_state (int, optional): Random seed for reproducibility. Defaults to 42.

    Attributes:
        bins (int): Dimensionality of input features.
        lin1 (torch.nn.Linear): First linear transformation layer.
        lin2 (torch.nn.Linear): Second linear transformation layer.
        out (torch.nn.Linear): Output layer.
        ReLU (torch.nn.ReLU): Rectified Linear Unit activation function.
        sigmoid (torch.nn.Sigmoid): Sigmoid activation function.
        batch_size (int): Size of batches for training.
        learning_rate (float): Learning rate for optimization.
        random_state (int): Random seed for reproducibility.

    Methods:
        forward(x, m_s, sin2theta): Forward pass through the MLP.
        train_simple(epochs, X_train, y_train, m_train, s_train, X_validation, y_validation, m_validation, s_validation, lr=1e-3, batch_size=32, gradient_flow=False, device="cpu"): Trains the parametrized MLP model.
        eval_simple(losses_training, losses_validation, X_validation, y_validation, m_validation, s_validation, Nsamples=1000, threshold_pred=0.5, plot=True, device="cpu"): Evaluates the performance of the trained model.
        model_out(x_sterile_test=None, y_sterile_test=None, m_sterile_test=None, s_sterile_test=None, x_ref_test=None, y_ref_test=None, m_ref_test=None, s_ref_test=None, mode="Both", device="cpu"): Computes the model output for given test data.
    """

    def __init__(
        self,
        bins,
        params,
        hidden_dim,
        batch_size,
        learning_rate,
        scheduler=None,
        random_state=42,
    ):

        super(class_MLP_parametrized, self).__init__()
        self.bins = bins
        self.lin1 = torch.nn.Linear(bins + params, hidden_dim)
        self.lin2 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.out = torch.nn.Linear(hidden_dim, 1)
        self.ReLU = torch.nn.ReLU()
        self.sigmoid = torch.nn.Sigmoid()

        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.scheduler = scheduler
        self.random_state = random_state

    def forward(self, x, m_s, sin2theta):
        """
        Forward pass through the parametrized MLP.

        Args:
            x (torch.Tensor): Input data.
            m_s (torch.Tensor): Additional parameter.
            sin2theta (torch.Tensor): Additional parameter.

        Returns:
            torch.Tensor: Output predictions.
        """
        i = torch.cat((x, m_s, sin2theta), 1)
        h1 = self.ReLU(self.lin1(i))
        h2 = self.ReLU(self.lin2(h1))
        out = self.sigmoid(self.out(h2))
        return out

    def train_simple(
        self,
        X_train,
        y_train,
        m_train,
        s_train,
        X_validation,
        y_validation,
        m_validation,
        s_validation,
        epochs,
        lr=1e-3,
        batch_size=32,
        scheduler=None,
        gradient_flow=False,
        device="cpu",
        verbose=1,
    ):
        """
        Trains the parametrized MLP model.

        Args:
            epochs (int): Number of training epochs.
            X_train (torch.Tensor): Training input data.
            y_train (torch.Tensor): Training target labels.
            m_train (torch.Tensor): Additional parameters for training data (sterile mass).
            s_train (torch.Tensor): Additional parameters for training data (mixing angle).
            X_validation (torch.Tensor): Validation input data.
            y_validation (torch.Tensor): Validation target labels.
            m_validation (torch.Tensor): Additional parameters for validation data (sterile mass).
            s_validation (torch.Tensor): Additional parameters for validation data (mixing angle).
            lr (float, optional): Learning rate for optimization. Defaults to 1e-3.
            batch_size (int, optional): Size of batches for training. Defaults to 32.
            gradient_flow (bool, optional): Whether to compute and return gradients. Defaults to False.
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            tuple: Tuple containing training losses, validation losses, and gradients if gradient_flow=True.
        """

        optim = torch.optim.Adam(self.parameters(), lr)
        if scheduler is not None:
            sched = torch.optim.lr_scheduler.ReduceLROnPlateau(
                optim, "min", **scheduler
            )  # def: 'patience': 10, 'factor': 0.5

        train_data = Dataset_Parametrized(
            X_train, y_train, m_train, s_train, seed=self.random_state
        )
        train_dl = DataLoader_Parametrized(
            train_data, batch_size=batch_size, device=device
        )
        val_data = Dataset_Parametrized(
            X_validation,
            y_validation,
            m_validation,
            s_validation,
            seed=self.random_state,
        )
        val_dl = DataLoader_Parametrized(val_data, batch_size=batch_size, device=device)
        losses = []
        validation_losses = []
        gradients = {"lin1.weight": [], "lin2.weight": [], "out.weight": []}
        with trange(epochs, unit="epochs") as iterable:
            for count in iterable:
                if count > 0:
                    train_data.shuffle()
                    train_dl = DataLoader_Parametrized(
                        train_data, batch_size=batch_size, device=device
                    )
                for count_batch, (x_b, y_b, m_b, s_b) in enumerate(train_dl):
                    optim.zero_grad()
                    p = self(x_b, m_b, s_b)
                    loss = torch.nn.functional.binary_cross_entropy(p, y_b)
                    losses.append(loss.cpu().detach().numpy())
                    loss.backward()
                    if gradient_flow:
                        for n, p in self.named_parameters():
                            if (p.requires_grad) and ("bias" not in n):
                                avg_grad = p.grad.abs().mean()
                                gradients[n].append(avg_grad.cpu().detach().numpy())
                    optim.step()
                    if count_batch % 100 == 0:
                        x_b_val, y_b_val, m_b_val, s_b_val = iter(val_dl).__next__()
                        x_b_val = x_b_val.to(device)
                        y_b_val = y_b_val.to(device)
                        m_b_val = m_b_val.to(device)
                        s_b_val = s_b_val.to(device)
                        with torch.no_grad():
                            pred = self(
                                x_b_val, m_b_val, s_b_val
                            )  # reshape not really necessary anymore
                        loss_val = torch.nn.functional.binary_cross_entropy(
                            pred, y_b_val
                        )
                        if scheduler is not None:
                            sched.step(loss_val)
                        validation_losses.append(loss_val.cpu().detach().numpy())
                        if verbose == 1:
                            iterable.set_description("Training")
                            iterable.set_postfix(
                                tr_loss=f"{float(losses[-1]):.4f}",
                                val_loss=f"{float(validation_losses[-1]):.4f}",
                            )

        if gradient_flow:
            return losses, validation_losses, pd.DataFrame(gradients)

        return losses, validation_losses

    def eval_simple(
        self,
        losses_training,
        losses_validation,
        X_validation,
        y_validation,
        m_validation,
        s_validation,
        Nsamples=1000,
        threshold_pred=0.5,
        plot=True,
        device="cpu",
    ):
        """
        Evaluates the performance of the trained model.

        Args:
            losses_training (list): Training losses.
            losses_validation (list): Validation losses.
            X_validation (torch.Tensor): Validation input data.
            y_validation (torch.Tensor): Validation target labels.
            m_validation (torch.Tensor): Additional parameters for validation data (sterile mass).
            s_validation (torch.Tensor): Additional parameters for validation data (mixing angle).
            Nsamples (int, optional): Number of samples. Defaults to 1000.
            threshold_pred (float, optional): Prediction threshold. Defaults to 0.5.
            plot (bool, optional): Whether to plot the loss curves. Defaults to True.
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            dict: Dictionary containing evaluation metrics.
        """

        val_data = Dataset_Parametrized(
            X_validation,
            y_validation,
            m_validation,
            s_validation,
            seed=self.random_state,
        )
        val_dl = DataLoader_Parametrized(
            val_data, batch_size=len(val_data), device=device
        )
        x_val, y_val, m_val, s_val = iter(val_dl).__next__()
        y_val = y_val.cpu()
        with torch.no_grad():
            pred = self(x_val, m_val, s_val)
            pred = pred.cpu()
        sterile_pred = np.where(pred > threshold_pred, 1, 0)
        gt = y_val.detach().numpy()

        if plot is not False:
            if plot[0] == "epochs":
                r = int(len(losses_training) / len(losses_validation))
                e = int(len(losses_training) / plot[1])
                x_ax_val = []
                x_ax_epochs = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                    if i % e == 0:
                        x_ax_epochs.append(i)

                fig, ax = plt.subplots(figsize=(12, 8))
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                ax.plot(
                    x_ax_val, losses_validation, linewidth=3, label="validation loss"
                )
                for c, epoch in enumerate(x_ax_epochs):
                    if c % 5 == 0:
                        ax.axvline(
                            epoch,
                            ymin=0,
                            ymax=1,
                            color="grey",
                            linestyle="--",
                            linewidth=0.5,
                        )

                ax.axvline(
                    x_ax_epochs[-1],
                    ymin=0,
                    ymax=1,
                    color="grey",
                    linestyle="--",
                    linewidth=0.5,
                    label="every fifth training epoch",
                )

                # ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

            if plot[0] == "grid":
                r = int(len(losses_training) / len(losses_validation))
                x_ax_val = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                fig, ax = plt.subplots(figsize=(12, 8))
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                ax.plot(
                    x_ax_val, losses_validation, linewidth=3, label="validation loss"
                )
                ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

        score_dict = {
            "accuracy": accuracy(gt, sterile_pred),
            "precision": precision(gt, sterile_pred),
            "recall": recall(gt, sterile_pred),
            "fall-out": fallout(gt, sterile_pred),
            "f1": f1(gt, sterile_pred),
            "threshold_roc": threshold_pred,
        }
        # accuracy(gt, sterile_pred), recall(gt, sterile_pred), precision(gt, sterile_pred), f1(gt, sterile_pred)
        return score_dict

    def model_out(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        m_sterile_test=None,
        s_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        m_ref_test=None,
        s_ref_test=None,
        mode="Both",
        device="cpu",
    ):
        """
        Computes the model output for given test data.

        Args:
            x_sterile_test (numpy.ndarray, optional): Test input data for sterile class. Defaults to None.
            y_sterile_test (numpy.ndarray, optional): Test target labels for sterile class. Defaults to None.
            m_sterile_test (numpy.ndarray, optional): Additional parameters for sterile test data (sterile mass). Defaults to None.
            s_sterile_test (numpy.ndarray, optional): Additional parameters for sterile test data (mixing angle). Defaults to None.
            x_ref_test (numpy.ndarray, optional): Test input data for reference class. Defaults to None.
            y_ref_test (numpy.ndarray, optional): Test target labels for reference class. Defaults to None.
            m_ref_test (numpy.ndarray, optional): Additional parameters for reference test data (sterile mass). Defaults to None.
            s_ref_test (numpy.ndarray, optional): Additional parameters for reference test data (mixing angle). Defaults to None.
            mode (str, optional): Kind of spectra for which the output is calculated, possible modes: ("Both", "ref", or "ster"). Defaults to "Both".
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            numpy.ndarray: Model outputs for the specified mode.
        """
        if mode == "Both":
            data_s = Dataset_Parametrized(
                x_sterile_test, y_sterile_test, m_sterile_test, s_sterile_test
            )
            x_s, y_s, m_s, s_s = data_s[:]
            x_s, y_s, m_s, s_s = (
                torch.FloatTensor(x_s.astype(np.float64)),
                torch.FloatTensor(y_s.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(m_s.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(s_s.astype(np.float64)).unsqueeze(-1),
            )
            x_s, y_s, m_s, s_s = (
                x_s.to(device),
                y_s.to(device),
                m_s.to(device),
                s_s.to(device),
            )

            data_r = Dataset_Parametrized(
                x_ref_test, y_ref_test, m_ref_test, s_ref_test
            )
            x_r, y_r, m_r, s_r = data_r[:]
            x_r, y_r, m_r, s_r = (
                torch.FloatTensor(x_r.astype(np.float64)),
                torch.FloatTensor(y_r.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(m_r.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(s_r.astype(np.float64)).unsqueeze(-1),
            )
            x_r, y_r, m_r, s_r = (
                x_r.to(device),
                y_r.to(device),
                m_r.to(device),
                s_r.to(device),
            )

            with torch.no_grad():
                out_s = self(x_s, m_s, s_s)
                out_r = self(x_r, m_r, s_r)

            return out_s.cpu().detach().numpy(), out_r.cpu().detach().numpy()

        if mode == "ref":
            data_r = Dataset_Parametrized(
                x_ref_test, y_ref_test, m_ref_test, s_ref_test
            )
            x_r, y_r, m_r, s_r = data_r[:]
            x_r, y_r, m_r, s_r = (
                torch.FloatTensor(x_r.astype(np.float64)),
                torch.FloatTensor(y_r.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(m_r.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(s_r.astype(np.float64)).unsqueeze(-1),
            )
            x_r, y_r, m_r, s_r = (
                x_r.to(device),
                y_r.to(device),
                m_r.to(device),
                s_r.to(device),
            )

            with torch.no_grad():
                out_r = self(x_r, m_r, s_r)

            return out_r.cpu().detach().numpy()

        if mode == "ster":
            data_s = Dataset_Parametrized(
                x_sterile_test, y_sterile_test, m_sterile_test, s_sterile_test
            )
            x_s, y_s, m_s, s_s = data_s[:]
            x_s, y_s, m_s, s_s = (
                torch.FloatTensor(x_s.astype(np.float64)),
                torch.FloatTensor(y_s.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(m_s.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(s_s.astype(np.float64)).unsqueeze(-1),
            )
            x_s, y_s, m_s, s_s = (
                x_s.to(device),
                y_s.to(device),
                m_s.to(device),
                s_s.to(device),
            )

            with torch.no_grad():
                out_s = self(x_s, m_s, s_s)

            return out_s.cpu().detach().numpy()

    def integrated_gradients(
        self, x_data, y_data, m_data, s_data, baseline=None, steps=50, device="cpu"
    ):
        self.eval()
        if baseline is None:
            baseline = np.zeros_like(x_data)

        gradients = []

        y_arr = np.zeros(steps + 1) + y_data
        m_data = np.zeros(steps + 1) + m_data
        s_data = np.zeros(steps + 1) + s_data

        scaled_inputs = np.array(
            [
                baseline + (float(i) / steps) * (x_data - baseline)
                for i in range(steps + 1)
            ]
        )
        ds = Dataset_Parametrized(scaled_inputs, y_arr, m_data, s_data, 42)
        dl = DataLoader_Parametrized(ds, batch_size=1, device=device)

        for c, (scaled_input, y, m, s) in enumerate(dl):
            scaled_input.requires_grad_(True)
            output = self(scaled_input, m, s)
            loss = output
            loss.backward(retain_graph=True)
            gradients.append(scaled_input.grad.cpu().detach().clone())

        avg_gradients = torch.mean(torch.stack(gradients), dim=0)
        approx_int_grad = (
            torch.Tensor(x_data) - torch.Tensor(baseline)
        ) * avg_gradients

        return approx_int_grad.detach().numpy()

    def eval_full(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        m_sterile_test=None,
        s_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        m_ref_test=None,
        s_ref_test=None,
        losses_training=None,
        losses_validation=None,
        X_validation=None,
        y_validation=None,
        m_validation=None,
        s_validation=None,
        grads=None,
        threshold_pred=0.5,
        device="cpu",
        plot=("all", {"epochs": 100, "int_grad_spec": 100}),
    ):
        self.eval()
        score = self.eval_simple(
            losses_training,
            losses_validation,
            X_validation,
            y_validation,
            m_validation,
            s_validation,
            threshold_pred,
            plot=False,
            device=device,
        )
        out_s, out_r = self.model_out(
            x_sterile_test,
            y_sterile_test,
            m_sterile_test,
            s_sterile_test,
            x_ref_test,
            y_ref_test,
            m_ref_test,
            s_ref_test,
            device=device,
        )
        int_grad_ster = self.integrated_gradients(
            x_sterile_test[plot[1]["int_grad_spec"]],
            y_sterile_test[plot[1]["int_grad_spec"]],
            m_sterile_test[plot[1]["int_grad_spec"]],
            s_sterile_test[plot[1]["int_grad_spec"]],
            device=device,
        )[0]
        int_grad_ref = self.integrated_gradients(
            x_ref_test[0], y_ref_test[0], m_ref_test[0], s_ref_test[0], device=device
        )[0]

        if plot[0] == "all":
            fig, (l_ax, g_ax, o_ax, i_g_ax) = plt.subplots(4, 1, figsize=(15, 30))

            # l_ax

            r = int(len(losses_training) / len(losses_validation))
            e = int(len(losses_training) / plot[1]["epochs"])
            x_ax_val = []
            x_ax_epochs = []
            for i in np.arange(len(losses_training)):
                if i % r == 0:
                    x_ax_val.append(i)
                if i % e == 0:
                    x_ax_epochs.append(i)

            l_ax.plot(
                np.arange(len(losses_training)),
                losses_training,
                label="training loss",
            )
            l_ax.set_yscale("log")
            l_ax.set_xlabel("training iterations")
            l_ax.set_ylabel("Loss value")
            l_ax.set_title("BCE Loss", weight="bold")
            l_ax.plot(x_ax_val, losses_validation, linewidth=3, label="validation loss")
            for c, epoch in enumerate(x_ax_epochs):
                if c % 5 == 0:
                    l_ax.axvline(
                        epoch,
                        ymin=0,
                        ymax=1,
                        color="grey",
                        linestyle="--",
                        linewidth=0.5,
                    )

            l_ax.axvline(
                x_ax_epochs[-1],
                ymin=0,
                ymax=1,
                color="grey",
                linestyle="--",
                linewidth=0.5,
                label="every fifth training epoch",
            )

            l_ax.legend()

            l_ax.table(
                cellText=[[k, v] for k, v in zip(score.keys(), score.values())],
                cellLoc="left",
                edges="open",
                bbox=[0.05, 0.05, 0.3, 0.3],
            )

            # g_ax
            g_ax.plot(list(grads.index.values), grads["lin1.weight"], label="lin1")
            g_ax.plot(list(grads.index.values), grads["lin2.weight"], label="lin2")
            g_ax.plot(list(grads.index.values), grads["out.weight"], label="out")
            g_ax.legend()
            g_ax.set_xlabel("training iterations")
            g_ax.set_ylabel("avg gradient")

            # o_ax
            ul = 1
            o_ax.hist(
                out_s,
                bins=100,
                range=(out_r.min(), ul),
                fill=True,
                color="r",
                alpha=0.3,
                label="Model Output w/ sterile",
            )
            o_ax.hist(
                out_r,
                bins=100,
                range=(out_r.min(), ul),
                fill=True,
                color="g",
                alpha=0.3,
                label="Reference",
            )
            o_ax.set_yscale("log")
            o_ax.set_xlabel("Model Output")
            o_ax.set_ylabel("Counts")
            o_ax.set_title("Histogram of Model Outputs", weight="bold")
            o_ax.legend()

            # i_g_ax
            i_g_ax.plot(
                int_grad_ster,
                marker="o",
                linestyle="-",
                color="b",
                markersize=8,
                linewidth=2,
                alpha=0.75,
                label="Sterile Spectrum",
            )
            i_g_ax.plot(
                int_grad_ref,
                marker="o",
                linestyle="-",
                color="g",
                markersize=8,
                linewidth=2,
                alpha=0.75,
                label="Reference Spectrum",
            )

            i_g_ax.set_title("Integrated Gradients Attributions", weight="bold")
            i_g_ax.set_xlabel("Energy Bin")
            i_g_ax.set_ylabel("Attribution Value")
            i_g_ax.grid(True, which="both", linestyle="--", linewidth=0.5)
            i_g_ax.axhline(0, color="grey", linewidth=0.8)

            i_g_ax.legend()

            fig.tight_layout()
            fig.show()


# ===========================================================================================================================================================
# ===========================================================================================================================================================
# ===========================================================================================================================================================
# Autoencoders (TODO need update) ===========================================================================================================================
# ===========================================================================================================================================================
# ===========================================================================================================================================================
# ===========================================================================================================================================================


class Autoencoder_test(torch.nn.Module):
    def __init__(self, bins, hidden_dim, latent_dim):
        super().__init__()
        self.bins = bins
        self.encoder = torch.nn.Sequential(
            # torch.nn.Flatten(),
            torch.nn.Linear(bins, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, latent_dim),
        )

        self.decoder = torch.nn.Sequential(
            torch.nn.Linear(latent_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, bins),
        )

    def forward(self, x):
        code = self.encoder(x)
        reco = self.decoder(code)
        return code, reco

    def train(
        self,
        epochs,
        X_train,
        y_train,
        X_validation,
        y_validation,
        lr=1e-3,
        batch_size=32,
        device="cpu",
        random_state=1,
        plot_model=True,
    ):
        ekin = np.linspace(0, 18600, X_train[0].shape[0])
        train_data = Dataset(X_train, y_train)
        train_dl = DataLoader(train_data, batch_size=batch_size, device=device)
        val_data = Dataset(X_validation, y_validation)
        val_dl = DataLoader(val_data, batch_size=batch_size, device=device)
        optim = torch.optim.Adam(self.parameters(), lr)
        losses = []
        val_losses = []
        for count in range(epochs):
            if count > 0:
                X_train_shuffled, y_train_shuffled = shuffle(
                    X_train, y_train, random_state=random_state
                )
                train_data_shuffled = Dataset(X_train_shuffled, y_train_shuffled)
                train_dl = DataLoader(
                    train_data_shuffled, batch_size=batch_size, device=device
                )
                random_state += 1
            for count_batch, (x_b, y_b) in enumerate(train_dl):
                optim.zero_grad()
                code, reco = self(x_b)
                loss = torch.nn.functional.mse_loss(
                    x_b.squeeze(), reco
                )  # need squeeze?
                losses.append(loss.cpu().detach().numpy())
                loss.backward()
                optim.step()
                if count_batch % 100 == 0:
                    x_b_val, y_b_val = iter(val_dl).__next__()
                    x_b_val = x_b_val.to(device)
                    y_b_val = y_b_val.to(device)
                    with torch.no_grad():
                        code, reco = self(x_b_val)  # reshape ?
                    loss_val = torch.nn.functional.mse_loss(reco, x_b_val)
                    val_losses.append(loss_val.cpu().detach().numpy())
                    print(
                        f"Epoch: {count} | Batch: [{count_batch}/{len(train_data) / batch_size}] training loss: {float(loss):.10f}  validation loss: {float(loss_val):.10f}",
                    )
                    if plot_model:
                        f, axarr = plt.subplots(1, 3, figsize=(10, 10))
                        axarr[0].plot(ekin, x_b_val[0].cpu().detach().numpy())
                        axarr[1].plot(ekin, reco[0].cpu().detach().numpy())  # m[-1][0]
                        axarr[2].scatter(
                            code[:, 0].cpu().detach().numpy(),
                            code[:, 1].cpu().detach().numpy(),
                        )
                        f.set_tight_layout(True)

        return losses, val_losses

    def reco_loss(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        mode="Both",
        device="cpu",
    ):
        if mode == "Both":
            data_s = Dataset(x_sterile_test, y_sterile_test)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            data_r = Dataset(x_ref_test, y_ref_test)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                c_s, r_s = self(x_s)
                c_r, r_r = self(x_r)

            # r_s = r_s.cpu().detach().numpy()
            # r_r = r_r.cpu().detach().numpy()

            reco_losses = []
            ref_losses = []
            for count, reco_spec in enumerate(r_s):
                reco_loss = torch.nn.functional.mse_loss(
                    reco_spec, x_s.squeeze()[count]
                )
                reco_losses.append(reco_loss.cpu().detach().numpy())
            for count, value in enumerate(r_r):
                reco_ref_loss = torch.nn.functional.mse_loss(
                    value, x_r.squeeze()[count]
                )
                ref_losses.append(reco_ref_loss.cpu().detach().numpy())
            return np.array(reco_losses, dtype=np.float64), np.array(
                ref_losses, dtype=np.float64
            )

        if mode == "ref":
            data_r = Dataset(x_ref_test, y_ref_test)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                c_r, r_r = self(x_r)

            ref_losses = []
            for count, value in enumerate(r_r):
                reco_ref_loss = torch.nn.functional.mse_loss(
                    value, x_r.squeeze()[count]
                )
                ref_losses.append(reco_ref_loss.cpu().detach().numpy())

            return np.array(ref_losses, dtype=np.float64)

        if mode == "ster":
            data_s = Dataset(x_sterile_test, y_sterile_test)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            with torch.no_grad():
                c_s, r_s = self(x_s)

            reco_losses = []
            for count, reco_spec in enumerate(r_s):
                reco_loss = torch.nn.functional.mse_loss(
                    reco_spec, x_s.squeeze()[count]
                )
                reco_losses.append(reco_loss.cpu().detach().numpy())

            return np.array(reco_losses, dtype=np.float64)


# VAE


class VAE_Encoder(torch.nn.Module):
    def __init__(self, bins, hidden_dim, latent_dim, slope):
        super(VAE_Encoder, self).__init__()
        self.bins = bins
        self.slope = slope
        self.flatten_layer = torch.nn.Sequential(torch.nn.Flatten())
        self.lin1 = torch.nn.Linear(bins, hidden_dim)
        self.lin2 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.lin_mean = torch.nn.Linear(hidden_dim, latent_dim)
        self.lin_var = torch.nn.Linear(hidden_dim, latent_dim)

        self.LeakyReLU = torch.nn.LeakyReLU(slope)

        self.training = True

    def forward(self, x):  # maybe need to use flatten here
        x_flat = self.flatten_layer(x)
        h_ = self.LeakyReLU(self.lin1(x_flat))
        h_ = self.LeakyReLU(self.lin2(h_))
        mean = self.lin_mean(h_)
        log_var = self.lin_var(h_)
        return mean, log_var


class VAE_Decoder(torch.nn.Module):
    def __init__(self, bins, hidden_dim, latent_dim, slope):
        super(VAE_Decoder, self).__init__()
        self.bins = bins
        self.slope = slope
        self.lin1 = torch.nn.Linear(latent_dim, hidden_dim)
        self.lin2 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.out = torch.nn.Linear(hidden_dim, bins)

        self.LeakyReLU = torch.nn.LeakyReLU(slope)

    def forward(self, x):
        h = self.LeakyReLU(self.lin1(x))
        h = self.LeakyReLU(self.lin2(h))
        out = self.out(h)
        return out


class VAE(torch.nn.Module):
    def __init__(self, Encoder, Decoder):
        super(VAE, self).__init__()
        self.Encoder = Encoder
        self.Decoder = Decoder

    def reparametrization(self, mean, var):
        epsilon = torch.randn_like(var)
        z = mean + var * epsilon
        return z

    def forward(self, x):
        mean, log_var = self.Encoder(x)
        z = self.reparametrization(mean, torch.exp(0.5 * log_var))
        reco = self.Decoder(z)
        return mean, log_var, reco

    def loss_function(self, x, reco, code_mean, code_log_var, beta=1):
        reproduction_loss = torch.nn.functional.mse_loss(x, reco)
        KL_div = -0.5 * torch.sum(
            1 + code_log_var - code_mean.pow(2) - code_log_var.exp()
        )
        return reproduction_loss + beta * KL_div

    def train(
        self,
        epochs,
        X_train,
        y_train,
        X_validation,
        y_validation,
        lr=1e-3,
        batch_size=32,
        beta=1,
        device="cpu",
        random_state=1,
        plot_model=True,
    ):
        ekin = np.linspace(0, 18600, X_train[0].shape[0])
        train_data = Dataset(X_train, y_train)
        train_dl = DataLoader(train_data, batch_size=batch_size, device=device)
        val_data = Dataset(X_validation, y_validation)
        val_dl = DataLoader(val_data, batch_size=batch_size, device=device)
        optim = torch.optim.Adam(self.parameters(), lr)
        losses = []
        val_losses = []
        for count in range(epochs):
            if count > 0:
                X_train_shuffled, y_train_shuffled = shuffle(
                    X_train, y_train, random_state=random_state
                )
                train_data_shuffled = Dataset(X_train_shuffled, y_train_shuffled)
                train_dl = DataLoader(
                    train_data_shuffled, batch_size=batch_size, device=device
                )
                random_state += 1
            for count_batch, (x_b, y_b) in enumerate(train_dl):
                optim.zero_grad()
                code_mean, code_logvar, reco = self(x_b)
                loss = self.loss_function(
                    x_b.squeeze(), reco, code_mean, code_logvar, beta=beta
                )
                losses.append(loss.cpu().detach().numpy())
                loss.backward()
                optim.step()
                if count_batch % 100 == 0:
                    x_b_val, y_b_val = iter(val_dl).__next__()
                    x_b_val = x_b_val.to(device)
                    y_b_val = y_b_val.to(device)
                    with torch.no_grad():
                        code_mean, code_logvar, reco = self(x_b_val)  # reshape ?
                    loss_val = self.loss_function(
                        x_b_val.squeeze(), reco, code_mean, code_logvar, beta=beta
                    )
                    val_losses.append(loss_val.cpu().detach().numpy())
                    print(
                        f"Epoch: {count} | Batch: [{count_batch}/{len(train_data) / batch_size}] training loss: {float(loss):.10f}  validation loss: {float(loss_val):.10f}",
                    )
                    if plot_model:
                        f, axarr = plt.subplots(1, 3, figsize=(10, 10))
                        axarr[0].plot(ekin, x_b_val[0].cpu().detach().numpy())
                        axarr[1].plot(ekin, reco[0].cpu().detach().numpy())  # m[-1][0]
                        axarr[2].scatter(
                            code_mean[:, 0].cpu().detach().numpy(),
                            code_mean[:, 1].cpu().detach().numpy(),
                        )
                        f.set_tight_layout(True)

        return losses, val_losses

    def reco_loss(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        beta=1,
        mode="Both",
        device="cpu",
    ):
        if mode == "Both":
            data_s = Dataset(x_sterile_test, y_sterile_test)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            data_r = Dataset(x_ref_test, y_ref_test)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                c_m_s, c_l_s, r_s = self(x_s)
                c_m_r, c_l_r, r_r = self(x_r)

            # r_s = r_s.cpu().detach().numpy()
            # r_r = r_r.cpu().detach().numpy()

            reco_losses = []
            ref_losses = []
            for count, reco_spec in enumerate(r_s):
                reco_loss = self.loss_function(
                    x_s.squeeze()[count], reco_spec, c_m_s, c_l_s, beta=beta
                )
                reco_losses.append(reco_loss.cpu().detach().numpy())
            for count, reco_spec_ref in enumerate(r_r):
                reco_ref_loss = self.loss_function(
                    x_r.squeeze()[count], reco_spec_ref, c_m_r, c_l_r, beta=beta
                )
                ref_losses.append(reco_ref_loss.cpu().detach().numpy())
            return np.array(reco_losses, dtype=np.float64), np.array(
                ref_losses, dtype=np.float64
            )

        if mode == "ref":
            data_r = Dataset(x_ref_test, y_ref_test)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                c_m_r, c_l_r, r_r = self(x_r)

            ref_losses = []
            for count, reco_spec_ref in enumerate(r_r):
                reco_ref_loss = self.loss_function(
                    x_r.squeeze()[count], reco_spec_ref, c_m_r, c_l_r, beta=beta
                )
                ref_losses.append(reco_ref_loss.cpu().detach().numpy())

            return np.array(ref_losses, dtype=np.float64)

        if mode == "ster":
            data_s = Dataset(x_sterile_test, y_sterile_test)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            with torch.no_grad():
                c_m_s, c_l_s, r_s = self(x_s)

            reco_losses = []
            for count, reco_spec in enumerate(r_s):
                reco_loss = self.loss_function(
                    x_s.squeeze()[count], reco_spec, c_m_s, c_l_s, beta=beta
                )
                reco_losses.append(reco_loss.cpu().detach().numpy())

            return np.array(reco_losses, dtype=np.float64)


# Should implement this into model class: DONE


def reco_loss(
    ae,
    x_sterile_test=None,
    y_sterile_test=None,
    x_ref_test=None,
    y_ref_test=None,
    mode="Both",
    device="cpu",
):
    if mode == "Both":
        data_s = Dataset(x_sterile_test, y_sterile_test)
        x_s, y_s = data_s[:]
        x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
            y_s.astype(np.float64)
        ).unsqueeze(-1)
        x_s, y_s = x_s.to(device), y_s.to(device)

        data_r = Dataset(x_ref_test, y_ref_test)
        x_r, y_r = data_r[:]
        x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
            y_r.astype(np.float64)
        ).unsqueeze(-1)
        x_r, y_r = x_r.to(device), y_r.to(device)

        with torch.no_grad():
            c_s, r_s = ae(x_s)
            c_r, r_r = ae(x_r)

        # r_s = r_s.cpu().detach().numpy()
        # r_r = r_r.cpu().detach().numpy()

        reco_losses = []
        ref_losses = []
        for count, reco_spec in enumerate(r_s):
            reco_loss = torch.nn.functional.mse_loss(reco_spec, x_s.squeeze()[count])
            reco_losses.append(reco_loss.cpu().detach().numpy())
        for count, value in enumerate(r_r):
            reco_ref_loss = torch.nn.functional.mse_loss(value, x_r.squeeze()[count])
            ref_losses.append(reco_ref_loss.cpu().detach().numpy())
        return np.array(reco_losses, dtype=np.float64), np.array(
            ref_losses, dtype=np.float64
        )

    if mode == "ref":
        data_r = Dataset(x_ref_test, y_ref_test)
        x_r, y_r = data_r[:]
        x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
            y_r.astype(np.float64)
        ).unsqueeze(-1)
        x_r, y_r = x_r.to(device), y_r.to(device)

        with torch.no_grad():
            c_r, r_r = ae(x_r)

        ref_losses = []
        for count, value in enumerate(r_r):
            reco_ref_loss = torch.nn.functional.mse_loss(value, x_r.squeeze()[count])
            ref_losses.append(reco_ref_loss.cpu().detach().numpy())

        return np.array(ref_losses, dtype=np.float64)

    if mode == "ster":
        data_s = Dataset(x_sterile_test, y_sterile_test)
        x_s, y_s = data_s[:]
        x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
            y_s.astype(np.float64)
        ).unsqueeze(-1)
        x_s, y_s = x_s.to(device), y_s.to(device)

        with torch.no_grad():
            c_s, r_s = ae(x_s)

        reco_losses = []
        for count, reco_spec in enumerate(r_s):
            reco_loss = torch.nn.functional.mse_loss(reco_spec, x_s.squeeze()[count])
            reco_losses.append(reco_loss.cpu().detach().numpy())

        return np.array(reco_losses, dtype=np.float64)


# def plot_grad_flow(named_parameters):
#     """Plots the gradients flowing through different layers in the net during training.
#     Can be used for checking for possible gradient vanishing / exploding problems."""
#     ave_grads = []
#     max_grads = []
#     layers = []
#     for n, p in named_parameters:
#         if (p.requires_grad) and ("bias" not in n):
#             layers.append(n)
#             ave_grads.append(p.grad.abs().mean())
#             max_grads.append(p.grad.abs().max())
#     plt.bar(np.arange(len(max_grads)), max_grads, alpha=0.1, lw=1, color="c")
#     plt.bar(np.arange(len(max_grads)), ave_grads, alpha=0.1, lw=1, color="b")
#     plt.hlines(0, 0, len(ave_grads) + 1, lw=2, color="k")
#     plt.xticks(range(0, len(ave_grads), 1), layers, rotation="vertical")
#     plt.xlim(left=0, right=len(ave_grads))
#     plt.ylim(bottom=-0.001, top=0.02)  # zoom in on the lower gradient regions
#     plt.xlabel("Layers")
#     plt.ylabel("average gradient")
#     plt.title("Gradient flow")
#     plt.grid(True)
#     plt.legend(
#         [
#             Line2D([0], [0], color="c", lw=4),
#             Line2D([0], [0], color="b", lw=4),
#             Line2D([0], [0], color="k", lw=4),
#         ],
#         ["max-gradient", "mean-gradient", "zero-gradient"],
#     )


# ===========================================================================================================================================================
# ===========================================================================================================================================================
# ===========================================================================================================================================================
# TRANSFORMERs (EVERYTHING ATTENTION) ========================================================================================================================
# ===========================================================================================================================================================
# ===========================================================================================================================================================
# ===========================================================================================================================================================


class Attention(torch.nn.Module):
    def __init__(self, d_model):
        super(Attention, self).__init__()
        self.d_model = d_model

        self.W_q = torch.nn.Linear(d_model, d_model)  # query weight matrix
        self.W_k = torch.nn.Linear(d_model, d_model)  # key weight matrix
        self.W_v = torch.nn.Linear(d_model, d_model)  # values weight matrix

    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        attn_scores = torch.matmul(Q, K.transpose(-2, -1)) / np.sqrt(self.d_model)
        if mask is not None:
            attn_scores = attn_scores.masked_fill(mask == 0, -1e9)
        attn_probs = torch.softmax(attn_scores, dim=-1)
        output = torch.matmul(attn_probs, V)
        return output

    def forward(self, Q, K, V, mask=None):
        output = self.scaled_dot_product_attention(Q, K, V, mask)
        return output


class PositionWiseFeedForward(torch.nn.Module):
    def __init__(self, d_model, d_ff):
        super(PositionWiseFeedForward, self).__init__()
        self.fc1 = torch.nn.Linear(d_model, d_ff)
        self.fc2 = torch.nn.Linear(d_ff, d_model)
        self.relu = torch.nn.ReLU()

    def forward(self, x):
        return self.fc2(self.relu(self.fc1(x)))

    def _initialize_linear_layers(self, bias=0, mode="uniform"):

        if mode == "uniform":
            initialize = torch.nn.init.xavier_uniform_
        if mode == "normal":
            initialize = torch.nn.init.xavier_normal_

        initialize(self.fc1.weight)
        initialize(self.fc2.weight)

        if bias is not None:
            if self.fc1.bias is not None:
                torch.nn.init.constant_(self.fc1.bias, bias)
            if self.fc2.bias is not None:
                torch.nn.init.constant_(self.fc2.bias, bias)


class EncoderLayer(torch.nn.Module):
    def __init__(self, d_model, d_ff, dropout: float):
        super(EncoderLayer, self).__init__()
        self.self_attn = Attention(d_model)
        self.feed_forward = PositionWiseFeedForward(d_model, d_ff)
        self.norm1 = torch.nn.LayerNorm(d_model)
        self.norm2 = torch.nn.LayerNorm(d_model)
        self.dropout = torch.nn.Dropout(dropout)

    def forward(self, x, mask=None):
        attn_output = self.self_attn(
            x, x, x
        )  # maybe dont need the masked self attention here as beta spectrum is not time dependent data -> should be able to attend to future positions
        x = self.norm1(x + self.dropout(attn_output))
        ff_output = self.feed_forward(x)
        x = self.norm2(x + self.dropout(ff_output))
        return x


class self_attn_mlp(torch.nn.Module):
    def __init__(
        self,
        input_bins,
        d_model,
        d_ff,
        out_dim,
        num_layers,
        dropout,
        batch_size,
        learning_rate,
        scheduler,
        random_state=42,
    ):
        super(self_attn_mlp, self).__init__()
        self.in_layer = torch.nn.Linear(input_bins, d_model)
        self.out_layer = torch.nn.Linear(d_model, out_dim)

        self.random_state = random_state

        self.encoder_layers = torch.nn.ModuleList(
            [EncoderLayer(d_model, d_ff, dropout) for _ in range(num_layers)]
        )

        self.dropout = torch.nn.Dropout(dropout)

        self.output = torch.nn.Sigmoid()

        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.scheduler = scheduler

    def forward(self, x):
        inp = self.dropout(self.in_layer(x))

        enc_out = inp
        for layer in self.encoder_layers:
            enc_out = layer(enc_out)

        out = self.output(self.out_layer(enc_out))
        return out

    def train_simple(
        self,
        X_train,
        y_train,
        X_val,
        y_val,
        epochs,
        lr=1e-3,
        batch_size=32,
        gradient_flow=False,
        device="cpu",
        verbose=1,
    ):

        # tracking gradient flow
        if gradient_flow:
            layer_dict = {}
            for n, p in self.named_parameters():
                if (p.requires_grad) and ("bias" not in n):
                    layer_dict[str(n)] = p

        # Loss Tracking
        losses = []
        validation_losses = []

        # setting training mode
        self.train()
        optim = torch.optim.Adam(self.parameters(), lr=lr, betas=(0.9, 0.98), eps=1e-9)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optim, "min", patience=10, factor=0.5
        )

        # train and validation Datasets and Dataloaders
        train_data = Dataset(X_train, y_train, seed=self.random_state)
        train_dl = DataLoader(train_data, batch_size=batch_size, device=device)
        val_data = Dataset(X_val, y_val, seed=self.random_state)
        val_dl = DataLoader(val_data, batch_size=batch_size, device=device)

        # Actual training
        with trange(epochs, unit="epochs") as iterable:
            for count in iterable:
                if count > 0:
                    train_data.shuffle()
                    train_dl = DataLoader(
                        train_data, batch_size=batch_size, device=device
                    )
                for count_batch, (x_b, y_b) in enumerate(train_dl):
                    optim.zero_grad()
                    p = self(x_b)
                    loss = torch.nn.functional.binary_cross_entropy(p, y_b)
                    losses.append(loss.cpu().detach().numpy())
                    loss.backward()
                    if gradient_flow:
                        for n, p in self.named_parameters():
                            if (p.requires_grad) and ("bias" not in n):
                                avg_grad = p.grad.abs().mean()
                                layer_dict[str(n)].append(
                                    avg_grad.cpu().detach().numpy()
                                )
                    optim.step()
                    if count_batch % 10 == 0:
                        x_b_val, y_b_val = iter(val_dl).__next__()
                        x_b_val = x_b_val.to(device)
                        y_b_val = y_b_val.to(device)
                        with torch.no_grad():
                            pred = self(x_b_val)
                        loss_val = torch.nn.functional.binary_cross_entropy(
                            pred, y_b_val
                        )
                        scheduler.step(loss_val)
                        validation_losses.append(loss_val.cpu().detach().numpy())
                        if verbose == 1:
                            iterable.set_description("Training")
                            iterable.set_postfix(
                                tr_loss=f"{float(losses[-1]):.4f}",
                                val_loss=f"{float(validation_losses[-1]):.4f}",
                            )
        if gradient_flow:
            return losses, validation_losses, pd.DataFrame(layer_dict)

        return losses, validation_losses

    def eval_simple(
        self,
        losses_training,
        losses_validation,
        X_validation,
        y_validation,
        threshold_pred=0.5,
        plot=True,
        device="cpu",
    ):
        """
        Evaluates the performance of the trained model.

        Args:
            losses_training (list): Training losses.
            losses_validation (list): Validation losses.
            X_validation (torch.Tensor): Validation input data.
            y_validation (torch.Tensor): Validation target labels.
            Nsamples (int, optional): Number of samples. Defaults to 1000.
            threshold_pred (float, optional): Prediction threshold. Defaults to 0.5.
            plot (bool, optional): Whether to plot the loss curves. Defaults to True.
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            dict: Dictionary containing evaluation metrics.
        """

        val_data = Dataset(X_validation, y_validation, seed=self.random_state)
        val_dl = DataLoader(val_data, batch_size=len(val_data), device=device)
        x_val, y_val = iter(val_dl).__next__()
        y_val = y_val.cpu()
        with torch.no_grad():
            pred = self(x_val)
            pred = pred.cpu()
        sterile_pred = np.where(pred > threshold_pred, 1, 0)
        gt = y_val.detach().numpy()

        if plot is not False:
            if plot[0] == "epochs":
                r = int(len(losses_training) / len(losses_validation))
                e = int(len(losses_training) / plot[1])
                x_ax_val = []
                x_ax_epochs = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                    if i % e == 0:
                        x_ax_epochs.append(i)

                fig, ax = plt.subplots(figsize=(12, 8))
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                ax.plot(
                    x_ax_val, losses_validation, linewidth=3, label="validation loss"
                )
                for c, epoch in enumerate(x_ax_epochs):
                    if c % 5 == 0:
                        ax.axvline(
                            epoch,
                            ymin=0,
                            ymax=1,
                            color="grey",
                            linestyle="--",
                            linewidth=0.5,
                        )

                ax.axvline(
                    x_ax_epochs[-1],
                    ymin=0,
                    ymax=1,
                    color="grey",
                    linestyle="--",
                    linewidth=0.5,
                    label="every fifth training epoch",
                )

                # ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

            if plot[0] == "grid":
                r = int(len(losses_training) / len(losses_validation))
                x_ax_val = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                fig, ax = plt.subplots(figsize=(12, 8))
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                ax.plot(
                    x_ax_val, losses_validation, linewidth=3, label="validation loss"
                )
                ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

        score_dict = {
            "accuracy": accuracy(gt, sterile_pred),
            "precision": precision(gt, sterile_pred),
            "recall": recall(gt, sterile_pred),
            "fall-out": fallout(gt, sterile_pred),
            "f1": f1(gt, sterile_pred),
            "threshold_roc": threshold_pred,
        }
        # accuracy(gt, sterile_pred), recall(gt, sterile_pred), precision(gt, sterile_pred), f1(gt, sterile_pred)
        return score_dict

    def model_out(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        mode="Both",
        device="cpu",
        random_state=42,
    ):
        self.eval()
        """
        Computes the model output for given test data.

        Args:
            x_sterile_test (numpy.ndarray, optional): Test input data for sterile class. Defaults to None.
            y_sterile_test (numpy.ndarray, optional): Test target labels for sterile class. Defaults to None.
            x_ref_test (numpy.ndarray, optional): Test input data for reference class. Defaults to None.
            y_ref_test (numpy.ndarray, optional): Test target labels for reference class. Defaults to None.
            mode (str, optional): Kind of spectra for which the output is calculated, possible modes: ("Both", "ref", or "ster"). Defaults to "Both".
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".
            random_state (int, optional): Random seed for reproducibility. Defaults to 42.

        Returns:
            numpy.ndarray: Model outputs for the specified mode.
        """

        if mode == "Both":
            data_s = Dataset(x_sterile_test, y_sterile_test, seed=self.random_state)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            data_r = Dataset(x_ref_test, y_ref_test, seed=self.random_state)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                out_s = self(x_s)
                out_r = self(x_r)

            return out_s.cpu().detach().numpy(), out_r.cpu().detach().numpy()

        if mode == "ref":
            data_r = Dataset(x_ref_test, y_ref_test, seed=self.random_state)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                out_r = self(x_r)

            return out_r.cpu().detach().numpy()

        if mode == "ster":
            data_s = Dataset(x_sterile_test, y_sterile_test, seed=self.random_state)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            with torch.no_grad():
                out_s = self(x_s)

            return out_s.cpu().detach().numpy()


# ===========================================================================================================================================================
# ===========================================================================================================================================================
# ===========================================================================================================================================================
#   CNNs ====================================================================================================================================================
# ===========================================================================================================================================================
# ===========================================================================================================================================================
# ===========================================================================================================================================================


class class_CNN_Base:
    """
    Simple binary classification CNN Base Class. Contains training and evaluation methods for binary classification MLPs

    Methods:
        train_simple(epochs, X_train, y_train, X_validation, y_validation, gradient_flow=False, lr=1e-3, batch_size=32, device="cpu"): Trains the MLP model.
        eval_simple(losses_training, losses_validation, X_validation, y_validation, Nsamples=1000, threshold_pred=0.5, plot=True, device="cpu"): Evaluates the performance of the trained model.
        model_out(x_sterile_test=None, y_sterile_test=None, x_ref_test=None, y_ref_test=None, mode="Both", device="cpu", random_state=42): Computes the model output for given test data.
        eval_full
    """

    def train_simple(
        self,
        X_train,
        y_train,
        X_validation,
        y_validation,
        epochs,
        scheduler=None,
        lr=1e-3,
        batch_size=32,
        device="cpu",
        verbose=1,
        seed=42,
        gradient_flow=False,
    ):
        """
        Trains the MLP model.

        Args:
            epochs (int): Number of training epochs.
            X_train (torch.Tensor): Training input data.
            y_train (torch.Tensor): Training target labels.
            X_validation (torch.Tensor): Validation input data.
            y_validation (torch.Tensor): Validation target labels.
            gradient_flow (bool, optional): Whether to compute and return gradients. Defaults to False.
            lr (float, optional): Learning rate for optimization. Defaults to 1e-3.
            batch_size (int, optional): Size of batches for training. Defaults to 32.
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            tuple: Tuple containing training losses, validation losses, and gradients if gradient_flow=True.
        """

        # assert (
        #     self.bins == X_train[0].shape[0]
        # ), f"Model input dimension ({self.bins}) doesnt match data ({X_train[0].shape[0]})!"

        optim = torch.optim.Adam(self.parameters(), lr)
        if scheduler is not None:
            sched = torch.optim.lr_scheduler.ReduceLROnPlateau(
                optim, "min", **scheduler
            )  # def: 'patience': 10, 'factor': 0.5

        train_data = Dataset(X_train, y_train, seed=seed)
        train_dl = DataLoader(train_data, batch_size=batch_size, device=device)
        val_data = Dataset(X_validation, y_validation, seed=seed)
        val_dl = DataLoader(val_data, batch_size=batch_size, device=device)
        losses = []
        validation_losses = []

        with trange(epochs, unit="epochs") as iterable:
            for count in iterable:
                if count > 0:
                    train_data.shuffle()
                    train_dl = DataLoader(
                        train_data, batch_size=batch_size, device=device
                    )
                for count_batch, (x_b, y_b) in enumerate(train_dl):
                    optim.zero_grad()
                    p = self(x_b.view((x_b.shape[0], 1, x_b[0].shape[0])))
                    loss = torch.nn.functional.binary_cross_entropy(p, y_b)
                    losses.append(loss.cpu().detach().numpy())
                    loss.backward()

                    optim.step()
                    if count_batch % 100 == 0:
                        x_b_val, y_b_val = iter(val_dl).__next__()
                        x_b_val = x_b_val.to(device)
                        y_b_val = y_b_val.to(device)
                        with torch.no_grad():
                            pred = self(
                                x_b_val.view((x_b_val.shape[0], 1, x_b_val[0].shape[0]))
                            )  # reshape not really necessary anymore
                        loss_val = torch.nn.functional.binary_cross_entropy(
                            pred, y_b_val
                        )
                        if scheduler is not None:
                            sched.step(loss_val)
                        validation_losses.append(loss_val.cpu().detach().numpy())
                        if verbose == 1:
                            iterable.set_description("Training")
                            iterable.set_postfix(
                                tr_loss=f"{float(losses[-1]):.4f}",
                                val_loss=f"{float(validation_losses[-1]):.4f}",
                            )

        return losses, validation_losses

    def eval_simple(
        self,
        losses_training,
        losses_validation,
        X_validation,
        y_validation,
        threshold_pred=0.5,
        plot=("epochs", 100),
        device="cpu",
    ):
        self.eval()
        """
        Evaluates the performance of the trained model.

        Args:
            losses_training (list): Training losses.
            losses_validation (list): Validation losses.
            X_validation (torch.Tensor): Validation input data.
            y_validation (torch.Tensor): Validation target labels.
            Nsamples (int, optional): Number of samples. Defaults to 1000.
            threshold_pred (float, optional): Prediction threshold. Defaults to 0.5.
            plot (tuple, optional): In which mode to plot the loss curve. Defaults to True.
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".

        Returns:
            dict: Dictionary containing evaluation metrics.
        """

        val_data = Dataset(X_validation, y_validation, seed=self.random_state)
        val_dl = DataLoader(val_data, batch_size=len(val_data), device=device)
        x_val, y_val = iter(val_dl).__next__()
        y_val = y_val.cpu()
        with torch.no_grad():
            pred = self(x_val.view((len(val_data), 1, x_val[0].shape[0])))
            pred = pred.cpu()
        sterile_pred = np.where(pred > threshold_pred, 1, 0)
        gt = y_val.detach().numpy()

        if plot is not False:
            if plot[0] == "epochs":
                r = int(len(losses_training) / len(losses_validation))
                e = int(len(losses_training) / plot[1])
                x_ax_val = []
                x_ax_epochs = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                    if i % e == 0:
                        x_ax_epochs.append(i)

                fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                if len(x_ax_val) == len(losses_validation):
                    ax.plot(
                        x_ax_val,
                        losses_validation,
                        linewidth=3,
                        label="validation loss",
                    )
                else:
                    ax.plot(
                        x_ax_val[:-1],
                        losses_validation,
                        linewidth=3,
                        label="validation loss",
                    )
                for c, epoch in enumerate(x_ax_epochs):
                    if c % 5 == 0:
                        ax.axvline(
                            epoch,
                            ymin=0,
                            ymax=1,
                            color="grey",
                            linestyle="--",
                            linewidth=0.5,
                        )

                ax.axvline(
                    x_ax_epochs[-1],
                    ymin=0,
                    ymax=1,
                    color="grey",
                    linestyle="--",
                    linewidth=0.5,
                    label="every fifth training epoch",
                )

                # ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

            if plot[0] == "grid":
                r = int(len(losses_training) / len(losses_validation))
                x_ax_val = []
                for i in np.arange(len(losses_training)):
                    if i % r == 0:
                        x_ax_val.append(i)
                fig, ax = plt.subplots(figsize=(12, 8))
                ax.plot(
                    np.arange(len(losses_training)),
                    losses_training,
                    label="training loss",
                )
                ax.set_yscale("log")
                ax.set_xlabel("training iterations")
                ax.set_ylabel("Loss value")
                ax.set_title("BCE Loss", weight="bold")
                ax.plot(
                    x_ax_val, losses_validation, linewidth=3, label="validation loss"
                )
                ax.grid(linestyle="--", which="both")
                ax.legend()
                fig.tight_layout()
                fig.show()

        score_dict = {
            "accuracy": accuracy(gt, sterile_pred),
            "precision": precision(gt, sterile_pred),
            "recall": recall(gt, sterile_pred),
            "fall-out": fallout(gt, sterile_pred),
            "f1": f1(gt, sterile_pred),
            "threshold_roc": threshold_pred,
        }
        # accuracy(gt, sterile_pred), recall(gt, sterile_pred), precision(gt, sterile_pred), f1(gt, sterile_pred)
        return score_dict

    def model_out(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        size=10000,
        mode="Both",
        device="cpu",
        random_state=42,
    ):
        """
        Computes the model output for given test data.

        Args:
            x_sterile_test (numpy.ndarray, optional): Test input data for sterile class. Defaults to None.
            y_sterile_test (numpy.ndarray, optional): Test target labels for sterile class. Defaults to None.
            x_ref_test (numpy.ndarray, optional): Test input data for reference class. Defaults to None.
            y_ref_test (numpy.ndarray, optional): Test target labels for reference class. Defaults to None.
            mode (str, optional): Kind of spectra for which the output is calculated, possible modes: ("Both", "ref", or "ster"). Defaults to "Both".
            device (str, optional): Device to perform computations on (e.g., "cpu" or "cuda"). Defaults to "cpu".
            random_state (int, optional): Random seed for reproducibility. Defaults to 42.

        Returns:
            numpy.ndarray: Model outputs for the specified mode.
        """
        self.eval()
        if size is not None:
            if x_sterile_test is not None:
                x_sterile_test = x_sterile_test[:size]
                y_sterile_test = y_sterile_test[:size]
            if x_ref_test is not None:
                x_ref_test = x_ref_test[:size]
                y_ref_test = y_ref_test[:size]

        if mode == "Both":
            data_s = Dataset(x_sterile_test, y_sterile_test, seed=self.random_state)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            data_r = Dataset(x_ref_test, y_ref_test, seed=self.random_state)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                out_s = self(x_s.view((len(data_s), 1, x_s[0].shape[0])))
                out_r = self(x_r.view((len(data_r), 1, x_r[0].shape[0])))

            return out_s.cpu().detach().numpy(), out_r.cpu().detach().numpy()

        if mode == "ref":
            data_r = Dataset(x_ref_test, y_ref_test, seed=self.random_state)
            x_r, y_r = data_r[:]
            x_r, y_r = torch.FloatTensor(x_r.astype(np.float64)), torch.FloatTensor(
                y_r.astype(np.float64)
            ).unsqueeze(-1)
            x_r, y_r = x_r.to(device), y_r.to(device)

            with torch.no_grad():
                out_r = self(x_r.view((len(data_r), 1, x_r[0].shape[0])))

            return out_r.cpu().detach().numpy()

        if mode == "ster":
            data_s = Dataset(x_sterile_test, y_sterile_test, seed=self.random_state)
            x_s, y_s = data_s[:]
            x_s, y_s = torch.FloatTensor(x_s.astype(np.float64)), torch.FloatTensor(
                y_s.astype(np.float64)
            ).unsqueeze(-1)
            x_s, y_s = x_s.to(device), y_s.to(device)

            with torch.no_grad():
                out_s = self(x_s.view((len(data_s), 1, x_s[0].shape[0])))

            return out_s.cpu().detach().numpy()

    def integrated_gradients(
        self, x_data, y_data, baseline=None, steps=50, device="cpu"
    ):
        self.eval()
        if baseline is None:
            baseline = np.zeros_like(x_data)

        gradients = []

        y_arr = np.zeros(steps + 1) + y_data
        scaled_inputs = np.array(
            [
                baseline + (float(i) / steps) * (x_data - baseline)
                for i in range(steps + 1)
            ]
        )
        ds = Dataset(scaled_inputs, y_arr, 42)
        dl = DataLoader(ds, batch_size=1, device=device)

        for c, (scaled_input, y) in enumerate(dl):
            scaled_input.requires_grad_(True)
            output = self(
                scaled_input.view((self.batch_size, 1, scaled_input.shape[0]))
            )
            loss = output
            loss.backward(retain_graph=True)
            gradients.append(scaled_input.grad.cpu().detach().clone())

        avg_gradients = torch.mean(torch.stack(gradients), dim=0)
        approx_int_grad = (
            torch.Tensor(x_data) - torch.Tensor(baseline)
        ) * avg_gradients

        return approx_int_grad.detach().numpy()

    def eval_full(
        self,
        x_sterile_test=None,
        y_sterile_test=None,
        x_ref_test=None,
        y_ref_test=None,
        losses_training=None,
        losses_validation=None,
        X_validation=None,
        y_validation=None,
        grads=None,
        threshold_pred=0.5,
        device="cpu",
        plot=("all", {"epochs": 100, "int_grad_spec": 100}),
    ):
        self.eval()
        score = self.eval_simple(
            losses_training,
            losses_validation,
            X_validation,
            y_validation,
            threshold_pred,
            plot=False,
            device=device,
        )
        out_s, out_r = self.model_out(
            x_sterile_test, y_sterile_test, x_ref_test, y_ref_test, device=device
        )
        int_grad_ster = self.integrated_gradients(
            x_sterile_test[plot[1]["int_grad_spec"]],
            y_sterile_test[plot[1]["int_grad_spec"]],
            device=device,
        )[0]
        int_grad_ref = self.integrated_gradients(
            x_ref_test[0], y_ref_test[0], device=device
        )[0]

        if plot[0] == "all":
            fig, (l_ax, g_ax, o_ax, i_g_ax) = plt.subplots(4, 1, figsize=(15, 30))

            # l_ax

            r = int(len(losses_training) / len(losses_validation))
            e = int(len(losses_training) / plot[1]["epochs"])
            x_ax_val = []
            x_ax_epochs = []
            for i in np.arange(len(losses_training)):
                if i % r == 0:
                    x_ax_val.append(i)
                if i % e == 0:
                    x_ax_epochs.append(i)

            l_ax.plot(
                np.arange(len(losses_training)),
                losses_training,
                label="training loss",
            )
            l_ax.set_yscale("log")
            l_ax.set_xlabel("training iterations")
            l_ax.set_ylabel("Loss value")
            l_ax.set_title("BCE Loss", weight="bold")
            l_ax.plot(x_ax_val, losses_validation, linewidth=3, label="validation loss")
            for c, epoch in enumerate(x_ax_epochs):
                if c % 5 == 0:
                    l_ax.axvline(
                        epoch,
                        ymin=0,
                        ymax=1,
                        color="grey",
                        linestyle="--",
                        linewidth=0.5,
                    )

            l_ax.axvline(
                x_ax_epochs[-1],
                ymin=0,
                ymax=1,
                color="grey",
                linestyle="--",
                linewidth=0.5,
                label="every fifth training epoch",
            )

            l_ax.legend()

            l_ax.table(
                cellText=[[k, v] for k, v in zip(score.keys(), score.values())],
                cellLoc="left",
                edges="open",
                bbox=[0.05, 0.05, 0.3, 0.3],
            )

            # g_ax
            g_ax.plot(list(grads.index.values), grads["lin1.weight"], label="lin1")
            g_ax.plot(list(grads.index.values), grads["lin2.weight"], label="lin2")
            g_ax.plot(list(grads.index.values), grads["out.weight"], label="out")
            g_ax.legend()
            g_ax.set_xlabel("training iterations")
            g_ax.set_ylabel("avg gradient")

            # o_ax
            ul = 1
            o_ax.hist(
                out_s,
                bins=100,
                range=(out_r.min(), ul),
                fill=True,
                color="r",
                alpha=0.3,
                label="Model Output w/ sterile",
            )
            o_ax.hist(
                out_r,
                bins=100,
                range=(out_r.min(), ul),
                fill=True,
                color="g",
                alpha=0.3,
                label="Reference",
            )
            o_ax.set_yscale("log")
            o_ax.set_xlabel("Model Output")
            o_ax.set_ylabel("Counts")
            o_ax.set_title("Histogram of Model Outputs", weight="bold")
            o_ax.legend()

            # i_g_ax
            i_g_ax.plot(
                int_grad_ster,
                marker="o",
                linestyle="-",
                color="b",
                markersize=8,
                linewidth=2,
                alpha=0.75,
                label="Sterile Spectrum",
            )
            i_g_ax.plot(
                int_grad_ref,
                marker="o",
                linestyle="-",
                color="g",
                markersize=8,
                linewidth=2,
                alpha=0.75,
                label="Reference Spectrum",
            )

            i_g_ax.set_title("Integrated Gradients Attributions", weight="bold")
            i_g_ax.set_xlabel("Energy Bin")
            i_g_ax.set_ylabel("Attribution Value")
            i_g_ax.grid(True, which="both", linestyle="--", linewidth=0.5)
            i_g_ax.axhline(0, color="grey", linewidth=0.8)

            i_g_ax.legend()

            fig.tight_layout()
            fig.show()


class ConvBlock(torch.nn.Module):
    def __init__(
        self,
        in_ch,
        out_ch,
        kernel_size,
        batch_norm=True,
        batch_size=32,
        stride=1,
        padding=0,
        dilation=1,
        incl_ReLU=True,
    ):  # kwargs are stride (1), padding (0) and dilation (1)
        super(ConvBlock, self).__init__()
        self.in_ch = in_ch
        self.out_ch = out_ch
        self.kernel_size = kernel_size
        self.batch_norm = batch_norm
        self.batch_size = batch_size
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        # self.padding = calculate_padding(self.kernel_size)

        self.incl_ReLU = incl_ReLU

        self.conv1 = torch.nn.Conv1d(
            self.in_ch,
            self.out_ch,
            self.kernel_size,
            self.stride,
            self.padding,
            self.dilation,
        )
        if self.batch_norm:
            self.batch_norm = torch.nn.BatchNorm1d(self.out_ch)
        if incl_ReLU:
            self.ReLU = torch.nn.ReLU()

    def forward(self, x):
        out = self.conv1(x)
        if self.batch_norm:
            out = self.batch_norm(out)
        if self.incl_ReLU:
            out = self.ReLU(out)
        return out


class FCN(torch.nn.Module, class_CNN_Base):
    def __init__(
        self, batch_size, learning_rate=1e-3, random_state=42, **layer_kwargs
    ) -> None:
        super(FCN, self).__init__()

        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.layer_kwargs = layer_kwargs
        self.random_state = random_state

        self.conv_layers = torch.nn.ModuleList(
            [
                ConvBlock(batch_size=self.batch_size, **layer_kwargs[str(i)])
                for i in range(len(layer_kwargs))
            ]
        )
        self.AvgPool = torch.nn.AdaptiveAvgPool1d(1)
        self.ff = torch.nn.Linear(layer_kwargs[str(len(layer_kwargs) - 1)]["out_ch"], 1)
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x):

        for layer in self.conv_layers:
            x = layer(x)

        avg = self.AvgPool(x).view(
            x.shape[0], self.layer_kwargs[str(len(self.layer_kwargs) - 1)]["out_ch"]
        )

        ff_out = self.ff(avg)
        out = self.sigmoid(ff_out)

        return out


class ResNetBlock(torch.nn.Module):
    def __init__(self, batch_size, **layer_kwargs):
        super(ResNetBlock, self).__init__()
        self.batch_size = batch_size
        self.conv_blocks = torch.nn.ModuleList(
            [
                ConvBlock(batch_size=self.batch_size, **layer_kwargs[str(i)])
                for i in range(len(layer_kwargs) - 1)
            ]
        )
        self.conv_blocks.append(
            ConvBlock(
                batch_size=self.batch_size,
                incl_ReLU=False,
                **layer_kwargs[str(len(layer_kwargs) - 1)],
            )
        )  # last block shouldnt have relu as first the residual connection is added
        self.relu = torch.nn.ReLU()

    def forward(self, x):
        inp = x
        for block in self.conv_blocks:
            x = block(x)
        return self.relu(x + inp)


class ResNet(torch.nn.Module, class_CNN_Base):
    def __init__(
        self, batch_size, learning_rate=1e-3, random_state=42, **resnet_kwargs
    ) -> None:
        super(ResNet, self).__init__()

        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.resnet_kwargs = resnet_kwargs
        self.random_state = random_state

        self.resnet_blocks = torch.nn.ModuleList(
            [
                ResNetBlock(self.batch_size, **self.resnet_kwargs[str(i)])
                for i in range(len(self.resnet_kwargs))
            ]
        )
        self.AvgPool = torch.nn.AdaptiveAvgPool1d(1)
        self.ff = torch.nn.Linear(
            self.resnet_kwargs[str(len(self.resnet_kwargs) - 1)][
                str(len(self.resnet_kwargs[str(len(self.resnet_kwargs) - 1)]) - 1)
            ]["out_ch"],
            1,
        )
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x):

        for block in self.resnet_blocks:
            x = block(x)

        avg = self.AvgPool(x).view(
            x.shape[0],
            self.resnet_kwargs[str(len(self.resnet_kwargs) - 1)][
                str(len(self.resnet_kwargs[str(len(self.resnet_kwargs) - 1)]) - 1)
            ]["out_ch"],
        )

        ff_out = self.ff(avg)
        out = self.sigmoid(ff_out)

        return out


def init_resnet_dict(ch_dims, kernel_sizes, num_blocks):

    def calculate_padding(kernel_size):
        # Ensure padding calculation works only for odd kernel sizes
        if kernel_size % 2 == 0:
            raise ValueError(
                "Kernel size must be an odd number to maintain same spatial dimensions."
            )
        return (kernel_size - 1) // 2

    # assert len(ch_dims) == num_blocks, f"input sizes dont match! ch_dims {len(ch_dims)}, kernel sizes {len(kernel_sizes)}, num blocks {num_blocks}"
    block_dict = {}
    for n_block in range(num_blocks):
        if n_block == 0:
            block = {
                "0": {
                    "in_ch": 1,
                    "out_ch": ch_dims[0],
                    "kernel_size": kernel_sizes[0],
                    "batch_norm": True,
                    "padding": calculate_padding(kernel_sizes[0]),
                },
                "1": {
                    "in_ch": ch_dims[0],
                    "out_ch": ch_dims[1],
                    "kernel_size": kernel_sizes[1],
                    "batch_norm": True,
                    "padding": calculate_padding(kernel_sizes[1]),
                },
                "2": {
                    "in_ch": ch_dims[1],
                    "out_ch": ch_dims[2],
                    "kernel_size": kernel_sizes[2],
                    "batch_norm": True,
                    "padding": calculate_padding(kernel_sizes[2]),
                },
            }
        else:
            block = {
                "0": {
                    "in_ch": ch_dims[2],
                    "out_ch": ch_dims[0],
                    "kernel_size": kernel_sizes[0],
                    "batch_norm": True,
                    "padding": calculate_padding(kernel_sizes[0]),
                },
                "1": {
                    "in_ch": ch_dims[0],
                    "out_ch": ch_dims[1],
                    "kernel_size": kernel_sizes[1],
                    "batch_norm": True,
                    "padding": calculate_padding(kernel_sizes[1]),
                },
                "2": {
                    "in_ch": ch_dims[1],
                    "out_ch": ch_dims[2],
                    "kernel_size": kernel_sizes[2],
                    "batch_norm": True,
                    "padding": calculate_padding(kernel_sizes[2]),
                },
            }

        block_dict[str(n_block)] = block
    return block_dict
