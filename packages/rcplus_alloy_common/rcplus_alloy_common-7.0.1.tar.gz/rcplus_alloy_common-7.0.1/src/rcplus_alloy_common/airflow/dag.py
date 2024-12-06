from airflow.models.dag import DAG

from rcplus_alloy_common.version import head_ref
from rcplus_alloy_common.airflow import DagSlaConfig
from rcplus_alloy_common.airflow.utils import AlloyProject
from rcplus_alloy_common.airflow.observability import publish_dag_metrics_callback


class AlloyDag(DAG):
    """Alloy DAG class which enforces tags and dag_id naming convention."""

    def __init__(  # noqa: PLR0912
        self,
        dag_id,
        *args,
        sla_config: DagSlaConfig | None = None,
        tenant: str | None = None,
        **kwargs
    ):
        self.base_dag_id = dag_id
        project = AlloyProject(3)  # __init__, _load_project_config, __init__, dag_fun
        dag_id_prefix = f"{project['project_id']}-{project['software_component']}"
        if tenant is not None and not isinstance(tenant, str):
            raise ValueError(f"Malformed tenant parameter. Expected `str` received `{tenant}`")
        self.tenant = tenant
        if self.tenant:
            dag_id_prefix = f"{dag_id_prefix}-{self.tenant}"

        if not dag_id.startswith(dag_id_prefix):
            dag_id = f"{dag_id_prefix}-{dag_id}"

        tags = kwargs.pop("tags", None) or []
        if not isinstance(tags, list):
            self.log.warning(f"Malformed tags. Expected `list[str]` received `{tags}`")
            tags = []

        if self.tenant:
            if isinstance(tags, list):
                if self.tenant not in tags:
                    tags.append(self.tenant)
            else:
                tags = [self.tenant]

        if project["git_repo_name"] not in tags:
            tags.append(project["git_repo_name"])
        if project["project_version"] not in tags:
            tags.append(project["project_version"])

        kwargs["tags"] = tags

        # NOTE: Setup default callbacks
        if "on_success_callback" not in kwargs:
            kwargs["on_success_callback"] = [publish_dag_metrics_callback]
        elif isinstance(kwargs["on_success_callback"], list):
            kwargs["on_success_callback"] = (
                [x for x in kwargs["on_success_callback"] if x is not publish_dag_metrics_callback]
            )
            kwargs["on_success_callback"] += [publish_dag_metrics_callback]
        elif kwargs["on_success_callback"] is not publish_dag_metrics_callback:
            kwargs["on_success_callback"] = [kwargs["on_success_callback"], publish_dag_metrics_callback]

        if "on_failure_callback" not in kwargs:
            kwargs["on_failure_callback"] = [publish_dag_metrics_callback]
        elif isinstance(kwargs["on_failure_callback"], list):
            kwargs["on_failure_callback"] = (
                [x for x in kwargs["on_failure_callback"] if x is not publish_dag_metrics_callback]
            )
            kwargs["on_failure_callback"] += [publish_dag_metrics_callback]
        elif kwargs["on_failure_callback"] is not publish_dag_metrics_callback:
            kwargs["on_failure_callback"] = [kwargs["on_failure_callback"], publish_dag_metrics_callback]

        if sla_config is not None:
            # override some DAG docs parameters for SLA purposes. It is a bit strange but in Airflow docs for
            # the version 2.7.3 (which we have at the moment) they claim they have a number of params for docs
            # https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#dag-task-documentation
            # but in code only `description` and `doc_md` parameters are present so `description` is used to build a
            # human-readable SLA description and `doc_md` is used to store the JSON config for SLA (`doc_json` looks
            # more appropriate for this but it is missed in the code at the moment)
            kwargs["description"] = f"This DAG SLA period is {sla_config.sla_period}"
            kwargs["doc_md"] = sla_config.to_json()

        super().__init__(dag_id, *args, **kwargs)

    def run(self, *args, **kwargs):
        # NOTE-zw: This log message went nowhere even when we change the level to ERROR, further investigation required.
        self.log.info(f"Running dag `{self.dag_id}` with version `rcplus_alloy_common@{head_ref}`")
        super().run(*args, **kwargs)
