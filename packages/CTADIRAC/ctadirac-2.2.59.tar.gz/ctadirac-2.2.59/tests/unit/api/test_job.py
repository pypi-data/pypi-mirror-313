import pytest
from CTADIRAC.Interfaces.API.CtapipeMergeJob import CtapipeMergeJob
from CTADIRAC.Interfaces.API.CtapipeProcessJob import CtapipeProcessJob
from CTADIRAC.Interfaces.API.CTAJob import (
    MetadataDict,
)
from ruamel.yaml import YAML
from CTADIRAC.Interfaces.API.MCPipeJob import MCPipeJob

from tests.unit.production import (
    COMMON_CONFIG,
    CTAPIPE_PROCESS_METADATA,
    CTAPIPE_PROCESS_OUTPUT_METADATA,
    MERGING1_METADATA,
    MERGING1_OUTPUT_METADATA,
    MERGING_CONFIG_1,
    PROCESSING_CONFIG,
    SIMULATION_CONFIG,
    SIMULATION_OUTPUT_METADATA,
)


yaml = YAML(typ="safe", pure=True)
software_version = "v0.19.2"
parents_list: list[int] = [1, 2, 3]


def test_metadata_dict() -> None:
    metadata = MetadataDict()
    key = "unknown_key"
    error_message = f"Key '{key}' is not allowed in MetadataDict"
    with pytest.raises(KeyError) as exc_info:
        metadata[key] = "unknown"
    assert error_message in str(exc_info)


sim_job = MCPipeJob()
process_job = CtapipeProcessJob()
merge_job = CtapipeMergeJob()


def test_set_output_metadata() -> None:
    # Simulation Job:
    # Setting class variables 'as' done in WorkflowElement
    sim_job.particle = SIMULATION_CONFIG["job_config"]["particle"]
    sim_job.array_layout = SIMULATION_CONFIG["job_config"]["array_layout"]
    sim_job.site = SIMULATION_CONFIG["job_config"]["site"]
    sim_job.pointing_dir = SIMULATION_CONFIG["job_config"]["pointing_dir"]
    sim_job.version = SIMULATION_CONFIG["job_config"]["version"]
    sim_job.MCCampaign = COMMON_CONFIG["MCCampaign"]
    sim_job.configuration_id = COMMON_CONFIG["configuration_id"]
    assert sim_job.output_metadata == MetadataDict()
    sim_job.set_output_metadata()
    assert sim_job.output_metadata == SIMULATION_OUTPUT_METADATA

    # Processing Job:
    # Setting class variables 'as' done in WorkflowElement
    process_job.particle = SIMULATION_CONFIG["job_config"]["particle"]
    process_job.array_layout = PROCESSING_CONFIG["job_config"]["array_layout"]
    process_job.site = SIMULATION_CONFIG["job_config"]["site"]
    process_job.pointing_dir = SIMULATION_CONFIG["job_config"]["pointing_dir"]
    process_job.version = PROCESSING_CONFIG["job_config"]["version"]
    process_job.MCCampaign = COMMON_CONFIG["MCCampaign"]
    process_job.configuration_id = COMMON_CONFIG["configuration_id"]

    assert process_job.output_metadata == MetadataDict()
    process_job.set_output_metadata(CTAPIPE_PROCESS_METADATA)
    assert process_job.output_metadata == CTAPIPE_PROCESS_OUTPUT_METADATA

    # Merging Job:
    # Setting class variables 'as' done in WorkflowElement
    merge_job.MCCampaign = COMMON_CONFIG["MCCampaign"]
    merge_job.version = MERGING_CONFIG_1["job_config"]["version"]

    assert merge_job.output_metadata == MetadataDict()
    merge_job.set_output_metadata(MERGING1_METADATA)
    assert merge_job.output_metadata == MERGING1_OUTPUT_METADATA


def test_set_site() -> None:
    sites = ["Paranal", "LaPalma"]
    for site in sites:
        sim_job.set_site(site)
        assert sim_job.site == site


def test_set_particle() -> None:
    particles = ["gamma", "gamma-diffuse", "electron", "proton", "helium"]
    for particle in particles:
        sim_job.set_particle(particle)
        assert sim_job.particle == particle


def test_set_pointing_dir() -> None:
    pointing_dirs: list[str] = ["North", "South", "East", "West"]
    for pointing in pointing_dirs:
        sim_job.set_pointing_dir(pointing)
        assert sim_job.pointing_dir == pointing


def test_set_moon() -> None:
    moon: list[str] = ["dark"]
    sim_job.set_moon(moon)
    assert sim_job.moon == ""
    assert sim_job.output_file_metadata["nsb"] == [1]

    moon = ["dark", "half"]
    sim_job.set_moon(moon)
    assert sim_job.moon == "--with-half-moon"
    assert sim_job.output_file_metadata["nsb"] == [1, 5]

    moon = ["dark", "half", "full"]
    sim_job.set_moon(moon)
    assert sim_job.moon == "--with-full-moon"
    assert sim_job.output_file_metadata["nsb"] == [1, 5, 19]


def test_set_div_ang() -> None:
    div_ang = [
        "0.0098",
        "0.0075",
        "0.0089",
        "0.01568",
        "0.04568",
    ]
    with pytest.raises(SystemExit) as exc_info:
        sim_job.set_div_ang(div_ang)
    assert str(exc_info.value) == "-1"


def test_set_magic() -> None:
    sim_job.set_magic(True)
    assert sim_job.magic == "--with-magic"


def set_sct() -> None:
    sim_version = sim_job.version
    sim_job.set_sct(None)
    assert sim_job.sct == ""
    assert sim_job.version == sim_version

    sim_job.set_sct("all")
    assert sim_job.sct == "--with-all-scts"
    assert sim_job.version == sim_version + "-sc"

    sim_job.set_sct("non-alpha")
    assert sim_job.sct == "--with-sct"
    assert sim_job.version == sim_version + "-sc"
