import dataclasses
import enum
import functools
import importlib.util
import logging
import os
import typing
from abc import ABC, abstractmethod
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

logger = logging.getLogger(__name__)


class ExperimentUnitRole(enum.Enum):
    WORK_UNIT = enum.auto()
    AUX_UNIT = enum.auto()


@dataclasses.dataclass(kw_only=True, frozen=True)
class ExperimentPatchModel:
    title: str | None = None
    description: str | None = None
    note: str | None = None
    tags: list[str] | None = None


@dataclasses.dataclass(kw_only=True, frozen=True)
class SlurmJobModel:
    name: str
    slurm_job_id: int
    slurm_ssh_config: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class ArtifactModel:
    name: str
    uri: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class ExperimentUnitModel:
    identity: str
    args: str | None = None
    jobs: list[SlurmJobModel] = dataclasses.field(default_factory=list)


@dataclasses.dataclass(kw_only=True, frozen=True)
class ExperimentUnitPatchModel:
    identity: str | None
    args: str | None = None


@dataclasses.dataclass(kw_only=True, frozen=True)
class WorkUnitModel(ExperimentUnitModel):
    wid: int
    artifacts: list[ArtifactModel] = dataclasses.field(default_factory=list)


@dataclasses.dataclass(kw_only=True, frozen=True)
class ExperimentModel:
    title: str
    description: str | None
    note: str | None
    tags: list[str] | None

    work_units: list[WorkUnitModel]
    artifacts: list[ArtifactModel]


class XManagerAPI(ABC):
    @abstractmethod
    def get_experiment(self, xid: int) -> ExperimentModel:
        pass

    @abstractmethod
    def delete_experiment(self, experiment_id: int) -> None:
        pass

    @abstractmethod
    def insert_experiment(self, experiment: ExperimentPatchModel) -> int:
        pass

    @abstractmethod
    def update_experiment(self, experiment_id: int, experiment_patch: ExperimentPatchModel) -> None:
        pass

    @abstractmethod
    def insert_job(self, experiment_id: int, work_unit_id: int, job: SlurmJobModel) -> None:
        pass

    @abstractmethod
    def insert_work_unit(self, experiment_id: int, work_unit: WorkUnitModel) -> None:
        pass

    @abstractmethod
    def update_work_unit(
        self, experiment_id: int, work_unit_id: int, patch: ExperimentUnitPatchModel
    ) -> None:
        pass

    @abstractmethod
    def delete_work_unit_artifact(self, experiment_id: int, work_unit_id: int, name: str) -> None:
        pass

    @abstractmethod
    def insert_work_unit_artifact(
        self, experiment_id: int, work_unit_id: int, artifact: ArtifactModel
    ) -> None:
        pass

    @abstractmethod
    def delete_experiment_artifact(self, experiment_id: int, name: str) -> None:
        pass

    @abstractmethod
    def insert_experiment_artifact(self, experiment_id: int, artifact: ArtifactModel) -> None:
        pass


class XManagerWebAPI(XManagerAPI):
    def __init__(self, base_url: str, token: str):
        if importlib.util.find_spec("xm_slurm_api_client") is None:
            raise ImportError("xm_slurm_api_client not found.")

        from xm_slurm_api_client import AuthenticatedClient  # type: ignore
        from xm_slurm_api_client import models as _models  # type: ignore

        self.models = _models
        self.client = AuthenticatedClient(
            base_url,
            token=token,
            raise_on_unexpected_status=True,
            verify_ssl=False,
        )

    def get_experiment(self, xid: int) -> ExperimentModel:
        from xm_slurm_api_client.api.experiment import (  # type: ignore
            get_experiment as _get_experiment,
        )

        experiment: Any = _get_experiment.sync(xid, client=self.client)  # type: ignore
        wus = []
        for wu in experiment.work_units:
            jobs = []
            for job in wu.jobs:
                jobs.append(SlurmJobModel(**job.dict()))
            artifacts = []
            for artifact in wu.artifacts:
                artifacts.append(ArtifactModel(**artifact.dict()))
            wus.append(
                WorkUnitModel(
                    wid=wu.wid,
                    identity=wu.identity,
                    args=wu.args,
                    jobs=jobs,
                    artifacts=artifacts,
                )
            )

        artifacts = []
        for artifact in experiment.artifacts:
            artifacts.append(ArtifactModel(**artifact.dict()))

        return ExperimentModel(
            title=experiment.title,
            description=experiment.description,
            note=experiment.note,
            tags=experiment.tags,
            work_units=wus,
            artifacts=artifacts,
        )

    def delete_experiment(self, experiment_id: int) -> None:
        from xm_slurm_api_client.api.experiment import (  # type: ignore
            delete_experiment as _delete_experiment,
        )

        _delete_experiment.sync(experiment_id, client=self.client)

    def insert_experiment(self, experiment: ExperimentPatchModel) -> int:
        from xm_slurm_api_client.api.experiment import (  # type: ignore
            insert_experiment as _insert_experiment,
        )

        assert experiment.title is not None, "Title must be set in the experiment model."
        assert (
            experiment.description is None and experiment.note is None and experiment.tags is None
        ), "Only title should be set in the experiment model."
        experiment_response = _insert_experiment.sync(
            client=self.client,
            body=self.models.Experiment(title=experiment.title),
        )
        return typing.cast(int, experiment_response["xid"])  # type: ignore

    def update_experiment(self, experiment_id: int, experiment_patch: ExperimentPatchModel) -> None:
        from xm_slurm_api_client.api.experiment import (  # type: ignore
            update_experiment as _update_experiment,
        )

        _update_experiment.sync(
            experiment_id,
            client=self.client,
            body=self.models.ExperimentPatch(**dataclasses.asdict(experiment_patch)),
        )

    def insert_job(self, experiment_id: int, work_unit_id: int, job: SlurmJobModel) -> None:
        from xm_slurm_api_client.api.job import insert_job as _insert_job  # type: ignore

        _insert_job.sync(
            experiment_id,
            work_unit_id,
            client=self.client,
            body=self.models.SlurmJob(**dataclasses.asdict(job)),
        )

    def insert_work_unit(self, experiment_id: int, work_unit: WorkUnitModel) -> None:
        from xm_slurm_api_client.api.work_unit import (  # type: ignore
            insert_work_unit as _insert_work_unit,
        )

        _insert_work_unit.sync(
            experiment_id,
            client=self.client,
            body=self.models.WorkUnit(**dataclasses.asdict(work_unit)),
        )

    def delete_work_unit_artifact(self, experiment_id: int, work_unit_id: int, name: str) -> None:
        from xm_slurm_api_client.api.artifact import (  # type: ignore
            delete_work_unit_artifact as _delete_work_unit_artifact,
        )

        _delete_work_unit_artifact.sync(experiment_id, work_unit_id, name, client=self.client)

    def insert_work_unit_artifact(
        self, experiment_id: int, work_unit_id: int, artifact: ArtifactModel
    ) -> None:
        from xm_slurm_api_client.api.artifact import (  # type: ignore
            insert_work_unit_artifact as _insert_work_unit_artifact,
        )

        _insert_work_unit_artifact.sync(
            experiment_id,
            work_unit_id,
            client=self.client,
            body=self.models.Artifact(**dataclasses.asdict(artifact)),
        )

    def delete_experiment_artifact(self, experiment_id: int, name: str) -> None: ...

    def insert_experiment_artifact(self, experiment_id: int, artifact: ArtifactModel) -> None:
        from xm_slurm_api_client.api.artifact import (  # type: ignore
            insert_experiment_artifact as _insert_experiment_artifact,
        )

        _insert_experiment_artifact.sync(
            experiment_id,
            client=self.client,
            body=self.models.Artifact(**dataclasses.asdict(artifact)),
        )


Base = declarative_base()


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    note = Column(String)
    tags = Column(String)
    work_units = relationship("WorkUnit", back_populates="experiment")
    artifacts = relationship("Artifact", back_populates="experiment")


class WorkUnit(Base):
    __tablename__ = "work_units"

    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    wid = Column(Integer)
    identity = Column(String)
    args = Column(String)
    experiment = relationship("Experiment", back_populates="work_units")
    jobs = relationship("SlurmJob", back_populates="work_unit")
    artifacts = relationship("Artifact", back_populates="work_unit")


class SlurmJob(Base):
    __tablename__ = "slurm_jobs"

    id = Column(Integer, primary_key=True)
    work_unit_id = Column(Integer, ForeignKey("work_units.id"))
    name = Column(String)
    slurm_job_id = Column(Integer)
    slurm_ssh_config = Column(String)
    work_unit = relationship("WorkUnit", back_populates="jobs")


class Artifact(Base):
    __tablename__ = "artifacts"

    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    work_unit_id = Column(Integer, ForeignKey("work_units.id"))
    name = Column(String)
    uri = Column(String)
    experiment = relationship("Experiment", back_populates="artifacts")
    work_unit = relationship("WorkUnit", back_populates="artifacts")


class XManagerSqliteAPI(XManagerAPI):
    def __init__(self):
        if "XM_SLURM_STATE_DIR" in os.environ:
            db_path = Path(os.environ["XM_SLURM_STATE_DIR"]) / "db.sqlite3"
        else:
            db_path = Path.home() / ".local" / "state" / "xm-slurm" / "db.sqlite3"
        logger.debug("Looking for db at: ", db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_experiment(self, xid: int) -> ExperimentModel:
        with self.session_scope() as session:
            experiment = session.query(Experiment).filter(Experiment.id == xid).first()
            if not experiment:
                raise ValueError(f"Experiment with id {xid} not found")

            work_units = []
            for wu in experiment.work_units:
                jobs = [
                    SlurmJobModel(
                        name=job.name,
                        slurm_job_id=job.slurm_job_id,
                        slurm_ssh_config=job.slurm_ssh_config,
                    )
                    for job in wu.jobs
                ]
                artifacts = [
                    ArtifactModel(name=artifact.name, uri=artifact.uri) for artifact in wu.artifacts
                ]
                work_units.append(
                    WorkUnitModel(
                        wid=wu.wid,
                        identity=wu.identity,
                        args=wu.args,
                        jobs=jobs,
                        artifacts=artifacts,
                    )
                )

            artifacts = [
                ArtifactModel(name=artifact.name, uri=artifact.uri)
                for artifact in experiment.artifacts
            ]

            return ExperimentModel(
                title=experiment.title,
                description=experiment.description,
                note=experiment.note,
                tags=experiment.tags.split(",") if experiment.tags else None,
                work_units=work_units,
                artifacts=artifacts,
            )

    def delete_experiment(self, experiment_id: int) -> None:
        with self.session_scope() as session:
            experiment = session.query(Experiment).filter(Experiment.id == experiment_id).first()
            if experiment:
                session.delete(experiment)

    def insert_experiment(self, experiment: ExperimentPatchModel) -> int:
        with self.session_scope() as session:
            new_experiment = Experiment(
                title=experiment.title,
                description=experiment.description,
                note=experiment.note,
                tags=",".join(experiment.tags) if experiment.tags else None,
            )
            session.add(new_experiment)
            session.flush()
            return new_experiment.id

    def update_experiment(self, experiment_id: int, experiment_patch: ExperimentPatchModel) -> None:
        with self.session_scope() as session:
            experiment = session.query(Experiment).filter(Experiment.id == experiment_id).first()
            if experiment:
                if experiment_patch.title is not None:
                    experiment.title = experiment_patch.title
                if experiment_patch.description is not None:
                    experiment.description = experiment_patch.description
                if experiment_patch.note is not None:
                    experiment.note = experiment_patch.note
                if experiment_patch.tags is not None:
                    experiment.tags = ",".join(experiment_patch.tags)

    def insert_job(self, experiment_id: int, work_unit_id: int, job: SlurmJobModel) -> None:
        with self.session_scope() as session:
            work_unit = (
                session.query(WorkUnit)
                .filter_by(experiment_id=experiment_id, wid=work_unit_id)
                .first()
            )
            if work_unit:
                new_job = SlurmJob(
                    work_unit_id=work_unit.id,
                    name=job.name,
                    slurm_job_id=job.slurm_job_id,
                    slurm_ssh_config=job.slurm_ssh_config,
                )
                session.add(new_job)
            else:
                raise ValueError(
                    f"Work unit with id {work_unit_id} not found in experiment {experiment_id}"
                )

    def insert_work_unit(self, experiment_id: int, work_unit: WorkUnitModel) -> None:
        with self.session_scope() as session:
            new_work_unit = WorkUnit(
                experiment_id=experiment_id,
                wid=work_unit.wid,
                identity=work_unit.identity,
                args=work_unit.args,
            )
            session.add(new_work_unit)
            for job in work_unit.jobs:
                new_job = SlurmJob(
                    work_unit_id=new_work_unit.id,
                    name=job.name,
                    slurm_job_id=job.slurm_job_id,
                    slurm_ssh_config=job.slurm_ssh_config,
                )
                session.add(new_job)
            for artifact in work_unit.artifacts:
                new_artifact = Artifact(
                    work_unit_id=new_work_unit.id, name=artifact.name, uri=artifact.uri
                )
                session.add(new_artifact)

    def update_work_unit(
        self, experiment_id: int, work_unit_id: int, patch: ExperimentUnitPatchModel
    ) -> None:
        with self.session_scope() as session:
            work_unit = (
                session.query(WorkUnit)
                .filter(WorkUnit.experiment_id == experiment_id, WorkUnit.wid == work_unit_id)
                .first()
            )

            if work_unit:
                if patch.identity is not None:
                    work_unit.identity = patch.identity
                if patch.args is not None:
                    work_unit.args = patch.args
            else:
                raise ValueError(
                    f"Work unit with id {work_unit_id} not found in experiment {experiment_id}"
                )

    def delete_work_unit_artifact(self, experiment_id: int, work_unit_id: int, name: str) -> None:
        with self.session_scope() as session:
            artifact = (
                session.query(Artifact)
                .filter(Artifact.work_unit_id == work_unit_id, Artifact.name == name)
                .first()
            )
            if artifact:
                session.delete(artifact)

    def insert_work_unit_artifact(
        self, experiment_id: int, work_unit_id: int, artifact: ArtifactModel
    ) -> None:
        with self.session_scope() as session:
            new_artifact = Artifact(work_unit_id=work_unit_id, name=artifact.name, uri=artifact.uri)
            session.add(new_artifact)

    def delete_experiment_artifact(self, experiment_id: int, name: str) -> None:
        with self.session_scope() as session:
            artifact = (
                session.query(Artifact)
                .filter(Artifact.experiment_id == experiment_id, Artifact.name == name)
                .first()
            )
            if artifact:
                session.delete(artifact)

    def insert_experiment_artifact(self, experiment_id: int, artifact: ArtifactModel) -> None:
        with self.session_scope() as session:
            new_artifact = Artifact(
                experiment_id=experiment_id, name=artifact.name, uri=artifact.uri
            )
            session.add(new_artifact)


@functools.cache
def client() -> XManagerAPI:
    if importlib.util.find_spec("xm_slurm_api_client") is not None:
        if (base_url := os.environ.get("XM_SLURM_API_BASE_URL")) is not None and (
            token := os.environ.get("XM_SLURM_API_TOKEN")
        ) is not None:
            return XManagerWebAPI(base_url=base_url, token=token)
        else:
            logger.warn(
                "XM_SLURM_API_BASE_URL and XM_SLURM_API_TOKEN not set. "
                "Disabling XManager API client."
            )

    return XManagerSqliteAPI()
