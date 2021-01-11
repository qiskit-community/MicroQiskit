#lang racket

(require "microqiskit.rkt")

(define qc (new quantum-circuit% [qubits 3] [clbits 3]))
(send qc h 0)
(send qc cx 0 1)
(send qc cx 0 2)
(send qc measure 0 0)
(send qc measure 1 1)
(send qc measure 2 2)

(displayln "statevector")
(simulate qc 1024 "statevector")

(displayln "\nprob-dict")
(simulate qc 1024 "prob-dict")

(displayln "\ncounts")
(simulate qc 1024 "counts")
