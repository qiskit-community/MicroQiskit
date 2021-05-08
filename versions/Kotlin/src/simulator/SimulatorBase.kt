package simulator

import model.ComplexNumber
import model.QuantumCircuit
import util.MathConstants
import kotlin.math.pow

class SimulatorBase {

    fun simulate(circuit: QuantumCircuit): List<ComplexNumber> {
        val sum = circuit.probabilitySum()

        return if (sum > MathConstants.Eps) {
            if (sum < 1 - MathConstants.Eps || sum > 1 + MathConstants.Eps)
                circuit.normalize(sum)

            val amplitudes = arrayListOf<ComplexNumber>()
            circuit.amplitudes.forEach { amplitudes.add(it) }

            amplitudes
        } else {
            val amplitudes = arrayListOf<ComplexNumber>()
            circuit.amplitudes.forEach { amplitudes.add(ComplexNumber(0.0, 0.0)) }
            amplitudes.first().real = 1.0

            amplitudes
        }
    }

    fun simulateInPlace(circuit: QuantumCircuit): List<ComplexNumber> {
        val localAmplitudes = arrayListOf<ComplexNumber>()
        val sum = circuit.probabilitySum()

        if (sum > MathConstants.Eps) {
            if (sum < 1 - MathConstants.Eps || sum > 1 + MathConstants.Eps) {
                circuit.normalize(sum)
            }

            circuit.amplitudes.forEach { localAmplitudes.add(it) }
        } else {
            circuit.amplitudes.forEach { _ -> localAmplitudes.add(ComplexNumber(0.0, 0.0)) }
            localAmplitudes.first().real = 1.0
        }

        return localAmplitudes
    }

    fun getProbabilities(circuit: QuantumCircuit): List<Double> {
        val probabilities = arrayListOf<Double>()
        val length = 2.0.pow(circuit.numberOfQubits).toInt()
        for (i in 0..length) probabilities.add(0.0)
        return probabilities
    }

    fun getProbabilities(amplitudes: List<ComplexNumber>): List<Double> =
        amplitudes.map { it.real.pow(2) + it.complex.pow(2) }

}