import logging
import mlflow
import numpy as np

from typing import Optional
from mlflow.models.signature import infer_signature, ModelSignature
from mlflow.models.utils import ModelInputExample
from .base_mlflow_client import BaseMLflowClient
from .schema import Schema

"""
ModelInputExample
    mlflow 1.x 버전에서는 from mlflow.models.utils import ModelInputExample
    mlflow 2.x 버전에서는 from mlflow.models.signature import ModelInputExample
"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


"""
triton inference server 에서 .pth 모델을 사용할 수 없다.
.pt 로 직렬화하고 mlflow.pytorch.log 를 사용해도 .pth 로 저장된다.
log_artifact 는 다른 메타파일이 저장되지 않고 .pt 파일만 업로드해도 UNAVAILABLE 상태로 사용할 수 없다.
torch 모델을 연동하는건 당장 불가능해보인다.
"""


class TorchClient(BaseMLflowClient):
    def upload(
        self,
        model,
        input_example: Optional[Schema] = None,
        output_example: Optional[Schema] = None,
    ):
        signature = infer_signature(input_example, output_example)
        self._log_tensor(model, input_example)
        path = self._log_model(model=model, model_name=os.environ["MODEL_NAME"],, signature=signature)
        try:
            self._channel.basic_publish(
                exchange=self._uploadModelExchange,
                routing_key=self._uploadModelExchange,
                body=path,
            )
        except Exception as e:
            logger.error("Failed to upload model to RabbitMQ: %s", e)

        """
        _log_tensor:
        onnx.load 로 로드된 모델을 통해 input tensor와 output tensor의 정보를 출력합니다.
        """

    def _log_tensor(self, model, input_example):
        hooks = []

        def register_hook(module):
            def hook(module, input, output):
                print(f"{module.__class__.__name__}:")
                print(f"  Input Shape: {list(input[0].size())}")
                print(f"  Output Shape: {list(output.size())}")
                if hasattr(output, "dtype"):
                    print(f"  Data Type: {output.dtype}")

            # Check if it's a layer with parameters; skip for non-layer modules
            if list(module.children()) == []:  # Leaf module, e.g., Conv2d, Linear
                hooks.append(module.register_forward_hook(hook))

        # Apply the hook to all the layers
        model.apply(register_hook)

        # Dummy forward pass to trigger the hooks
        model(input_example)

        # Remove hooks to clean up
        for hook in hooks:
            hook.remove()

    def _log_model(
        self,
        model,
        model_name: str,
        signature: ModelSignature = None,
        input_example: ModelInputExample = None,
    ) -> str:
        with mlflow.start_run():
            mlflow.pytorch.log_model(
                pytorch_model=model,
                artifact_path=model_name,
                signature=signature,
                input_example=input_example,
            )

            artifact_uri = mlflow.get_artifact_uri()
            model_full_path = f"{artifact_uri}/{model_name}"

            logger.info("Full path of the logged model: %s", model_full_path)
            return model_full_path
