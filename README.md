### Unofficial Firefox ESR flatpak

## Install

1. Install [flatpak](https://flatpak.org/setup/) (>=0.11.1), [xdg-desktop-portal](https://github.com/flatpak/xdg-desktop-portal) and its [backends](https://github.com/flatpak/xdg-desktop-portal#using-portals). Latest versions are preferred.

2. Add the [Flathub](https://flathub.org/setup) repository if absent

3. Install this package

```bash
# System
flatpak install https://github.com/ri-fumo/firefox_esr_flatpak/raw/refs/heads/main/firefox_esr.flatpakref

# User
flatpak install --user https://github.com/ri-fumo/firefox_esr_flatpak/raw/refs/heads/main/firefox_esr.flatpakref
```

## Uninstall

```bash
# Only remove
flatpak remove org.mozilla.FirefoxESR

# Delete data and remove
flatpak remove org.mozilla.FirefoxESR --delete-data

# Clear dependencies
flatpak uninstall --unused

# Delete the remote
flatpak remote-delete firefox_esr
```

## Bugs

Check if it is already a known issue first https://bugzilla.mozilla.org/show_bug.cgi?id=flatpak

Check if it is reproducible in the official tarball (preferably in a new profile or safe mode). If it is, open a bug with Mozilla, optionally use [mozregression](https://mozilla.github.io/mozregression/quickstart.html) to bisect it.

Common troubleshooting help https://fedoraproject.org/wiki/How_to_debug_Firefox_problems

Otherwise feel free to open an issue here.

## Credits

Mozilla for mainlining the stable flatpak recipes.

Original Firefox ESR flatpak project https://gitlab.com/projects261/firefox-esr-flatpak and CI https://github.com/andyholmes/flatter

Logo: [Source](https://www.creativetail.com/40-free-flat-animal-icons/), [License](https://www.creativetail.com/licensing/)

## Set up personal repo

See https://docs.flatpak.org/en/latest/hosting-a-repository.html#hosting-a-repository-on-gitlab-github-pages

## Build locally

1. Clone this repository

```bash
git clone https://github.com/ri-fumo/firefox_esr_flatpak.git && cd firefox_esr_flatpak
```

2. Install flatpak, [flatpak-builder](https://docs.flatpak.org/en/latest/flatpak-builder.html) and set up the Flathub repository
on `user` location.

3. Run these commands to build and install

```bash
python3 generate.py && flatpak-builder build --force-clean --user --install-deps-from=flathub --install org.mozilla.FirefoxESR.yaml
```

4. To update, redo step #3.

## Signature

GPG key used to sign repo: F8A5F798CA257770

You can verify the key used, using

```bash
gpg --no-default-keyring --keyring=</var/lib | ~/.local/share>/flatpak/repo/firefox_esr.trustedkeys.gpg --lock-never --list-keys
```

and even create the keyring yourself using:

```bash
gpg --no-default-keyring --keyring ./firefox_esr.trustedkeys.gpg --keyserver keyserver.ubuntu.com --recv-keys F8A5F798CA257770

mv firefox_esr.trustedkeys.gpg </var/lib | ~/.local/share>/flatpak/repo
```
~
### Expired

If `flatpak` says that the key is expired, remove the remote and
[install](#install) it again.

```bash
flatpak remote-delete firefox_esr

# Press y on the prompt
```
