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



namespace Qiskit {
    public class SimulatorBase {
        public virtual ComplexNumber[] Simulate(QuantumCircuit circuit) {

            double sum = circuit.ProbabilitySum();

            if (sum > MathHelper.Eps) {
                if (sum < 1 - MathHelper.Eps || sum > 1 + MathHelper.Eps) {
                    circuit.Normalize(sum);
                }

                ComplexNumber[] amplitudes = new ComplexNumber[circuit.AmplitudeLength];

                for (int i = 0; i < amplitudes.Length; i++) {
                    amplitudes[i] = circuit.Amplitudes[i];
                }
                return amplitudes;
            } else {
                //Initialize the all 0 vector
                ComplexNumber[] amplitudes = new ComplexNumber[circuit.AmplitudeLength];
                amplitudes[0].Real = 1;
                return amplitudes;
            }

        }


        public virtual void SimulateInPlace(QuantumCircuit circuit, ref ComplexNumber[] amplitudes) {
            int length = circuit.AmplitudeLength;
            if (amplitudes == null || amplitudes.Length != length) {
                //Post message
                amplitudes = new ComplexNumber[length];
            }

            double sum = circuit.ProbabilitySum();

            //if
            if (sum > MathHelper.Eps) {
                if (sum < 1 - MathHelper.Eps || sum > 1 + MathHelper.Eps) {
                    circuit.Normalize(sum);
                }

                for (int i = 0; i < amplitudes.Length; i++) {
                    amplitudes[i] = circuit.Amplitudes[i];
                }
            } else {
                //Initialize the all 0 vector
                amplitudes[0].Real = 1;
            }
        }


        public virtual double[] GetProbabilities(QuantumCircuit circuit) {
            //Doing nothing just preparing an array
            double[] probabilities = new double[MathHelper.IntegerPower(2, circuit.NumberOfQubits)];
            return probabilities;
        }


        public virtual double[] GetProbabilities(ComplexNumber[] amplitudes) {
            //Calculating the probability from the amplitudes
            double[] probabilities = new double[amplitudes.Length];

            for (int i = 0; i < probabilities.Length; i++) {
                probabilities[i] = amplitudes[i].Real * amplitudes[i].Real + amplitudes[i].Complex * amplitudes[i].Complex;
            }

            return probabilities;
        }

        public virtual void CalculateProbabilities(ComplexNumber[] amplitudes, ref double[] probabilities) {
            if (probabilities == null || probabilities.Length != amplitudes.Length) {
                //Throw a message
                probabilities = new double[amplitudes.Length];
            }

            //Calculating the probability from the amplitudes
            for (int i = 0; i < probabilities.Length; i++) {
                probabilities[i] = amplitudes[i].Real * amplitudes[i].Real + amplitudes[i].Complex * amplitudes[i].Complex;
            }

        }

    }
}