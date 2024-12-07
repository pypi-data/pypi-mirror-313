import functools
import mlflow
import logging
import threading
import os
import onnx

from typing import Optional
from pathlib import Path
from .onnx_client import OnnxClient

# 스레드 로컬 스토리지 설정
_thread_local = threading.local()
client = OnnxClient()
logger = logging.getLogger(__name__)


def set_log_functions(log_param, log_metric):
    _thread_local.log_param = log_param
    _thread_local.log_metric = log_metric


def clear_log_functions():
    _thread_local.log_param = None
    _thread_local.log_metric = None


def log_param(key, value):
    if hasattr(_thread_local, "log_param") and _thread_local.log_param:
        _thread_local.log_param(key, value)
    else:
        raise RuntimeError(
            "trace 데코레이터 내에서 log_param 함수가 사용되지 않았습니다."
        )


def log_metric(key, value, step=None):
    if hasattr(_thread_local, "log_metric") and _thread_local.log_metric:
        _thread_local.log_metric(key, value, step)
    else:
        raise RuntimeError(
            "trace 데코레이터 내에서 log_metric 함수가 사용되지 않았습니다."
        )


def trace(experiment_name: Optional[str] = None, run_name: Optional[str] = None):
    """
    MLflow 실험을 설정하고 함수 실행 결과를 ONNX 모델로 로깅하는 데코레이터.

    Args:
        experiment_name (str): MLflow 실험 이름.
        run_name (Optional[str]): MLflow 실행 이름. Defaults to None.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 실험 설정
            if experiment_name is not None:
                mlflow.set_experiment(experiment_name)
            with mlflow.start_run(run_name=run_name):
                try:
                    # 로깅 함수 설정
                    set_log_functions(
                        log_param=mlflow.log_param,
                        log_metric=mlflow.log_metric,
                    )
                    logger.info(
                        f"Logging functions have been set for experiment '{experiment_name}'."
                    )

                    # 함수 실행
                    result = func(*args, **kwargs)

                    # 반환값이 str 또는 Path인지 확인
                    if isinstance(result, (str, os.PathLike)):
                        model_path = Path(result)  # pathlib.Path로 변환
                        if not model_path.exists():
                            raise FileNotFoundError(
                                f"Model path does not exist: {model_path}"
                            )

                        logger.info(f"Loading ONNX model from: {model_path}")

                        # ONNX 모델 로드
                        onnx_model = onnx.load(model_path)

                        # 모델 로깅
                        client.upload(onnx_model)

                        logger.info(f"Model logged successfully from: {model_path}")
                    else:
                        raise TypeError(
                            f"Function '{func.__name__}' must return a str or Path, but got {type(result)}"
                        )
                    return result  # 원래 함수의 반환값을 그대로 반환
                except Exception as e:
                    logger.error(f"Error in trace decorator: {e}")
                    raise e
                finally:
                    # 로깅 함수 해제
                    clear_log_functions()
                    logger.info("Logging functions have been cleared.")

        return wrapper

    return decorator
