import logging
import mlflow
import onnx
import json
import numpy as np

from typing import Union, Optional, Dict
from pathlib import Path
from mlflow.models.signature import infer_signature, ModelSignature
from .base_mlflow_client import BaseMLflowClient
from wtu_mlflow.schema import Schema, ModelInputOutput

# from mlflow.models.utils import ModelInputExample

"""
ModelInputExample
    mlflow 1.x 버전에서는 from mlflow.models.utils import ModelInputExample
    mlflow 2.x 버전에서는 from mlflow.models.signature import ModelInputExample
"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OnnxClient(BaseMLflowClient):
    def __init__(self):
        super().__init__()

    def upload(
        self,
        model: Union[onnx.ModelProto, str, bytes, Path],
    ) -> Optional[str]:
        """ONNX 모델을 MLflow에 업로드하고 필요한 경우 RabbitMQ에 알림을 보냅니다.

        Args:
            model: ONNX 모델 또는 모델 경로

        Returns:
            Optional[str]: 프로덕션 모드가 아닌 경우 모델 경로 반환
        """
        try:
            logger.info("모델 유효성 검사 시작")
            onnx.checker.check_model(model)

            if isinstance(model, (str, Path)):
                logger.debug(f"모델 파일 로드 중: {model}")
                model = onnx.load(model)

            self._log_tensor(model)
            example = self._get_dummy_input_output(model)

            signature = infer_signature(
                model_input=example.inputs,
                model_output=example.outputs,
            )

            path = self._log_model(model=model, signature=signature)

            if not self.isProduction:
                logger.info("개발 모드: RabbitMQ 메시지 전송 건너뜀")
                return path

            self._publish_to_rabbitmq(path)
            return path

        except Exception as e:
            logger.error(f"모델 업로드 중 오류 발생: {str(e)}", exc_info=True)
            raise

    def _get_dummy_input_output(self, onnx_model: onnx.ModelProto) -> ModelInputOutput:
        """ONNX 모델의 입출력 스키마를 분석하여 더미 데이터를 생성합니다."""
        try:
            input_schema_params = self._process_tensors(onnx_model.graph.input)
            output_schema_params = self._process_tensors(onnx_model.graph.output)

            return ModelInputOutput(
                input_schema=Schema(params=input_schema_params),
                output_schema=Schema(params=output_schema_params),
            )
        except Exception as e:
            logger.error(f"더미 입출력 생성 중 오류 발생: {str(e)}", exc_info=True)
            raise

    def _process_tensors(self, tensors) -> Dict[str, np.ndarray]:
        """텐서 정보를 처리하여 스키마 파라미터를 생성합니다."""
        schema_params = {}
        for tensor in tensors:
            name = tensor.name
            dtype = self.get_triton_compatible_type(tensor.type.tensor_type)
            shape = [
                dim.dim_value if dim.dim_value > 0 else 1  # "N" 대신 1 사용
                for dim in tensor.type.tensor_type.shape.dim
            ]

            schema_params[name] = np.ones(shape, dtype=self._get_numpy_dtype(dtype))
            logger.debug(f"텐서 처리: {name}, 형태: {shape}, 타입: {dtype}")

        return schema_params

    def _publish_to_rabbitmq(self, path: str) -> None:
        """RabbitMQ에 모델 업로드 메시지를 발행합니다."""

        channel = self.get_connection().channel()

        message = json.dumps(
            {"train_id": self.train_id, "full_path": path}, ensure_ascii=False
        )

        try:
            channel.basic_publish(
                exchange=self._uploadModelExchange,
                routing_key=self._uploadModelExchange,
                body=message,
            )
            logger.info(f"RabbitMQ에 모델 업로드 완료: {message}")
        except Exception as e:
            logger.error(f"RabbitMQ 메시지 발행 실패: {str(e)}", exc_info=True)
            raise
        finally:
            channel.close()

    def _log_model(
        self,
        model: onnx.ModelProto,
        signature: ModelSignature,
        # input_example: Optional[ModelInputExample] = None,
    ) -> str:
        """MLflow에 모델을 로깅합니다."""
        try:
            mlflow.onnx.log_model(
                onnx_model=model,
                artifact_path=self.model_name,
                signature=signature,
                # input_example=signature.inputs,
            )

            artifact_uri = mlflow.get_artifact_uri()
            model_full_path = f"{artifact_uri}/{self.model_name}"
            logger.info(f"MLflow에 모델 저장 완료: {model_full_path}")

            return model_full_path
        except Exception as e:
            logger.error(f"모델 로깅 중 오류 발생: {str(e)}", exc_info=True)
            raise

    def _log_tensor(self, onnx_model):
        """
        onnx.load 로 로드된 모델을 통해 input tensor와 output tensor의 정보를 출력합니다.
        """
        for input_tensor in onnx_model.graph.input:
            input_name = input_tensor.name

            input_type = self.get_triton_compatible_type(input_tensor.type.tensor_type)
            input_shape = [
                dim.dim_value for dim in input_tensor.type.tensor_type.shape.dim
            ]

            print(f"Input tensor name: {input_name}")
            print(f"Data type: {input_type}")
            print(f"Shape: {input_shape}")

        for output_tensor in onnx_model.graph.output:
            output_name = output_tensor.name
            output_type = self.get_triton_compatible_type(
                output_tensor.type.tensor_type
            )
            output_shape = [
                dim.dim_value for dim in output_tensor.type.tensor_type.shape.dim
            ]

            print(f"Output tensor name: {output_name}")
            print(f"Data type: {output_type}")
            print(f"Shape: {output_shape}")

    def _get_numpy_dtype(self, triton_type: str) -> type:
        """
        Triton 데이터 타입을 NumPy 데이터 타입으로 변환합니다.
        """
        mapping = {
            "BOOL": np.bool_,
            "UINT8": np.uint8,
            "UINT16": np.uint16,
            "INT32": np.int32,
            "INT64": np.int64,
            "FP16": np.float16,
            "FP32": np.float32,
            "FP64": np.float64,
            # 필요한 경우 추가 매핑
        }
        return mapping.get(triton_type, np.float32)  # 기본값으로 float32 사용
