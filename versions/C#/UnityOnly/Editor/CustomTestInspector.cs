using UnityEngine;
using UnityEditor;


[CustomEditor(typeof(SimpleMicroQiskitTest))]
//Custom Editor for the BazeMaze class, adding some buttons and a representation of the Maze
public class CustomTestInspector : Editor {

    SimpleMicroQiskitTest targetTest;

    void OnEnable() {
        targetTest = target as SimpleMicroQiskitTest;
    }

    public override void OnInspectorGUI() {

        // Let the default inspecter draw all the values
        DrawDefaultInspector();

        // Spawn buttons

        if (GUILayout.Button("Initialize the Simulator")) {
            targetTest.SetSimulator();
        }

        if (GUILayout.Button("Initialize the test")) {
            targetTest.InitTest();
        }

        if (GUILayout.Button("Normalize")) {
            targetTest.Normalize();
        }

        if (GUILayout.Button("Start the test")) {
            targetTest.StartTest();
        }


        /*


        //if the tiles should be hidden stop here
        if (targetMaze.HideTiles) {
            return;
        }

        // Make black or red backgrounds
        Texture2D blueBack = MakeTex(1, 1, new Color(0f, 0f, 1.0f, 0.2f));
        Texture2D redBack = MakeTex(1, 1, new Color(1.0f, 0f, 0f, 0.1f));

        //Making 2 different guy styles
        GUIStyle blue = new GUIStyle(EditorStyles.textField);
        blue.normal.background = blueBack;

        GUIStyle red = new GUIStyle(EditorStyles.textField);
        red.normal.background = redBack;


        //Spawn fields to represent the Maze. Walls get blue background open places red.
        EditorGUILayout.BeginHorizontal();
        for (int x = 0; x < targetMaze.X; x++) {
            EditorGUILayout.BeginVertical();
            for (int y = 0; y < targetMaze.Y; y++) {
                if (targetMaze.Maze[x, y].Number>0) {
                    targetMaze.Maze[x, y].Number = EditorGUILayout.IntField(targetMaze.Maze[x, y].Number, blue);
                } else {
                    targetMaze.Maze[x, y].Number = EditorGUILayout.IntField(targetMaze.Maze[x, y].Number, red);
                }
            }
            EditorGUILayout.EndVertical();
        }
        EditorGUILayout.EndHorizontal();

        */
    }


    // Small helper function to make a background texture
    private Texture2D MakeTex(int width, int height, Color col) {
        Color[] pix = new Color[width * height];

        for (int i = 0; i < pix.Length; i++)
            pix[i] = col;

        Texture2D result = new Texture2D(width, height);
        result.SetPixels(pix);
        result.Apply();

        return result;
    }


}