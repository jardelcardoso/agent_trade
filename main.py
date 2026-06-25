from src.agent.orchestrator import Orchestrator


def main() -> None:
    orchestrator = Orchestrator()
    result = orchestrator.run_cycle()
    print(f"Agent Trade inicializado. Modo dry run ativo. {result}")


if __name__ == "__main__":
    main()
