from typing import Dict, List, Optional, Union
from typing_extensions import Literal

from clipped.compact.pydantic import StrictStr
from clipped.types.ref_or_obj import RefField

from congruent.schemas.agent import Agent
from congruent.schemas.history import History
from congruent.schemas.tool import Tool
from polyaxon._flow.environment import V1Environment
from polyaxon._flow.init import V1Init
from polyaxon._flow.run.enums import V1RunKind
from polyaxon._flow.run.job import V1Job
from polyaxon._k8s import k8s_schemas


class LLM(V1Job):
    """LLMs are used to make calls to an LLM API.

    Args:
        kind: str, should be equal `llm`
        environment: [V1Environment](/docs/core/specification/environment/), optional
        connections: List[str], optional
        volumes: List[[Kubernetes Volume](https://kubernetes.io/docs/concepts/storage/volumes/)],
             optional
        init: List[[V1Init](/docs/core/specification/init/)], optional
        sidecars: List[[sidecar containers](/docs/core/specification/sidecars/)], optional
        container: [Kubernetes Container](https://kubernetes.io/docs/concepts/containers/)
        bot: V1Bot, optional
        prompt: str, optional
        memory: bool, optional
        history: History, optional

    ## YAML usage

    ```yaml
    >>> run:
    >>>   kind: llm
    >>>   environment:
    >>>   connections:
    >>>   volumes:
    >>>   init:
    >>>   sidecars:
    >>>   container:
    >>>   prompt:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.schemas import V1Environment, V1Init
    >>> from congruent.schemas.llm import LLM
    >>> from polyaxon import k8s
    >>> job = V1LLM(
    >>>     environment=V1Environment(...),
    >>>     connections=["connection-name1"],
    >>>     volumes=[k8s.V1Volume(...)],
    >>>     init=[V1Init(...)],
    >>>     sidecars=[k8s.V1Container(...)],
    >>>     container=k8s.V1Container(...),
    >>> )
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools that this component's runtime is a job.

    If you are using the python client to create the runtime,
    this field is not required and is set by default.

    ```yaml
    >>> run:
    >>>   kind: job
    ```

    ### environment

    Optional [environment section](/docs/core/specification/environment/),
    it provides a way to inject pod related information.

    ```yaml
    >>> run:
    >>>   kind: job
    >>>   environment:
    >>>     labels:
    >>>        key1: "label1"
    >>>        key2: "label2"
    >>>      annotations:
    >>>        key1: "value1"
    >>>        key2: "value2"
    >>>      nodeSelector:
    >>>        node_label: node_value
    >>>      ...
    >>>  ...
    ```

    ### connections

    A list of [connection names](/docs/setup/connections/) to resolve for the job.

    <blockquote class="light">
    If you are referencing a connection it must be configured.
    All referenced connections will be checked:

     * If they are accessible in the context of the project of this run

     * If the user running the operation can have access to those connections
    </blockquote>

     After checks, the connections will be resolved and inject any volumes, secrets, configMaps,
    environment variables for your main container to function correctly.

    ```yaml
    >>> run:
    >>>   kind: job
    >>>   connections: [connection1, connection2]
    ```

    ### volumes

    A list of [Kubernetes Volumes](https://kubernetes.io/docs/concepts/storage/volumes/)
    to resolve and mount for your jobs.

    This is an advanced use-case where configuring a connection is not an option.

    When you add a volume you need to mount it manually to your container(s).

    ```yaml
    >>> run:
    >>>   kind: job
    >>>   volumes:
    >>>     - name: volume1
    >>>       persistentVolumeClaim:
    >>>         claimName: pvc1
    >>>   ...
    >>>   container:
    >>>     name: myapp-container
    >>>     image: busybox:1.28
    >>>     command: ['sh', '-c', 'echo custom init container']
    >>>     volumeMounts:
    >>>     - name: volume1
    >>>       mountPath: /mnt/vol/path
    ```

    ### init

    A list of [init handlers and containers](/docs/core/specification/init/)
    to resolve for the job.

    <blockquote class="light">
    If you are referencing a connection it must be configured.
    All referenced connections will be checked:

     * If they are accessible in the context of the project of this run

     * If the user running the operation can have access to those connections
    </blockquote>

    ```yaml
    >>> run:
    >>>   kind: job
    >>>   init:
    >>>     - artifacts:
    >>>         dirs: ["path/on/the/default/artifacts/store"]
    >>>     - connection: gcs-large-datasets
    >>>       artifacts:
    >>>         dirs: ["data"]
    >>>       container:
    >>>         resources:
    >>>           requests:
    >>>             memory: "256Mi"
    >>>             cpu: "500m"
    >>>     - container:
    >>>       name: myapp-container
    >>>       image: busybox:1.28
    >>>       command: ['sh', '-c', 'echo custom init container']
    ```

    ### sidecars


    A list of [sidecar containers](/docs/core/specification/sidecars/)
    that will be used as sidecars.

    ```yaml
    >>> run:
    >>>   kind: job
    >>>   sidecars:
    >>>     - name: sidecar2
    >>>       image: busybox:1.28
    >>>       command: ['sh', '-c', 'echo sidecar2']
    >>>     - name: sidecar1
    >>>       image: busybox:1.28
    >>>       command: ['sh', '-c', 'echo sidecar1']
    >>>       resources:
    >>>         requests:
    >>>           memory: "128Mi"
    >>>           cpu: "500m"
    ```

    ### container

    The [main Kubernetes Container](https://kubernetes.io/docs/concepts/containers/)
    that will run your experiment training or data processing logic.

    ```yaml
    >>> run:
    >>>   kind: job
    >>>   init:
    >>>     - connection: my-code-repo
    >>>   container:
    >>>     name: tensorflow:2.1
    >>>     command: ["python", "/plx-context/artifacts/my-code-repo/model.py"]
    ```
    """

    _IDENTIFIER = V1RunKind.JOB
    _SWAGGER_FIELDS = ["volumes", "sidecars", "container"]

    kind: Literal[_IDENTIFIER] = _IDENTIFIER
    tools: Optional[Union[Tool, RefField]] = None
    environment: Optional[Union[V1Environment, RefField]] = None
    connections: Optional[Union[List[StrictStr], RefField]] = None
    volumes: Optional[Union[List[k8s_schemas.V1Volume], RefField]] = None
    init: Optional[Union[List[V1Init], RefField]] = None
    sidecars: Optional[Union[List[k8s_schemas.V1Container], RefField]] = None
    container: Optional[Union[k8s_schemas.V1Container, RefField]] = None
    config: Optional[Dict] = None
    agent: Optional[Agent] = None
    prompt: Optional[str] = None
    history: Optional[History] = None
    memory: Optional[bool] = None
