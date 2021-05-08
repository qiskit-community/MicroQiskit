package simulator

import model.ComplexNumber
import model.QuantumCircuit
import util.Circuits
import util.MathConstants

class MicroQiskitSimulator : SimulatorBase() {

    private val gatesHandler = GatesHandler()

    companion object {
        var power2Values = listOf<Int>()
    }

    override fun simulate(circuit: QuantumCircuit): List<ComplexNumber> {
        power2Values = MathConstants.initializePower2Values(power2Values, circuit.numberOfQubits+2)

        var amplitudes = super.simulate(circuit)

        circuit.gates.forEach { gate ->
            amplitudes = when (gate.circuitType) {
                Circuits.X -> gatesHandler.handleX(amplitudes, gate, circuit.numberOfQubits)
                Circuits.RX -> gatesHandler.handleRX(amplitudes, gate, circuit.numberOfQubits)
                Circuits.CX -> gatesHandler.handleCX(amplitudes, gate, circuit.numberOfQubits)
                Circuits.CRX -> gatesHandler.handleCRX(amplitudes, gate, circuit.numberOfQubits)
                Circuits.H -> gatesHandler.handleH(amplitudes, gate, circuit.numberOfQubits)
                Circuits.M -> gatesHandler.handleM(amplitudes, gate, circuit.numberOfQubits)
            }
        }

        return amplitudes
    }

    override fun simulateInPlace(circuit: QuantumCircuit): List<ComplexNumber> {
        power2Values = MathConstants.initializePower2Values(power2Values, circuit.numberOfQubits+2)

        var localAmplitudes = super.simulateInPlace(circuit)

        circuit.gates.forEach { gate ->
            localAmplitudes = when (gate.circuitType) {
                Circuits.X -> gatesHandler.handleX(localAmplitudes, gate, circuit.numberOfQubits)
                Circuits.RX -> gatesHandler.handleRX(localAmplitudes, gate, circuit.numberOfQubits)
                Circuits.CX -> gatesHandler.handleCX(localAmplitudes, gate, circuit.numberOfQubits)
                Circuits.CRX -> gatesHandler.handleCRX(localAmplitudes, gate, circuit.numberOfQubits)
                Circuits.H -> gatesHandler.handleH(localAmplitudes, gate, circuit.numberOfQubits)
                Circuits.M -> gatesHandler.handleM(localAmplitudes, gate, circuit.numberOfQubits)
            }
        }

        return localAmplitudes
    }

    override fun getProbabilities(circuit: QuantumCircuit): List<Double> {
        val amplitudes = simulate(circuit)
        return super.getProbabilities(amplitudes)
    }

    fun calculateProbabilities(circuit: QuantumCircuit, probabilities: List<Double>): List<Double> {
        return super.calculateProbabilities(simulateInPlace(circuit), probabilities)
    }

}