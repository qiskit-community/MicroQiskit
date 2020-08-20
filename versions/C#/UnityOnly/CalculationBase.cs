using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CalculationBase : MonoBehaviour
{

    //[HideInInspector]
    public double[] Probabilities;

    [HideInInspector]
    public int QubitCount;

    [HideInInspector]
    public Action CalculationFinished;

    public virtual void Calculate()
    {

        if (CalculationFinished!=null)
        {
            CalculationFinished.Invoke();
        }
    }

}
