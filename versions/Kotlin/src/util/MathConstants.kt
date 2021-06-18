package util

import kotlin.math.pow

object MathConstants {

    const val Pi: Double = 3.1415926535897932384626433832795
    const val PiHalf: Double = 1.5707963267948966192313216916398
    const val PiQuarter: Double = 0.78539816339744830961566084581988

    const val Norm2: Double = 0.5//0.70710678118654752440084436210485
    const val Eps: Double = 0.0000001

    fun initializePower2Values(power2Values: List<Int>, number: Int = 20): List<Int> {
        val localPower2Values = arrayListOf<Int>()
        if(power2Values.size >= number) {
            return emptyList()
        }

        power2Values.forEachIndexed { index, _ ->
            localPower2Values[index] = 2.0.pow(index).toInt()
        }

        return localPower2Values
    }

}