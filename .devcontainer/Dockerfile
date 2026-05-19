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

# Create dev user with sudo access
RUN useradd -m -s /bin/zsh -u 1000 dev && \
    echo "dev ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER dev
WORKDIR /home/dev

# Install uv (Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/home/dev/.local/bin:$PATH"

# Install fnm (Fast Node Manager)
RUN curl -fsSL https://fnm.vercel.app/install | bash
ENV PATH="/home/dev/.local/share/fnm:$PATH"

# Install direnv
RUN curl -sfL https://direnv.net/install.sh | bash
RUN mkdir -p /home/dev/.config/direnv

# Create standard directories
RUN mkdir -p \
    /home/dev/.config \
    /home/dev/.local/bin \
    /home/dev/.local/share \
    /home/dev/.cache

# Set up zsh as default shell
ENV SHELL=/bin/zsh

WORKDIR /workspace-nbry-libs

CMD ["/bin/zsh"]
