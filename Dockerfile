# Download Calm DSL latest from hub.docker.com
FROM ntnx/calm-dsl:v3.4.0

# Add packages needed for development
RUN apk update \
    && apk upgrade \
    && apk add --no-cache make \
        docker \
        git \
        yq \
        curl \
        unzip \
        tar \
        openssl \
        gnupg \
        gpg \
        ca-certificates \
        tree \
        fzf \
        vim \
        bash-completion \
        zsh \
        perl \
        ncurses \
        jq \
        aws-cli \
        packer \
        terraform && \
    rm -rf /tmp/* && \
    rm -rf /var/cache/apk/*

## configure zsh
RUN apk add --no-cache zsh \
    && sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
    && git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k \
    && git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions \
    && git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting \
    && git config --global --add safe.directory /dsl-workspace

COPY ./scripts/dotfiles /root

# ## install utils
COPY ./scripts/bastion /tmp
WORKDIR /tmp
RUN chmod +x *.sh \
    && ./install_helm.sh \
    && ./install_kubectl.sh \
    && ./install_kubectx_kubens.sh \
    && ./install_kube-ps1.sh \
    && ./install_kubectl_krew.sh \
    && ./configure_bashrc.sh \
    && ./configure_vimrc.sh \
    && ./configure_kubectl_aliases.sh \
    && ./install_stern.sh \
    && ./install_argocd_cli.sh \
    && ./install_vault_cli.sh \
    && ./install_istio_cli.sh \
    && ./install_crossplane.sh \
    && ./install_clusterctl.sh \
    && ./install_rancher_cli.sh \
    && calm completion install zsh && \
    rm -rf /tmp/*

SHELL ["/bin/zsh", "-c"]
RUN source /root/.zshrc
RUN zsh -i -c -- 'zinit module build; @zinit-scheduler burst || true '
