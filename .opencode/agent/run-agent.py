#!/usr/bin/env python3
"""
run-agent.py — Fast path monocanal para un solo agente. ~65 líneas.

Ejecuta un único agente opencode con memoria compartida mínima,
sin la maquinaria multi-agente (DAGs, rounds, deadlock detection).

Uso:
  python run-agent.py --agent python-expert --prompt "..."           # síncrono
  python run-agent.py --agent python-expert --prompt "..." --detach  # background
  python run-agent.py tasks.json                                     # background callback
"""
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timezone

SHARED_DIR = Path(".multiagent")
MEMORY_FILE = SHARED_DIR / "memory.json"
IS_WINDOWS = sys.platform == "win32"


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    SHARED_DIR.mkdir(exist_ok=True)


def load_mem() -> dict:
    return json.loads(MEMORY_FILE.read_text("utf-8")) if MEMORY_FILE.exists() else {}


def save_mem(mem: dict) -> None:
    MEMORY_FILE.write_text(json.dumps(mem, indent=2, ensure_ascii=False), "utf-8")


def run_agent(agent: str, prompt: str) -> int:
    """Ejecuta opencode y escribe resultado en memory.json."""
    ensure_dirs()

    # Memoria compartida mínima (sin DAGs, sin rounds múltiples)
    mem = {
        "project": "Yardis",
        "agents": {
            agent: {
                "status": "running",
                "task": prompt[:120],
                "messages": [],
                "output": {},
                "round": 1,
            }
        },
    }
    save_mem(mem)

    prompt_flat = prompt.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    result = subprocess.run(
        ["opencode", "run", prompt_flat, "--agent", agent],
        capture_output=True,
        text=True,
    )

    # Actualizar memoria al finalizar
    mem = load_mem()
    a = mem.setdefault("agents", {}).setdefault(agent, {"messages": [], "output": {}})
    a["status"] = "completed" if result.returncode == 0 else "failed"
    a["messages"].append({
        "type": a["status"],
        "body": f"exit {result.returncode}",
        "ts": utcnow(),
    })
    a["output"]["stdout"] = result.stdout[:2000] if result.stdout else ""
    save_mem(mem)

    print(result.stdout)
    return result.returncode


def main() -> None:
    # Modo background: python run-agent.py <taskfile.json>
    if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        task = json.loads(Path(sys.argv[1]).read_text("utf-8"))
        sys.exit(run_agent(task["agent"], task["prompt"]))

    parser = argparse.ArgumentParser(description="Ejecuta un solo agente opencode")
    parser.add_argument("--agent", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--detach", action="store_true")
    args = parser.parse_args()

    if args.detach:
        # Paso 1: escribir archivo de tarea
        ensure_dirs()
        task_file = SHARED_DIR / "_run_task.json"
        task_file.write_text(
            json.dumps({"agent": args.agent, "prompt": args.prompt}), "utf-8"
        )
        # Paso 2: lanzar run-agent.py <taskfile> en background (sin consola)
        # Este segundo proceso sí espera a opencode y actualiza memory.json
        subprocess.Popen(
            [sys.executable, __file__, str(task_file)],
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW,
        )
        print(f"  → {args.agent} lanzado en background")
        return

    sys.exit(run_agent(args.agent, args.prompt))


if __name__ == "__main__":
    main()
