#!/usr/bin/env python3
"""
multiagent.py — OpenCode multi-agent orchestrator with shared memory.

Spawnea múltiples agentes opencode en paralelo, cada uno con su tarea
y comunicándose via un archivo de memoria compartida .multiagent/memory.json.

Cada agente escribe SOLO en su sección con nombre y lee las secciones
de los demás para coordinarse.

Uso:
  python .opencode/agent/multiagent.py tasks.json
  echo '{"tasks":[...]}' | python .opencode/agent/multiagent.py --pipe
  python .opencode/agent/multiagent.py --agent python-expert --prompt "implementar X"
"""

import sys
import os
import json
import asyncio
import argparse
import subprocess
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

SHARED_DIR = Path(".multiagent")
MEMORY_FILE = SHARED_DIR / "memory.json"
LOGS_DIR = SHARED_DIR / "logs"


IS_WINDOWS = sys.platform == "win32"


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    SHARED_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)


def load_memory() -> dict:
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    return {}


def create_fresh_memory(tasks: list[dict], project: str = "Yardis") -> dict:
    agents = {}
    for t in tasks:
        name = t["agent"]
        if name not in agents:
            agents[name] = {
                "status": "pending",
                "task": t["prompt"],
                "messages": [],
                "output": {},
                "round": 0,
            }
    return {
        "project": project,
        "round": 0,
        "agents": agents,
        "artifacts": {},
    }


def save_memory(mem: dict) -> None:
    MEMORY_FILE.write_text(
        json.dumps(mem, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def build_agent_prompt(task_def: dict, mem: dict, round_num: int) -> str:
    agent_name = task_def["agent"]
    task_prompt = task_def["prompt"]

    other_context = []
    for name, data in mem.get("agents", {}).items():
        if name == agent_name:
            continue
        status = data.get("status", "")
        if status in ("completed", "running", "failed"):
            out = data.get("output", {})
            files = out.get("files", [])
            api = out.get("api", "")
            parts = [f"[{status}] {name}"]
            if files:
                parts.append(f"archivos: {', '.join(files)}")
            if api:
                parts.append(f"expone: {api}")
            other_context.append("  " + " | ".join(parts))

    ctx_str = (
        "\n".join(other_context) if other_context else "  (nadie ha reportado aún)"
    )

    return f"""Eres **{agent_name}** en el proyecto {mem.get("project", "Yardis")}.

## Memoria compartida multi-agente

Existe un archivo en `.multiagent/memory.json` con secciones por cada agente.
LEE las secciones de otros para contexto — ESCRIBE SOLO en tu sección `{agent_name}`.

### Estado actual de otros agentes:
{ctx_str}

### Instrucciones
1. Lee `.multiagent/memory.json` para contexto inicial
2. Trabaja en tu tarea específica
3. Cuando termines, ACTUALIZA tu sección en `.multiagent/memory.json`:
   - `status`: "completed" (o "failed")
   - `output.files`: rutas de archivos creados/modificados
   - `output.api`: funciones/componentes que exportaste
   - `output.deps`: dependencias añadidas
   - `messages`: agrega un mensaje con resumen de lo que hiciste
4. NO modifiques las secciones de otros agentes
5. Confirma con un resumen

### Tu tarea
{task_prompt}"""


async def run_agent(
    task_def: dict, mem: dict, round_num: int, log_file: Path
) -> tuple[str, int, float, Path]:
    agent_name = task_def["agent"]

    mem["agents"][agent_name]["status"] = "running"
    mem["agents"][agent_name]["round"] = round_num
    save_memory(mem)

    prompt = build_agent_prompt(task_def, mem, round_num)

    prompt_flat = prompt.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")

    start = time.time()
    if IS_WINDOWS:
        cmd_str = subprocess.list2cmdline(
            ["opencode", "run", prompt_flat, "--agent", agent_name]
        )
        proc = await asyncio.create_subprocess_shell(
            cmd_str,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
    else:
        cmd = ["opencode", "run", prompt_flat, "--agent", agent_name]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    stdout, stderr = await proc.communicate()
    elapsed = time.time() - start

    log_content = (
        f"=== {agent_name} | round {round_num} | "
        f"{elapsed:.1f}s | exit {proc.returncode} ===\n"
    )
    log_content += stdout.decode("utf-8", errors="replace")
    if stderr:
        log_content += "\n=== STDERR ===\n" + stderr.decode("utf-8", errors="replace")
    log_file.write_text(log_content, encoding="utf-8")

    mem = load_memory()
    if agent_name not in mem["agents"]:
        mem.setdefault("agents", {})[agent_name] = {"messages": [], "output": {}}
    mem["agents"][agent_name].setdefault("messages", []).append(
        {
            "type": "completed" if proc.returncode == 0 else "failed",
            "body": f"exit {proc.returncode}, {elapsed:.1f}s",
            "ts": utcnow(),
        }
    )
    if proc.returncode != 0:
        if mem["agents"][agent_name].get("status") != "completed":
            mem["agents"][agent_name]["status"] = "failed"
    save_memory(mem)

    return agent_name, proc.returncode, elapsed, log_file


async def run_tasks(tasks: list[dict], parallel: int = 2) -> list[dict]:
    ensure_dirs()

    for i, t in enumerate(tasks):
        if "id" not in t:
            t["id"] = t.get("agent", f"task-{i}")

    remaining = {t["id"] for t in tasks}
    completed: set[str] = set()
    all_results: list[dict] = []
    round_num = 0

    mem = create_fresh_memory(tasks)
    save_memory(mem)

    while remaining:
        round_num += 1
        mem["round"] = round_num
        save_memory(mem)

        ready = []
        for t in tasks:
            tid = t["id"]
            if tid in completed or tid not in remaining:
                continue
            deps = set(t.get("deps", []))
            if deps.issubset(completed):
                ready.append(t)

        if not ready and remaining:
            print(f"[!] Deadlock: {len(remaining)} tareas esperan dependencias")
            for t in tasks:
                if t["id"] in remaining:
                    blocker = set(t.get("deps", [])) - completed
                    print(f"    {t['id']} ({t['agent']}) espera: {blocker}")
            break

        print(f"\n{'=' * 50}")
        print(f"  Round {round_num}: {len(ready)} tareas — {len(remaining)} pendientes")
        print(f"{'=' * 50}")
        for t in ready:
            print(f"  ▶ {t['agent']}: {t['prompt'][:70]}...")

        sem = asyncio.Semaphore(parallel)

        async def run_one(td: dict) -> tuple[str, int, float, Path]:
            async with sem:
                tid = td["id"]
                log_file = LOGS_DIR / f"{tid.replace('/', '_')}.log"
                return await run_agent(td, mem, round_num, log_file)

        results = await asyncio.gather(*[run_one(t) for t in ready])

        for agent_name, rc, elapsed, log_path in results:
            icon = "[OK]" if rc == 0 else "[X]"
            print(f"  {icon} {agent_name}: {elapsed:.1f}s (exit {rc})")
            all_results.append(
                {
                    "agent": agent_name,
                    "returncode": rc,
                    "elapsed": round(elapsed, 1),
                }
            )
            for t in tasks:
                if t["agent"] == agent_name and t["id"] in remaining:
                    completed.add(t["id"])
                    remaining.discard(t["id"])
                    break

        mem = load_memory()

    success = sum(1 for r in all_results if r["returncode"] == 0)
    total = len(all_results)
    print(f"\n{'=' * 50}")
    print(f"  FINAL: {success}/{total} exitosas")
    print(f"{'=' * 50}")
    for r in all_results:
        icon = "[OK]" if r["returncode"] == 0 else "[X]"
        print(f"  {icon} {r['agent']}: {r['elapsed']:.1f}s")
    print(f"\n  Memoria compartida: {MEMORY_FILE.resolve()}")
    print(f"  Logs: {LOGS_DIR.resolve()}")

    return all_results


def watch_memory(interval: float = 3.0, notify: bool = False) -> None:
    """Observa memory.json y notifica cambios de estado en los agentes."""
    sys.stdout.reconfigure(line_buffering=True)
    known: dict[str, tuple[str, int]] = {}
    print(f"   Observando {MEMORY_FILE.resolve()}", flush=True)
    print(f"  Presiona Ctrl+C para salir\n", flush=True)

    if notify and IS_WINDOWS:
        try:
            import winrt.windows.ui.notifications as notifications  # type: ignore
            from winrt.windows.data.xml.dom import XmlDocument  # type: ignore

            _toast = notifications.ToastNotificationManager.create_toast_notifier()
        except ImportError:
            notify = False
    else:
        notify = False

    def _notify(title: str, body: str) -> None:
        if not notify:
            return
        try:
            template = """<toast><visual><binding template="ToastText02">
            <text id="1">{title}</text>
            <text id="2">{body}</text>
            </binding></visual></toast>"""
            xdoc = XmlDocument()
            xdoc.load_xml(template.format(title=title, body=body))
            _toast.show(notifications.ToastNotification(xdoc))
        except Exception:
            pass

    try:
        while True:
            time.sleep(interval)
            if not MEMORY_FILE.exists():
                continue
            mem = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
            for name, data in mem.get("agents", {}).items():
                status = data.get("status", "pending")
                msgs = len(data.get("messages", []))
                prev_status, prev_msgs = known.get(name, ("", -1))
                if prev_msgs == -1:
                    known[name] = (status, msgs)
                    continue
                if status != prev_status or msgs != prev_msgs:
                    elapsed = ""
                    if msgs > 0:
                        last = data["messages"][-1]
                        if isinstance(last, dict):
                            body = last.get("body", "")
                            if "exit 0" in body or "completed" in body:
                                elapsed = body
                            ts = last.get("ts", "")
                            if not elapsed and ts:
                                elapsed = ts[-8:] if len(ts) >= 8 else ts
                    icon = {
                        "running": "[>]",
                        "completed": "[OK]",
                        "failed": "[X]",
                        "pending": "[..]",
                    }
                    line = f"  {icon.get(status, '?')} {name}: {status}"
                    if elapsed:
                        line += f" ({elapsed})"
                    task = data.get("task", "")
                    if task and status in ("completed", "failed"):
                        line += f" — {task[:60]}"
                    files = data.get("output", {}).get("files", [])
                    if files:
                        line += f" → {', '.join(files)}"
                    print(line, flush=True)
                    _notify(f"Multiagent: {name}", f"{status}: {task[:80]}")
                    known[name] = (status, msgs)
    except KeyboardInterrupt:
        print("\n   Observador detenido", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="OpenCode multi-agent orchestrator with shared memory"
    )
    parser.add_argument("file", nargs="?", help="JSON file with task list")
    parser.add_argument("--pipe", action="store_true", help="Read task list from stdin")
    parser.add_argument(
        "--parallel", type=int, default=2, help="Max agents to run simultaneously"
    )
    parser.add_argument("--agent", help="Single agent name (quick mode)")
    parser.add_argument("--prompt", help="Single agent prompt (quick mode)")
    parser.add_argument(
        "--detach",
        action="store_true",
        help="Lanzar en background y devolver el control inmediatamente",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Observar memory.json y notificar cambios en vivo",
    )
    parser.add_argument(
        "--notify",
        action="store_true",
        help="Enviar notificación del sistema en cambios (Windows Toast)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=3.0,
        help="Intervalo de polling en segundos (default: 3)",
    )
    return parser.parse_args()


def _pythonw() -> str:
    """Busca pythonw.exe (sin consola) en Windows, o usa sys.executable como fallback."""
    if not IS_WINDOWS:
        return sys.executable
    exe = Path(sys.executable)
    # Mismo directorio que python.exe → pythonw.exe
    alt = exe.with_name("pythonw.exe")
    if alt.exists():
        return str(alt)
    # Fallback: probar en PATH
    for p in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(p) / "pythonw.exe"
        if candidate.exists():
            return str(candidate)
    return str(exe)  # fallback a python.exe (mostrará consola)


def launch_detached(file_path: Path) -> None:
    """Lanza el script en background (proceso desprendido de la terminal y SIN ventana de consola)."""
    ensure_dirs()
    python_exe = _pythonw()
    cmd = [python_exe, __file__, str(file_path)]
    if IS_WINDOWS:
        proc = subprocess.Popen(
            cmd,
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    else:
        proc = subprocess.Popen(
            cmd,
            start_new_session=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    print(f"  → Background task PID {proc.pid}")
    print(f"  → Resultados en {MEMORY_FILE.resolve()}")


def main() -> None:
    args = parse_args()

    if args.watch:
        watch_memory(interval=args.interval, notify=args.notify)
        return

    # Fast path: single agent -> run-agent.py (sin DAGs, rounds, deadlock)
    if args.agent and args.prompt:
        runner = Path(__file__).parent / "run-agent.py"
        cmd = [
            sys.executable,
            str(runner),
            "--agent",
            args.agent,
            "--prompt",
            args.prompt,
        ]
        if args.detach:
            cmd.append("--detach")
            subprocess.Popen(
                cmd,
                creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW,
            )
            print(f"  → {args.agent} lanzado en background via run-agent")
            return
        subprocess.run(cmd)
        return

    if args.pipe or (args.file is None and not sys.stdin.isatty()):
        raw = sys.stdin.read()
        data: Any = json.loads(raw)
        if isinstance(data, list):
            task_list = data
            parallel = args.parallel
        elif isinstance(data, dict):
            task_list = data.get("tasks", [])
            parallel = data.get("parallel", args.parallel)
            os.environ["MULTIAGENT_PROJECT"] = data.get(
                "project", os.environ.get("MULTIAGENT_PROJECT", "Yardis")
            )
        else:
            print("Error: stdin debe ser JSON con 'tasks' array", file=sys.stderr)
            sys.exit(1)
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            task_list = data
            parallel = args.parallel
        else:
            task_list = data.get("tasks", [])
            parallel = data.get("parallel", args.parallel)
            os.environ["MULTIAGENT_PROJECT"] = data.get(
                "project", os.environ.get("MULTIAGENT_PROJECT", "Yardis")
            )
    else:
        parser.print_help()
        sys.exit(1)

    if not task_list:
        print("No tasks provided", file=sys.stderr)
        sys.exit(1)

    if args.detach:
        ensure_dirs()
        task_file = SHARED_DIR / "_detach_tasks.json"
        task_file.write_text(
            json.dumps(
                {
                    "project": os.environ.get("MULTIAGENT_PROJECT", "Yardis"),
                    "parallel": parallel,
                    "tasks": task_list,
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        launch_detached(task_file)
        return

    asyncio.run(run_tasks(task_list, parallel))


if __name__ == "__main__":
    main()
