#!/bin/sh

install_conda() {
    # Check if conda is already installed
    if command -v conda >/dev/null 2>&1; then
        echo "Conda is already installed. Skipping installation."
        return 0
    fi

    # Check the operating system
    case "$(uname)" in
        Linux)
            echo "Detected Linux OS."
            mkdir -p "$HOME/miniconda3"
            wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O "$HOME/miniconda3/miniconda.sh"
            sh "$HOME/miniconda3/miniconda.sh" -b -u -p "$HOME/miniconda3"
            rm -rf "$HOME/miniconda3/miniconda.sh"
            ;;
        Darwin)
            echo "Detected macOS."
            mkdir -p "$HOME/miniconda3"
            curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o "$HOME/miniconda3/miniconda.sh"
            sh "$HOME/miniconda3/miniconda.sh" -b -u -p "$HOME/miniconda3"
            rm -rf "$HOME/miniconda3/miniconda.sh"
            ;;
        *)
            echo "Unsupported OS type: $(uname)"
            exit 1
            ;;
    esac

    # Add Miniconda to PATH
    echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.profile

    # Initialize Conda
    . ~/.profile

    # Initialize Conda for the shell
    conda init "$(basename "$SHELL")"
}

# Run the install_conda function
install_conda

echo "Conda installation completed or was already installed. Please restart your terminal or run '. ~/.profile' to start using Conda."

