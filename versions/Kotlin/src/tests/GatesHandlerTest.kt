package tests

import model.QuantumCircuit
import org.junit.jupiter.api.Test
import simulator.MicroQiskitSimulator
import util.MathConstants

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

    @Test
    fun testRXGate() {
        var qc = QuantumCircuit(2, 2)

        qc.rx(0, MathConstants.PiQuarter)
        assert(simulator.simulate(qc).toString() == "[0.9238795325112867 + 0.0 i, 0.0 - 0.3535533905932738 i, 0.0 + 0.0 i, 0.0 + 0.0 i]")

        qc = QuantumCircuit(2, 2)
        qc.rx(0, MathConstants.PiQuarter)
        qc.rx(1, MathConstants.PiQuarter/2)
        assert(simulator.simulate(qc).toString() == "[0.9061274463528878 + 0.0 i, 0.0 - 0.3467599613305369 i, 0.0 - 0.17677669529663684 i, -0.06764951251827461 + 0.0 i]")

        qc.h(0)
        qc.h(1)
        assert(simulator.simulate(qc).toString() == "[0.20961948345865328 + 0.13088416415679344 i, 0.20961948345865328 + 0.13088416415679344 i, 0.20961948345865328 + 0.13088416415679344 i, 0.20961948345865328 + 0.13088416415679344 i]")
    }

    @Test
    fun testRZGate() {
        val qcx = QuantumCircuit(1, 1)
        val qcz = QuantumCircuit(1, 1)

        val tx = 2.8777603974458796
        val tz = 0.5589019778800038

        qcx.rx(0, tx)
        qcx.h(0)
        qcx.rx(0, tz)
        qcx.h(0)

        qcz.rx(0, tx)
        qcz.rz(0, tz)

        assert(simulator.simulate(qcx) == simulator.simulate(qcz))
    }

}