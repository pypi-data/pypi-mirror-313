from pathlib import Path

import numpy as np
import pytest
from aiosqlite import Connection, connect

from lisa.globalfit.framework.catalogs.sqlite import SqliteSourceCatalog
from lisa.globalfit.framework.model import MarkovChainSamples, ParametricModel
from lisa.globalfit.framework.msg.data import ModuleState


@pytest.fixture
def sample_module_states() -> dict[str, ModuleState]:
    def mock_module_state(model_name: str, params: np.ndarray) -> ModuleState:
        unused = ParametricModel(name="UNUSED", parameters=np.array([]))
        return ModuleState(
            chain=MarkovChainSamples(
                idx_iteration=0,
                idx_step_end=0,
                waveforms=ParametricModel(name=model_name, parameters=params),
            ),
            log_prior=unused,
            log_likelihood=unused,
            log_proposal=unused,
        )

    return {
        "A": mock_module_state("ModelA", np.array([[1, 2]])),
        "B": mock_module_state("ModelB", np.array([[3, 4]])),
    }


@pytest.fixture
async def sample_db():
    sample_data = [
        ("A", "2024-01-01 12:00:00+00:00", 1, 2),
        ("B", "2024-01-01 12:00:00+00:00", 3, 4),
        ("A", "2024-01-02 12:00:00+00:00", 5, 6),
        ("A", "2024-01-02 12:00:00+00:00", 7, 8),
    ]
    async with connect(":memory:") as db:
        await db.execute(
            """
            CREATE TABLE test_table (
                subject TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                p0 INTEGER NOT NULL,
                p1 INTEGER NOT NULL
            )
            """
        )
        await db.executemany("INSERT INTO test_table VALUES (?, ?, ?, ?)", sample_data)
        await db.commit()
        yield db


@pytest.mark.asyncio
async def test_catalog_select_latest_model(sample_db: Connection, tmp_path: Path):
    result = await SqliteSourceCatalog(tmp_path).select_latest_model(
        sample_db, "test_table"
    )
    # Check that the two latest simulatneous updates from A are correctly concatenated.
    expected_result = {
        "A": ParametricModel(name="test_table", parameters=np.array([[5, 6], [7, 8]])),
        "B": ParametricModel(name="test_table", parameters=np.array([[3, 4]])),
    }
    assert result == expected_result


@pytest.mark.asyncio
async def test_catalog_roundtrip(
    sample_module_states: dict[str, ModuleState], tmp_path: Path
):
    # Make sure that sample data is not empty.
    assert sample_module_states

    obj = SqliteSourceCatalog(tmp_path / "catalog.db")
    for subject, state in sample_module_states.items():
        await obj.update(subject, state)
    latest = await obj.get_source_parameters()
    assert latest == {
        module: state.chain.waveforms for module, state in sample_module_states.items()
    }
