#lang racket

(provide quantum-circuit% simulate)

(define r2 0.70710678118)

(define (swap-two lst m1 m2)
    (let ([val-1 (list-ref lst m1)]
          [val-2 (list-ref lst m2)])
      (let ([val-1 val-2]
            [val-2 val-1])
        (list-set
         (list-set lst m1 val-1) m2 val-2))))

(define quantum-circuit%
  (class object%
    (init qubits clbits)

    (define num-qubits qubits)
    (define num-clbits clbits)
    (define name "")
    (define data '() )

    (define/public (show-data)
      data)

    (define/public (nqubits)
      num-qubits)
    (define/public (nclbits)
      num-clbits)
    
    (define/public (initialize k)
      (set! data '() )
      (set! data (append data (list (list "init" k))))
      )

    (define/public (x q)
      (set! data (append data (list (list "x" q)))))

    (define/public (rx theta q)
      (set! data (append data (list (list "rx" theta q)))))

    (define/public (h q)
      (set! data (append data (list (list"h" q)))))

    (define/public (cx s t)
      (set! data (append data (list (list "cx" s t)))))

    (define/public (crx theta s t)
      (set! data (append data (list (list "crx" theta s t)))))

    (define/public (measure q b)
      (if (< b num-clbits) "Index for output bit out of range." "Ready")
      (if (< q num-qubits) "Index for qubit out of range." "Ready")
      (set! data (append data (list (list "m" q b)))))

    (define/public (rz theta q)
      (h q)
      (rx theta q)
      (h q))

    (define/public (ry theta q)
      (rx (/ pi 2) q)
      (rz theta q)
      (rx (/ (- pi) 2) q))

    (define/public (z q)
      (rz pi q))

    (define/public (y q)
      (rz pi q)
      (x q))

    (super-new)))


(define (simulate qc shots get)
  (define (superpose x y)
    (list
     (list (* r2 (+ (first x) (first y)))
           (* r2 (+ (second x) (second y))))
     (list (* r2 (- (first x) (first y)))
           (* r2 (- (second x) (second y))))))

  (define (turn x y theta)
    (list
     (list
      (+ (* (first x) (cos (/ theta 2))) (* (second y) (sin (/ theta 2))))
      (- (* (second x) (cos (/ theta 2))) (* (first y) (sin (/ theta 2)))))
     (list
      (+ (* (first y) (cos (/ theta 2))) (* (second x) (sin (/ theta 2))))
      (- (* (second y) (cos (/ theta 2))) (* (first x) (sin (/ theta 2)))))))

  (define k (append (list (list 1.0 0.0)) (make-list (expt 2 (send qc nqubits)) (list 0 0))))

  (define outputnum-clbitsap (make-hash))

  (define-values (j b0 b1 theta s t l h) (values 0 0 0 0 0 0 0 0))

  (define probs null)
  (define m null)
  (define cumu 0)
  (define un #f)
  (define r 0)
  (define raw-out "")
  (define out-list null)
  (define out "")
  (define counts (make-hash))
  (define finalized-hash (make-hash))

  (for ([gate (send qc show-data)])
    (cond
     [(equal? (first gate) "init")
        (if (list? (first (second gate)))
            (set! k (second gate))
            
            (set! k (foldr (λ (i res)
                             (cons (list i 0) res))
                           '() (second gate))))]
     [(equal? (first gate) "m")
      (hash-set! outputnum-clbitsap (third gate) (second gate))]
     [(member (first gate) '("x" "h" "rx"))
      (set! j (last gate))
      (for ([i0 (range (expt 2 j))])
        (for ([i1 (range (expt 2 (- (send qc nqubits) (+ j 1))))])
          (set! b0 (+ i0 (* (expt 2 (+ j 1)) i1)))
          (set! b1 (+ b0 (expt 2 j)))

          (cond
           [(equal? (first gate) "x")
              (set! k (swap-two k b0 b1))]
           [(equal? (first gate) "h")
            (let ([sup (superpose (list-ref k b0) (list-ref k b1))])
              (set! k (list-set
                       (list-set k b0 (first sup)) b1 (second sup))))]
           [else
            (set! theta (second gate))
            (let ([turned (turn (list-ref k b0) (list-ref k b1) theta)])
              (set! k (list-set
                       (list-set k b0 (first turned)) b1 (second turned))))])))]
     [(member (first gate) '("cx" "crx"))
      (if (equal? (first gate) "cx")
          (set!-values (s t) (values (second gate) (third gate)))
          
          (set!-values (theta s t) (values (second gate) (third gate) (fourth gate))))
      (let ([sorted (sort (list s t) <)])
        (set!-values (l h) (values (first sorted) (second sorted))))

      (for ([i0 (range (expt 2 l))])
        (for ([i1 (range (expt 2 (- h (+ l 1))))])
          (for ([i2 (range (expt 2 (- (send qc nqubits) (+ h 1))))])
            (set! b0 (+ i0 (* (expt 2 (+ l 1)) i1) (* (expt 2 (+ h 1)) i2) (expt 2 s)))
            (set! b1 (+ b0 (expt 2 t)))
            (if (equal? (first gate) "cx")
                (set! k (swap-two k b0 b1))
                (let ([turned (turn (list-ref k b0) (list-ref k b1) theta)])
                  (set! k (list-set
                           (list-set k b0 (first turned)) b1 (second turned))))))))]))

  (if (equal? get "statevector")
      k

      (begin
        (set! probs (map (λ (e)
                             (+ (expt (first e) 2) (expt (second e) 2)))
                           k))
        (cond
          [(equal? get "prob-dict")
           (set! finalized-hash (make-hash))
           (for ([j (range (length probs))]
                 [p probs])
             (hash-set! finalized-hash (~r j #:base 2 #:min-width (send qc nqubits) #:pad-string "0") p))
           finalized-hash
           ]

          [(member get '("counts" "memory"))
           (set! m (make-list (send qc nqubits) #f))
           (for ([gate (send qc show-data)])
             (for ([j (range (send qc nqubits))])
               (when (and (equal? (last gate) j) (list-ref m j))
                 (raise "Incorrect or missing measure command."))
               (set! m (list-set m j (equal? gate (list "m" j j))))))
           (set! m null)

           (for ([i (range shots)])
             (set! cumu 0)
             (set! un #t)
             (set! r (random))

             (for ([j (range (length probs))]
                   [p probs])
               (set! cumu (+ cumu p))
               (if (and (< r cumu) un)
                   (begin
                     (set! raw-out (~r j #:base 2 #:min-width (send qc nqubits) #:pad-string "0"))
                     (set! out-list (make-list (send qc nclbits) #\0))

                     (for ([(bit value) outputnum-clbitsap])
                       (set! out-list (list-set out-list (- (send qc nclbits) 1 bit)
                                                (string-ref raw-out (- (send qc nclbits)
                                                             1 (hash-ref outputnum-clbitsap bit))))))
                     
                     (set! out (list->string out-list))
                     (set! m (append m (list out)))
                     (set! un #f))

                   null)))

           (if (equal? get "memory")
               m

               (begin
                 (set! counts (make-hash))

                 (for ([out m])
                   (if (hash-has-key? counts out)
                             (hash-set! counts out (+ (hash-ref counts out) 1))

                             (hash-set! counts out 1)))
                 counts))
           ])
        ))
  )
