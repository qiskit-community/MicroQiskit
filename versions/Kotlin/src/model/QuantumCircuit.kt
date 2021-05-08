package model

import util.Circuits
import util.MathConstants
import java.lang.StringBuilder
import kotlin.math.pow
import kotlin.math.sqrt

class QuantumCircuit(var numberOfQubits: Int, var numberOfOutputs: Int) {

    var gates: ArrayList<Gate> = arrayListOf()
    var amplitudes: ArrayList<ComplexNumber> = arrayListOf()

    var amplitudeLength: Int = 0
    var dimensionString: String = ""
    var originalSum: Double = 0.0

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
        rx(targetQubit, MathConstants.PiHalf)
        h(targetQubit)
        rx(targetQubit, rotation)
        h(targetQubit)
        rx(targetQubit, -MathConstants.PiHalf)
    }

    fun z(targetQubit: Int) = rz(targetQubit, MathConstants.Pi)

    fun y(targetQubit: Int) {
        rz(targetQubit, MathConstants.Pi)
        x(targetQubit)
    }

    fun resetGates() = gates.clear()

    fun probabilitySum(): Double {
        var sum = 0.0
        amplitudes.forEach { sum += it.real * it.real + it.complex * it.complex }
        return sum
    }

    fun normalize() = normalize(probabilitySum())

    fun normalize(sum: Double) {
        if (sum < MathConstants.Eps) {
            print("Sum is 0: $sum")
            return
        }

        var localSum = sum

        if (localSum < 1 - MathConstants.Eps || localSum > 1 + MathConstants.Eps) {
            if (originalSum == 0.0) {
                originalSum = localSum
            } else {
                originalSum *= localSum
            }
            localSum = sqrt(localSum)

            amplitudes.forEach {
                it.real /= localSum
                it.complex /= localSum
            }
        }
    }

    fun getAmplitudeList(): ArrayList<ArrayList<Double>> {
        val returnValue: ArrayList<ArrayList<Double>> = arrayListOf()

        amplitudes.forEach {
            val amplitude = arrayListOf<Double>()
            amplitude.add(it.real)
            amplitude.add(it.complex)
            returnValue.add(amplitude)
        }

        return returnValue
    }

    fun getAllNumbersString(length: Int): String {
        val builder = StringBuilder()
        val numbers = arrayOf<Int>()
        for (i in 0..length) numbers[i] = i
        builder.append("[${numbers.joinToString(separator = ",")}]")
        return builder.toString()
    }

    fun getQiskitString(includeAllMeasures: Boolean = false): String {
        val builder = StringBuilder()
        val allNumbers = getAllNumbersString(numberOfQubits)

        if (numberOfOutputs == 0)
            builder.append("qc = QuantumCircuit($numberOfQubits)\n")
        else
            builder.append("qc = QuantumCircuit($numberOfQubits,$numberOfOutputs)\n")

        if (amplitudes.isNotEmpty() && originalSum > 0) {
            builder.append("qc.initialize([${amplitudes.joinToString(separator = ",")}],$allNumbers)\n")
        }

        gates.forEach {
            when (it.circuitType) {
                Circuits.X -> builder.append("qc.x(${it.first})\n")
                Circuits.RX -> builder.append("qc.rx(${it.theta}, ${it.first})\n")
                Circuits.H -> builder.append("qc.h(${it.first}, ${it.second})\n")
                Circuits.CX -> builder.append("qc.cx(${it.first}, ${it.second})\n")
                Circuits.CRX -> builder.append("qc.rx(${it.theta}, ${it.first}), ${it.second})\n")
                Circuits.M -> builder.append("qc.measure(${it.first}, ${it.second})\n")
            }
        }

        if (includeAllMeasures) builder.append("qc.measure($allNumbers, $allNumbers)\n")

        return builder.toString()
    }

    fun addCircuit(circuit: QuantumCircuit) {
        if (circuit.numberOfQubits > numberOfQubits) {
            print("Number of qubit is bigger: ${circuit.numberOfQubits} vs $numberOfQubits")
            numberOfQubits = circuit.numberOfOutputs
            val newQubits = arrayListOf<ComplexNumber>()

            amplitudes.forEach { newQubits.add(it) }
            for (i in 0..numberOfQubits) newQubits.add(circuit.amplitudes[i])
        }

        gates.addAll(circuit.gates)
    }

}