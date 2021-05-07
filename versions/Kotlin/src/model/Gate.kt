package model

data class Gate(
    val circuitType: Circuits,
    val first: Int,
    val second: Int? = null,
    val theta: Double? = null,
)
