import model.QuantumCircuit
import simulator.MicroQiskitSimulator
import util.MathConstants

fun main() {
    val qc = QuantumCircuit(2, 2)
    val simulator = MicroQiskitSimulator()

//    qc.x(1)
    qc.rx( 0, MathConstants.PiQuarter)
    qc.rx( 1, MathConstants.PiQuarter/2)
    qc.h(0)
    qc.h(1)
//    qc.x(1)

//    qc.y(0)
//    qc.z(0)
//    qc.rx(0, MathConstants.PiHalf)
//    qc.ry(0, MathConstants.PiHalf)
//    qc.rz(0, MathConstants.PiHalf)
//    qc.crx(0, 1, MathConstants.PiHalf)
//    qc.measure(0, 0)

    val result = simulator.simulate(qc)
    println(result)
//    qc.normalize()
//    print(qc.getQiskitString())
//    print(qc.getAmplitudeList())
}
