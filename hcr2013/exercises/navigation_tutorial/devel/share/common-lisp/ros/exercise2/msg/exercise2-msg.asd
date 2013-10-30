
(cl:in-package :asdf)

(defsystem "exercise2-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "JoyAxis" :depends-on ("_package_JoyAxis"))
    (:file "_package_JoyAxis" :depends-on ("_package"))
  ))