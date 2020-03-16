using UnityEngine;

public class Example : MonoBehaviour
{
    // Start recording with built-in Microphone and play the recorded audio right away
    void Start()
    {
        AudioSource audioSource = GetComponent<AudioSource>();
        audioSource.clip = Microphone.Start(null, true, 10, 44100);
        while (!(Microphone.GetPosition(null) > 0)) { }
        audioSource.Play();
    }
}