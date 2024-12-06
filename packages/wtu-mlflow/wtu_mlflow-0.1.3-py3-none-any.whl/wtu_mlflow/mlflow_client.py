import logging
import os
import mlflow
import pika
import onnx
import numpy as np

from mlflow.models.signature import infer_signature, ModelSignature
from mlflow.models.utils import ModelInputExample

"""
ModelInputExample
    mlflow 1.x 버전에서는 from mlflow.models.utils import ModelInputExample
    mlflow 2.x 버전에서는 from mlflow.models.signature import ModelInputExample
"""

logger = logging.getLogger(__name__)


class MLflowClient:
    def __init__(self):
        self._ONNX_TO_TRITON_DTYPE = {
            onnx.TensorProto.BOOL: "TYPE_BOOL",
            onnx.TensorProto.UINT8: "TYPE_UINT8",
            onnx.TensorProto.UINT16: "TYPE_UINT16",
            onnx.TensorProto.UINT32: "TYPE_UINT32",
            onnx.TensorProto.UINT64: "TYPE_UINT64",
            onnx.TensorProto.INT8: "TYPE_INT8",
            onnx.TensorProto.INT16: "TYPE_INT16",
            onnx.TensorProto.INT32: "TYPE_INT32",
            onnx.TensorProto.INT64: "TYPE_INT64",
            onnx.TensorProto.FLOAT16: "TYPE_FP16",
            onnx.TensorProto.FLOAT: "TYPE_FP32",
            onnx.TensorProto.DOUBLE: "TYPE_FP64",
            onnx.TensorProto.STRING: "TYPE_STRING",
            # Brain floating point (bfloat16) is not directly supported in ONNX, you might need to handle it separately
            # "TYPE_BF16": <corresponding ONNX type if available or a custom handler>
        }
        self._uploadModelExchange = os.environ["RABBIT_MODEL_UPLOAD_TOPIC"]

        self._connection = pika.BlockingConnection(
            pika.URLParameters(os.environ["RABBIT_ENDPOINT_URL"])
        )
        self._channel = self._connection.channel()

    def upload(
        self,
        onnx_model,
        model_name: str,
        input_example: np.ndarray,
        output_example: np.ndarray,
    ):
        onnx.checker.check_model(onnx_model)
        self._log_tensor(onnx_model)
        signature = infer_signature(input_example, output_example)
        path = self._log_model(onnx_model, model_name, signature, input_example)
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

    def _log_tensor(self, onnx_model):
        for input_tensor in onnx_model.graph.input:
            input_name = input_tensor.name
            input_type = self._get_triton_compatible_type(input_tensor.type.tensor_type)
            input_shape = [
                dim.dim_value for dim in input_tensor.type.tensor_type.shape.dim
            ]

            print(f"Input tensor name: {input_name}")
            print(f"Data type: {input_type}")
            print(f"Shape: {input_shape}")

        for output_tensor in onnx_model.graph.output:
            output_name = output_tensor.name
            output_type = self._get_triton_compatible_type(
                output_tensor.type.tensor_type
            )
            output_shape = [
                dim.dim_value for dim in output_tensor.type.tensor_type.shape.dim
            ]

            print(f"Output tensor name: {output_name}")
            print(f"Data type: {output_type}")
            print(f"Shape: {output_shape}")

    def _log_model(
        self,
        onnx_model,
        model_name: str,
        signature: ModelSignature,
        input_example: ModelInputExample,
    ) -> str:
        with mlflow.start_run():
            mlflow.onnx.log_model(
                onnx_model=onnx_model,
                artifact_path=model_name,
                signature=signature,
                input_example=input_example,
            )

            artifact_uri = mlflow.get_artifact_uri()
            model_full_path = f"{artifact_uri}/{model_name}"

            logger.info("Full path of the logged model: %s", model_full_path)
            return model_full_path

    def _get_triton_compatible_type(self, tensor_type):
        return self._ONNX_TO_TRITON_DTYPE.get(tensor_type.elem_type, "UNKNOWN")
