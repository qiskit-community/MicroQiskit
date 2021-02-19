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
// that they have been altered from the originals.

using System;
using System.Collections.Generic;
using System.Text;
#if Unity_Editor || UNITY_STANDALONE
using UnityEngine;
#else
using System.ComponentModel;
#endif

namespace Qiskit {

    [System.Serializable]
    public class QuantumCircuit {

        public int NumberOfQubits;
        public int NumberOfOutputs;
        public List<Gate> Gates;
        public ComplexNumber[] Amplitudes;
#if Unity_Editor
        [HideInInspector]
#endif
        public int AmplitudeLength;
        //public Vector2Int Dimensions;
#if Unity_Editor
        [HideInInspector]
#endif       
        public string DimensionString;
#if Unity_Editor
        [HideInInspector]
#endif        
        public double OriginalSum = 0;

        public QuantumCircuit(int numberOfQuibits, int numberOfOutputs, bool initializeAmplitudes = false) {
            Gates = new List<Gate>();
            NumberOfQubits = numberOfQuibits;
            NumberOfOutputs = numberOfOutputs;
            AmplitudeLength = MathHelper.IntegerPower(2, NumberOfQubits);

            if (initializeAmplitudes) {
                Amplitudes = new ComplexNumber[AmplitudeLength];

            }
        }

        public void InitializeValues(List<double> values) {
            if (Amplitudes == null || Amplitudes.Length != AmplitudeLength) {
                Amplitudes = new ComplexNumber[AmplitudeLength];
            }

            if (values.Count > AmplitudeLength) {
                LogError("To many values " + values.Count + " while there are only " + AmplitudeLength + " qubits");
                return;
            }
            for (int i = 0; i < values.Count; i++) {
                Amplitudes[i].Real = values[i];
            }
        }

        public void InitializeValues(List<ComplexNumber> values) {
            if (Amplitudes == null || Amplitudes.Length != AmplitudeLength) {
                Amplitudes = new ComplexNumber[AmplitudeLength];
            }

            if (values.Count > AmplitudeLength) {
                LogError("To many values " + values.Count + " while there are only " + AmplitudeLength + " qubits");
                return;
            }
            for (int i = 0; i < values.Count; i++) {
                Amplitudes[i] = values[i];
            }
        }

        public void InitializeValues(double[] values) {
            if (Amplitudes == null || Amplitudes.Length != AmplitudeLength) {
                Amplitudes = new ComplexNumber[AmplitudeLength];
            }

            if (values.Length > AmplitudeLength) {
                LogError("To many values " + values.Length + " while there are only " + AmplitudeLength + " qubits");
                return;
            }
            for (int i = 0; i < values.Length; i++) {
                Amplitudes[i].Real = values[i];
            }
        }
        public void InitializeValues(ComplexNumber[] values) {
            //Amplitudes = new ComplexNumber[AmplitudeLength];

            if (values.Length > AmplitudeLength) {
                LogError("To many values " + values.Length + " while there are only " + AmplitudeLength + " qubits");
                return;
            }

            /*
            for (int i = 0; i < values.Length; i++)
            {
                Amplitudes[i] = values[i];
            }
            */
            Amplitudes = values;
        }

        public void X(int targetQubit) {
            Gate gate = new Gate {
                CircuitType = CircuitType.X,
                First = targetQubit

            };
            Gates.Add(gate);
        }


        public void RX(int targetQubit, double rotation) {
            Gate gate = new Gate {
                CircuitType = CircuitType.RX,
                First = targetQubit,
                Theta = rotation

            };
            Gates.Add(gate);
        }

        public void H(int targetQubit) {
            Gate gate = new Gate {
                CircuitType = CircuitType.H,
                First = targetQubit

            };
            Gates.Add(gate);
        }

        public void CX(int controlQubit, int targetQubit) {
            Gate gate = new Gate {
                CircuitType = CircuitType.CX,
                First = controlQubit,
                Second = targetQubit

            };
            Gates.Add(gate);
        }

        public void CRX(int controlQubit, int targetQubit, double rotation) {
            Gate gate = new Gate {
                CircuitType = CircuitType.CRX,
                First = controlQubit,
                Second = targetQubit,
                Theta = rotation

            };
            Gates.Add(gate);
        }

        public void Measure(int output, int qubit) {
            Gate gate = new Gate {
                CircuitType = CircuitType.M,
                First = output,
                Second = qubit

            };
            Gates.Add(gate);
        }

        public void RZ(int targetQubit, double rotation) {
            H(targetQubit);
            RX(targetQubit, rotation);
            H(targetQubit);
        }

        public void RY(int targetQubit, double rotation) {
            RX(targetQubit, MathHelper.PiHalf);
            H(targetQubit);
            RX(targetQubit, rotation);
            H(targetQubit);
            RX(targetQubit, -MathHelper.PiHalf);

        }

        public void Z(int targetQubit) {
            RZ(targetQubit, MathHelper.Pi);
        }

        public void Y(int targetQubit) {
            RZ(targetQubit, MathHelper.Pi);
            X(targetQubit);
        }

        public void ResetGates() {
            Gates.Clear();
        }

        public double ProbabilitySum() {
            double sum = 0;
            if (Amplitudes == null || Amplitudes.Length == 0) {
                return 0;
            }

            for (int i = 0; i < Amplitudes.Length; i++) {
                sum += Amplitudes[i].Real * Amplitudes[i].Real + Amplitudes[i].Complex * Amplitudes[i].Complex;
            }
            return sum;
        }

        public void Normalize() {
            double sum = ProbabilitySum();
            //Debug.Log(sum);
            Normalize(sum);
        }

        public void Normalize(double sum) {
            if (sum < MathHelper.Eps) {
                LogError("Sum is 0 " + sum);
                return;
            }

            if (sum < 1 - MathHelper.Eps || sum > 1 + MathHelper.Eps) {
                //This can happen for really large inputs due to rounding errors.
                if (OriginalSum == 0) {
                    OriginalSum = sum;
                } else {
                    OriginalSum *= sum;
                }
                sum = Math.Sqrt(sum);

                for (int i = 0; i < Amplitudes.Length; i++) {
                    Amplitudes[i].Real /= sum;
                    Amplitudes[i].Complex /= sum;

                }
            }
        }

        public List<List<double>> GetAmplitudeList() {
            List<List<double>> returnValue = new List<List<double>>();

            for (int i = 0; i < Amplitudes.Length; i++) {
                List<double> amplitude = new List<double>();
                amplitude.Add(Amplitudes[i].Real);
                amplitude.Add(Amplitudes[i].Complex);
                returnValue.Add(amplitude);
            }

            return returnValue;
        }

        public string GetQiskitString(bool includeAllMeasures = false) {

            //todo use correct number
            StringBuilder builder = new StringBuilder();


            //string translation = "";

            string allnumbers = getAllNumbersString(NumberOfQubits);

            if (NumberOfOutputs == 0) {
                //translation += "qc = QuantumCircuit(" + NumberOfQubits + ")\n";
                builder.Append("qc = QuantumCircuit(");
                builder.Append(NumberOfQubits);
                builder.Append(")\n");


            } else {
                //translation += "qc = QuantumCircuit(" + NumberOfQubits + "," + NumberOfOutputs + ")\n";
                builder.Append("qc = QuantumCircuit(");
                builder.Append(NumberOfQubits);
                builder.Append(",");
                builder.Append(NumberOfOutputs);
                builder.Append(")\n");
            }

            if (Amplitudes != null && Amplitudes.Length > 0 && OriginalSum > 0) {

                //hack only possible because the Amplitudes.ToString() only gives the Real values.
                //This makes this quite a bit faster though.
                string amplitudes = string.Join(",", Amplitudes);

                //string state = "[" + amplitudes + "]";                
                //translation += "qc.initialize(" + state + ", " + allnumbers + ")\n";

                builder.Append("qc.initialize([");
                builder.Append(amplitudes);
                builder.Append("],");
                builder.Append(allnumbers);
                builder.Append(")\n");

                /*
                state += Amplitudes[0].Real;

                for (int i = 1; i < AmplitudeLength; i++) {
                    state += "," + Amplitudes[i].Real;                    
                }     
                state += "]"; 
                */
            }

            for (int i = 0; i < Gates.Count; i++) {
                Gate gate = Gates[i];
                switch (gate.CircuitType) {
                    case CircuitType.X:
                        //translation += "qc.x(" + gate.First + ")\n";
                        builder.Append("qc.x(");
                        builder.Append(gate.First);
                        builder.Append(")\n");
                        break;
                    case CircuitType.RX:
                        //translation += "qc.rx(" + gate.Theta + "," + gate.First + ")\n";
                        builder.Append("qc.rx(");
                        builder.Append(gate.Theta);
                        builder.Append(", ");
                        builder.Append(gate.First);
                        builder.Append(")\n");
                        break;
                    case CircuitType.H:
                        //translation += "qc.h(" + gate.First + ")\n";
                        builder.Append("qc.h(");
                        builder.Append(gate.First);
                        builder.Append(", ");
                        builder.Append(gate.Second);
                        builder.Append(")\n");
                        break;
                    case CircuitType.CX:
                        //translation += "qc.cx(" + gate.First + "," + gate.Second + ")\n";
                        builder.Append("qc.cx(");
                        builder.Append(gate.First);
                        builder.Append(", ");
                        builder.Append(gate.Second);
                        builder.Append(")\n");
                        break;
                    case CircuitType.CRX:
                        //TODO using uniform
                        /*                         
        U = np.array([
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
        ])
        U = fractional_matrix_power(U,fraction)
            combined_qc.unitary(U, [q0,q1],\
                                 label='partial_swap')
                        */

                        /*
                        builder.Append("qc.crx(");
                        builder.Append(gate.Theta);
                        builder.Append(", ");
                        builder.Append(gate.First);
                        builder.Append(", ");
                        builder.Append(gate.Second);
                        builder.Append(")\n");
                        */
                        break;
                    case CircuitType.M:
                        //translation += "qc.measure(" + gate.First + "," + gate.Second + ")\n";
                        builder.Append("qc.measure(");
                        builder.Append(gate.First);
                        builder.Append(", ");
                        builder.Append(gate.Second);
                        builder.Append(")\n");
                        break;
                    default:
                        break;
                }
            }

            if (includeAllMeasures) {
                /*
                string allQubits = "0";
                for (int i = 1; i < NumberOfQubits && i<NumberOfOutputs; i++) {
                    allQubits += "," + i;
                }
                translation += "qc.measure([" + allQubits + "], [" + allQubits + "])\n";
                */


                //translation += "qc.measure(" + allnumbers + ", " + allnumbers + ")\n";


                builder.Append("qc.measure(");
                builder.Append(allnumbers);
                builder.Append(", ");
                builder.Append(allnumbers);
                builder.Append(")\n");

            }

            return builder.ToString();

            //return translation;
        }


        string getAllNumbersString(int length) {

            StringBuilder builder = new StringBuilder(2 * length + 2);


            //Generating an int array and transform the whole array into string,
            //This makes the string construction faster with the join.
            int[] numbers = new int[length];
            for (int i = 0; i < length; i++) {
                numbers[i] = i;
            }
            string numberString = string.Join(",", numbers);

            builder.Append("[");
            builder.Append(numberString);
            builder.Append("]");

            string output = builder.ToString();

            //string output = "["+ numberString+"]";

            return output;
            /*
            output += "0";
            for (int i = 1; i < NumberOfQubits && i < NumberOfOutputs; i++) {
                output += "," + i;
            }
            output += "]";
            return output;
            */
        }

        public void AddCircuit(QuantumCircuit circuit) {
            if (circuit.NumberOfQubits > NumberOfQubits) {
                LogWarning("Number of qubits is bigger " + circuit.NumberOfQubits + " vs " + NumberOfQubits);
                NumberOfQubits = circuit.NumberOfQubits;
                ComplexNumber[] newQubits = new ComplexNumber[NumberOfQubits];
                for (int i = 0; i < Amplitudes.Length; i++) {
                    newQubits[i] = Amplitudes[i];
                }
                for (int i = Amplitudes.Length; i < NumberOfQubits; i++) {
                    newQubits[i] = circuit.Amplitudes[i];
                }
            }
            //TODO different behavious when other is smaller?
            Gates.AddRange(circuit.Gates);
        }

        void LogError(string errorMessage) {
#if Unity_Editor || UNITY_STANDALONE
            Debug.LogError(errorMessage);
#else
            throw new Exception(errorMessage);
#endif
        }

        void LogWarning(string errorMessage) {
#if Unity_Editor || UNITY_STANDALONE
            Debug.LogWarning(errorMessage);
#else
            WarningException myEx = new WarningException(errorMessage);
            Console.Write(myEx.ToString());
#endif
        }

    }

}