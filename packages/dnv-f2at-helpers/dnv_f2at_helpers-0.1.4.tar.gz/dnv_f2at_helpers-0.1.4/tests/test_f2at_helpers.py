from glob import glob
import json
from pathlib import Path
from typing import Generator, List
from shutil import rmtree
import pytest
from dnv.f2at_helpers import f2at_helpers


@pytest.fixture
def single_empty_loadcase_workspace() -> Generator[Path, None, None]:
    workspace = f2at_helpers._create_infidep_workspace({})
    yield workspace
    rmtree(workspace)


def test_create_workspace_creates_workspace_directory(
        single_empty_loadcase_workspace):
    assert single_empty_loadcase_workspace.exists()


def test_workspace_contains_CommonFiles_directory(
        single_empty_loadcase_workspace):
    assert single_empty_loadcase_workspace.joinpath("CommonFiles").exists()


def test_workspace_contains_LoadCases_directory(
        single_empty_loadcase_workspace):
    assert single_empty_loadcase_workspace.joinpath("LoadCases").exists()


def test_single_loadcase_workspace_contains_single_loadcase(
        single_empty_loadcase_workspace):
    loadcases = single_empty_loadcase_workspace.joinpath("LoadCases")
    subdirs = [x for x in loadcases.iterdir() if x.is_dir()]
    assert len(subdirs) == 1


@pytest.fixture
def three_empty_loadcases_workspace() -> Generator[Path, None, None]:
    workspace = f2at_helpers._create_infidep_workspace([{}, {}, {}])
    yield workspace
    rmtree(workspace)


def test_three_loadcase_workspace_contains_three_loadcases(
        three_empty_loadcases_workspace):
    loadcases = three_empty_loadcases_workspace.joinpath("LoadCases")
    subdirs = [x for x in loadcases.iterdir() if x.is_dir()]
    assert len(subdirs) == 3


@pytest.fixture
def input_data() -> List[dict]:
    return [{
        "id": "item1",
    }, {
        "id": "item2",
    }]


@pytest.fixture
def workspace_with_data(input_data) -> Generator[Path, None, None]:
    workspace = f2at_helpers._create_infidep_workspace(input_data)
    yield workspace
    rmtree(workspace)


@pytest.fixture
def json_files(workspace_with_data) -> List[Path]:
    return [
        workspace_with_data.joinpath(x)
        for x
        in glob(
            "LoadCases/LoadCase*/input.json",
            root_dir=workspace_with_data)
        ]


def test_loadcase_directories_contain_json_files(json_files):
    assert len(json_files) == 2


def load_json(file_path):
    with open(file_path, "r", encoding="utf8") as f:
        return json.load(f)


def test_json_file_contents(json_files):
    contents = list(map(load_json, json_files))
    assert contents[0]['id'] == "item1"
    assert contents[1]['id'] == "item2"
