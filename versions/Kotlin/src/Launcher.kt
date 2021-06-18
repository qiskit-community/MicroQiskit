import model.QuantumCircuit
import simulator.MicroQiskitSimulator

fun main() {
    val qc = QuantumCircuit(2, 2)
    val simulator = MicroQiskitSimulator()

    qc.h(0)
    qc.cx(0, 1)
    qc.measure(0, 0)

    val result = simulator.simulate(qc)
    qc.amplitudes.apply { clear(); addAll(result) }
    println("$result\n")
    println(qc.getQiskitString(true))
    print(qc.probabilitySum())
}
