import logging
import os
import pika
import onnx

from abc import ABCMeta, abstractmethod
from mlflow.models.signature import ModelSignature
from mlflow.models.utils import ModelInputExample
from .env_checker import check_env_vars

"""
ModelInputExample
    mlflow 1.x 버전에서는 from mlflow.models.utils import ModelInputExample
    mlflow 2.x 버전에서는 from mlflow.models.signature import ModelInputExample
"""

logger = logging.getLogger(__name__)


class BaseMLflowClient(metaclass=ABCMeta):
    isProduction: bool
    ONNX_TO_TRITON_DTYPE = {
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

    def __init__(self):
        profile = os.environ.get("PROFILE")
        if profile not in ["prod", "production"]:
            logging.warn(
                """
                You are using a non-production profile.
                If you are in production, please set the PROFILE environment variable to 'prod' or 'production'.
                """
            )
            self.isProduction = False

            if os.environ.get("MLFLOW_S3_ENDPOINT_URL") is None:
                os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
            if os.environ.get("MLFLOW_TRACKING_URI") is None:
                os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5000"
            if os.environ.get("AWS_ACCESS_KEY_ID") is None:
                os.environ["AWS_ACCESS_KEY_ID"] = "minio"
            if os.environ.get("AWS_SECRET_ACCESS_KEY") is None:
                os.environ["AWS_SECRET_ACCESS_KEY"] = "miniostorage"

            self.model_name = os.environ.get("MODEL_NAME", "my_model")
            self.train_id = os.environ.get("TRAIN_ID", "1")
            return
        else:
            self.isProduction = True
            check_env_vars()

            self.model_name = os.environ["MODEL_NAME"]
            self.train_id = os.environ["TRAIN_ID"]
            self._uploadModelExchange = os.environ["RABBIT_MODEL_UPLOAD_TOPIC"]
            # self._connection = pika.BlockingConnection(
            #     pika.URLParameters(os.environ["RABBIT_ENDPOINT_URL"])
            # )

    def get_connection(self):
        return pika.BlockingConnection(
            pika.URLParameters(os.environ["RABBIT_ENDPOINT_URL"])
        )

    def get_triton_compatible_type(self, tensor_type):
        return self.ONNX_TO_TRITON_DTYPE.get(tensor_type.elem_type, "UNKNOWN")

    @abstractmethod
    def upload(
        self,
        model,
        # input_example: Schema,
        # output_example: Schema,
    ):
        pass

    @abstractmethod
    def _log_tensor(self, model):
        """
        _log_tensor:
        onnx.load 로 로드된 모델을 통해 input tensor와 output tensor의 정보를 출력합니다.
        """
        pass

    @abstractmethod
    def _log_model(
        self,
        model,
        signature: ModelSignature,
        # input_example: ModelInputExample,
    ) -> str:
        pass
