import os
import pickle
import shutil

import numpy as np
from torch import nn, optim
from tracebloc_package.model_file_checks.sklearn_checks import SklearnChecks
from tracebloc_package.upload_model_classes.model_upload import Model
from tracebloc_package.utils.general_utils import (
    get_model_parameters,
    define_device,
)
from tracebloc_package.utils.constants import (
    PRETRAINED_WEIGHTS_FILENAME,
    TRAINED_WEIGHTS_FILENAME,
    AVERAGED_WEIGHTS_PATH,
)
from tracebloc_package.utils.generic_classification_utils import get_dataloader
from sklearn.ensemble import VotingClassifier


class SKLGenericClassifier(Model, SklearnChecks):

    def __init__(
        self,
        model_name,
        token,
        weights,
        url,
        model_path,
        tmp_model_file_path,
        tmp_dir_path,
        progress_bar_1,
        classes,
        weights_path,
        input_shape,
        model,
        category,
        progress_bar,
        message,
        framework,
        image_size,
        batch_size,
        model_type,
        num_feature_points,
    ):
        super().__init__(
            model_name=model_name,
            token=token,
            weights=weights,
            url=url,
            model_path=model_path,
            tmp_model_file_path=tmp_model_file_path,
            tmp_dir_path=tmp_dir_path,
            progress_bar_1=progress_bar_1,
            classes=classes,
            weights_path=weights_path,
            framework=framework,
            image_size=image_size,
            batch_size=batch_size,
            model_type=model_type,
            num_feature_points=num_feature_points,
        )
        SklearnChecks.__init__(
            self,
            model=model,
            category=category,
            progress_bar=progress_bar,
            message=message,
            classes=classes,
            model_type=model_type,
        )
        self.__weights_path = weights_path
        self.tmp_file_path = ""
        self.input_shape = input_shape
        self.loss = None

    def small_training_loop(
        self, weight_filename, custom_loss=False, criterion=nn.MSELoss()
    ):
        try:
            dataloader = get_dataloader(
                num_feature_points=self.num_feature_points, num_classes=self.classes
            )
            for inputs, labels in dataloader:
                try:
                    self.model.fit(inputs, labels)
                except:
                    pass

            # dump weights from trained model will be used in averaging check
            get_model_parameters(
                model=self.model,
                weight_file_path=self.tmp_dir_path,
                weights_file_name=TRAINED_WEIGHTS_FILENAME,
                framework=self.framework,
                preweights=False,
            )
            if self.progress_bar is not None:
                self.progress_bar.update(1)
        except Exception as e:  # pragma: no cover
            self.message = f"\nModel not support training on {self.category} dataset as there is error {e} "
            raise

    def model_func_checks(self):
        try:
            self.is_model_supported()
            self.small_training_loop(TRAINED_WEIGHTS_FILENAME)
            if not os.path.exists(
                os.path.join(self.tmp_dir_path, f"{PRETRAINED_WEIGHTS_FILENAME}.pkl")
            ):
                shutil.copy(
                    os.path.join(self.tmp_dir_path, f"{TRAINED_WEIGHTS_FILENAME}.pkl"),
                    os.path.join(
                        self.tmp_dir_path, f"{PRETRAINED_WEIGHTS_FILENAME}.pkl"
                    ),
                )
                self.progress_bar.update(1)
            self.average_weights()
            self.load_averaged_weights()
            self.message = "all check passed"
            eligible = True
        except Exception as e:  # pragma: no cover
            self.message = f"\nModel checks failed with error:\n {e}"
            eligible = False
        if not eligible:
            return eligible, self.message, None, self.progress_bar  # pragma: no cover
        return eligible, self.message, self.model_name, self.progress_bar

    def average_weights(self):
        """
        Average two weight dictionaries.
        """
        weights = []
        averaged_model = self.model
        weights_file_path_1 = os.path.join(
            self.tmp_dir_path, f"{PRETRAINED_WEIGHTS_FILENAME}.pkl"
        )
        weights_file_path_2 = os.path.join(
            self.tmp_dir_path, f"{TRAINED_WEIGHTS_FILENAME}.pkl"
        )
        self.average_weights_file_path = os.path.join(
            self.tmp_dir_path, f"{AVERAGED_WEIGHTS_PATH}.pkl"
        )
        try:
            with open(weights_file_path_1, "rb") as pkl_file, open(
                weights_file_path_2, "rb"
            ) as pkl_file2:
                weights.append(pickle.load(pkl_file))
                weights.append(pickle.load(pkl_file2))
        except Exception as e:
            raise

        if self.model_type == "linear":
            # Average coefficients and intercepts
            coefs = np.mean([model.coef_ for model in weights], axis=0)
            intercepts = np.mean([model.intercept_ for model in weights], axis=0)
            averaged_model.coef_ = coefs
            averaged_model.intercept_ = intercepts

        elif self.model_type == "tree":
            # Ensemble strategy: Use a VotingClassifier for Decision Trees
            voting_classifiers = [
                ("tree_" + str(i), weights[i]) for i in range(len(weights))
            ]
            ensemble_model = VotingClassifier(
                estimators=voting_classifiers, voting="hard"
            )
            averaged_model = ensemble_model

        elif self.model_type == "naive":
            # Average theta_ (means) and sigma_ (variances) for each class
            thetas = np.mean([model.theta_ for model in weights], axis=0)
            averaged_model.theta_ = thetas
            try:
                sigmas = np.mean([model.sigma_ for model in weights], axis=0)
                averaged_model.sigma_ = sigmas
            except:
                pass

        elif self.model_type == "mlp":
            # Average coefs_ and intercepts_ for each layer in MLP
            coefs = [
                np.mean([model.coefs_[i] for model in weights], axis=0)
                for i in range(len(weights[0].coefs_))
            ]
            intercepts = [
                np.mean([model.intercepts_[i] for model in weights], axis=0)
                for i in range(len(weights[0].intercepts_))
            ]
            averaged_model.coefs_ = coefs
            averaged_model.intercepts_ = intercepts

        elif self.model_type == "svc":
            # For linear SVM, average coef_ and intercept_
            voting_classifiers = [
                ("svc_" + str(i), weights[i]) for i in range(len(weights))
            ]
            ensemble_model = VotingClassifier(
                estimators=voting_classifiers, voting="hard"
            )
            averaged_model = ensemble_model

        elif self.model_type == "knn":
            # Ensemble strategy for k-NN
            voting_classifiers = [
                ("knn_" + str(i), self.model_type[i])
                for i in range(len(self.model_type))
            ]
            ensemble_model = VotingClassifier(
                estimators=voting_classifiers, voting="soft"
            )
            averaged_model = ensemble_model
        else:
            raise ValueError(
                f"model type {self.model_type} is not supported for Sklearn"
            )

        # Save averaged weights
        try:
            with open(self.average_weights_file_path, "wb") as f:
                pickle.dump(averaged_model, f)
            del averaged_model
            self.progress_bar.update(1)
        except Exception as e:
            raise e

    def load_averaged_weights(self):
        """
        Load the averaged weights
        Set the model's weights using a dictionary of weights.
        """
        try:
            with open(self.average_weights_file_path, "rb") as f:
                self.model = pickle.load(f)

        except Exception as e:
            raise e
