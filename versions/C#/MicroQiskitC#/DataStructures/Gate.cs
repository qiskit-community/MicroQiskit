namespace Qiskit
{
    //Todo Give better names?
    public enum CircuitType
    {
        X,
        RX,
        H,
        CX,
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