# Terminal Configuration for Screenshots

## Requirements
- Resolution: 1920x1080
- Theme: Light
- Font: Monospace, 14px
- Terminal emulator: GNOME Terminal or similar

## Configuration Steps

### 1. Set Terminal to Light Theme
```bash
# GNOME Terminal
gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:default/ use-theme-colors false
gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:default/ background-color '#FFFFFF'
gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:default/ foreground-color '#000000'
```

### 2. Set Window Size
```bash
# Resize terminal to 1920x1080
# Use window manager or terminal settings
```

### 3. Set Font
```bash
# GNOME Terminal
gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:default/ font 'Monospace 14'
gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:default/ use-system-font false
```

## Ready for Screenshots
After configuration, terminal is ready for screenshot capture at 1920x1080 with light theme.
