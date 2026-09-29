---
name: comfyui-shanghai-remote
description: Remotely maintain and inspect the user's Shanghai Windows ComfyUI workstation over OpenVPN SSH when the user explicitly asks to operate that remote host. Use for remote task-status diagnosis, logs and system checks, downloading or importing workflows, models, LoRAs, custom nodes, and plugins, plus closely related installation, update, troubleshooting, and file-transfer work. Do not use for local Codex image generation, prompt writing, local ComfyUI work, workflow design without remote import, or creative generation merely because the workspace is E:\work\comfyui.
---

# Shanghai ComfyUI remote workstation

Treat the Shanghai Windows machine as the execution and GPU host. Treat the local machine as the control, browser, and artifact-review host.

## Activation boundary

Use this skill only when the user explicitly asks to perform an operation on the Shanghai remote ComfyUI machine, refers to the Shanghai/remote host in context, or explicitly invokes `$comfyui-shanghai-remote`.

Typical in-scope work is downloading, installing, importing, updating, inspecting, or troubleshooting remote workflows, checkpoints, diffusion models, VAEs, LoRAs, custom nodes, plugins, and their dependencies. Starting, stopping, or checking the remote ComfyUI service is also in scope when needed for that maintenance.

Do not activate this skill solely because:

- the current workspace is `E:\work\comfyui`;
- the request mentions ComfyUI but is local or does not target the Shanghai host;
- the user asks Codex to generate or edit an image;
- the user asks for prompt writing, prompt refinement, storyboarding, or workflow design without asking to import it remotely; or
- a local image-generation or prompt-writing skill could optionally use remote compute.

For a mixed request, use this skill only for the explicitly requested remote-maintenance portion. Do not connect to or preflight the remote host until an actual remote action or remote inspection is requested.

## Connection

- Default host: `10.8.67.78` over OpenVPN.
- Credential file: `E:\work\comfyui\openvpn\passwd.txt`.
- The first non-empty line of the credential file is the SSH username; the second non-empty line is the SSH password. Treat any other shape as invalid and report it without printing the file contents.
- Expected ED25519 host-key fingerprint: `SHA256:TAGZu6xnSaSYpTYKVJEzO7NpIpfL3Q23DcYUDmSjHDU`.
- Verified Windows host: `CHINAMI-RUPRRBK` (`chinami-ruprrbk\administrator`).
- Default to password authentication with the username and password read from the credential file at connection time. Do not fall back to a private key, another account, another password, or another host unless the user explicitly asks.
- Use `StrictHostKeyChecking=yes`, `PubkeyAuthentication=no`, `PreferredAuthentications=password,keyboard-interactive`, and `NumberOfPasswordPrompts=1`. Supply the password only to the SSH client's password prompt through a non-echoing interactive mechanism. Never place the password in command arguments, environment variables, generated scripts, logs, tool output, chat messages, or any file other than the user-designated credential file.
- Do not print, quote, summarize, hash, copy, upload, or commit the credential file. Read only the two required values and keep them only for the duration of the connection attempt. If the available SSH mechanism cannot consume the password without exposing it, stop and report that limitation instead of weakening these rules.

Before changing the remote machine, confirm port 22, password authentication, host name, user, and remote root. A normal command shape is shown below; `$sshUser` is read from the credential file and the password is supplied only when SSH prompts for it:

```powershell
ssh.exe -o StrictHostKeyChecking=yes -o PubkeyAuthentication=no -o PreferredAuthentications=password,keyboard-interactive -o NumberOfPasswordPrompts=1 "$sshUser@10.8.67.78" <remote-command>
```

Make one password-authentication attempt. If the credential file is missing or malformed, the host is unreachable, host-key verification fails, or authentication fails, stop and report the failure category and safe diagnostic details without exposing either credential. Ask the user to verify the file, address, VPN, or remote SSH configuration as applicable. Do not scan for another host, guess an address, change VPN configuration, or fall back to another credential. Sunlogin is a human-operated fallback only.

## Remote status diagnosis

For remote task, health, or “stuck versus slow” checks, prefer SSH evidence from the remote machine. Use the ComfyUI HTTP API only as a supplement for mapping prompt IDs, queue state, workflow parameters, and history; a prompt remaining in `/queue` is not by itself proof that useful work is continuing.

Start read-only and inspect, in this order when available:

1. The relevant ComfyUI log file under `C:\home\AI\comfyui`, including its last-write time, size, recent lines, current node, sampler progress, warnings, exceptions, and completion markers.
2. The ComfyUI/Python process state: PID, start time, CPU time or CPU usage, working set, command line, and whether the process still exists.
3. GPU state from `nvidia-smi`: utilization, memory usage, temperature, performance state, and active compute processes.
4. ComfyUI `/queue`, `/history/{prompt_id}`, `/prompt`, and `/system_stats` only to correlate the operating-system evidence with the queued workflow.

Locate logs and the active launch command from the running process, service configuration, or known files under the remote root. Do not search unrelated areas of the machine. Tail only the amount needed for diagnosis and avoid returning full prompts or unrelated user content.

When the first snapshot is inconclusive, take a second short-interval read-only snapshot and compare log size or timestamp, sampler step, process CPU time, and GPU utilization. Do not use a long blocking wait. Classify the result using evidence:

- **Active:** sampler step, log position, process CPU time, or GPU work advances.
- **Loading or slow:** process is alive and resource activity continues, but the sampler has not begun or individual steps are long.
- **Likely stalled:** repeated snapshots show no log, CPU, GPU, or progress change and there is no documented long-running load or offload phase.
- **Failed:** the process or prompt reports an exception, out-of-memory condition, cancellation, or terminated execution.
- **Completed:** history or logs show completion and expected outputs exist.
- **Unknown:** required evidence is unavailable; state exactly what could not be observed.

Do not interrupt, cancel, restart, clear queues, or modify files during a status check unless the user separately asks for that action.

## Path boundary

- Local project root: `E:\work\comfyui`.
- Remote root: `C:\home\AI\comfyui`.
- Keep every task-owned installation, portable runtime, virtual environment, repository, custom node, model, download, cache, log, temporary file, input, and output under the remote root.
- Never install or copy task artifacts elsewhere on the remote machine unless the user explicitly changes this boundary.
- Existing remote subdirectories include `apps`, `backups`, `logs`, `openvpn`, `shared`, and `staging`. Inspect before choosing final paths; do not overwrite an existing installation blindly.
- System-provided Git and `nvidia-smi` are available. A usable Python installation has not yet been confirmed; the current `python.exe` discovery points to the WindowsApps alias. If Python is needed, verify it first and keep any new portable runtime or environment under the remote root.

## Remote execution and downloads

- Install, update, inspect, and repair ComfyUI or its task-owned dependencies on the Shanghai machine only when the user requests that remote maintenance.
- Download workflows, ComfyUI releases, custom nodes, plugins, Python packages, models, LoRAs, VAEs, and related assets directly from the Shanghai machine. Do not download large remote dependencies locally and relay them through this project.
- Put partial downloads and extraction work under `C:\home\AI\comfyui\staging`, verify completion or checksums when available, then move them to their final location under the remote root.
- Check remote free space before large models or bulk outputs. Preserve existing user data and unrelated changes.
- Make ComfyUI reachable through the VPN at `http://10.8.67.78:8188`. Prefer binding to the VPN address; if binding broadly is necessary, restrict Windows Firewall access to the VPN subnet and do not expose ComfyUI publicly.
- When importing a workflow, preserve the source JSON, verify that referenced models and custom nodes are available, and report unresolved dependencies rather than silently substituting them.

## Asset and output transfer

- Use SSH/SCP/SFTP with the same password-authenticated account from `openvpn\passwd.txt`. Apply the same one-attempt, non-echoing credential rules to every transfer. User-provided local material and reference images flow from local to remote; generated images, video, audio, workflow JSON, and requested logs flow from remote to local.
- Preserve relative paths under `shared` when practical. Default to `E:\work\comfyui\shared\input` and `E:\work\comfyui\shared\output` locally, with matching `C:\home\AI\comfyui\shared\input` and `C:\home\AI\comfyui\shared\output` remotely. Create these subdirectories only when first needed.
- Stage transfers inside the corresponding project root, compare size or SHA-256 for important files, and then place them in the requested destination.
- Do not treat synchronization as permission to delete or overwrite the other side. Transfer only the files needed for the current task, and request direction before resolving a conflicting existing file.
- Never transfer model or plugin downloads from local to remote; initiate those downloads remotely instead.

## Verified baseline

As of 2026-09-03, SSH password login, the remote-root check, and an SCP upload/download round trip were successful. The round-trip file hashes matched. ComfyUI 0.34.0 was reachable at `http://10.8.67.78:8188`; `/system_stats` and `/queue` responded successfully, and the runtime used shared input/output directories under the remote root. Re-run a lightweight preflight at the start of a future remote operation because VPN state and the assigned address can change.
