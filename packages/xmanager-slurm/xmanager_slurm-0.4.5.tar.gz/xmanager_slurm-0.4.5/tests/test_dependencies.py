import datetime as dt
from typing import Callable

import pytest

from xm_slurm import config, dependencies, execution

SlurmHandleGenerator = Callable[[str], execution.SlurmHandle]


@pytest.fixture
def slurm_handle() -> SlurmHandleGenerator:
    dummy_ssh_config = config.SlurmSSHConfig(host="localhost")

    def _slurm_handle(job_id: str):
        return execution.SlurmHandle(
            experiment_id=0, ssh=dummy_ssh_config, slurm_job=job_id, job_name="job"
        )

    return _slurm_handle


def test_slurm_job_dependency_and(slurm_handle: SlurmHandleGenerator):
    dep1 = dependencies.SlurmJobDependencyAfter([slurm_handle("123")])
    dep2 = dependencies.SlurmJobDependencyAfter([slurm_handle("456")])
    combined_dep = dep1 & dep2
    assert isinstance(combined_dep, dependencies.SlurmJobDependencyAND)
    assert combined_dep.to_dependency_str() == "after:123,after:456"


def test_slurm_job_dependency_or(slurm_handle: SlurmHandleGenerator):
    dep1 = dependencies.SlurmJobDependencyAfter([slurm_handle("123")])
    dep2 = dependencies.SlurmJobDependencyAfter([slurm_handle("456")])
    combined_dep = dep1 | dep2
    assert isinstance(combined_dep, dependencies.SlurmJobDependencyOR)
    assert combined_dep.to_dependency_str() == "after:123?after:456"


def test_slurm_job_dependency_mixing_logical_operations(slurm_handle: SlurmHandleGenerator):
    dep1 = dependencies.SlurmJobDependencyAfter([slurm_handle("123")])
    dep2 = dependencies.SlurmJobDependencyAfter([slurm_handle("456")])
    dep3 = dependencies.SlurmJobDependencyAfter([slurm_handle("789")])
    with pytest.raises(
        dependencies.SlurmDependencyException,
        match="Slurm only supports chaining dependencies with the same logical operator. ",
    ):
        dep1 & dep2 | dep3  # type: ignore

    with pytest.raises(
        dependencies.SlurmDependencyException,
        match="Slurm only supports chaining dependencies with the same logical operator. ",
    ):
        dep1 | dep2 & dep3  # type: ignore


def test_slurm_job_dependency_chaining_and(slurm_handle: SlurmHandleGenerator):
    dep1 = dependencies.SlurmJobDependencyAfter([slurm_handle("1")])
    dep2 = dependencies.SlurmJobDependencyAfter([slurm_handle("2")])
    dep3 = dependencies.SlurmJobDependencyAfter([slurm_handle("3")])
    dep4 = dependencies.SlurmJobDependencyAfter([slurm_handle("4")])
    combined_dep = dep1 & dep2 & dep3 & dep4
    assert isinstance(combined_dep, dependencies.SlurmJobDependencyAND)
    assert combined_dep.to_dependency_str() == "after:1,after:2,after:3,after:4"


def test_slurm_job_dependency_chaining_or(slurm_handle: SlurmHandleGenerator):
    dep1 = dependencies.SlurmJobDependencyAfter([slurm_handle("1")])
    dep2 = dependencies.SlurmJobDependencyAfter([slurm_handle("2")])
    dep3 = dependencies.SlurmJobDependencyAfter([slurm_handle("3")])
    dep4 = dependencies.SlurmJobDependencyAfter([slurm_handle("4")])
    combined_dep = dep1 | dep2 | dep3 | dep4
    assert isinstance(combined_dep, dependencies.SlurmJobDependencyOR)
    assert combined_dep.to_dependency_str() == "after:1?after:2?after:3?after:4"


def test_slurm_job_dependency_after(slurm_handle: SlurmHandleGenerator):
    dep = dependencies.SlurmJobDependencyAfter([slurm_handle("123")])
    assert dep.to_dependency_str() == "after:123"


def test_slurm_job_dependency_after_with_time(slurm_handle: SlurmHandleGenerator):
    dep = dependencies.SlurmJobDependencyAfter([slurm_handle("123")], time=dt.timedelta(minutes=10))
    assert dep.to_dependency_str() == "after:123+10"


def test_slurm_job_dependency_after_with_invalid_time(slurm_handle: SlurmHandleGenerator):
    with pytest.raises(
        dependencies.SlurmDependencyException, match="Time must be specified in exact minutes"
    ):
        dependencies.SlurmJobDependencyAfter([slurm_handle("123")], time=dt.timedelta(seconds=30))


@pytest.mark.parametrize(
    "dependency_cls,dependency_type",
    [
        (dependencies.SlurmJobDependencyAfter, "after"),
        (dependencies.SlurmJobDependencyAfterAny, "afterany"),
        (dependencies.SlurmJobDependencyAfterNotOK, "afternotok"),
        (dependencies.SlurmJobDependencyAfterOK, "afterok"),
    ],
)
def test_slurm_job_dependency_after_not_ok(
    slurm_handle: SlurmHandleGenerator,
    dependency_cls: type,
    dependency_type: str,
):
    dep = dependency_cls([slurm_handle("123"), slurm_handle("456")])
    assert dep.to_dependency_str() == f"{dependency_type}:123:456"


@pytest.mark.parametrize(
    "dependency_cls",
    [
        dependencies.SlurmJobDependencyAfter,
        dependencies.SlurmJobDependencyAfterAny,
        dependencies.SlurmJobDependencyAfterNotOK,
        dependencies.SlurmJobDependencyAfterOK,
    ],
)
def test_slurm_job_dependency_after_no_handles(dependency_cls: type):
    with pytest.raises(
        dependencies.SlurmDependencyException, match="Dependency doesn't have any handles."
    ):
        dependency_cls([])


def test_dependency_flatten(slurm_handle: SlurmHandleGenerator):
    dep1 = dependencies.SlurmJobDependencyAfter([slurm_handle("1")])
    dep2 = dependencies.SlurmJobDependencyAfter([slurm_handle("2")])
    dep3 = dependencies.SlurmJobDependencyAfter([slurm_handle("3")])
    combined_dep = dep1 & dep2 & dep3
    assert combined_dep.flatten() == (dep1, dep2, dep3)


def test_dependency_traverse(slurm_handle: SlurmHandleGenerator):
    dep1 = dependencies.SlurmJobDependencyAfterOK([slurm_handle("1")])
    dep2 = dependencies.SlurmJobDependencyAfterOK([slurm_handle("2")])
    dep3 = dependencies.SlurmJobDependencyAfterOK([slurm_handle("3")])
    combined_dep = dep1 & dep2 & dep3

    def traverse_fn(dep: dependencies.SlurmJobDependency):
        if isinstance(dep, dependencies.SlurmJobDependencyAfterOK):
            return dependencies.SlurmJobDependencyAfterNotOK(dep.handles)
        return dep

    transformed_combined_dep = combined_dep.traverse(traverse_fn)
    for dep in transformed_combined_dep.flatten():
        assert isinstance(dep, dependencies.SlurmJobDependencyAfterNotOK)
    assert transformed_combined_dep.to_dependency_str() == "afternotok:1,afternotok:2,afternotok:3"
