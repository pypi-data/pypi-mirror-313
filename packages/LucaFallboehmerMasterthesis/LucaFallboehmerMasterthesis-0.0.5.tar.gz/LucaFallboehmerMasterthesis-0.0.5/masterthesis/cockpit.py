"""Contains the Macro Control Class used to train and evaluate models. For a usage guide and more elaborate examples see the Experiment_Control or Cookbook Notebooks"""

import os
import logging
import json
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


# from constants import *
# from beta_gen import *
# from models import *
# from dataset import *
# from model_eval import *
# from model_pipeline import *

# if USE_NUMBA_JIT:
#     from beta_decay_jit import *

#     print("using numbas jit compilation")
# else:
#     from beta_decay import *

from .constants import *
from .beta_decay import *
from .beta_gen import *
from .models import *
from .dataset import *
from .model_eval import *
from .model_pipeline import *


class Macro_Control:
    """
    Macro_Control manages the training, evaluation, and scanning of models based on provided parameters and plans.

    Attributes:
    -----------
        spectra_init_dict (dict):
            Initial spectrum parameters for training.
        model_init_dict (dict):
            Initial model parameters.
        scan_init_dict (dict):
            Initial scanning parameters.
        dataset_plan (dict):
            Plan for training dataset updates. Each parameter of the spectra contained in the dataset used for training that shoud be changed should be included as a corresponding {key: value} pair, and value = [value_subrun1, value_subrun2, value_subrun3, ...]
        training_plan (dict):
            Plan for training updates. Each parameter of the model iteself that shoud be changed should be included as a corresponding {key: value} pair, and value = [value_subrun1, value_subrun2, value_subrun3, ...]
        scanning_plan (dict):
            Plan for scanning dataset updates. Each parameter of the spectra contained in the dataset used for scanning that shoud be changed needs to be included as a corresponding {key: value} pair, with value = [value_subrun1, value_subrun2, value_subrun3, ...]
        num_models (int):
            Number of models to train and evaluate. Should match with the provided dataset and scanning plans i.e. num_models == len(dataset_plan[key]) for all keys (provided it is desired to incorporate all the values in your run)
        device (str):
            Device to run the models on, default is "cpu".
        run_name (str):
            Name of the current run, default is "initialization". This should not be changed from the default.
        verbose (int):
            Level of verbosity for logging and printing, default is 1.
        log_name (str):
            Name of the log file, default is "logging.log".
        seed (int):
            Seed for random number generation, default is 42.
        data_path (str):
            Path to store data and model weights, default is "../../../../Data/Run1".

    Methods:
    --------
        __getattr__(name: str):
            Get the value of an attribute dynamically.

        __setattr__(name, value):
            Set the value of an attribute dynamically and update number of bins if bin_width is set.

        update_dataset():
            Update dataset parameters based on the current run number.

        update_scanning():
            Update scanning parameters based on the current run number.

        update_training():
            Update training parameters based on the current run number.

        update_run(name: str):
            Update the run number and name, and refresh dataset, scanning, and training parameters.

        make_spectrum_dict() -> dict:
            Create a dictionary of current spectrum parameters.

        make_scanning_dict() -> dict:
            Create a dictionary of current scanning parameters.

        init_scan():
            Initialize scanning parameters.

        initialize_model() -> model:
            Initialize and return a new model based on the current parameters.

        load_model() -> model:
            Load and return a model from the saved state.

        save_contour(scan: dict):
            Save contour data from a scan.

        generate_data(mode="training") -> dict:
            Generate data for training or evaluation.

        conduct_trainings():
            Conduct the training of models based on the current plan.

        conduct_evaluation():
            Conduct the evaluation of models using a grid search based on the current plan.

        get_model_names(directory_path: str) -> list:
            Get a list of model file names in the specified directory.

        plot_contours(which_chisq=["stat_cov", "stat_fit", "sf_cov", "sf_fit"], path_to_chisq="../../../../Data/data/", plot_range=((1e-8, 1e-2), (0, 18.6)), errorbars=False, path_to_models=None, contours_individually=False):
            Plot the exclusion contours for the models and chisq scans.


        Examples:
        ---------
            For model initialization, use e.g.: {"model_architecture": "MLP", "epochs": 20, "lr": 1e-3, "bs": 5000, "nhidden": 256} (placeholder values, change however you see fit)

            training_plan = {"epochs": [20, 30, 40], "bs": [25000, 30000, 40000]}
            dataset_plan = {"bin_width": [30, 100, 300]}
            scanning_plan = dataset_plan

            The Resulting trainings will be:
                1. Model trained for 20 epochs w/ a batch size of 25000 on data with a bin width of 30 eV
                2. Model trained for 30 epochs w/ a batch size of 30000 on data with a bin width of 100 eV
                3. Model trained for 40 epochs w/ a batch size of 40000 on data with a bin width of 300 eV

            The rest of the parameters of the datasets and models will stay consistent throughout the process.

            To run the trainings, use the conduct_trainings() method
            To run the evaluation, use the conduct_evaluation() method
            To plot your results, use the plot_contours(path_to_model_weights_file) method, providing the path to your model weights
    """

    def __init__(
        self,
        spectra_init_dict,
        model_init_dict,
        scan_init_dict,
        dataset_plan,
        training_plan,
        scanning_plan,
        num_models,
        device="cpu",
        run_name="initialization",
        verbose=1,
        log_name="logging.log",
        seed=42,
        data_path="../../../../Data/Run1",
        mode="Normal",
    ):
        """Initiates macro parameters"""
        if mode != "Plot":
            os.mkdir(data_path)
            os.mkdir(data_path + "/model_weights")
            os.mkdir(data_path + "/contours")
            os.mkdir(data_path + "/losses")
            os.mkdir(data_path + "/data_dicts")
            logging.basicConfig(
                filename=data_path + "/" + log_name,
                level=logging.INFO,
                format="%(asctime)s - %(message)s",
            )

        self.seed = seed
        self.data_path = data_path

        # Spectrum Parameters: Training Focussed
        self.bins, self.bins0 = spectra_init_dict["bins"], spectra_init_dict["bins"]
        self.ekin_min = spectra_init_dict["ekin_min"]
        self.ekin_max = spectra_init_dict["ekin_max"]
        self.bin_width = spectra_init_dict["bin_width"]
        self.num_sterile_vals = spectra_init_dict["num_sterile_vals"]
        self.num_spec_it = spectra_init_dict["num_spec_it"]
        self.m_sterile_min = spectra_init_dict["m_sterile_min"]
        self.m_sterile_max = spectra_init_dict["m_sterile_max"]
        self.sin2theta_log_min = spectra_init_dict["sin2theta_log_min"]
        self.sin2theta_log_max = spectra_init_dict["sin2theta_log_max"]
        self.m_neutrino = spectra_init_dict["m_n"]
        self.smallterms = spectra_init_dict["smallterms"]
        self.mod_dict = spectra_init_dict["mod_dict"]

        # Spectrum Parameters: Evaluation Focussed (placeholder values, run init_scan to update)
        self.scan_init_dict = scan_init_dict
        self.num_sin2theta_scan = 100
        self.num_spec_scan = 100
        self.model_type = "vanilla"
        self.contour_method = "default"

        # Model Parameters
        self.device = device
        self.model_architecture = model_init_dict["model_architecture"]
        self.epochs = model_init_dict["epochs"]
        self.lr = model_init_dict["lr"]
        self.scheduler = model_init_dict["scheduler"]
        self.bs = model_init_dict["bs"]
        self.model_name = ""
        self.num_models = num_models

        # Additional Model Parameters Transformer
        if self.model_architecture == "Transformer":
            self.d_model = model_init_dict["d_model"]
            self.d_ff = model_init_dict["d_ff"]
            self.out_dim = model_init_dict["out_dim"]
            self.num_layers = model_init_dict["num_layers"]
            self.dropout = model_init_dict["dropout"]
        else:
            self.nhidden = model_init_dict["nhidden"]

        if self.model_architecture == "CNN":
            self.lay_dict = model_init_dict["lay_dict"]

        if self.model_architecture == "Reg_MLP":
            self.reg_dict = model_init_dict["reg_dict"]

        if self.model_architecture == "Reg_PMLP":
            self.reg_dict = model_init_dict["reg_dict"]

        if self.model_architecture == "ResNet":
            self.resnet_dict = model_init_dict["resnet_dict"]

        if self.model_architecture == "ResMLP":
            self.resmlp_parametrized = model_init_dict["parametrized"]
            self.resmlp_num_params = model_init_dict["num_params"]
            self.resmlp_dict = model_init_dict["resmlp_dict"]

        # Dataset Plan
        self.dataset_plan = dataset_plan

        # Training Plan
        self.training_plan = training_plan

        # Scanning Plan
        self.scanning_plan = scanning_plan

        # Experiment State Tracking
        self.run_number = 0
        self.run_name = run_name
        self.model_names = []
        self.scanning = False

        # Verbosity
        self.verbose = verbose

    def __getattr__(self, name: str):
        return self.__dict__[f"_{name}"]

    def __setattr__(self, name, value):
        self.__dict__[f"_{name}"] = value

        # Automatically also update number of bins when setting bin_width
        if name == "bin_width":
            self.bins = int((self.ekin_max - self.ekin_min) / self.bin_width)

    def update_dataset(self):
        if self.dataset_plan is not None:
            n = self.run_number
            for key in self.dataset_plan.keys():
                if self.verbose >= 1:
                    print(f"Dataset: {key} -> {self.dataset_plan[key][n]}")
                setattr(self, key, self.dataset_plan[key][n])
                # if key == "mod_dict":
                #     if self.dataset_plan[key][n] is not None:
                #         for mod_key in self.dataset_plan[key][n].keys():
                #             if mod_key == "PAE":
                #                 self.bins = int((self.dataset_plan[key][n][mod_key][1][1] - self.dataset_plan[key][n][mod_key][1][0]) / self.bin_width)

                # logging changes
                if isinstance(self.dataset_plan[key][n], np.ndarray):
                    logging.info(f"Updated {key} to {n}th value")
                else:
                    logging.info(f"Updated {key} to {self.dataset_plan[key][n]}")

    def update_scanning(self):
        if self.scanning_plan is not None:
            n = self.run_number
            for key in self.scanning_plan.keys():
                if self.verbose >= 1:
                    print(f"Scanning: {key} -> {self.scanning_plan[key][n]}")
                setattr(self, key, self.scanning_plan[key][n])
                # if key == "mod_dict":
                #     if self.scanning_plan[key][n] is not None:
                #         for mod_key in self.scanning_plan[key][n].keys():
                #             if mod_key == "PAE":
                #                 self.bins = int((self.scanning_plan[key][n][mod_key][1][1] - self.scanning_plan[key][n][mod_key][1][0]) / self.bin_width)

                # logging changes
                if isinstance(self.scanning_plan[key][n], np.ndarray):
                    logging.info(f"Updated {key} to {n}th value")
                else:
                    logging.info(f"Updated {key} to {self.scanning_plan[key][n]}")

    def update_training(self):
        n = self.run_number
        for key in self.training_plan.keys():
            if self.verbose >= 1:
                print(f"{key} -> {self.training_plan[key][n]}")
            setattr(self, key, self.training_plan[key][n])

            # logging changes
            if isinstance(self.training_plan[key][n], np.ndarray):
                logging.info(f"Updated {key} to {n}th value")
            else:
                logging.info(f"Updated {key} to {self.training_plan[key][n]}")

    def update_run(self, name: str):
        "Should be run once directly after initialization and then every time a run finishes"
        if self.verbose >= 1:
            print(
                f"====================== Finished Run Number: {self.run_number} | {self.run_name}, Starting next Run: {self.run_number + 1} | {name} ======================"
            )

        # logging
        logging.info(
            f"====================== Finished Run Number: {self.run_number} | {self.run_name}, Starting next Run: {self.run_number + 1} | {name} ======================"
        )

        self.update_dataset()
        if self.scanning:
            self.update_scanning()
        self.update_training()
        self.run_number += 1
        self.run_name = name

    def make_spectrum_dict(self):
        return {
            "bins": self.bins,
            "bin_width": self.bin_width,
            "ekin_min": self.ekin_min,
            "ekin_max": self.ekin_max,
            "num_sterile_vals": self.num_sterile_vals,
            "num_spec_it": self.num_spec_it,
            "m_sterile_min": self.m_sterile_min,
            "m_sterile_max": self.m_sterile_max,
            "sin2theta_log_min": self.sin2theta_log_min,
            "sin2theta_log_max": self.sin2theta_log_max,
            "m_n": self.m_neutrino,
            "smallterms": self.smallterms,
            "mod_dict": self.mod_dict,
        }

    def make_scanning_dict(self):
        return {
            "bins": self.bins,
            "bin_width": self.bin_width,
            "ekin_min": self.ekin_min,
            "ekin_max": self.ekin_max,
            "num_sterile_vals": self.num_sterile_vals,
            "num_spec_it": self.num_spec_it,
            "m_sterile_min": self.m_sterile_min,
            "m_sterile_max": self.m_sterile_max,
            "sin2theta_log_min": self.sin2theta_log_min,
            "sin2theta_log_max": self.sin2theta_log_max,
            "m_n": self.m_neutrino,
            "smallterms": self.smallterms,
            "mod_dict": self.mod_dict,
            "num_sin2theta_scan": self.num_sin2theta_scan,
            "num_spec_scan": self.num_spec_scan,
            "model_type": self.model_type,
            "contour_method": self.contour_method,
        }

    def init_scan(self):
        for key in self.scan_init_dict.keys():
            setattr(self, key, self.scan_init_dict[key])

    def initialize_model(self):
        spectrum_parameters = self.make_spectrum_dict()
        bins_prev = self.bins

        for key in spectrum_parameters:
            if key == "mod_dict":
                if spectrum_parameters[key] is not None:
                    for mod_key in spectrum_parameters[key].keys():
                        if mod_key == "PAE":
                            self.bins = int(
                                (
                                    spectrum_parameters[key][mod_key][1][1]
                                    - spectrum_parameters[key][mod_key][1][0]
                                )
                                / self.bin_width
                            )
                        if mod_key == "multi_scale_fourier_encoding":
                            self.bins = self.bins0 + (
                                2
                                * spectrum_parameters[key][mod_key][0].shape[1]
                                * len(spectrum_parameters[key][mod_key])
                            )
                            print(self.bins, self.bins0)

        print("Init model", spectrum_parameters)
        logging.info(f"Created {self.model_architecture}: {self.model_name}")
        if self.model_architecture == "MLP":
            self.model_name = model_name_constructor(
                self.run_number,
                spectrum_parameters,
                self.nhidden,
                self.epochs,
                self.bs,
                self.lr,
                additional_info=f"{self.run_name}",
            )
            model = class_MLP(
                bins=self.bins,
                hidden_dim=self.nhidden,
                batch_size=self.bs,
                learning_rate=self.lr,
                random_state=self.seed,
                scheduler=self.scheduler,
            ).to(self.device)
        if self.model_architecture == "Parametrized_MLP":
            self.model_name = model_name_constructor(
                self.run_number,
                spectrum_parameters,
                self.nhidden,
                self.epochs,
                self.bs,
                self.lr,
                additional_info=f"parametrized_{self.run_name}",
            )
            model = class_MLP_parametrized(
                bins=self.bins,
                params=2,
                hidden_dim=self.nhidden,
                batch_size=self.bs,
                learning_rate=self.lr,
                scheduler=self.scheduler,
                random_state=self.seed,
            ).to(self.device)
        if self.model_architecture == "Transformer":
            self.model_name = model_name_constructor(
                self.run_number,
                spectrum_parameters,
                0,  # need fix for this (need to provide nhidden)
                self.epochs,
                self.bs,
                self.lr,
                model_type="Transformer",
                transformer={"lr": self.lr},
                additional_info=f"{self.run_name}",
            )
            model = self_attn_mlp(
                input_bins=self.bins,
                d_model=self.d_model,
                d_ff=self.d_ff,
                out_dim=self.out_dim,
                num_layers=self.num_layers,
                dropout=self.dropout,
                random_state=self.seed,
                batch_size=self.bs,
                learning_rate=self.lr,
                scheduler=self.scheduler,
            ).to(self.device)
        if self.model_architecture == "CNN":
            self.model_name = model_name_constructor(
                self.run_number,
                spectrum_parameters,
                epochs=self.epochs,
                bs=self.bs,
                lr=self.lr,
                cnn=self.lay_dict,
            )
            model = FCN(
                batch_size=self.bs,
                learning_rate=self.lr,
                **self.lay_dict,
            ).to(self.device)

        if self.model_architecture == "ResNet":
            self.model_name = model_name_constructor(
                self.run_number,
                spectrum_parameters,
                epochs=self.epochs,
                bs=self.bs,
                lr=self.lr,
                resnet=self.resnet_dict,
            )
            model = ResNet(
                batch_size=self.bs,
                learning_rate=self.lr,
                **self.resnet_dict,
            ).to(self.device)

        if self.model_architecture == "ResMLP":
            print(self.resmlp_dict)
            self.model_name = model_name_constructor(
                self.run_number,
                spectrum_parameters,
                epochs=self.epochs,
                bs=self.bs,
                lr=self.lr,
                resnet=self.resmlp_dict,
            )
            model = ResMLP(
                bins=self.bins,
                batch_size=self.bs,
                lr=self.lr,
                parametrized=self.resmlp_parametrized,
                num_params=self.resmlp_num_params,
                **self.resmlp_dict,
            ).to(self.device)

        if self.model_architecture == "Reg_MLP":
            self.model_name = model_name_constructor(
                self.run_number,
                spectrum_parameters,
                epochs=self.epochs,
                bs=self.bs,
                lr=self.lr,
                mlp=self.reg_dict,
            )
            model = class_MLP_reg(
                bins=self.bins, batch_size=self.bs, **self.reg_dict
            ).to(self.device)

        if self.model_architecture == "Reg_PMLP":
            self.model_name = model_name_constructor(
                self.run_number,
                spectrum_parameters,
                epochs=self.epochs,
                bs=self.bs,
                lr=self.lr,
                mlp=self.reg_dict,
                parametrized=True,
            )
            model = class_PMLP_reg(
                bins=self.bins, batch_size=self.bs, **self.reg_dict
            ).to(self.device)

        if self.model_architecture != "Transformer":
            init_weights(model, bias=True)

        # if pae:
        #     self.bins = bins_prev
        self.bins = self.bins0
        return model

    def load_model(self):
        spectrum_parameters = self.make_scanning_dict()
        bins_prev = self.bins

        # recalculate the needed number of bins
        for key in spectrum_parameters:
            if key == "mod_dict":
                if spectrum_parameters[key] is not None:
                    for mod_key in spectrum_parameters[key].keys():
                        if mod_key == "PAE":
                            self.bins = int(
                                (
                                    spectrum_parameters[key][mod_key][1][1]
                                    - spectrum_parameters[key][mod_key][1][0]
                                )
                                / self.bin_width
                            )
                            pae = True
                        if mod_key == "multi_scale_fourier_encoding":
                            self.bins = self.bins0 + (
                                2
                                * spectrum_parameters[key][mod_key][0].shape[1]
                                * len(spectrum_parameters[key][mod_key])
                            )

        if self.model_architecture == "MLP":
            model = class_MLP(
                bins=self.bins,
                hidden_dim=self.nhidden,
                batch_size=self.bs,
                learning_rate=self.lr,
                scheduler=self.scheduler,
                random_state=self.seed,
            ).to(self.device)
        if self.model_architecture == "Parametrized_MLP":
            model = class_MLP_parametrized(
                bins=self.bins,
                params=2,
                hidden_dim=self.nhidden,
                batch_size=self.bs,
                learning_rate=self.lr,
                scheduler=self.scheduler,
                random_state=self.seed,
            ).to(self.device)
        if self.model_architecture == "Transformer":
            model = self_attn_mlp(
                input_bins=self.bins,
                d_model=self.d_model,
                d_ff=self.d_ff,
                out_dim=self.out_dim,
                num_layers=self.num_layers,
                dropout=self.dropout,
                random_state=self.seed,
                batch_size=self.bs,
                learning_rate=self.lr,
                scheduler=self.scheduler,
            ).to(self.device)
        if self.model_architecture == "CNN":
            model = FCN(
                batch_size=self.bs,
                learning_rate=self.lr,
                **self.lay_dict,
            ).to(self.device)
        if self.model_architecture == "ResNet":
            model = ResNet(
                batch_size=self.bs,
                learning_rate=self.lr,
                **self.resnet_dict,
            ).to(self.device)
        if self.model_architecture == "ResMLP":
            model = ResMLP(
                bins=self.bins,
                batch_size=self.bs,
                lr=self.lr,
                parametrized=self.resmlp_parametrized,
                num_params=self.resmlp_num_params,
                **self.resmlp_dict,
            ).to(self.device)
        if self.model_architecture == "Reg_MLP":
            model = class_MLP_reg(
                bins=self.bins, batch_size=self.bs, **self.reg_dict
            ).to(self.device)
        if self.model_architecture == "Reg_PMLP":
            model = class_PMLP_reg(
                bins=self.bins, batch_size=self.bs, **self.reg_dict
            ).to(self.device)

        model.load_state_dict(
            torch.load(
                self.data_path
                + "/model_weights/"
                + self.model_names[self.run_number - 1]
            )
        )
        print(
            self.data_path + "/model_weights/" + self.model_names[self.run_number - 1]
        )
        # if pae:
        #     self.bins = bins_prev
        self.bins = self.bins0  # unnecessary
        return model

    def save_contour(self, scan):
        np.save(
            self.data_path
            + "/contours/"
            + self.model_names[self.run_number - 1]
            + "_contour_s2t_95CL",
            scan["contour_s2t"],
        )
        np.save(
            self.data_path
            + "/contours/"
            + self.model_names[self.run_number - 1]
            + "_contour_ms_95CL",
            scan["contour_ms"],
        )
        # np.save(                                      # TODO: Uncomment this
        #     self.data_path
        #     + "/contours/"
        #     + self.model_names[self.run_number - 1]
        #     + "_contour_s2t_err_95CL",
        #     scan["contour_s2t_err"],
        # )

    def save_data_dicts(self, data_dict):
        def convert_ndarray_to_list(obj):
            # Check if obj is a dictionary
            if isinstance(obj, dict):
                return {
                    key: convert_ndarray_to_list(value) for key, value in obj.items()
                }
            # Check if obj is a list
            elif isinstance(obj, list):
                return [convert_ndarray_to_list(item) for item in obj]
            # Check if obj is a numpy array
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            # Return the object itself if it's not a dictionary, list, or ndarray
            else:
                return obj

        # handle numpy arrays
        converted_dict = convert_ndarray_to_list(data_dict)

        if self.scanning:
            with open(
                self.data_path + "/data_dicts/" + self.run_name + "scanning.json",
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(converted_dict, f, ensure_ascii=False, indent=4)
        else:
            with open(
                self.data_path + "/data_dicts/" + self.run_name + "training.json",
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(converted_dict, f, ensure_ascii=False, indent=4)

    def save_scan_dict(self, scan_dict):
        def convert_ndarray_to_list(obj):
            # Check if obj is a dictionary
            if isinstance(obj, dict):
                return {
                    key: convert_ndarray_to_list(value) for key, value in obj.items()
                }
            # Check if obj is a list
            elif isinstance(obj, list):
                return [convert_ndarray_to_list(item) for item in obj]
            # Check if obj is a numpy array
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            # Return the object itself if it's not a dictionary, list, or ndarray
            else:
                return obj

        # handle numpy arrays
        converted_dict = convert_ndarray_to_list(scan_dict)

        with open(
            self.data_path + "/" + self.run_name + "scan_dict.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(converted_dict, f, ensure_ascii=False, indent=4)

    def generate_data(self, mode="training"):
        spectrum_parameters = self.make_spectrum_dict()
        self.save_data_dicts(spectrum_parameters)
        print("Gen Data", spectrum_parameters)
        logging.info(f"Generating data with parameters: {spectrum_parameters}")

        if (
            self.model_architecture == "Parametrized_MLP"
            or self.model_architecture == "Reg_PMLP"
        ):
            parametrized = True

        elif self.model_architecture == "ResMLP":
            if self.resmlp_parametrized:

                parametrized = True

        else:
            parametrized = False

        return data_gen_pipeline(
            spectrum_parameters, "MLP", parametrized=parametrized, only_train_val=True
        )

    def conduct_trainings(self):
        self.update_run(name=f"subrun{0}")

        if self.dataset_plan == None:
            if self.verbose >= 1:
                print(
                    f"============ Starting Data Generation for {self.model_architecture} ==============="
                )
            training_data = self.generate_data()

        for run in range(self.num_models):
            if self.dataset_plan is not None:
                if self.verbose >= 1:
                    print(
                        f"============ Starting Data Generation for {self.model_architecture} ==============="
                    )
                training_data = self.generate_data()
            # Training of Model
            if self.verbose >= 1:
                print(
                    f"============ Starting Training of {self.model_architecture} ==============="
                )
            model = self.initialize_model()

            l, l_val = model.train_simple(
                *training_data,
                epochs=self.epochs,
                batch_size=model.batch_size,
                lr=model.learning_rate,
                device=self.device,
                # gradient_flow=False,
                verbose=1,
            )
            self.model_names.append(
                self.model_name[14:]
            )  # dont want to include the 'model_weights/' part
            torch.save(model.state_dict(), self.data_path + "/" + self.model_name)
            self.plot_losses(l, l_val)
            logging.info(f"saved model: {self.data_path + '/' + self.model_name}")

            if torch.cuda.is_available():
                torch.cuda.empty_cache()

            if torch.backends.mps.is_available():
                torch.mps.empty_cache()

            if self.run_number < self.num_models:
                self.update_run(name=f"subrun{run+1}")

    def conduct_evaluation(
        self, use_interpolation=False, num_gp=20, show_fits=False, **interpolation_dict
    ):
        logging.info(
            f"============================== Now starting Evaluation =============================="
        )
        self.scanning = True
        # Set run number back to zero
        self.run_number = 0
        # Initialize the scan dictionairy
        self.init_scan()
        # Start first run
        self.update_run(name=f"subrun{0}")

        for run in range(self.num_models):
            # Get scanning dict
            scan_dict = self.make_scanning_dict()

            print("here:")
            print(scan_dict["mod_dict"])

            self.save_data_dicts(scan_dict)
            # Load Model
            model = self.load_model()
            # Start search
            if self.verbose >= 1:
                print(
                    f"============ Starting Gridscan of {self.model_architecture} | Subrun {run} ==============="
                )
            GS = Gridsearch(
                model=model,
                scan_spectra_df=None,
                scan_dict=scan_dict,
                CL=95,
                device=self.device,
                gen_data_on_the_fly=True,
            )
            # if use_interpolation:
            #     print(show_fits)
            #     scan_res = GS.gridscan_custom_gp(num_gp)
            #     scan = GS.contour_interpolation(
            #         scan_res, plot_fits=show_fits, **interpolation_dict
            #     )
            # else:
            #     scan = GS.gridscan_full(
            #         errorbars=False,
            #         verbose=self.verbose,
            #         method=self.contour_method,
            #     )  # TODO: Turn errorbars back on eventually (UPDATE: Change to Bootstrapping)
            scan = GS.gridscan_full(
                errorbars=False,
                verbose=self.verbose,
                method=self.contour_method,
            )  # TODO: Turn errorbars back on eventually (UPDATE: Change to Bootstrapping)
            if use_interpolation:
                ci = ContourInterpolation(
                    scan_data=scan,
                )
                _, scan["contour_s2t"] = ci.contour_int_simple()

            self.save_contour(scan)
            self.save_scan_dict(scan)
            logging.info(
                f"saved contour: {self.data_path + '/contours/' + self.model_names[self.run_number-1][14:]}"
            )
            if self.run_number < self.num_models:
                self.update_run(name=f"subrun{run+1}")

    def conduct_full_run(self, interp_dict=None, show_fits=False, **plot_kwargs):
        self.conduct_trainings()
        if interp_dict is not None:
            self.conduct_evaluation(
                use_interpolation=True, show_fits=show_fits, **interp_dict
            )
        else:
            self.conduct_evaluation()
        self.plot_contours(
            path_to_models=self.data_path + "/model_weights/", **plot_kwargs
        )

    def get_model_names(self, directory_path):
        """
        Get a list of file names in the specified directory.

        Args:
            directory_path (str): The path to the directory.

        Returns:
            list: A list of file names in the directory.
        """
        try:
            # List all entries in the directory
            entries = os.listdir(directory_path)

            # Filter out directories, only keep files
            self.model_names = [
                entry
                for entry in entries
                if os.path.isfile(os.path.join(directory_path, entry))
            ]

        except FileNotFoundError:
            print(f"The directory {directory_path} does not exist.")
            return []
        except PermissionError:
            print(f"Permission denied to access the directory {directory_path}.")
            return []

    def add_log(self, log: str):
        logging.info(log)

    def plot_contours(
        self,
        which_chisq=["stat_cov", "_fit", "_sf_10", "_fit_sf"],
        path_to_chisq="../../../../Data/data/",
        plot_range=((1e-8, 1e-2), (0, 18.6)),
        errorbars=False,
        path_to_models=None,
        contours_individually=False,
        scan_titles=None,
        context="talk",
        palette="husl",
    ):
        list_of_scans = []
        if scan_titles == None:
            scan_titles_final = []
        else:
            scan_titles_final = scan_titles

        # Loading in Chisq Contours
        for entry in which_chisq:
            if entry == "stat_cov":
                scan_chisq_load = load_contour(path_to_chisq, "ChiSqScan", errors=False)
                list_of_scans.append(scan_chisq_load)
                if scan_titles == None:
                    scan_titles_final.append("$\chi^2$ - stat only, covariance")
            else:
                scan_chisq_load = load_contour(
                    path_to_chisq, "ChiSqScan", appendix=entry, errors=False
                )
                list_of_scans.append(scan_chisq_load)
                if scan_titles == None:
                    scan_titles_final.append(f"$\chi^2$ - {entry}")

        # If this is ran independently, need to get the model contour names that should be plotted first
        if path_to_models is not None:
            self.get_model_names(path_to_models)

        for model_name in self.model_names:
            scan_model_load = load_contour(
                self.data_path + "/contours/", model_name, errorbars
            )
            list_of_scans.append(scan_model_load)
            if scan_titles == None:
                scan_titles_final.append(model_name)

        if contours_individually:
            # Set the Seaborn style
            # sns.set(style="whitegrid", context=context)

            # Define a color palette
            palette = sns.color_palette(palette, len(list_of_scans))

            for count, scan in enumerate(list_of_scans[len(which_chisq) :]):

                fig, ax = plt.subplots(figsize=(11, 8))

                for scan in list_of_scans[: len(which_chisq) + 1]:
                    ax.plot(
                        scan["contour_ms"] / 1000,
                        scan["contour_s2t"],
                        label=scan_titles_final[count],
                        color=palette[count],
                    )

                # Account for offset in count
                count += len(which_chisq)
                # Plot the contour line
                ax.plot(
                    scan["contour_ms"] / 1000,
                    scan["contour_s2t"],
                    label=scan_titles_final[count],
                    color=palette[count],
                )

                # Plot error bars if they exist
                if errorbars:
                    for key in scan.keys():
                        if key == "contour_s2t_err":
                            ax.fill_between(
                                scan["contour_ms"] / 1000,
                                scan["contour_s2t_err"][0],
                                scan["contour_s2t_err"][1],
                                color=palette[count],
                                alpha=0.2,
                            )

                ax.grid(linestyle="--", linewidth=0.7)
                ax.set_xlabel("m$_{\mathrm{s}}$ (keV)", fontsize=21)
                ax.set_xlim(plot_range[1][0], plot_range[1][1])
                ax.set_ylabel("sin$^{2}$ $\Theta$ ", fontsize=21)
                ax.set_ylim(plot_range[0][0], plot_range[0][1])
                ax.set_yscale("log")

                # Set tick parameters
                ax.tick_params(axis="x", labelsize=18)
                ax.tick_params(axis="y", labelsize=18)

                # Add a legend with a title
                legend = ax.legend(title="Scan Title", fontsize=15, title_fontsize=17)
                legend.get_frame().set_edgecolor("black")

                # Set the title
                ax.set_title(
                    f"Exclusion line at 95% CL for $\mathbf{{2*10^{15}}}$ electrons\n{scan_titles[count]}",
                    fontsize=24,
                    weight="bold",
                )

                # Adjust plot margins
                fig.tight_layout()

                # Generate filenames
                filename_base = scan_titles[count].replace(" ", "_").replace("/", "_")
                pdf_filename = self.data_path + f"/{filename_base}_contour.pdf"
                png_filename = self.data_path + f"/{filename_base}_contour.png"

                # Save the figure
                fig.savefig(pdf_filename)
                fig.savefig(png_filename)

                # Show the plot (optional)
                # plt.show()

                # Close the plot to free up memory
                plt.close(fig)
        else:
            # Set the Seaborn style
            fig, ax = plt.subplots(figsize=(11, 8))

            # sns.set(style="whitegrid", context=context)

            # Define a color palette
            palette = sns.color_palette(palette, len(list_of_scans))

            for count, scan in enumerate(list_of_scans):
                ax.plot(
                    scan["contour_ms"] / 1000,
                    scan["contour_s2t"],
                    label=scan_titles_final[count],
                    color=palette[count],
                )
                if errorbars:
                    for key in scan.keys():
                        if key == "contour_s2t_err":
                            ax.fill_between(
                                scan["contour_ms"] / 1000,
                                scan["contour_s2t_err"][0],
                                scan["contour_s2t_err"][1],
                                color=palette[count],
                                alpha=0.2,
                            )

            ax.grid(linestyle="--", linewidth=0.7)
            ax.set_xlabel("m$_{\mathrm{s}}$ (keV)", fontsize=21)
            ax.set_xlim(plot_range[1][0], plot_range[1][1])
            ax.set_ylabel("sin$^{2}$ $\Theta$ ", fontsize=21)
            ax.set_ylim(plot_range[0][0], plot_range[0][1])
            ax.set_yscale("log")

            # Set tick parameters
            ax.tick_params(axis="x", labelsize=18)
            ax.tick_params(axis="y", labelsize=18)

            # Add a legend with a title
            legend = ax.legend(fontsize=15)
            legend.get_frame().set_edgecolor("black")

            # Set the title
            ax.set_title(
                "Exclusion lines at 95% CL for $\mathbf{2*10^{15}}$ electrons",
                fontsize=24,
                weight="bold",
            )

            # Adjust plot margins
            fig.tight_layout()

            # Save the figure
            fig.savefig(self.data_path + "/combined_contours.pdf")
            fig.savefig(self.data_path + "/combined_contours.png")

            # Show the plot
            plt.show()

    def plot_losses(self, losses_training, losses_validation, show=True):
        r = int(len(losses_training) / len(losses_validation))
        e = int(len(losses_training) / self.epochs)
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
        ax.plot(
            np.array(x_ax_val)[range(len(losses_validation))],
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
        fig.savefig(self.data_path + "/losses/" + self.model_name[14:] + ".pdf")
        if show:
            fig.show()
