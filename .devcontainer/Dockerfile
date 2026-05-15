FROM fedora:latest

# Install system dependencies
RUN dnf update -y && \
    dnf install -y \
    zsh \
    git \
    make \
    curl \
    wget \
    gcc \
    gcc-c++ \
    postgresql-devel \
    libpq-devel \
    redis \
    neovim \
    ripgrep \
    fd-find \
    unzip \
    tar \
    sudo \
    && dnf clean all

# Create vscode user with sudo access
RUN useradd -m -s /bin/zsh -u 1000 vscode && \
    echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER vscode
WORKDIR /home/vscode

# Install uv (Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/home/vscode/.local/bin:$PATH"

# Install fnm (Fast Node Manager)
RUN curl -fsSL https://fnm.vercel.app/install | bash
ENV PATH="/home/vscode/.local/share/fnm:$PATH"

# Install direnv
RUN curl -sfL https://direnv.net/install.sh | bash
RUN mkdir -p /home/vscode/.config/direnv

# Create standard directories
RUN mkdir -p \
    /home/vscode/.config \
    /home/vscode/.local/bin \
    /home/vscode/.local/share \
    /home/vscode/.cache

# Set up zsh as default shell
ENV SHELL=/bin/zsh

WORKDIR /workspace

CMD ["/bin/zsh"]
