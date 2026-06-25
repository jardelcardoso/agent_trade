from pathlib import Path

from src.agent.memory import AgentMemory


def test_agent_memory_persists_and_reads_recent_decisions(tmp_path: Path) -> None:
    db_path = tmp_path / "trading_db.sqlite"
    memory = AgentMemory(db_path=db_path)

    memory.save_decision("BTCUSDT", "buy", "dry_run", "2024-01-01T00:00:00")
    memory.save_decision("BTCUSDT", "sell", "dry_run", "2024-01-01T01:00:00")

    decisions = memory.get_recent_decisions("BTCUSDT", limit=2)

    assert len(decisions) == 2
    assert decisions[0]["decision"] == "sell"
    assert decisions[1]["decision"] == "buy"
