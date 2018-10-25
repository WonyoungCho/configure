(custom-set-variables
'(initial-frame-alist (quote ((fullscreen . maximized)))))

(custom-set-variables
  ;; custom-set-variables was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 '(inhibit-startup-screen t)
 '(scroll-bar-mode (quote right)))
(custom-set-faces
  ;; custom-set-faces was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 '(default ((t (:inherit nil :stipple nil :background "black" :foreground "white" :inverse-video nil :box nil :strike-through nil :overline nil :underline nil :slant normal :weight bold :height 161 :width normal :foundry "monotype" :family "Courier New")))))

(require 'package)
(add-to-list 'package-archives '("melpa" . "http://melpa.org/packages/"))

(display-time)

(global-font-lock-mode t)
(show-paren-mode t)
(global-auto-revert-mode 1)
;;(global-linum-mode 1)
(define-key global-map (kbd "RET") 'newline-and-indent)
;;(setq gdb-many-windows t)
(setq backup-inhibited t)
(setq column-number-mode t)
;(add-to-list 'custom-theme-load-path "~/.emacs.d/themes")
;(add-to-list 'load-path "~/.emacs.d/themes")
;(require 'color-theme)
;(color-theme-initialize)
;(color-theme-tango)

;(load-theme 'moe)
(global-unset-key (kbd "\C-z"))
(global-unset-key (kbd "<f10>"))
(global-set-key (kbd "\C-c C-s") 'gnuplot-run-buffer)
(global-set-key (kbd "\C-c C-g") 'gnuplot-mode)
(global-set-key (kbd "\C-c C-a") 'my-macro)
(global-set-key (kbd "\C-x C-a") 'other-window)
(global-set-key (kbd "\C-a") 'clipboard-yank)
(global-set-key (kbd "\C-z") 'undo)
(global-set-key (kbd "<f2>") 'call-last-kbd-macro)
(global-set-key (kbd "<f4>") 'split-window-right)
(global-set-key (kbd "<M-up>") 'enlarge-window)
(global-set-key (kbd "<M-down>") 'shrink-window)
(global-set-key (kbd "<f5>") 'enlarge-window-horizontally)
(global-set-key (kbd "<f6>") 'other-window)
(global-set-key (kbd "<f7>") 'split-window-below)
(global-set-key (kbd "<f8>") 'delete-other-windows)
(global-set-key (kbd "<f9>") 'python-run)
(global-set-key (kbd "<f11>") 'my-next-error)
(global-set-key (kbd "<f12>") 'my-previous-error)


(setq smart-compile-alist
      '(("\\.py\\'"."python %n.py")
	("\\.for\\'"."ifort -ffixed-line-length-none %f -o %n.exe")
        ("\\.f\\'"."ifort -O3 %f -o %n.exe")
        ("\\.tex\\'"."pdflatex %f %n")))
(setq compilation-read-command nil)

;; Close the compilation window if there was no error at all.
(setq compilation-exit-message-function
      (lambda (status code msg)
        ;; If M-x compile exists with a 0
        (when (and (eq status 'exit) (zerop code))
          ;; then bury the *compilation* buffer, so that C-x b doesn't go there
          (bury-buffer "*compilation*")
          ;; and return to whatever were looking at before
          (replace-buffer-in-windows "*compilation*"))
        ;; Always return the anticipated result of compilation-exit-message-function
        (cons msg code)))

(defun bind-keys ()
  "do something"
  (interactive)
  (split-window-below)
  (other-window 1)
  (eshell)
  (insert "python "))
;  (insert (expand-file-name filename)))

(defun below-keys ()
  "do something"
  (interactive)
  (other-window 1)
  (insert "python "))


(defun python-run ()
  (interactive)
  (defvar name-only (file-name-sans-extension (buffer-name)))
  (shell-command (format "python  \"%s.py\"" name-only (buffer-name))))

(global-set-key (kbd "\C-c C-d") 'kill-this-buffer)
(global-set-key (kbd "\C-c C-a") 'switch-to-previous-buffer)

(defun switch-to-previous-buffer ()
  (interactive)
  (switch-to-buffer (other-buffer (current-buffer) 1)))
