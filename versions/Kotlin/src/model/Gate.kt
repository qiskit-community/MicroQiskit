package model

import util.Circuits

data class Gate(
    val circuitType: Circuits,
    val targetQubit: Int,
    val controlQubit: Int? = null,
    val theta: Double? = null,
)
