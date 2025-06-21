---
layout: page
title: Quick Start Guide
permalink: /docs/quick-start
---

## Installation

### Using the installer script (Recommended)

```bash
curl -sSf https://install.asthra-lang.org | sh
```

### Package Managers

**Homebrew (macOS/Linux):**
```bash
brew install asthra-lang/tap/asthra
```

**Chocolatey (Windows):**
```powershell
choco install asthra
```

## Your First Program

Create `hello.asthra`:

```asthra
func main() {
    print("Hello, Asthra!")
}
```

Run it:

```bash
asthra run hello.asthra
```

## Language Basics

```asthra
// Variables
let name = "Asthra"
mut counter = 0

// Functions
func greet(name: String) -> String {
    return "Hello, ${name}!"
}

// Data structures
struct User {
    name: String
    age: Int
}

// Pattern matching
match result {
    Ok(value) => print("Success: ${value}"),
    Err(error) => print("Error: ${error}")
}
```

---

## Getting Help

- **[GitHub Discussions](https://github.com/orgs/asthra-lang/discussions)** - Ask questions and share ideas
- **[GitHub Issues](https://github.com/asthra-lang/asthra/issues)** - Report bugs and request features
- **[Discord Server](https://discord.gg/asthra)** - Real-time chat with the community

---

*Happy coding with Asthra! 🚀* 