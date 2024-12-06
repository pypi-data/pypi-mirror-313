# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0
"""Integration tests that exercise the full audit workflow pipeline.

These tests need to be run together as a batch, because workflows that come later in the
pipeline depend on resources created by earlier workflows. Tests that depend on a
previous step that failed will be skipped.

These tests can be run against a remote instance via Client, or against an instance of
DyffLocalPlatform. Certain tests are only implemented for one or the other; they will be
skipped if not applicable.
"""

from __future__ import annotations

import os
import tempfile
import time

# mypy: disable-error-code="import-untyped"
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

import pydantic
import pytest

from dyff.audit.local import mocks
from dyff.audit.local.platform import DyffLocalPlatform
from dyff.client import Client, HttpResponseError, Timeout
from dyff.schema import ids
from dyff.schema.base import int32
from dyff.schema.dataset import ReplicatedItem, arrow
from dyff.schema.platform import *
from dyff.schema.requests import *


class BlurstCountScoredItem(ReplicatedItem):
    blurstCount: int32() = pydantic.Field(  # type: ignore
        description="Number of times the word 'blurst' is used in the response."
    )
    cromulent: int32() = pydantic.Field(  # type: ignore
        description="Whether the text is cromulent."
    )
    embiggen: str = pydantic.Field(description="Which man to embiggen.")


DATA_DIR = Path(__file__).parent.resolve() / "data"
COMPARISON_REPLICATIONS = 5


def _create_client(pytestconfig, *, timeout: Optional[Timeout] = None):
    endpoint = pytestconfig.getoption("api_endpoint") or os.environ["DYFF_API_ENDPOINT"]
    token = pytestconfig.getoption("api_token") or os.environ["DYFF_API_TOKEN"]
    insecure = (
        pytestconfig.getoption("api_insecure")
        or os.environ.get("DYFF_API_INSECURE") == "1"
    )
    return Client(api_key=token, endpoint=endpoint, insecure=insecure, timeout=timeout)


@pytest.fixture(scope="session")
def dyffapi(pytestconfig, tmp_path_factory):
    """Creates a DyffLocalPlatform that is shared by all tests.

    This is needed because a workflow's dependencies must be present before we can test
    the workflow.
    """
    if pytestconfig.getoption("test_remote"):
        yield _create_client(pytestconfig)
    else:
        storage_root = pytestconfig.getoption("storage_root")
        if storage_root is None:
            storage_root = os.getenv("DYFF_AUDIT_LOCAL_STORAGE_ROOT")
        if storage_root is not None:
            storage_root_path = Path(storage_root).resolve()
            yield DyffLocalPlatform(storage_root_path)
        else:
            yield DyffLocalPlatform(tmp_path_factory.mktemp("dyff"))


@pytest.fixture(scope="session")
def ctx(pytestconfig):
    """Shared dict for storing the workflow dependencies that we add incrementally as
    testing progresses."""
    d: dict[str, Any] = {"model": None}
    if pytestconfig.getoption("test_remote"):
        d.update(
            {
                "account": "test",
            }
        )
    else:
        account = ids.generate_entity_id()
        d.update(
            {
                "account": account,
                "inferenceservice": DyffModelWithID(
                    id=ids.generate_entity_id(), account=account
                ),
            }
        )
    yield d


@pytest.fixture(scope="session", autouse=True)
def cleanup(dyffapi: Client | DyffLocalPlatform, ctx, request):
    def terminate_session():
        for session_key in ["inferencesession_mock", "inferencesession_huggingface"]:
            session = ctx.get(session_key)
            if session:
                dyffapi.inferencesessions.delete(session.id)

    request.addfinalizer(terminate_session)


def wait_for_ready(
    dyffapi: Client | DyffLocalPlatform, session_id: str, *, timeout: timedelta
):
    then = datetime.now(timezone.utc)
    while (datetime.now(timezone.utc) - then) < timeout:
        if dyffapi.inferencesessions.ready(session_id):
            return
        time.sleep(10)
    raise AssertionError("timeout")


def wait_for_terminal_status(get_entity_fn, *, timeout: timedelta) -> str:
    then = datetime.now(timezone.utc)
    while (datetime.now(timezone.utc) - then) < timeout:
        try:
            status = get_entity_fn().status
            if is_status_terminal(status):
                return status
        except HttpResponseError as ex:
            if ex.status_code != 404:
                raise
        time.sleep(10)
    raise AssertionError("timeout")


def wait_for_success(get_entity_fn, *, timeout: timedelta):
    then = datetime.now(timezone.utc)
    while (datetime.now(timezone.utc) - then) < timeout:
        try:
            status = get_entity_fn().status
            if is_status_success(status):
                return
            elif is_status_failure(status):
                raise AssertionError(f"failure status: {status}")
        except HttpResponseError as ex:
            if ex.status_code != 404:
                raise
        time.sleep(10)
    raise AssertionError("timeout")


# ----------------------------------------------------------------------------
# Tests for successful workflow execution
# ----------------------------------------------------------------------------


@pytest.mark.datafiles(DATA_DIR)
def test_datasets_create(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    account = ctx["account"]
    dataset_dir = datafiles / "dataset"
    dataset = dyffapi.datasets.create_arrow_dataset(
        dataset_dir, account=account, name="dataset"
    )
    dyffapi.datasets.upload_arrow_dataset(dataset, dataset_dir)
    print(f"dataset: {dataset.id}")
    ctx["dataset"] = dataset

    wait_for_success(
        lambda: dyffapi.datasets.get(dataset.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.datafiles(DATA_DIR)
def test_datasets_create_tiny(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    account = ctx["account"]
    dataset_dir = datafiles / "dataset_tiny"
    dataset = dyffapi.datasets.create_arrow_dataset(
        dataset_dir, account=account, name="dataset_tiny"
    )
    dyffapi.datasets.upload_arrow_dataset(dataset, dataset_dir)
    print(f"dataset_tiny: {dataset.id}")
    ctx["dataset_tiny"] = dataset

    wait_for_success(
        lambda: dyffapi.datasets.get(dataset.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_datasets_create",
    ]
)
def test_datasets_download(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    dataset: Dataset = ctx["dataset"]

    if not pytestconfig.getoption("test_remote"):
        pytest.skip()

    assert isinstance(dyffapi, Client)

    with tempfile.TemporaryDirectory() as tmp:
        dyffapi.datasets.download(dataset.id, Path(tmp) / "nested" / "dataset")

        with pytest.raises(FileExistsError):
            dyffapi.datasets.download(dataset.id, Path(tmp) / "nested")


@pytest.mark.datafiles(DATA_DIR)
def test_models_create_mock(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    account = ctx["account"]
    model_request = ModelCreateRequest(
        name="mock-model",
        account=account,
        artifact=ModelArtifact(
            kind=ModelArtifactKind.Mock,
        ),
        storage=ModelStorage(
            medium=ModelStorageMedium.Mock,
        ),
        source=ModelSource(
            kind=ModelSourceKinds.Mock,
        ),
        resources=ModelResources(storage="0"),
    )
    model = dyffapi.models.create(model_request)
    print(f"model: {model.id}")
    ctx["model_mock"] = model

    wait_for_success(
        lambda: dyffapi.models.get(model.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.parametrize("replication", range(COMPARISON_REPLICATIONS))
def test_models_create_mock_compare(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles, replication
):
    if not pytestconfig.getoption("enable_comparisons"):
        pytest.skip()

    account = ctx["account"]
    model_request = ModelCreateRequest(
        name=f"mock-model-compare-{replication}",
        account=account,
        artifact=ModelArtifact(
            kind=ModelArtifactKind.Mock,
        ),
        storage=ModelStorage(
            medium=ModelStorageMedium.Mock,
        ),
        source=ModelSource(
            kind=ModelSourceKinds.Mock,
        ),
        resources=ModelResources(storage="0"),
    )
    model = dyffapi.models.create(model_request)
    print(f"model compare {replication}: {model.id}")
    ctx[f"model_mock_compare_{replication}"] = model

    wait_for_success(
        lambda: dyffapi.models.get(model.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.datafiles(DATA_DIR)
def test_models_create_huggingface(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    if pytestconfig.getoption("skip_huggingface"):
        pytest.skip()
    if not pytestconfig.getoption("test_remote"):
        pytest.skip()

    account = ctx["account"]
    model_request = ModelCreateRequest(
        name="facebook/opt-125m",
        account=account,
        artifact=ModelArtifact(
            kind=ModelArtifactKind.HuggingFaceCache,
            huggingFaceCache=ModelArtifactHuggingFaceCache(
                repoID="facebook/opt-125m",
                revision="27dcfa74d334bc871f3234de431e71c6eeba5dd6",  # pragma: allowlist secret
            ),
        ),
        source=ModelSource(
            kind=ModelSourceKinds.HuggingFaceHub,
            huggingFaceHub=ModelSourceHuggingFaceHub(
                repoID="facebook/opt-125m",
                revision="27dcfa74d334bc871f3234de431e71c6eeba5dd6",  # pragma: allowlist secret
                # Repos sometimes contain multiple copies of the weights in
                # different formats; we want just the regular PyTorch .bin weights
                allowPatterns=[
                    ".gitattributes",
                    "pytorch_model*.bin",
                    "*.json",
                    "*.md",
                    "*.model",
                    "*.py",
                    "*.txt",
                ],
                # Ignore everything in subdirectories
                ignorePatterns=["*/*"],
            ),
        ),
        storage=ModelStorage(
            medium=ModelStorageMedium.ObjectStorage,
        ),
        resources=ModelResources(
            storage="300Mi",
            memory="8Gi",
        ),
    )
    model = dyffapi.models.create(model_request)
    print(f"model_huggingface: {model.id}")
    ctx["model_huggingface"] = model

    wait_for_success(
        lambda: dyffapi.models.get(model.id),
        timeout=timedelta(minutes=5),
    )


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_models_create_mock",
    ]
)
def test_inferenceservices_create_mock(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    account = ctx["account"]
    model: Model = ctx["model_mock"]

    if pytestconfig.getoption("test_remote"):
        assert isinstance(dyffapi, Client)

        service_request = InferenceServiceCreateRequest(
            account=account,
            name="mock-llm",
            model=model.id,
            runner=InferenceServiceRunner(
                kind=InferenceServiceRunnerKind.MOCK,
                resources=ModelResources(
                    storage="1Gi",
                    memory="2Gi",
                ),
            ),
            interface=InferenceInterface(
                # This is the inference endpoint for the vLLM runner
                endpoint="generate",
                # The output records should look like: {"text": "To be, or not to be"}
                outputSchema=DataSchema.make_output_schema(
                    DyffDataSchema(
                        components=["text.Text"],
                    ),
                ),
                # How to convert the input dataset into the format the runner expects
                inputPipeline=[
                    # {"text": "The question"} -> {"prompt": "The question"}
                    SchemaAdapter(
                        kind="TransformJSON",
                        configuration={"prompt": "$.text"},
                    ),
                ],
                # How to convert the runner output to match outputSchema
                outputPipeline=[
                    # {"text": ["The answer"]} -> [{"text": "The answer"}]
                    SchemaAdapter(
                        kind="ExplodeCollections",
                        configuration={"collections": ["text"]},
                    ),
                ],
            ),
        )

        inferenceservice = dyffapi.inferenceservices.create(service_request)
        dyffapi.inferenceservices.edit_documentation(
            inferenceservice.id,
            DocumentationEditRequest(title="Mock Svc", summary="Main Mock Svc"),
        )
        print(f"inferenceservice_mock: {inferenceservice.id}")
        ctx["inferenceservice_mock"] = inferenceservice
    else:
        assert isinstance(dyffapi, DyffLocalPlatform)

        inferenceservice = dyffapi.inferenceservices.create_mock(
            mocks.TextCompletion,
            account=account,
            model=model.id,
        )
        print(f"inferenceservice_mock: {inferenceservice.id}")
        ctx["inferenceservice_mock"] = inferenceservice

    wait_for_success(
        lambda: dyffapi.inferenceservices.get(inferenceservice.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_models_create_mock_compare",
    ]
)
@pytest.mark.parametrize("replication", range(COMPARISON_REPLICATIONS))
def test_inferenceservices_create_mock_compare(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles, replication
):
    if not pytestconfig.getoption("enable_comparisons"):
        pytest.skip()

    account = ctx["account"]
    model: Model = ctx[f"model_mock_compare_{replication}"]

    if pytestconfig.getoption("test_remote"):
        assert isinstance(dyffapi, Client)

        service_request = InferenceServiceCreateRequest(
            account=account,
            name=f"mock-llm-svc-compare-{replication}",
            model=model.id,
            runner=InferenceServiceRunner(
                kind=InferenceServiceRunnerKind.MOCK,
                resources=ModelResources(
                    storage="1Gi",
                    memory="2Gi",
                ),
            ),
            interface=InferenceInterface(
                # This is the inference endpoint for the vLLM runner
                endpoint="generate",
                # The output records should look like: {"text": "To be, or not to be"}
                outputSchema=DataSchema.make_output_schema(
                    DyffDataSchema(
                        components=["text.Text"],
                    ),
                ),
                # How to convert the input dataset into the format the runner expects
                inputPipeline=[
                    # {"text": "The question"} -> {"prompt": "The question"}
                    SchemaAdapter(
                        kind="TransformJSON",
                        configuration={"prompt": "$.text"},
                    ),
                ],
                # How to convert the runner output to match outputSchema
                outputPipeline=[
                    # {"text": ["The answer"]} -> [{"text": "The answer"}]
                    SchemaAdapter(
                        kind="ExplodeCollections",
                        configuration={"collections": ["text"]},
                    ),
                ],
            ),
        )

        inferenceservice = dyffapi.inferenceservices.create(service_request)
        dyffapi.inferenceservices.edit_documentation(
            inferenceservice.id,
            DocumentationEditRequest(
                title="Mock Svc (Method Compare)",
                summary="Other Mock Svc using same test method",
            ),
        )
        print(f"inferenceservice_mock_compare_{replication}: {inferenceservice.id}")
        ctx[f"inferenceservice_mock_compare_{replication}"] = inferenceservice
    else:
        assert isinstance(dyffapi, DyffLocalPlatform)

        inferenceservice = dyffapi.inferenceservices.create_mock(
            mocks.TextCompletion,
            account=account,
            model=model.id,
        )
        print(f"inferenceservice_mock_{replication}: {inferenceservice.id}")
        ctx[f"inferenceservice_mock_{replication}"] = inferenceservice

    wait_for_success(
        lambda: dyffapi.inferenceservices.get(inferenceservice.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_models_create_huggingface",
    ]
)
def test_inferenceservices_create_huggingface(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    if pytestconfig.getoption("skip_huggingface"):
        pytest.skip()
    if not pytestconfig.getoption("test_remote"):
        pytest.skip()

    account = ctx["account"]
    model: Model = ctx["model_huggingface"]

    assert isinstance(dyffapi, Client)

    service_request = InferenceServiceCreateRequest(
        account=account,
        name=model.name,
        model=model.id,
        runner=InferenceServiceRunner(
            kind=InferenceServiceRunnerKind.HUGGINGFACE,
            image=ContainerImageSource(
                host="registry.gitlab.com",
                name="dyff/workflows/huggingface-runner",
                digest="sha256:2d200fa3f56f8b0e902b9d2c079e1d73528a42f7f668883d8f56e4fe585a845f",
                tag="0.1.3",
            ),
            resources=ModelResources(
                storage="1Gi",
                memory="2Gi",
            ),
        ),
        interface=InferenceInterface(
            # This is the inference endpoint for the vLLM runner
            endpoint="generate",
            # The output records should look like: {"text": "To be, or not to be"}
            outputSchema=DataSchema.make_output_schema(
                DyffDataSchema(
                    components=["text.Text"],
                ),
            ),
            # How to convert the input dataset into the format the runner expects
            inputPipeline=[
                # {"text": "The question"} -> {"prompt": "The question"}
                SchemaAdapter(
                    kind="TransformJSON",
                    configuration={
                        "prompt": "$.text",
                        # When using HuggingFace runner, max_tokens counts the
                        # length of the input, too, so we need to override
                        # the default.
                        "max_new_tokens": 20,
                    },
                ),
            ],
            # How to convert the runner output to match outputSchema
            outputPipeline=[
                # {"text": ["The answer"]} -> [{"text": "The answer"}]
                SchemaAdapter(
                    kind="ExplodeCollections",
                    configuration={"collections": ["text"]},
                ),
            ],
        ),
    )

    inferenceservice = dyffapi.inferenceservices.create(service_request)
    print(f"inferenceservice_huggingface: {inferenceservice.id}")
    ctx["inferenceservice_huggingface"] = inferenceservice

    wait_for_success(
        lambda: dyffapi.inferenceservices.get(inferenceservice.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_models_create_huggingface",
    ]
)
def test_inferenceservices_create_vllm(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    if pytestconfig.getoption("skip_huggingface"):
        pytest.skip()
    if not pytestconfig.getoption("enable_vllm"):
        pytest.skip()
    if not pytestconfig.getoption("test_remote"):
        pytest.skip()

    account = ctx["account"]
    model: Model = ctx["model_huggingface"]

    assert isinstance(dyffapi, Client)

    service_request = InferenceServiceCreateRequest(
        account=account,
        name=model.name,
        model=model.id,
        runner=InferenceServiceRunner(
            kind=InferenceServiceRunnerKind.VLLM,
            image=ContainerImageSource(
                host="registry.gitlab.com",
                name="dyff/workflows/vllm-runner",
                digest="sha256:e26f4634da9ae736ba18b905eaec327f29feeba89acf9cbfb423058c21fc10e5",
                tag="0.3.2",
            ),
            # T4 GPUs don't support bfloat format, so force standard float format
            args=["--dtype", "float16"],
            accelerator=Accelerator(
                kind="GPU",
                gpu=AcceleratorGPU(
                    hardwareTypes=["nvidia.com/gpu-t4"],
                    memory="300Mi",
                    count=1,
                ),
            ),
            resources=ModelResources(
                storage="1Gi",
                # vLLM requires lot of memory, even for small models
                memory="8Gi",
            ),
        ),
        interface=InferenceInterface(
            # This is the inference endpoint for the vLLM runner
            endpoint="generate",
            # The output records should look like: {"text": "To be, or not to be"}
            outputSchema=DataSchema.make_output_schema(
                DyffDataSchema(
                    components=["text.Text"],
                ),
            ),
            # How to convert the input dataset into the format the runner expects
            inputPipeline=[
                # {"text": "The question"} -> {"prompt": "The question"}
                SchemaAdapter(
                    kind="TransformJSON",
                    configuration={
                        "prompt": "$.text",
                    },
                ),
            ],
            # How to convert the runner output to match outputSchema
            outputPipeline=[
                # {"text": ["The answer"]} -> [{"text": "The answer"}]
                SchemaAdapter(
                    kind="ExplodeCollections",
                    configuration={"collections": ["text"]},
                ),
            ],
        ),
    )

    inferenceservice = dyffapi.inferenceservices.create(service_request)
    print(f"inferenceservice_vllm: {inferenceservice.id}")
    ctx["inferenceservice_vllm"] = inferenceservice

    wait_for_success(
        lambda: dyffapi.inferenceservices.get(inferenceservice.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_inferenceservices_create_mock",
    ]
)
def test_inferencesessions_create_mock(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    account = ctx["account"]
    service: InferenceService = ctx["inferenceservice_mock"]

    session_request = InferenceSessionCreateRequest(
        account=account,
        inferenceService=service.id,
        useSpotPods=False,
        accelerator=service.runner.accelerator if service.runner else None,
    )
    session_and_token = dyffapi.inferencesessions.create(session_request)
    session = session_and_token.inferencesession

    print(f"inferencesession_mock: {session.id}")
    ctx["inferencesession_mock"] = session
    ctx["session_token_mock"] = session_and_token.token

    wait_for_ready(dyffapi, session.id, timeout=timedelta(minutes=5))


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_inferencesessions_create_mock",
    ]
)
def test_inferencesessions_infer_mock(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    session: InferenceSession = ctx["inferencesession_mock"]

    if pytestconfig.getoption("test_remote"):
        assert isinstance(dyffapi, Client)
        session_client = dyffapi.inferencesessions.client(
            session.id,
            ctx["session_token_mock"],
            interface=session.inferenceService.interface,
        )
        response = session_client.infer({"text": "Open the pod bay doors, Hal!"})
    else:
        assert isinstance(dyffapi, DyffLocalPlatform)
        response = dyffapi.inferencesessions.infer(
            session.id, "generate", {"text": "Open the pod bay doors, Hal!"}
        )
    print(f"infer_mock: {response}")


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_inferencesessions_create_mock",
    ]
)
def test_inferencesessions_infer_with_created_token(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    session: InferenceSession = ctx["inferencesession_mock"]
    token = dyffapi.inferencesessions.token(
        session.id, expires=datetime.now(timezone.utc) + timedelta(minutes=5)
    )

    if pytestconfig.getoption("test_remote"):
        assert isinstance(dyffapi, Client)
        session_client = dyffapi.inferencesessions.client(
            session.id,
            token,
            interface=session.inferenceService.interface,
        )
        response = session_client.infer({"text": "Open the pod bay doors, Hal!"})
    else:
        assert isinstance(dyffapi, DyffLocalPlatform)
        response = dyffapi.inferencesessions.infer(
            session.id, "generate", {"text": "Open the pod bay doors, Hal!"}
        )
    print(f"infer_with_created_token: {response}")


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_inferenceservices_create_huggingface",
    ]
)
def test_inferencesessions_create_huggingface(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    if pytestconfig.getoption("skip_huggingface"):
        pytest.skip()

    account = ctx["account"]
    service: InferenceService = ctx["inferenceservice_huggingface"]

    session_request = InferenceSessionCreateRequest(
        account=account,
        inferenceService=service.id,
        useSpotPods=False,
        accelerator=service.runner.accelerator if service.runner else None,
    )
    session_and_token = dyffapi.inferencesessions.create(session_request)
    session = session_and_token.inferencesession

    print(f"inferencesession_huggingface: {session.id}")
    ctx["inferencesession_huggingface"] = session
    ctx["session_token_huggingface"] = session_and_token.token

    wait_for_ready(dyffapi, session.id, timeout=timedelta(minutes=10))


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_inferencesessions_create_huggingface",
    ]
)
def test_inferencesessions_infer_huggingface(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    if pytestconfig.getoption("skip_huggingface"):
        pytest.skip()

    session: InferenceSession = ctx["inferencesession_huggingface"]

    if pytestconfig.getoption("test_remote"):
        assert isinstance(dyffapi, Client)
        session_client = dyffapi.inferencesessions.client(
            session.id,
            ctx["session_token_huggingface"],
            interface=session.inferenceService.interface,
        )
        response = session_client.infer({"text": "Open the pod bay doors, Hal!"})
    else:
        assert isinstance(dyffapi, DyffLocalPlatform)
        response = dyffapi.inferencesessions.infer(
            session.id, "generate", {"text": "Open the pod bay doors, Hal!"}
        )
    print(f"infer_huggingface: {response}")


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_datasets_create",
        "test_inferenceservices_create_mock",
    ]
)
def test_evaluations_create(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    account = ctx["account"]
    dataset = ctx["dataset"]

    inferenceservice = ctx["inferenceservice_mock"]
    evaluation_request = EvaluationCreateRequest(
        account=account,
        dataset=dataset.id,
        inferenceSession=EvaluationInferenceSessionRequest(
            inferenceService=inferenceservice.id,
            expires=datetime.now(timezone.utc) + timedelta(days=1),
            replicas=1,
            useSpotPods=False,
        ),
        replications=2,
        workersPerReplica=2,
    )
    evaluation = dyffapi.evaluations.create(evaluation_request)
    print(f"evaluation: {evaluation.id}")
    ctx["evaluation"] = evaluation

    wait_for_success(
        lambda: dyffapi.evaluations.get(evaluation.id),
        timeout=timedelta(minutes=10),
    )


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_datasets_create_tiny",
        "test_inferenceservices_create_huggingface",
    ]
)
def test_evaluations_create_huggingface(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    if pytestconfig.getoption("skip_huggingface"):
        pytest.skip()

    account = ctx["account"]
    dataset = ctx["dataset_tiny"]

    inferenceservice = ctx["inferenceservice_huggingface"]
    evaluation_request = EvaluationCreateRequest(
        account=account,
        dataset=dataset.id,
        inferenceSession=EvaluationInferenceSessionRequest(
            inferenceService=inferenceservice.id,
            expires=datetime.now(timezone.utc) + timedelta(days=1),
            replicas=1,
            useSpotPods=False,
        ),
        replications=2,
        workersPerReplica=2,
    )
    evaluation = dyffapi.evaluations.create(evaluation_request)
    print(f"evaluation_huggingface: {evaluation.id}")
    ctx["evaluation_huggingface"] = evaluation

    wait_for_success(
        lambda: dyffapi.evaluations.get(evaluation.id),
        timeout=timedelta(minutes=10),
    )


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_datasets_create_tiny",
        "test_inferenceservices_create_vllm",
    ]
)
def test_evaluations_create_vllm(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    if pytestconfig.getoption("skip_huggingface"):
        pytest.skip()
    if not pytestconfig.getoption("enable_vllm"):
        pytest.skip()

    account = ctx["account"]
    dataset = ctx["dataset_tiny"]

    inferenceservice = ctx["inferenceservice_vllm"]
    evaluation_request = EvaluationCreateRequest(
        account=account,
        dataset=dataset.id,
        inferenceSession=EvaluationInferenceSessionRequest(
            inferenceService=inferenceservice.id,
            expires=datetime.now(timezone.utc) + timedelta(days=1),
            replicas=1,
            useSpotPods=False,
        ),
        replications=2,
        workersPerReplica=2,
    )
    evaluation = dyffapi.evaluations.create(evaluation_request)
    print(f"evaluation_vllm: {evaluation.id}")
    ctx["evaluation_vllm"] = evaluation

    wait_for_success(
        lambda: dyffapi.evaluations.get(evaluation.id),
        # It can take a really long time to 1) allocate a GPU node, and then
        # 2) pull the gigantic CUDA-enabled Docker image
        timeout=timedelta(minutes=30),
    )


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_datasets_create",
        "test_inferencesessions_create_mock",
    ]
)
def test_evaluations_create_with_session_reference(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    account = ctx["account"]
    dataset = ctx["dataset"]
    session = ctx["inferencesession_mock"]

    evaluation_request = EvaluationCreateRequest(
        account=account,
        dataset=dataset.id,
        inferenceSessionReference=session.id,
        replications=2,
        workersPerReplica=2,
    )
    evaluation = dyffapi.evaluations.create(evaluation_request)
    print(f"evaluation_with_session_reference: {evaluation.id}")

    wait_for_success(
        lambda: dyffapi.evaluations.get(evaluation.id),
        timeout=timedelta(minutes=5),
    )


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.depends(
    on=[
        "test_datasets_create",
    ]
)
def test_evaluations_import(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    if pytestconfig.getoption("test_remote"):
        pytest.skip()
    assert isinstance(dyffapi, DyffLocalPlatform)

    account = ctx["account"]
    dataset = ctx["dataset"]

    evaluation_request = EvaluationCreateRequest(
        account=account,
        dataset=dataset.id,
        inferenceSession=EvaluationInferenceSessionRequest(inferenceService=""),
    )
    evaluation = dyffapi.evaluations.import_data(
        datafiles / "evaluation", evaluation_request=evaluation_request
    )

    print(f"evaluation_import: {evaluation.id}")


# ----------------------------------------------------------------------------
# Analysis-related workflows
# ----------------------------------------------------------------------------


@pytest.mark.datafiles(DATA_DIR)
def test_modules_create_jupyter_notebook(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    account = ctx["account"]
    module_jupyter_notebook_dir = datafiles / "module_jupyter_notebook"
    module_jupyter_notebook = dyffapi.modules.create_package(
        module_jupyter_notebook_dir, account=account, name="module_jupyter_notebook"
    )
    dyffapi.modules.upload_package(module_jupyter_notebook, module_jupyter_notebook_dir)
    print(f"module_jupyter_notebook: {module_jupyter_notebook.id}")
    ctx["module_jupyter_notebook"] = module_jupyter_notebook

    wait_for_success(
        lambda: dyffapi.modules.get(module_jupyter_notebook.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.datafiles(DATA_DIR)
def test_modules_create_jupyter_notebook_no_scores(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    account = ctx["account"]
    module_jupyter_notebook_dir = datafiles / "module_jupyter_notebook_no_scores"
    module_jupyter_notebook = dyffapi.modules.create_package(
        module_jupyter_notebook_dir,
        account=account,
        name="module_jupyter_notebook_no_scores",
    )
    dyffapi.modules.upload_package(module_jupyter_notebook, module_jupyter_notebook_dir)
    print(f"module_jupyter_notebook_no_scores: {module_jupyter_notebook.id}")
    ctx["module_jupyter_notebook_no_scores"] = module_jupyter_notebook

    wait_for_success(
        lambda: dyffapi.modules.get(module_jupyter_notebook.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.datafiles(DATA_DIR)
def test_modules_create_python_function(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    account = ctx["account"]
    module_python_function_dir = datafiles / "module_python_function"
    module_python_function = dyffapi.modules.create_package(
        module_python_function_dir, account=account, name="module_python_function"
    )
    dyffapi.modules.upload_package(module_python_function, module_python_function_dir)
    print(f"module_python_function: {module_python_function.id}")
    ctx["module_python_function"] = module_python_function

    wait_for_success(
        lambda: dyffapi.modules.get(module_python_function.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.datafiles(DATA_DIR)
def test_modules_create_python_rubric(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    account = ctx["account"]
    module_python_rubric_dir = datafiles / "module_python_rubric"
    module_python_rubric = dyffapi.modules.create_package(
        module_python_rubric_dir, account=account, name="module_python_rubric"
    )
    dyffapi.modules.upload_package(module_python_rubric, module_python_rubric_dir)
    print(f"module_python_rubric: {module_python_rubric.id}")
    ctx["module_python_rubric"] = module_python_rubric

    wait_for_success(
        lambda: dyffapi.modules.get(module_python_rubric.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.depends(
    on=[
        "test_modules_create_jupyter_notebook",
    ]
)
def test_methods_create_jupyter_notebook(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx
):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    account = ctx["account"]
    module_jupyter_notebook = ctx["module_jupyter_notebook"]
    method_jupyter_notebook_request = MethodCreateRequest(
        name="method_notebook",
        scope=MethodScope.InferenceService,
        description="""*Markdown Description*""",
        implementation=MethodImplementation(
            kind=MethodImplementationKind.JupyterNotebook,
            jupyterNotebook=MethodImplementationJupyterNotebook(
                notebookModule=module_jupyter_notebook.id,
                notebookPath="test-notebook.ipynb",
            ),
        ),
        parameters=[
            MethodParameter(keyword="trueName", description="His real name"),
            MethodParameter(
                keyword="isOutlier",
                description="If this safetycase should be used for outlier value in distribution scores.",
            ),
        ],
        inputs=[
            MethodInput(kind=MethodInputKind.Measurement, keyword="cromulence"),
        ],
        output=MethodOutput(
            kind=MethodOutputKind.SafetyCase,
            safetyCase=SafetyCaseSpec(
                name="safetycase_notebook",
                description="""*Markdown Description*""",
            ),
        ),
        scores=[
            ScoreSpec(
                name="float_unit_primary",
                title="Float (primary; with unit)",
                summary="A float with a unit that is the 'primary' score",
                minimum=0,
                maximum=1,
                unit="MJ/kg",
            ),
            ScoreSpec(
                name="int",
                title="Integer",
                summary="An Integer score",
                valence="positive",
                priority="secondary",
            ),
            ScoreSpec(
                name="int_big",
                title="Integer (Big)",
                summary="A big Integer score",
                valence="positive",
                priority="secondary",
            ),
            ScoreSpec(
                name="int_percent",
                title="Integer (Percentage)",
                summary="A percentage represented as an integer",
                valence="positive",
                priority="secondary",
                minimum=0,
                maximum=100,
            ),
            ScoreSpec(
                name="no_display",
                title="Not displayed",
                summary="A score that should not be displayed",
                valence="negative",
                priority="secondary",
            ),
            ScoreSpec(
                name="exp_rate_low",
                title="Exponential Distribution (Low Rate)",
                summary="An exponential distribution with a low rate, leading to a gradual decay.",
                valence="positive",
                priority="secondary",
                minimum=0.0,
                maximum=10.0,
            ),
            ScoreSpec(
                name="exp_rate_high",
                title="Exponential Distribution (High Rate)",
                summary="An exponential distribution with a high rate, causing rapid decay.",
                valence="positive",
                priority="secondary",
                minimum=0.0,
                maximum=10.0,
            ),
            ScoreSpec(
                name="poisson_rate_low",
                title="Poisson Distribution (Low Rate)",
                summary="A Poisson distribution with a low average event rate, generating fewer events.",
                valence="positive",
                priority="secondary",
                minimum=0,
                maximum=20,
            ),
            ScoreSpec(
                name="poisson_rate_high",
                title="Poisson Distribution (High Rate)",
                summary="A Poisson distribution with a high average event rate, generating more events.",
                valence="positive",
                priority="secondary",
                minimum=0,
                maximum=20,
            ),
            ScoreSpec(
                name="normal_standard",
                title="Normal Distribution (Standard)",
                summary="A normal distribution with a mean of 0 and a standard deviation of 1.",
                valence="positive",
                priority="secondary",
                minimum=-5.0,
                maximum=5.0,
            ),
            ScoreSpec(
                name="normal_shifted",
                title="Normal Distribution (Shifted)",
                summary="A normal distribution with a mean of 5 and a standard deviation of 2.",
                valence="positive",
                priority="secondary",
                minimum=0.0,
                maximum=10.0,
            ),
            ScoreSpec(
                name="bimodal_close",
                title="Bi-Modal Distribution (Close Peaks)",
                summary="A bi-modal distribution with two peaks close to each other, creating moderate separation.",
                valence="positive",
                priority="secondary",
                minimum=-5.0,
                maximum=15.0,
            ),
            ScoreSpec(
                name="bimodal_separated",
                title="Bi-Modal Distribution (Separated Peaks)",
                summary="A bi-modal distribution with two peaks far apart, creating clear separation between clusters.",
                valence="positive",
                priority="secondary",
                minimum=-5.0,
                maximum=20.0,
            ),
            ScoreSpec(
                name="close_together",
                title="Close Values Around 50",
                summary="Values generated close to 50 within an expanded range of ±10.",
                valence="positive",
                priority="secondary",
                minimum=0.0,
                maximum=100.0,
            ),
            ScoreSpec(
                name="in_middle",
                title="Values in the Middle",
                summary="Values generated in the middle of the range, centered around 50.",
                valence="positive",
                priority="secondary",
                minimum=0.0,
                maximum=100.0,
            ),
            ScoreSpec(
                name="near_min",
                title="Values Near Minimum",
                summary="Values generated near the minimum, within the range of 0 to 10.",
                valence="positive",
                priority="secondary",
                minimum=0.0,
                maximum=100.0,
            ),
            ScoreSpec(
                name="near_max",
                title="Values Near Maximum",
                summary="Values generated near the maximum, within the range of 90 to 100.",
                valence="positive",
                priority="secondary",
                minimum=0.0,
                maximum=100.0,
            ),
            ScoreSpec(
                name="extreme_outliers",
                title="Extreme Outliers",
                summary="Extreme outlier values that are far outside the typical range.",
                valence="positive",
                priority="secondary",
                minimum=0.0,
                maximum=100.0,
            ),
            ScoreSpec(
                name="same_values",
                title="All Values Exactly the Same",
                summary="All values are exactly the same, uniform data for testing.",
                valence="positive",
                priority="secondary",
                minimum=0.0,
                maximum=100.0,
            ),
        ],
        modules=[module_jupyter_notebook.id],
        account=account,
    )
    method_jupyter_notebook = dyffapi.methods.create(method_jupyter_notebook_request)
    print(f"method_jupyter_notebook: {method_jupyter_notebook.id}")
    ctx["method_jupyter_notebook"] = method_jupyter_notebook

    wait_for_success(
        lambda: dyffapi.methods.get(method_jupyter_notebook.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.depends(
    on=[
        "test_modules_create_jupyter_notebook_no_scores",
    ]
)
def test_methods_create_jupyter_notebook_no_scores(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx
):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    account = ctx["account"]
    module_jupyter_notebook = ctx["module_jupyter_notebook_no_scores"]
    method_jupyter_notebook_request = MethodCreateRequest(
        name="method_notebook_no_scores",
        scope=MethodScope.InferenceService,
        description="""# Markdown Description""",
        implementation=MethodImplementation(
            kind=MethodImplementationKind.JupyterNotebook,
            jupyterNotebook=MethodImplementationJupyterNotebook(
                notebookModule=module_jupyter_notebook.id,
                notebookPath="test-notebook.ipynb",
            ),
        ),
        parameters=[MethodParameter(keyword="trueName", description="His real name")],
        inputs=[
            MethodInput(kind=MethodInputKind.Measurement, keyword="cromulence"),
        ],
        output=MethodOutput(
            kind=MethodOutputKind.SafetyCase,
            safetyCase=SafetyCaseSpec(
                name="safetycase_notebook_no_scores",
                description="""# Markdown Description""",
            ),
        ),
        modules=[module_jupyter_notebook.id],
        account=account,
    )
    method_jupyter_notebook = dyffapi.methods.create(method_jupyter_notebook_request)
    print(f"method_jupyter_notebook_no_scores: {method_jupyter_notebook.id}")
    ctx["method_jupyter_notebook_no_scores"] = method_jupyter_notebook

    wait_for_success(
        lambda: dyffapi.methods.get(method_jupyter_notebook.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.depends(
    on=[
        "test_modules_create_python_function",
    ]
)
def test_methods_create_python_function(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx
):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    account = ctx["account"]
    module_python_function = ctx["module_python_function"]
    method_python_function_request = MethodCreateRequest(
        account=account,
        modules=[module_python_function.id],
        name="method_python_function",
        scope=MethodScope.Evaluation,
        description="""# Markdown Description""",
        implementation=MethodImplementation(
            kind=MethodImplementationKind.PythonFunction,
            pythonFunction=MethodImplementationPythonFunction(
                fullyQualifiedName="dyff.fake.method.blurst_count",
            ),
        ),
        parameters=[
            MethodParameter(keyword="embiggen", description="Who is being embiggened")
        ],
        inputs=[
            MethodInput(kind=MethodInputKind.Dataset, keyword="dataset"),
            MethodInput(kind=MethodInputKind.Evaluation, keyword="outputs"),
        ],
        output=MethodOutput(
            kind=MethodOutputKind.Measurement,
            measurement=MeasurementSpec(
                name="example.dyff.io/blurst-count",
                description="The number of times the word 'blurst' appears in the text.",
                level=MeasurementLevel.Instance,
                schema=DataSchema(
                    arrowSchema=arrow.encode_schema(
                        arrow.arrow_schema(BlurstCountScoredItem)
                    )
                ),
            ),
        ),
    )
    method_python_function = dyffapi.methods.create(method_python_function_request)
    print(f"method_python_function: {method_python_function.id}")
    ctx["method_python_function"] = method_python_function

    wait_for_success(
        lambda: dyffapi.methods.get(method_python_function.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.depends(
    on=[
        "test_datasets_create",
        "test_evaluations_create",
        "test_methods_create_python_function",
    ]
)
def test_measurements_create_python_function(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx
):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    account = ctx["account"]
    evaluation = ctx["evaluation"]
    inferenceservice = ctx["inferenceservice_mock"]
    model = ctx["model_mock"]
    dataset = ctx["dataset"]
    method_python_function = ctx["method_python_function"]
    measurement_python_function_request = AnalysisCreateRequest(
        account=account,
        method=method_python_function.id,
        scope=AnalysisScope(
            evaluation=evaluation.id,
            dataset=dataset.id,
            inferenceService=inferenceservice.id,
            model=(model and model.id),
        ),
        arguments=[
            AnalysisArgument(keyword="embiggen", value="smallest"),
        ],
        inputs=[
            AnalysisInput(keyword="dataset", entity=dataset.id),
            AnalysisInput(keyword="outputs", entity=evaluation.id),
        ],
    )
    measurement_python_function = dyffapi.measurements.create(
        measurement_python_function_request
    )
    print(f"measurement_python_function: {measurement_python_function.id}")
    ctx["measurement_python_function"] = measurement_python_function

    wait_for_success(
        lambda: dyffapi.measurements.get(measurement_python_function.id),
        timeout=timedelta(minutes=10),
    )


@pytest.mark.depends(
    on=[
        "test_datasets_create",
        "test_evaluations_create",
        "test_modules_create_python_rubric",
    ]
)
def test_reports_create(pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    account = ctx["account"]
    evaluation = ctx["evaluation"]
    module = ctx["module_python_rubric"]
    report_request = ReportCreateRequest(
        account=account,
        rubric="dyff.fake.rubric.BlurstCount",
        evaluation=evaluation.id,
        modules=[module.id],
    )
    report = dyffapi.reports.create(report_request)
    print(f"report: {report.id}")
    ctx["report"] = report

    wait_for_success(
        lambda: dyffapi.reports.get(report.id),
        timeout=timedelta(minutes=5),
    )


@pytest.mark.depends(
    on=[
        "test_methods_create_jupyter_notebook",
        "test_measurements_create_python_function",
    ]
)
# Run multiple times so we have multiple SafetyCases for one service; needed
# for testing the frontend UI.
@pytest.mark.parametrize("replication", range(3))
def test_safetycase(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, replication
):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    account = ctx["account"]
    inferenceservice = ctx["inferenceservice_mock"]
    model = ctx["model_mock"]
    method_jupyter_notebook = ctx["method_jupyter_notebook"]
    measurement_python_function = ctx["measurement_python_function"]

    # SafetyCase for JupyterNotebook
    safetycase_jupyter_notebook_request = AnalysisCreateRequest(
        account=account,
        method=method_jupyter_notebook.id,
        scope=AnalysisScope(
            evaluation=None,
            dataset=None,
            inferenceService=inferenceservice.id,
            model=(model and model.id),
        ),
        arguments=[
            AnalysisArgument(keyword="trueName", value="Hans Sprungfeld"),
            AnalysisArgument(keyword="isOutlier", value="true"),
        ],
        inputs=[
            AnalysisInput(keyword="cromulence", entity=measurement_python_function.id),
        ],
    )
    safetycase_jupyter_notebook = dyffapi.safetycases.create(
        safetycase_jupyter_notebook_request
    )
    print(f"safetycase_jupyter_notebook: {safetycase_jupyter_notebook.id}")
    ctx["safetycase_jupyter_notebook"] = safetycase_jupyter_notebook

    wait_for_success(
        lambda: dyffapi.safetycases.get(safetycase_jupyter_notebook.id),
        timeout=timedelta(minutes=5),
    )


# Comparison safetycase for same method, different model
@pytest.mark.depends(
    on=[
        "test_methods_create_jupyter_notebook",
        "test_measurements_create_python_function",
    ]
)
@pytest.mark.parametrize("replication", range(COMPARISON_REPLICATIONS))
def test_safetycase_compare(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, replication
):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()
    if not pytestconfig.getoption("enable_comparisons"):
        pytest.skip()

    account = ctx["account"]
    inferenceservice = ctx[f"inferenceservice_mock_compare_{replication}"]
    model = ctx[f"model_mock_compare_{replication}"]
    method_jupyter_notebook = ctx["method_jupyter_notebook"]  # Same method
    measurement_python_function = ctx[f"measurement_python_function"]
    isOutlier = "true" if replication == 0 else "false"

    # SafetyCase for JupyterNotebook
    safetycase_jupyter_notebook_request = AnalysisCreateRequest(
        account=account,
        method=method_jupyter_notebook.id,
        scope=AnalysisScope(
            evaluation=None,
            dataset=None,
            inferenceService=inferenceservice.id,
            model=(model and model.id),
        ),
        arguments=[
            AnalysisArgument(keyword="trueName", value="Hans Sprungfeld"),
            AnalysisArgument(keyword="isOutlier", value=isOutlier),
        ],
        inputs=[
            AnalysisInput(keyword="cromulence", entity=measurement_python_function.id),
        ],
    )
    safetycase_jupyter_notebook = dyffapi.safetycases.create(
        safetycase_jupyter_notebook_request
    )
    print(
        f"safetycase_jupyter_notebook_compare_{replication}: {safetycase_jupyter_notebook.id}"
    )
    ctx[f"safetycase_jupyter_notebook_compare_{replication}"] = (
        safetycase_jupyter_notebook
    )

    wait_for_success(
        lambda: dyffapi.safetycases.get(safetycase_jupyter_notebook.id),
        timeout=timedelta(minutes=5),
    )


@pytest.mark.depends(
    on=[
        "test_methods_create_jupyter_notebook_no_scores",
        "test_measurements_create_python_function",
    ]
)
def test_safetycase_no_scores(
    pytestconfig,
    dyffapi: Client | DyffLocalPlatform,
    ctx,
):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    account = ctx["account"]
    inferenceservice = ctx["inferenceservice_mock"]
    model = ctx["model_mock"]
    method_jupyter_notebook = ctx["method_jupyter_notebook_no_scores"]
    measurement_python_function = ctx["measurement_python_function"]

    # SafetyCase for JupyterNotebook
    safetycase_jupyter_notebook_request = AnalysisCreateRequest(
        account=account,
        method=method_jupyter_notebook.id,
        scope=AnalysisScope(
            evaluation=None,
            dataset=None,
            inferenceService=inferenceservice.id,
            model=(model and model.id),
        ),
        arguments=[
            AnalysisArgument(keyword="trueName", value="Hans Sprungfeld"),
        ],
        inputs=[
            AnalysisInput(keyword="cromulence", entity=measurement_python_function.id),
        ],
    )
    safetycase_jupyter_notebook = dyffapi.safetycases.create(
        safetycase_jupyter_notebook_request
    )
    print(f"safetycase_jupyter_notebook_no_scores: {safetycase_jupyter_notebook.id}")
    ctx["safetycase_jupyter_notebook_no_scores"] = safetycase_jupyter_notebook

    wait_for_success(
        lambda: dyffapi.safetycases.get(safetycase_jupyter_notebook.id),
        timeout=timedelta(minutes=5),
    )


@pytest.mark.depends(
    on=[
        "test_safetycase",
    ]
)
def test_safetycase_publish(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    safetycase: SafetyCase = ctx["safetycase_jupyter_notebook"]
    if not pytestconfig.getoption("test_remote"):
        pytest.skip()

    assert isinstance(dyffapi, Client)

    dyffapi.safetycases.publish(safetycase.id, "preview")
    dyffapi.methods.publish(safetycase.method.id, "preview")
    if safetycase.scope.inferenceService:
        dyffapi.inferenceservices.publish(safetycase.scope.inferenceService, "preview")
    if safetycase.scope.model:
        dyffapi.models.publish(safetycase.scope.model, "preview")
    time.sleep(10)
    labels = dyffapi.safetycases.get(safetycase.id).labels
    assert labels["dyff.io/access"] == "internal"


@pytest.mark.depends(
    on=[
        "test_safetycase_compare",
    ]
)
@pytest.mark.parametrize("replication", range(COMPARISON_REPLICATIONS))
def test_safetycase_publish_compare(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles, replication
):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()
    if not pytestconfig.getoption("enable_comparisons"):
        pytest.skip()
    if not pytestconfig.getoption("test_remote"):
        pytest.skip()

    safetycase: SafetyCase = ctx[f"safetycase_jupyter_notebook_compare_{replication}"]

    assert isinstance(dyffapi, Client)

    dyffapi.safetycases.publish(safetycase.id, "preview")
    dyffapi.methods.publish(safetycase.method.id, "preview")
    if safetycase.scope.inferenceService:
        dyffapi.inferenceservices.publish(safetycase.scope.inferenceService, "preview")
    if safetycase.scope.model:
        dyffapi.models.publish(safetycase.scope.model, "preview")
    time.sleep(10)
    labels = dyffapi.safetycases.get(safetycase.id).labels
    assert labels["dyff.io/access"] == "internal"


@pytest.mark.depends(
    on=[
        "test_safetycase",
    ]
)
def test_scores_get(pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles):
    if pytestconfig.getoption("test_remote"):
        # TODO: Enable once method is implemented in remote client
        pytest.skip()
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()
    # TODO: Enable once method is implemented in remote client
    assert isinstance(dyffapi, DyffLocalPlatform)

    safetycase: SafetyCase = ctx["safetycase_jupyter_notebook"]
    scores = dyffapi.scores.get(analysis=safetycase.id)
    print(f"scores_get: {[score.name for score in scores]}")


# ----------------------------------------------------------------------------
# Tests for error handling
# ----------------------------------------------------------------------------


@pytest.mark.depends(
    on=[
        "test_modules_create_python_function",
    ]
)
def test_methods_python_function_raises_error(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx
):
    """Create a Method backed by a Python function that deliberately raises an error."""
    if pytestconfig.getoption("skip_errors"):
        pytest.skip()
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    account = ctx["account"]
    module_python_function = ctx["module_python_function"]
    method_python_function_request = MethodCreateRequest(
        account=account,
        modules=[module_python_function.id],
        name="method_python_function",
        scope=MethodScope.Evaluation,
        description="""# Method that deliberately raises an error""",
        implementation=MethodImplementation(
            kind=MethodImplementationKind.PythonFunction,
            pythonFunction=MethodImplementationPythonFunction(
                fullyQualifiedName="dyff.fake.method.raise_error",
            ),
        ),
        parameters=[
            MethodParameter(keyword="embiggen", description="Who is being embiggened")
        ],
        inputs=[
            MethodInput(kind=MethodInputKind.Dataset, keyword="dataset"),
            MethodInput(kind=MethodInputKind.Evaluation, keyword="outputs"),
        ],
        output=MethodOutput(
            kind=MethodOutputKind.Measurement,
            measurement=MeasurementSpec(
                name="example.dyff.io/blurst-count",
                description="The number of times the word 'blurst' appears in the text.",
                level=MeasurementLevel.Instance,
                schema=DataSchema(
                    arrowSchema=arrow.encode_schema(
                        arrow.arrow_schema(BlurstCountScoredItem)
                    )
                ),
            ),
        ),
    )
    method_python_function_raises_error = dyffapi.methods.create(
        method_python_function_request
    )
    print(
        f"method_python_function_raises_error: {method_python_function_raises_error.id}"
    )
    ctx["method_python_function_raises_error"] = method_python_function_raises_error

    wait_for_success(
        lambda: dyffapi.methods.get(method_python_function_raises_error.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.depends(
    on=[
        "test_datasets_create",
        "test_evaluations_create",
        "test_methods_python_function_raises_error",
    ]
)
def test_measurements_python_function_raises_error(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx
):
    """Run a Measurement that calls a Python function that deliberately raises an
    error."""
    if pytestconfig.getoption("skip_errors"):
        pytest.skip()
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    account = ctx["account"]
    evaluation = ctx["evaluation"]
    inferenceservice = ctx["inferenceservice_mock"]
    model = ctx["model_mock"]
    dataset = ctx["dataset"]
    method_python_function_raises_error = ctx["method_python_function_raises_error"]
    measurement_python_function_request = AnalysisCreateRequest(
        account=account,
        method=method_python_function_raises_error.id,
        scope=AnalysisScope(
            evaluation=evaluation.id,
            dataset=dataset.id,
            inferenceService=inferenceservice.id,
            model=(model and model.id),
        ),
        arguments=[
            AnalysisArgument(keyword="embiggen", value="smallest"),
        ],
        inputs=[
            AnalysisInput(keyword="dataset", entity=dataset.id),
            AnalysisInput(keyword="outputs", entity=evaluation.id),
        ],
    )
    measurement_python_function_raises_error = dyffapi.measurements.create(
        measurement_python_function_request
    )
    print(
        f"measurement_python_function_raises_error: {measurement_python_function_raises_error.id}"
    )
    ctx["measurement_python_function_raises_error"] = (
        measurement_python_function_raises_error
    )

    terminal_status = wait_for_terminal_status(
        lambda: dyffapi.measurements.get(measurement_python_function_raises_error.id),
        timeout=timedelta(minutes=5),
    )

    # Expected to raise exception -> failure status
    assert is_status_failure(terminal_status)


@pytest.mark.depends(
    on=[
        "test_measurements_python_function_raises_error",
    ]
)
def test_measurements_error_log(pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx):
    """Test that the logs from a Measurement that raised an error are present and
    contain the expected error information."""
    if pytestconfig.getoption("skip_errors"):
        pytest.skip()
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    expected_logs = {
        "stdout message": False,
        "stderr message": False,
        "RuntimeError: deliberate error": False,
        "Traceback": False,
    }
    if isinstance(dyffapi, DyffLocalPlatform):
        # TODO: LocalPlatform hasn't implemented .logs() yet
        pytest.skip()
    measurement = ctx["measurement_python_function_raises_error"]
    logs = list(dyffapi.measurements.logs(measurement.id))
    for line in logs:
        for k in expected_logs:
            if k in line:
                expected_logs[k] = True
    missing = [k for k, v in expected_logs.items() if not v]
    assert missing == []


@pytest.mark.depends(
    on=[
        "test_datasets_create",
        "test_evaluations_create",
        "test_modules_create_python_rubric",
    ]
)
def test_reports_rubric_raises_error(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx
):
    """Run a Report that calls a Python function that deliberately raises an error."""

    if pytestconfig.getoption("skip_errors"):
        pytest.skip()
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    account = ctx["account"]
    evaluation = ctx["evaluation"]
    module = ctx["module_python_rubric"]
    report_request = ReportCreateRequest(
        account=account,
        rubric="dyff.fake.rubric.RaiseError",
        evaluation=evaluation.id,
        modules=[module.id],
    )
    report = dyffapi.reports.create(report_request)
    print(f"report_rubric_raises_error: {report.id}")
    ctx["report_rubric_raises_error"] = report

    terminal_status = wait_for_terminal_status(
        lambda: dyffapi.reports.get(report.id),
        timeout=timedelta(minutes=5),
    )

    # Expected to raise exception -> failure status
    assert is_status_failure(terminal_status)


@pytest.mark.depends(
    on=[
        "test_reports_rubric_raises_error",
    ]
)
def test_reports_error_log(pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx):
    """Test that the logs from a Report that raised an error are present and contain the
    expected error information."""
    if pytestconfig.getoption("skip_errors"):
        pytest.skip()
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()

    expected_logs = {
        "stdout message": False,
        "stderr message": False,
        "RuntimeError: deliberate error": False,
        "Traceback": False,
    }
    if isinstance(dyffapi, DyffLocalPlatform):
        # TODO: LocalPlatform hasn't implemented .logs() yet
        pytest.skip()
    report = ctx["report_rubric_raises_error"]
    logs = list(dyffapi.reports.logs(report.id))
    for line in logs:
        for k in expected_logs:
            if k in line:
                expected_logs[k] = True
    missing = [k for k, v in expected_logs.items() if not v]
    assert missing == []


@pytest.mark.datafiles(DATA_DIR)
def test_client_impossible_timeout(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx, datafiles
):
    if pytestconfig.getoption("skip_errors"):
        pytest.skip()
    if isinstance(dyffapi, DyffLocalPlatform):
        pytest.skip()

    import httpx

    timeout_client = _create_client(pytestconfig, timeout=Timeout(5.0, write=0.0001))

    account = ctx["account"]
    dataset_dir = datafiles / "dataset"
    dataset = timeout_client.datasets.create_arrow_dataset(
        dataset_dir, account=account, name="dataset"
    )
    with pytest.raises(httpx.WriteTimeout):
        timeout_client.datasets.upload_arrow_dataset(dataset, dataset_dir)


@pytest.mark.depends(
    on=[
        "test_modules_create_jupyter_notebook",
    ]
)
def test_methods_create_jupyter_notebook_raises_error(
    pytestconfig, dyffapi: Client | DyffLocalPlatform, ctx
):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()
    if pytestconfig.getoption("skip_errors"):
        pytest.skip()

    account = ctx["account"]
    module_jupyter_notebook = ctx["module_jupyter_notebook"]
    method_jupyter_notebook_request = MethodCreateRequest(
        name="method_notebook",
        scope=MethodScope.InferenceService,
        description="""# Markdown Description""",
        implementation=MethodImplementation(
            kind=MethodImplementationKind.JupyterNotebook,
            jupyterNotebook=MethodImplementationJupyterNotebook(
                notebookModule=module_jupyter_notebook.id,
                notebookPath="test-notebook-raises-error.ipynb",
            ),
        ),
        parameters=[MethodParameter(keyword="trueName", description="His real name")],
        output=MethodOutput(
            kind=MethodOutputKind.SafetyCase,
            safetyCase=SafetyCaseSpec(
                name="safetycase_notebook",
                description="""# Markdown Description""",
            ),
        ),
        scores=[
            ScoreSpec(
                name="int",
                title="Integer",
                summary="An Integer score",
                valence="positive",
            ),
        ],
        modules=[module_jupyter_notebook.id],
        account=account,
    )
    method_jupyter_notebook = dyffapi.methods.create(method_jupyter_notebook_request)
    print(f"method_jupyter_notebook_raises_error: {method_jupyter_notebook.id}")
    ctx["method_jupyter_notebook_raises_error"] = method_jupyter_notebook

    wait_for_success(
        lambda: dyffapi.methods.get(method_jupyter_notebook.id),
        timeout=timedelta(minutes=2),
    )


@pytest.mark.depends(
    on=[
        "test_methods_create_jupyter_notebook_raises_error",
    ]
)
def test_safetycase_raises_error(
    pytestconfig,
    dyffapi: Client | DyffLocalPlatform,
    ctx,
):
    if pytestconfig.getoption("skip_analyses"):
        pytest.skip()
    if pytestconfig.getoption("skip_errors"):
        pytest.skip()

    account = ctx["account"]
    inferenceservice = ctx["inferenceservice_mock"]
    model = ctx["model_mock"]
    method_jupyter_notebook = ctx["method_jupyter_notebook_raises_error"]

    # SafetyCase for JupyterNotebook
    safetycase_jupyter_notebook_request = AnalysisCreateRequest(
        account=account,
        method=method_jupyter_notebook.id,
        scope=AnalysisScope(
            evaluation=None,
            dataset=None,
            inferenceService=inferenceservice.id,
            model=(model and model.id),
        ),
        arguments=[
            AnalysisArgument(keyword="trueName", value="Hans Sprungfeld"),
        ],
    )
    safetycase_jupyter_notebook = dyffapi.safetycases.create(
        safetycase_jupyter_notebook_request
    )
    print(f"safetycase_jupyter_notebook_raises_error: {safetycase_jupyter_notebook.id}")
    ctx["safetycase_jupyter_notebook_raises_error"] = safetycase_jupyter_notebook

    terminal_status = wait_for_terminal_status(
        lambda: dyffapi.safetycases.get(safetycase_jupyter_notebook.id),
        timeout=timedelta(minutes=5),
    )

    # Expected to raise exception -> failure status
    assert is_status_failure(terminal_status)
