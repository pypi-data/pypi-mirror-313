import os
from torch import nn, optim
from tracebloc_package.model_file_checks.pytorch_checks import TorchChecks
from tracebloc_package.upload_model_classes.model_upload import Model
from tracebloc_package.utils.general_utils import (
    get_model_parameters,
    define_device,
)
from tracebloc_package.utils.constants import (
    PRETRAINED_WEIGHTS_FILENAME,
    TRAINED_WEIGHTS_FILENAME,
    DNN,
    ML,
)
from tracebloc_package.utils.constants import PYTORCH_FRAMEWORK
from tracebloc_package.utils.generic_classification_utils import get_dataloader


class TorchGenericClassifier(Model, TorchChecks):

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
        TorchChecks.__init__(
            self,
            model=model,
            category=category,
            progress_bar=progress_bar,
            message=message,
            classes=classes,
        )
        self.__weights_path = weights_path
        self.tmp_file_path = ""
        self.input_shape = input_shape
        self.device = define_device()
        self.deep_learning = (
            True if self.model_type == DNN or self.model_type == "" else False
        )
        self.loss = None

    def small_training_loop(
        self, weight_filename, custom_loss=False, criterion=nn.MSELoss()
    ):
        try:
            dataloader = get_dataloader(num_feature_points=self.num_feature_points)
            if self.deep_learning:
                self.model.train()
                optimizer = optim.Adam(self.model.parameters(), lr=0.001)

            # Training loop
            for epoch in range(1):
                running_loss = 0.0

                for inputs, labels in dataloader:
                    if self.deep_learning:
                        optimizer.zero_grad()

                        # Forward pass
                        outputs = self.model(inputs)
                        loss = criterion(outputs.squeeze(), labels)

                        # Backward pass and optimization
                        loss.backward()
                        optimizer.step()

                        running_loss += loss.item()
                    else:
                        try:
                            self.model.fit(inputs, labels)
                            predicted = self.model.predict(inputs)
                        except ValueError as e:
                            pass

            # dump weights from trained model will be used in averaging check
            get_model_parameters(
                model=self.model,
                weight_file_path=self.tmp_dir_path,
                weights_file_name=TRAINED_WEIGHTS_FILENAME,
                framework=PYTORCH_FRAMEWORK,
                preweights=False,
            )
            if self.progress_bar is not None:
                self.progress_bar.update(1)
        except Exception as e:  # pragma: no cover
            self.message = f"\nModel not support training on {self.category} dataset as there is error {e} "
            raise

    def model_func_checks(self):
        # check if model is eligible
        try:
            if self.model_type != ML:
                self.is_model_supported()
            self.small_training_loop(TRAINED_WEIGHTS_FILENAME)
            if os.path.exists(
                os.path.join(self.tmp_dir_path, f"{PRETRAINED_WEIGHTS_FILENAME}.pth")
            ):
                get_model_parameters(
                    model=self.model,
                    weight_file_path=self.tmp_dir_path,
                    weights_file_name=PRETRAINED_WEIGHTS_FILENAME,
                    framework=PYTORCH_FRAMEWORK,
                    preweights=True,
                )
                self.progress_bar.update(1)
            else:
                get_model_parameters(
                    model=self.model,
                    weight_file_path=self.tmp_dir_path,
                    weights_file_name=PRETRAINED_WEIGHTS_FILENAME,
                    framework=PYTORCH_FRAMEWORK,
                    preweights=False,
                )
                self.progress_bar.update(2)
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
