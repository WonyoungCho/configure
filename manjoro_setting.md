sudo pacman-mirrors --fasttrack && sudo pacman -Syyu

# DISPLAY MacOS in bootmenu
```sh
$ emacs /etc/grub.d/40_custom
```
```
Add 'menuentry "Mac OSX" { exit }'
```

# Korean key setting
```sh
$ sudo pacman -S ibus-hangul ibus-qt
$ emacs ~/.xprofile
```
```
export GTK_IM_MODULE=ibus
export XMODIFIERS=@im=ibus
export QT_IM_MODULE=ibus
ibus-daemon -drx
```
```sh
$ sudo reboot now
```
Bottom right keyboard icon - Preferences

General - Keyboard shortcuts - Next input method - [delete all]

Input method - Add - Korean - Hangul - [delete English]


# Install Cadabra2
```sh
$ sudo pacman -Sy yaourt
$ yaourt -Sy cadabra2-git
```

# 프로그램들
```sh
$ yaourt -Sy google-chrome
$ yaourt -Sy dropbox
```

# 프로그래밍 환경
```sh
$ sudo pacman -S gcc
$ sudo pacman -S gcc-fortran
$ sudo pacman -S openmpi
```

# SSH 접속 환경
```sh
$ sudo pacman -S openssh
$ sudo systemctl enable sshd
$ sudo systemctl start sshd
```

# GUI 환경
```sh
$ sudo pacman -S x2goserver
$ sudo x2godbadmin --createdb   ! create a new database for X2Go
$ sudo systemctl enable x2goserver.service
$ sudo systemctl start x2goserver.service
```
