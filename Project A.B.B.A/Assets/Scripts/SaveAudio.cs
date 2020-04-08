using System;
using System.IO;
using UnityEngine;
using System.Collections.Generic;
public class SaveAudio : MonoBehaviour
{

    AudioClip myAudioClip;
    public static int i;

    void Start() { i = 0; }
    void Update() { }
    void OnGUI()
    {
        //int i = 0;
        if (GUI.Button(new Rect(10, 10, 60, 50), "Record"))
        {
            myAudioClip = Microphone.Start(null, false, 10, 44100);
        }

        if (GUI.Button(new Rect(10, 70, 60, 50), "Save"))
        {
            //Debug.Log(Path.Combine(Application.dataPath, "myfile" + i + ".wav"));
            //Debug.Log(System.IO.File.Exists(Path.Combine(Application.dataPath, "myfile" + i + ".wav")));
            if (System.IO.File.Exists(Path.Combine(Application.dataPath, "myfile" + i +".wav")))
            {
                i += 1;
                SavWav.Save("myfile" + i, myAudioClip);
            }
            else
            {
                SavWav.Save("myfile" + i, myAudioClip);
                //audio.Play();
            }
        }
        if (GUI.Button(new Rect(10, 130, 60, 50), "Delete"))
        {
            if(i -1 > 0)
            {
                DeleteAudio(Path.Combine(Application.dataPath, "myfile" + i + ".wav"));
                i--;
            } else { i = 0; }
            
        }
    }

    void DeleteAudio(String filename)
    {
        System.IO.File.Delete(filename);
    }
}