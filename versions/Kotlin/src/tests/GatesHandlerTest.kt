package tests

import model.QuantumCircuit
import org.junit.jupiter.api.Test
import simulator.MicroQiskitSimulator

internal class GatesHandlerTest {
    private val simulator = MicroQiskitSimulator()

    @Test
    fun testXGate() {
        var qc = QuantumCircuit(1, 1)

        qc.x(0)
        assert(simulator.simulate(qc).toString() == "[0.0 + 0.0 i, 1.0 + 0.0 i]")

        qc = QuantumCircuit(2, 2)
        qc.x(0)
        assert(simulator.simulate(qc).toString() == "[0.0 + 0.0 i, 1.0 + 0.0 i, 0.0 + 0.0 i, 0.0 + 0.0 i]")

        qc = QuantumCircuit(2, 2)
        qc.x(1)
        assert(simulator.simulate(qc).toString() == "[0.0 + 0.0 i, 0.0 + 0.0 i, 1.0 + 0.0 i, 0.0 + 0.0 i]")

        qc = QuantumCircuit(2, 2)
        qc.x(0)
        qc.x(1)
        assert(simulator.simulate(qc).toString() == "[0.0 + 0.0 i, 0.0 + 0.0 i, 0.0 + 0.0 i, 1.0 + 0.0 i]")
    }

    @Test
    fun testCXGate() {
        var qc = QuantumCircuit(2, 2)

        qc.x(0)
        assert(simulator.simulate(qc).toString() == "[0.0 + 0.0 i, 1.0 + 0.0 i, 0.0 + 0.0 i, 0.0 + 0.0 i]")

        qc.cx(0, 1)
        assert(simulator.simulate(qc).toString() == "[0.0 + 0.0 i, 0.0 + 0.0 i, 0.0 + 0.0 i, 1.0 + 0.0 i]")

        qc.x(0)
        assert(simulator.simulate(qc).toString() == "[0.0 + 0.0 i, 0.0 + 0.0 i, 1.0 + 0.0 i, 0.0 + 0.0 i]")

        qc = QuantumCircuit(2, 2)

        qc.x(1)
        assert(simulator.simulate(qc).toString() == "[0.0 + 0.0 i, 0.0 + 0.0 i, 1.0 + 0.0 i, 0.0 + 0.0 i]")

        qc.cx(1, 0)
        assert(simulator.simulate(qc).toString() == "[0.0 + 0.0 i, 0.0 + 0.0 i, 0.0 + 0.0 i, 1.0 + 0.0 i]")

        qc.x(1)
        assert(simulator.simulate(qc).toString() == "[0.0 + 0.0 i, 1.0 + 0.0 i, 0.0 + 0.0 i, 0.0 + 0.0 i]")
    }

    @Test
    fun testHGate() {
        var qc = QuantumCircuit(1, 1)

        qc.h(0)
        assert(simulator.simulate(qc).toString() == "[0.5 + 0.0 i, 0.5 + 0.0 i]")

        qc = QuantumCircuit(2, 2)
        qc.h(0)
        assert(simulator.simulate(qc).toString() == "[0.5 + 0.0 i, 0.5 + 0.0 i, 0.0 + 0.0 i, 0.0 + 0.0 i]")

        qc = QuantumCircuit(2, 2)
        qc.h(1)
        assert(simulator.simulate(qc).toString() == "[0.5 + 0.0 i, 0.0 + 0.0 i, 0.5 + 0.0 i, 0.0 + 0.0 i]")

        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.h(1)
        assert(simulator.simulate(qc).toString() == "[0.25 + 0.0 i, 0.25 + 0.0 i, 0.25 + 0.0 i, 0.25 + 0.0 i]")
    }

}