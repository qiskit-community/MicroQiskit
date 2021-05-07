package model

import kotlin.math.abs

data class ComplexNumber(
    var real: Double,
    var complex: Double
) {
    override fun toString(): String {
        return if (complex >= 0) "$real + $complex i" else "$real - ${abs(complex)} i"
    }
}
