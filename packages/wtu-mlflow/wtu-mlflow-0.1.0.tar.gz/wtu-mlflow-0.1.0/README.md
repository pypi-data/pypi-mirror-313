# wtrainclient

## 가상환경 설정

```sh
pyenv install 3.8.18
pyenv virtualenv 3.8.18 wtrainclient3.8
pyenv activate wtrainclient3.8
```

---

## mlflow, minio 실행

```sh
cd docker
docker-compose up -d --build
```

---

## 환경 변수 설정

프로젝트를 실행하기 전에 아래의 환경 변수들을 설정해야 합니다:

| 환경변수                  | 설명                                                               | 예시                                      |
| ------------------------- | ------------------------------------------------------------------ | ----------------------------------------- |
| PROFILE                   | 개발/운영 환경설정, 개발환경에서는 모델을 실제로 업르도하지 않는다 | 운영: "prod" or "production", 개발: 그 외 |
| MLFLOW_S3_ENDPOINT_URL    | MLflow가 저장소로 사용하고있는 MinIO 엔드포인트 URL                | http://localhost:9000                     |
| MLFLOW_TRACKING_URI       | MLflow 트래킹 서버의 URI                                           | http://localhost:5001                     |
| AWS_ACCESS_KEY_ID         | MinIO 서버 접근을 위한 AWS 호환 액세스 키                          | minio                                     |
| AWS_SECRET_ACCESS_KEY     | MinIO 서버 접근을 위한 AWS 호환 시크릿 액세스 키                   | miniostorage                              |
| RABBIT_ENDPOINT_URL       | MinIO 서버에 모델 업로드 후 path 를 발행할 RMQ 엔드포인트 URL      | amqp://guest:guest@localhost:5672/        |
| RABBIT_MODEL_UPLOAD_TOPIC | 모델 업로드 path 를 전달할 토픽                                    | train.model.uploaded                      |
| TRAIN_ID                  | train_id (학습 서버에서 넣어주는 값)                               | 1                                         |
| MODEL_NAME                | model_name (학습 서버에서 넣어주는 값)                             | my_model                                  |

---
