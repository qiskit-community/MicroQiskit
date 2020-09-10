
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

using System;

namespace Qiskit
{
    /// <summary>
    /// Class to simulate a Quantum Circuit directly in C# same way as MicroQiskit does
    /// Uses basic constructor is not static in order to easy change simulators (Inheriting from SimulatorBase)
    /// </summary>
    public class MicroQiskitSimulator : SimulatorBase
    {
        /// <summary>
        /// Calculate the amplitude for a given circuit by simulating it directly in C#
        /// </summary>
        /// <param name="circuit">The quantum circuit which will be simulated</param>
        /// <returns></returns>
        public override ComplexNumber[] Simulate(QuantumCircuit circuit)
        {
            ComplexNumber[] amplitudes = base.Simulate(circuit);


            for (int i = 0; i < circuit.Gates.Count; i++)
            {
                Gate gate = circuit.Gates[i];

                switch (gate.CircuitType)
                {
                    case CircuitType.X:
                        handleX(amplitudes, gate, circuit.NumberOfQubits);
                        break;
                    case CircuitType.RX:
                        handleRX(amplitudes, gate, circuit.NumberOfQubits);
                        break;
                    case CircuitType.H:
                        handleH(amplitudes, gate, circuit.NumberOfQubits);
                        break;
                    case CircuitType.CX:
                        handleCX(amplitudes, gate, circuit.NumberOfQubits);
                        break;
                    case CircuitType.CRX:
                        handleCRX(amplitudes, gate, circuit.NumberOfQubits);
                        break;
                    case CircuitType.M:
                        handleM(amplitudes, gate, circuit.NumberOfQubits);
                        break;
                    default:
                        break;
                }

            }

            return amplitudes;

        }


        public override void SilumateInPlace(QuantumCircuit circuit, ref ComplexNumber[] amplitudes)
        {
            //Check Length
            base.SilumateInPlace(circuit, ref amplitudes);

            for (int i = 0; i < circuit.Gates.Count; i++)
            {
                Gate gate = circuit.Gates[i];

                switch (gate.CircuitType)
                {
                    case CircuitType.X:
                        handleX(amplitudes, gate, circuit.NumberOfQubits);
                        break;
                    case CircuitType.RX:
                        handleRX(amplitudes, gate, circuit.NumberOfQubits);
                        break;
                    case CircuitType.H:
                        handleH(amplitudes, gate, circuit.NumberOfQubits);
                        break;
                    case CircuitType.CX:
                        handleCX(amplitudes, gate, circuit.NumberOfQubits);
                        break;
                    case CircuitType.CRX:
                        handleCRX(amplitudes, gate, circuit.NumberOfQubits);
                        break;
                    case CircuitType.M:
                        handleM(amplitudes, gate, circuit.NumberOfQubits);
                        break;
                    default:
                        break;
                }

            }
        }


        /// <summary>
        /// Getting the probabilities of outcomes for a given circuit by simulating it.
        /// </summary>
        /// <param name="circuit">The quantum circuit which will be simulated.</param>
        /// <returns></returns>
        public override double[] GetProbabilities(QuantumCircuit circuit)
        {
            ComplexNumber[] amplitudes = Simulate(circuit);
            return base.GetProbabilities(amplitudes);
        }


        /// <summary>
        /// Getting the probabilities of outcomes for a given circuit by simulating it.
        /// </summary>
        /// <param name="circuit">The quantum circuit which will be simulated.</param>
        /// <param name="probabilities">The probability array which will be filled.</param>
        /// <param name="amplitudes">The amplitude array needed for calculating the probabilities.</param>
        /// <returns></returns>
        public void CalculateProbabilities(QuantumCircuit circuit, ref double[] probabilities, ref ComplexNumber[] amplitudes)
        {
            //Trying to optimize not needing to return arrays
            SilumateInPlace(circuit, ref amplitudes);
            base.CalculateProbabilities(amplitudes, ref probabilities);
        }


        void handleX(ComplexNumber[] amplitudes, Gate gate, int numberOfQubits)
        {
            int first = gate.First;
            int firstPow = MathHelper.IntegerPower(2, first);
            int firstPlusPow = MathHelper.IntegerPower(2, first + 1);
            int opposingPow = MathHelper.IntegerPower(2, numberOfQubits - first - 1);

            for (int i = 0; i < firstPow; i++)
            {
                for (int j = 0; j < opposingPow; j++)
                {
                    int pos1 = i + firstPlusPow * j;
                    int pos2 = pos1 + firstPow;

                    ComplexNumber old = amplitudes[pos1];
                    amplitudes[pos1] = amplitudes[pos2];
                    amplitudes[pos2] = old;

                }
            }
        }

        void handleRX(ComplexNumber[] amplitudes, Gate gate, int numberOfQubits)
        {
            int first = gate.First;
            int firstPow = MathHelper.IntegerPower(2, first);
            int firstPlusPow = MathHelper.IntegerPower(2, first + 1);
            int opposingPow = MathHelper.IntegerPower(2, numberOfQubits - first - 1);

            double theta = gate.Theta;
            double cosTheta = Math.Cos(theta / 2);
            double sinTheta = Math.Sin(theta / 2);

            for (int i = 0; i < firstPow; i++)
            {
                for (int j = 0; j < opposingPow; j++)
                {
                    int pos1 = i + firstPlusPow * j;
                    int pos2 = pos1 + firstPow;

                    ComplexNumber p1 = amplitudes[pos1];
                    ComplexNumber p2 = amplitudes[pos2];

                    amplitudes[pos1].Real = p1.Real * cosTheta + p2.Complex * sinTheta;
                    amplitudes[pos1].Complex = p1.Complex * cosTheta - p2.Real * sinTheta;
                    amplitudes[pos2].Real = p2.Real * cosTheta + p1.Complex * sinTheta;
                    amplitudes[pos2].Complex = p2.Complex * cosTheta - p1.Real * sinTheta;

                }
            }
        }

        void handleCX(ComplexNumber[] amplitudes, Gate gate, int numberOfQubits)
        {
            int first = gate.First;
            int second = gate.Second;

            int loop1 = first;
            int loop2 = second;

            if (second < first)
            {
                loop1 = second;
                loop2 = first;
            }


            int pow1 = MathHelper.IntegerPower(2, loop1);
            int pow2 = MathHelper.IntegerPower(2, loop2 - loop1 - 1);
            int pow3 = MathHelper.IntegerPower(2, numberOfQubits - loop2 - 1);

            int pow1Plus = MathHelper.IntegerPower(2, loop1 + 1);
            int pow2Plus = MathHelper.IntegerPower(2, loop2 + 1);

            int firstPow = MathHelper.IntegerPower(2, first);
            int secondPow = MathHelper.IntegerPower(2, second);

            for (int i = 0; i < pow1; i++)
            {
                for (int j = 0; j < pow2; j++)
                {
                    for (int k = 0; k < pow3; k++)
                    {
                        int pos1 = i + pow1Plus * j + pow2Plus * k + firstPow;
                        int pos2 = pos1 + secondPow;

                        ComplexNumber old = amplitudes[pos1];
                        amplitudes[pos1] = amplitudes[pos2];
                        amplitudes[pos2] = old;

                    }
                }
            }
        }

        void handleH(ComplexNumber[] amplitudes, Gate gate, int numberOfQubits)
        {
            int first = gate.First;
            int firstPow = MathHelper.IntegerPower(2, first);
            int firstPlusPow = MathHelper.IntegerPower(2, first + 1);
            int opposingPow = MathHelper.IntegerPower(2, numberOfQubits - first - 1);

            double theta = gate.Theta;

            for (int i = 0; i < firstPow; i++)
            {
                for (int j = 0; j < opposingPow; j++)
                {
                    int pos1 = i + firstPlusPow * j;
                    int pos2 = pos1 + firstPow;

                    ComplexNumber p1 = amplitudes[pos1];
                    ComplexNumber p2 = amplitudes[pos2];

                    amplitudes[pos1].Real = (p1.Real + p2.Real) * MathHelper.Norm2;
                    amplitudes[pos1].Complex = (p1.Complex + p2.Complex) * MathHelper.Norm2;
                    amplitudes[pos2].Real = (p1.Real - p2.Real) * MathHelper.Norm2;
                    amplitudes[pos2].Complex = (p1.Complex - p2.Complex) * MathHelper.Norm2;

                }
            }
        }



        void handleCRX(ComplexNumber[] amplitudes, Gate gate, int numberOfQubits)
        {
            int first = gate.First;
            int second = gate.Second;

            int loop1 = first;
            int loop2 = second;

            double theta = gate.Theta;
            double cosTheta = Math.Cos(theta / 2);
            double sinTheta = Math.Sin(theta / 2);

            if (second < first)
            {
                loop1 = second;
                loop2 = first;
            }


            int pow1 = MathHelper.IntegerPower(2, loop1);
            int pow2 = MathHelper.IntegerPower(2, loop2 - loop1 - 1);
            int pow3 = MathHelper.IntegerPower(2, numberOfQubits - loop2 - 1);

            int pow1Plus = MathHelper.IntegerPower(2, loop1 + 1);
            int pow2Plus = MathHelper.IntegerPower(2, loop2 + 1);

            int firstPow = MathHelper.IntegerPower(2, first);
            int secondPow = MathHelper.IntegerPower(2, second);

            for (int i = 0; i < pow1; i++)
            {
                for (int j = 0; j < pow2; j++)
                {
                    for (int k = 0; k < pow3; k++)
                    {
                        int pos1 = i + pow1Plus * j + pow2Plus * k + firstPow;
                        int pos2 = pos1 + secondPow;

                        ComplexNumber p1 = amplitudes[pos1];
                        ComplexNumber p2 = amplitudes[pos2];

                        amplitudes[pos1].Real = p1.Real * cosTheta + p2.Complex * sinTheta;
                        amplitudes[pos1].Complex = p1.Complex * cosTheta - p2.Real * sinTheta;
                        amplitudes[pos2].Real = p2.Real * cosTheta + p1.Complex * sinTheta;
                        amplitudes[pos2].Complex = p2.Complex * cosTheta - p1.Real * sinTheta;


                    }
                }
            }
        }

        void handleM(ComplexNumber[] amplitudes, Gate gate, int numberOfQubits)
        {
            //Todo
        }


    }
}