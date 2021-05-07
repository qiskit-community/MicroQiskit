package model

import kotlin.math.pow

class QuantumCircuit(var numberOfQubits: Int, var numberOfOutputs: Int) {

    var gates: ArrayList<Gate> = arrayListOf()
    var amplitudes: ArrayList<ComplexNumber> = arrayListOf()

    var amplitudeLength: Int = 0
    var dimensionString: String = ""
    var originalSum: Int = 0

    init {
        amplitudeLength = 2.0.pow(numberOfQubits).toInt()
    }

    fun x(targetQubit: Int) = gates.add(Gate(Circuits.X, targetQubit))
    fun rx(targetQubit: Int, rotation: Double) = gates.add(Gate(Circuits.RX, targetQubit, theta = rotation))

    fun h(targetQubit: Int) = gates.add(Gate(Circuits.H, targetQubit))

    fun cx(controlQubit: Int, targetQubit: Int) = gates.add(Gate(Circuits.CX, controlQubit, targetQubit))
    fun crx(controlQubit: Int, targetQubit: Int, rotation: Double) =
        gates.add(Gate(Circuits.CRX, controlQubit, targetQubit, rotation))

    fun measure(output: Int, qubit: Int) = gates.add(Gate(Circuits.M, output, qubit))

    fun rz(targetQubit: Int, rotation: Double) {
        h(targetQubit)
        rz(targetQubit, rotation)
        h(targetQubit)
    }

    fun ry(targetQubit: Int, rotation: Double) {
        rx(targetQubit, Math.PI / 2)
        h(targetQubit)
        rx(targetQubit, rotation)
        h(targetQubit)
        rx(targetQubit, -Math.PI / 2)
    }

    fun z(targetQubit: Int) = rz(targetQubit, Math.PI)

    fun y(targetQubit: Int) {
        rz(targetQubit, Math.PI)
        x(targetQubit)
    }

    fun resetGates() = gates.clear()

    fun probabilitySum(): Double {
        var sum = 0.0
        amplitudes.forEach { sum += it.real * it.real + it.complex * it.complex }
        return sum
    }

}