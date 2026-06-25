from src.agent.decision_policy import DecisionPolicy


def test_decision_policy_avoids_reversing_recent_signal() -> None:
    policy = DecisionPolicy()

    assert policy.decide("buy", [{"decision": "sell"}]) == "hold"
    assert policy.decide("buy", []) == "buy"
    assert policy.decide("sell", [{"decision": "buy"}]) == "hold"
    assert policy.decide("sell", []) == "sell"
