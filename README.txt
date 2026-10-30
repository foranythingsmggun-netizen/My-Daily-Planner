# My Daily Planner (Python + Kivy)

## Files
- `main.py` — app source code
- `buildozer.spec` — Android packaging settings

## Build an APK
Buildozer builds Android apps on Linux/macOS. On Windows, use WSL2 Ubuntu. You can also use a Linux cloud machine.

### 1. Install build dependencies (Ubuntu)
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-virtualenv \
  autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
  libtinfo6 cmake libffi-dev libssl-dev automake
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Buildozer
```bash
pip install --upgrade pip
pip install buildozer setuptools cython==0.29.34
```

### 4. Build
Open a terminal in this folder (where `main.py` and `buildozer.spec` are located), then run:
```bash
buildozer -v android debug
```
The first build downloads Android SDK/NDK and may take a while. When successful, the APK appears in the `bin/` folder.

Official docs:
- https://buildozer.readthedocs.io/
- https://github.com/kivy/buildozer
