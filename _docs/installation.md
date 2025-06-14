---
layout: page
title: Installation Guide
permalink: /docs/installation/
---

# Installing Asthra

This guide will help you install Asthra on your system and get your development environment set up.

## System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Memory**: At least 2GB RAM
- **Storage**: 500MB free disk space
- **Architecture**: x86_64 or ARM64

## Installation Methods

### Option 1: Using the Installer Script (Recommended)

The easiest way to install Asthra is using our installer script:

```bash
curl -fsSL https://install.asthra-lang.org | sh
```

This script will:
- Download the latest version of Asthra
- Install it to `/usr/local/bin` (or `~/.asthra/bin` if you don't have sudo access)
- Add Asthra to your PATH
- Install the Asthra package manager

### Option 2: Download Pre-built Binaries

1. Visit the [releases page](https://github.com/yourusername/asthra-lang/releases)
2. Download the appropriate binary for your platform
3. Extract the archive
4. Move the `asthra` binary to a directory in your PATH

### Option 3: Build from Source

If you prefer to build from source:

```bash
git clone https://github.com/yourusername/asthra-lang.git
cd asthra-lang
make install
```

**Prerequisites for building from source:**
- Rust 1.70 or later
- LLVM 15 or later
- CMake 3.20 or later

## Verify Installation

After installation, verify that Asthra is working correctly:

```bash
asthra --version
```

You should see output similar to:
```
Asthra 0.1.0 (build 2024-01-15)
```

## Next Steps

Now that you have Asthra installed, you're ready to:

1. [Write your first Asthra program](../first-program/)
2. [Take the language tour](../language-tour/)
3. [Set up your IDE](../ide-support/)

## Troubleshooting

### Common Issues

**Command not found: asthra**
- Make sure Asthra is in your PATH
- Try restarting your terminal
- Check if the installation completed successfully

**Permission denied**
- On Unix systems, you may need to make the binary executable: `chmod +x asthra`
- Ensure you have the necessary permissions to install software

**Version conflicts**
- If you have multiple versions installed, check which one is being used: `which asthra`
- Consider using a version manager or removing old installations

### Getting Help

If you encounter issues not covered here:

1. Check our [FAQ](../faq/)
2. Search existing [GitHub issues](https://github.com/yourusername/asthra-lang/issues)
3. Create a new issue with details about your system and the problem
4. Join our [community discussions](https://github.com/yourusername/asthra-lang/discussions) 