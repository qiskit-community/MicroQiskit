#lang racket

(require "microqiskit.rkt")

(define qc (new quantum-circuit% [qubits 2] [clbits 2]))
(send qc h 0)
(send qc x 1)
(send qc cx 0 1)
(send qc z 1)
(send qc measure 0 0)
(send qc measure 1 1)

(displayln "statevector")
(simulate qc 1024 "statevector")

(displayln "\nprob-dict")
(simulate qc 1024 "prob-dict")

(displayln "\ncounts")
(simulate qc 1024 "counts")

; (displayln "\nmemory")
; (simulate qc 1024 "memory")
