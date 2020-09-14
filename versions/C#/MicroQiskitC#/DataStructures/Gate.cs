// -*- coding: utf-8 -*-

// This code is part of Qiskit.
//
// (C) Copyright IBM 2020.
//
// This code is licensed under the Apache License, Version 2.0. You may
// obtain a copy of this license in the LICENSE.txt file in the root directory
// of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
//
// Any modifications or derivative works of this code must retain this
// copyright notice, and modified files need to carry a notice indicating
// that they have been altered from the originals.using System;

namespace Qiskit
{
    public enum CircuitType
    {
        X,
        RX,
        H,
        CX,
        CRX,
        M,
    }

    [System.Serializable]
    //DO NOT MAKE THIS A CLASS (used for copying! (explizit values vs reference))
    public struct ComplexNumber
    {
        public double Real;
        public double Complex;
    }

    [System.Serializable]
    public class Gate
    {
        public CircuitType CircuitType;

        public int First = 0;
        public int Second = 0;

        public double Theta = 0;
    }
}