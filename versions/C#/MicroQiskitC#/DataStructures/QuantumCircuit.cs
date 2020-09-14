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
using System.Collections.Generic;
#if Unity_Editor || UNITY_STANDALONE
using UnityEngine;
#else
using System.ComponentModel;
#endif


namespace Qiskit

{

    [System.Serializable]
    public class QuantumCircuit
    {

        public int NumberOfQubits;
        public int NumberOfOutputs;
        public List<Gate> Gates;
        public ComplexNumber[] Amplitudes;
        public int AmplitudeLength;
        //public Vector2Int Dimensions;
        public string DimensionString;
        public double OriginalSum;

        public QuantumCircuit(int numberOfQuibits, int numberOfOutputs, bool initializeAmplitudes=false)
        {
            Gates = new List<Gate>();
            NumberOfQubits = numberOfQuibits;
            NumberOfOutputs = numberOfOutputs;
            AmplitudeLength = MathHelper.IntegerPower(2, NumberOfQubits);

            if (initializeAmplitudes)
            {
                Amplitudes = new ComplexNumber[AmplitudeLength];

            }
        }

        public void InitializeValues(List<double> values)
        {
            if (Amplitudes==null  || Amplitudes.Length!=AmplitudeLength)
            {
                Amplitudes = new ComplexNumber[AmplitudeLength];
            }

            if (values.Count > AmplitudeLength)
            {
                LogError("To many values " + values.Count + " while there are only " + AmplitudeLength + " qubits");
                return;
            }
            for (int i = 0; i < values.Count; i++)
            {
                Amplitudes[i].Real = values[i];
            }
        }

        public void InitializeValues(List<ComplexNumber> values)
        {
            if (Amplitudes == null || Amplitudes.Length != AmplitudeLength)
            {
                Amplitudes = new ComplexNumber[AmplitudeLength];
            }

            if (values.Count > AmplitudeLength)
            {
                LogError("To many values " + values.Count + " while there are only " + AmplitudeLength + " qubits");
                return;
            }
            for (int i = 0; i < values.Count; i++)
            {
                Amplitudes[i] = values[i];
            }
        }

        public void InitializeValues(double[] values)
        {
            if (Amplitudes == null || Amplitudes.Length != AmplitudeLength)
            {
                Amplitudes = new ComplexNumber[AmplitudeLength];
            }

            if (values.Length > AmplitudeLength)
            {
                LogError("To many values " + values.Length + " while there are only " + AmplitudeLength + " qubits");
                return;
            }
            for (int i = 0; i < values.Length; i++)
            {
                Amplitudes[i].Real = values[i];
            }
        }
        public void InitializeValues(ComplexNumber[] values)
        {
            //Amplitudes = new ComplexNumber[AmplitudeLength];

            if (values.Length > AmplitudeLength)
            {
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




        public void X(int targetQubit)
        {
            Gate gate = new Gate
            {
                CircuitType = CircuitType.X,
                First = targetQubit

            };
            Gates.Add(gate);
        }


        public void RX(int targetQubit, double rotation)
        {
            Gate gate = new Gate
            {
                CircuitType = CircuitType.RX,
                First = targetQubit,
                Theta = rotation

            };
            Gates.Add(gate);
        }

        public void H(int targetQubit)
        {
            Gate gate = new Gate
            {
                CircuitType = CircuitType.H,
                First = targetQubit

            };
            Gates.Add(gate);
        }

        public void CX(int controlQubit, int targetQubit)
        {
            Gate gate = new Gate
            {
                CircuitType = CircuitType.CX,
                First = controlQubit,
                Second = targetQubit

            };
            Gates.Add(gate);
        }

        public void CRX(int controlQubit, int targetQubit, double rotation)
        {
            Gate gate = new Gate
            {
                CircuitType = CircuitType.CRX,
                First = controlQubit,
                Second = targetQubit,
                Theta= rotation          

            };
            Gates.Add(gate);
        }

        public void Measure(int output, int qubit)
        {
            Gate gate = new Gate
            {
                CircuitType = CircuitType.M,
                First = output,
                Second = qubit

            };
            Gates.Add(gate);
        }


        public void RZ(int targetQubit, double rotation)
        {
            H(targetQubit);
            RX(targetQubit, rotation);
            H(targetQubit);
        }

        public void RY(int targetQubit, double rotation)
        {
            RX(targetQubit, MathHelper.PiHalf);
            H(targetQubit);
            RX(targetQubit, rotation);
            H(targetQubit);
            RX(targetQubit, -MathHelper.PiHalf);

        }

        public void Z(int targetQubit)
        {
            RZ(targetQubit, MathHelper.Pi);
        }

        public void Y(int targetQubit)
        {
            RZ(targetQubit, MathHelper.Pi);
            X(targetQubit);
        }

        public double ProbabilitySum()
        {
            double sum = 0;
            if (Amplitudes==null || Amplitudes.Length==0)
            {
                return 0;
            }

            for (int i = 0; i < Amplitudes.Length; i++)
            {
                sum += Amplitudes[i].Real * Amplitudes[i].Real + Amplitudes[i].Complex * Amplitudes[i].Complex;
            }
            return sum;
        }

        public void Normalize()
        {
            double sum = ProbabilitySum();
            Normalize(sum);
        }

        public void Normalize(double sum)
        {
            if (sum<MathHelper.Eps)
            {
                LogError("Sum is 0");
                return;
            }


            if (sum < 1 - MathHelper.Eps || sum > 1 + MathHelper.Eps)
            {
                OriginalSum = sum;
                sum = Math.Sqrt(sum);

                for (int i = 0; i < Amplitudes.Length; i++)
                {
                    Amplitudes[i].Real /= sum;
                    Amplitudes[i].Complex /= sum;

                }
            }
        }


        public List<List<double>> GetAmplitudeList()
        {
            List<List<double>> returnValue = new List<List<double>>();

            for (int i = 0; i < Amplitudes.Length; i++)
            {
                List<double> amplitude = new List<double>();
                amplitude.Add(Amplitudes[i].Real);
                amplitude.Add(Amplitudes[i].Complex);
                returnValue.Add(amplitude);
            }

            return returnValue;
        }

        public string GetQiskitString()
        {
            string translation = "";

            if (NumberOfOutputs == 0)
            {
                translation += "qc = QuantumCircuit(" + NumberOfQubits + ")\n";

            }
            else
            {
                translation += "qc = QuantumCircuit(" + NumberOfQubits + "," + NumberOfOutputs + ")\n";
            }

            for (int i = 0; i < Gates.Count; i++)
            {
                Gate gate = Gates[i];
                switch (gate.CircuitType)
                {
                    case CircuitType.X:
                        translation += "qc.x(" + gate.First + ")\n";
                        break;
                    case CircuitType.RX:
                        translation += "qc.rx(" + gate.Theta + "," + gate.First + ")\n";
                        break;
                    case CircuitType.H:
                        translation += "qc.h(" + gate.First + ")\n";
                        break;
                    case CircuitType.CX:
                        translation += "qc.cx(" + gate.First + "," + gate.Second + ")\n";
                        break;
                    case CircuitType.M:
                        translation += "qc.measure(" + gate.First + "," + gate.Second + ")\n";
                        break;
                    default:
                        break;
                }
            }

            return translation;
        }

        public void AddCircuit(QuantumCircuit circuit)
        {
            if (circuit.NumberOfQubits > NumberOfQubits)
            {
                LogWarning("Number of qubits is bigger " + circuit.NumberOfQubits + " vs " + NumberOfQubits);
                NumberOfQubits = circuit.NumberOfQubits;
                ComplexNumber[] newQubits = new ComplexNumber[NumberOfQubits];
                for (int i = 0; i < Amplitudes.Length; i++)
                {
                    newQubits[i] = Amplitudes[i];
                }
                for (int i = Amplitudes.Length; i < NumberOfQubits; i++)
                {
                    newQubits[i] = circuit.Amplitudes[i];
                }
            }
            //TODO different behavious when other is smaller?
            Gates.AddRange(circuit.Gates);
        }

        void LogError(string errorMessage)
        {
#if Unity_Editor || UNITY_STANDALONE
            Debug.LogError(errorMessage);
#else
            throw new Exception(errorMessage);
#endif
        }

        void LogWarning(string errorMessage)
        {
#if Unity_Editor || UNITY_STANDALONE
            Debug.LogWarning(errorMessage);
#else
            WarningException myEx = new WarningException(errorMessage);
            Console.Write(myEx.ToString());
#endif
        }

    }

}