
namespace Qiskit
{
    //Simple Helper functions for math.
    public static class MathHelper
    {
        //Constants (potential) used
        public const double Pi = 3.1415926535897932384626433832795;
        public const double PiHalf = 1.5707963267948966192313216916398;
        public const double PiQuarter = 0.78539816339744830961566084581988;
        public const double Norm2 = 0.70710678118654752440084436210485;
        public const double Eps = 0.0000001;


        /// <summary>
        /// Fast Integer potency. Only works with positive numbers Returns baseValue to the power of powerValue
        /// </summary>
        /// <param name="baseValue"> The base </param>
        /// <param name="powerValue">The exponent </param>
        /// <returns></returns>
        public static int IntegerPower(int baseValue, int powerValue)
        {
            int returnValue = 1;
            while (powerValue != 0)
            {
                if ((powerValue & 1) == 1)
                {
                    returnValue *= baseValue;
                }
                baseValue *= baseValue;
                powerValue >>= 1;
            }
            return returnValue;
        }

    }
}
