# Contributing to Zidle

Thank you for considering contributing to Zidle! I am open to any contributions, from bug fixes to new animated scenes.

## Branching Strategy

Branching model:
* `main`: The stable release branch. **Do not open Pull Requests against this branch.**
* `dev`: The development branch where all new features are merged and tested. **All Pull Requests MUST be targeted against the `dev` branch.**

## How to Contribute

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/mariostabile1/zidle.git
   cd zidle
   ```
3. **Checkout the dev branch**:
   ```bash
   git checkout dev
   ```
4. **Create a new feature branch** starting from `dev`:
   ```bash
   git checkout -b feature/my-new-scene
   ```
5. Make your changes and test them locally. You can quickly test Zidle animations by just running the core engine:
   ```bash
   python3 core/main.py
   ```
6. **Commit your changes** using clean, descriptive commit messages.
7. **Push to your fork** on GitHub.
8. **Open a Pull Request** targeting the `dev` branch of the original repository.

## Adding a New Scene

If you want to contribute a new screensaver scene:
1. Create a new Python file in the `scenes/` directory (e.g., `scenes/my_new_scene.py`).
2. Implement the standard `Scene` class structure as shown in the documentation.
3. Test it locally to ensure it doesn't drop frames, leak memory, or cause terminal glitches upon resizing.
4. Submit your PR against the `dev` branch!

Thank you for your contributions!
