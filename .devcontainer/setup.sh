#!/bin/bash
set -e

echo "🚀 Starting dev container setup..."

DOTFILES_DIR="${DOTFILES_DIR:-$HOME/.dotfiles}"
DOTFILES_REPO_HTTPS="${DOTFILES_REPO_HTTPS:-https://github.com/nbry/dotfiles.git}"
DOTFILES_REPO_SSH="${DOTFILES_REPO_SSH:-git@github.com:nbry/dotfiles.git}"
DOTSETUP_BIN="$DOTFILES_DIR/bin/dotsetup"
ZSHRC="$HOME/.zshrc"
WORKSPACE_DIR="/workspace-nbry-libs"

DOTSETUP_APPLIED=false

command_exists() {
    command -v "$1" > /dev/null 2>&1
}

append_to_zshrc_if_missing() {
    marker="$1"
    comment="$2"
    line="$3"

    if [ -f "$ZSHRC" ] && ! grep -q "$marker" "$ZSHRC"; then
        echo "" >> "$ZSHRC"
        echo "$comment" >> "$ZSHRC"
        echo "$line" >> "$ZSHRC"
        return 0
    fi

    return 1
}

link_if_exists() {
    src="$1"
    dst="$2"
    label="$3"

    if [ -e "$src" ]; then
        ln -sfn "$src" "$dst"
        echo "✓ Linked $label"
        return 0
    fi

    return 1
}

# Clone dotfiles if not already present
if [ ! -d "$DOTFILES_DIR" ]; then
    echo "📦 Cloning dotfiles repository..."

    if git clone "$DOTFILES_REPO_HTTPS" "$DOTFILES_DIR"; then
        echo "✓ Cloned dotfiles via HTTPS"
    elif git clone "$DOTFILES_REPO_SSH" "$DOTFILES_DIR"; then
        echo "✓ Cloned dotfiles via SSH"
    else
        echo "⚠ Warning: failed to clone dotfiles. Continuing without dotfile links."
    fi
else
    echo "✓ Dotfiles already cloned"
fi

if [ -d "$DOTFILES_DIR" ] && [ -x "$DOTSETUP_BIN" ]; then
    echo "🔧 Applying dotfiles with dotsetup..."

    if ! command_exists yq; then
        echo "📦 Installing yq for dotsetup..."
        if command_exists sudo && command_exists dnf; then
            sudo dnf install -y yq > /dev/null 2>&1 || true
        fi
    fi

    if command_exists yq; then
        if DEVCONTAINER_MODE=true "$DOTSETUP_BIN" --devcontainer; then
            DOTSETUP_APPLIED=true
            echo "✓ Dotfiles applied via dotsetup"

            # dotsetup uses ln -s and may skip existing targets; force key links for idempotency.
            link_if_exists "$DOTFILES_DIR/nvim" "$HOME/.config/nvim" "~/.config/nvim" || true
            link_if_exists "$DOTFILES_DIR/zsh/zshrc" "$HOME/.zshrc" "~/.zshrc" || link_if_exists "$DOTFILES_DIR/.zshrc" "$HOME/.zshrc" "~/.zshrc" || true
            link_if_exists "$DOTFILES_DIR/zsh/zsh_aliases" "$HOME/.zsh_aliases" "~/.zsh_aliases" || true
        else
            echo "⚠ Warning: dotsetup failed, falling back to basic linking"
        fi
    else
        echo "⚠ Warning: yq is unavailable; falling back to basic linking"
    fi
fi

if [ "$DOTSETUP_APPLIED" != true ] && [ -d "$DOTFILES_DIR" ]; then
    # Symlink nvim config
    echo "🔗 Linking nvim configuration..."
    mkdir -p "$HOME/.config"

    if ! link_if_exists "$DOTFILES_DIR/nvim" "$HOME/.config/nvim" "~/.config/nvim"; then
        echo "⚠ Warning: nvim directory not found in dotfiles"
    fi

    # Symlink zsh configs
    echo "🔗 Linking zsh configuration..."
    if ! link_if_exists "$DOTFILES_DIR/.zshrc" "$HOME/.zshrc" "~/.zshrc" \
        && ! link_if_exists "$DOTFILES_DIR/zshrc" "$HOME/.zshrc" "~/.zshrc" \
        && ! link_if_exists "$DOTFILES_DIR/zsh/zshrc" "$HOME/.zshrc" "~/.zshrc"; then
        echo "⚠ Warning: zshrc not found in dotfiles"
    fi

    # Link common zsh companion files from repo root or zsh/ subdir.
    for file in .zshenv .zprofile .zlogin .zlogout zsh_aliases; do
        if ! link_if_exists "$DOTFILES_DIR/$file" "$HOME/$file" "~/$file"; then
            link_if_exists "$DOTFILES_DIR/zsh/$file" "$HOME/$file" "~/$file" || true
        fi
    done

    # Link .zsh directory if it exists
    link_if_exists "$DOTFILES_DIR/.zsh" "$HOME/.zsh" "~/.zsh/" || true
fi

# Set up direnv hook in zshrc if not already present
if append_to_zshrc_if_missing "direnv hook zsh" "# direnv hook" 'eval "$(direnv hook zsh)"'; then
    echo "✓ Added direnv hook to .zshrc"
fi

# Install Starship prompt
if command_exists starship; then
    echo "✓ Starship already installed"
elif command_exists curl; then
    echo "📦 Installing Starship..."
    mkdir -p "$HOME/.local/bin"
    if curl -fsSL https://starship.rs/install.sh | sh -s -- -y -b "$HOME/.local/bin"; then
        echo "✓ Starship installed"
    else
        echo "⚠ Warning: Starship installation failed"
    fi
else
    echo "⚠ Warning: curl is not installed; skipping Starship setup"
fi

# Set up Starship hook in zshrc if available and not already present
if command_exists starship && append_to_zshrc_if_missing "starship init zsh" "# starship prompt" 'eval "$(starship init zsh)"'; then
    echo "✓ Added Starship hook to .zshrc"
fi

# Install database CLI tools for local development
if ! command_exists psql || ! command_exists redis-cli; then
    echo "📦 Installing database CLI tools..."
    if command_exists sudo && command_exists dnf; then
        dnf_packages=()

        if ! command_exists psql; then
            # Fedora package that provides psql and related client tooling.
            dnf_packages+=(postgresql)
        fi

        if ! command_exists redis-cli; then
            dnf_packages+=(redis)
        fi

        if [ ${#dnf_packages[@]} -gt 0 ]; then
            if sudo dnf install -y "${dnf_packages[@]}"; then
                echo "✓ Database CLI tools installed"
            else
                echo "⚠ Warning: failed to install one or more database CLI tools"
            fi
        fi
    else
        echo "⚠ Warning: sudo or dnf not available; skipping database CLI install"
    fi
else
    echo "✓ Database CLI tools already installed"
fi

# Add handy aliases for DB shells if not already present
if append_to_zshrc_if_missing "alias pgdev=" "# local dev database shortcuts" "alias pgdev='PGPASSWORD=postgres psql -h postgres -U postgres -d lifting_website'"; then
    # append the companion alias in the same block when pgdev is first added
    echo "alias redisdev='redis-cli -h redis -p 6379'" >> "$ZSHRC"
    echo "✓ Added pgdev and redisdev aliases to .zshrc"
fi

# Install fnm and node if package.json exists
if [ -f "$WORKSPACE_DIR/package.json" ] && command_exists fnm; then
    echo "📦 Installing Node.js via fnm..."
    eval "$(fnm env --use-on-cd)"

    # Check if .node-version or .nvmrc exists
    if [ -f "$WORKSPACE_DIR/.node-version" ]; then
        NODE_VERSION=$(cat "$WORKSPACE_DIR/.node-version")
    elif [ -f "$WORKSPACE_DIR/.nvmrc" ]; then
        NODE_VERSION=$(cat "$WORKSPACE_DIR/.nvmrc")
    else
        NODE_VERSION="lts-latest"
    fi

    fnm install "$NODE_VERSION"
    fnm use "$NODE_VERSION"
    echo "✓ Node.js installed: $(node --version)"

    # Install npm dependencies
    if [ -f "$WORKSPACE_DIR/package-lock.json" ]; then
        echo "📦 Installing npm dependencies..."
        npm install
        echo "✓ npm dependencies installed"
    fi
elif [ -f "$WORKSPACE_DIR/package.json" ]; then
    echo "⚠ Warning: fnm is not installed; skipping Node.js setup"
fi

# Install Python dependencies with uv
if [ -f "$WORKSPACE_DIR/pyproject.toml" ] && command_exists uv; then
    echo "📦 Installing Python dependencies with uv..."
    cd "$WORKSPACE_DIR"
    uv sync
    echo "✓ Python dependencies installed"
elif [ -f "$WORKSPACE_DIR/pyproject.toml" ]; then
    echo "⚠ Warning: uv is not installed; skipping Python dependency sync"
fi

# Initialize database if needed
echo "🗄️  Checking database connectivity..."
if pg_isready -h postgres -U postgres > /dev/null 2>&1; then
    echo "✓ PostgreSQL is ready"
else
    echo "⚠ Warning: PostgreSQL not responding"
fi

# Check Redis connectivity
echo "🔴 Checking Redis connectivity..."
if redis-cli -h redis ping > /dev/null 2>&1; then
    echo "✓ Redis is ready"
else
    echo "⚠ Warning: Redis not responding"
fi

echo ""
echo "✨ Dev container setup complete!"
echo ""
echo "Available services:"
echo "  - PostgreSQL: postgres:5432 (user: postgres, db: lifting_website)"
echo "  - Redis: redis:6379"
echo ""
echo "Tools installed:"
echo "  - Python: $(python --version 2>&1)"
echo "  - uv: $(uv --version 2>&1)"
echo "  - Node.js: $(node --version 2>&1 || echo 'not installed')"
echo "  - Starship: $(starship --version 2>&1 || echo 'not installed')"
echo "  - psql: $(psql --version 2>&1 || echo 'not installed')"
echo "  - redis-cli: $(redis-cli --version 2>&1 || echo 'not installed')"
echo "  - neovim: $(nvim --version | head -n1)"
echo "  - direnv: $(direnv --version 2>&1)"
echo ""
echo "Ready to code! 🎉"
