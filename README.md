**Data Flow and Process of the Project**

## **Involved Devices**
- **Pepper**: Humanoid robot for interaction and audio/video data acquisition, equipped with microphones and a camera for facial expression and voice tone analysis.
- **Emotiv Epoc X**: EEG sensor for brain data acquisition, capable of detecting emotional states by reading brain waves.
- **Device 1 (Ubuntu 14.04LTS)**: Main server managing data processing and emotion prediction.
- **Device 2 (macOS)**: Used to manage EEG acquisition via the Emotiv APP and transfer data to the main server.

---

## **Process Phases**

### **0. Connection and Startup**
1. **Powering up Pepper** and connecting it to Device 1 via a local network for data transmission.
2. **User preparation:** correctly positioning the Emotiv Epoc X headset on the user's head to ensure accurate EEG readings.
3. **Starting the EEG session** on Device 2, which begins real-time brain data collection.
4. **Initial interaction:** Pepper asks the user how they feel, recording the response through audio and video.
5. **Processing delay:** a short pause is introduced to allow data transmission and emotion prediction.

---

### **1. Data Acquisition Phase**
#### **EEG Data:**
- Collected by the Emotiv Epoc X headset and managed via the Emotiv APP on Device 2.
- Transferred to Device 1 using the SCP protocol for secure and reliable connection.

#### **Audio/Video Data:**
- **Pepper uses its camera** to record the user's facial expressions and microphone to analyze voice tone.
- Data is stored locally on Pepper.
- Through a TCP connection, Pepper sends the data to Device 1 for processing.

---

### **2. Processing and Final Prediction**
1. **Data preprocessing:** EEG, audio, and video data are converted into formats compatible with training datasets:
   - **RAVDESS** for audio/video data (emotion recognition from voice and facial expressions).
   - **SEED-IV** for EEG data (brainwave analysis for emotion recognition).
2. **Emotion prediction:** preprocessed data is fed into the classification model, which generates an output among the four emotional classes:
   - **Angry**
   - **Sad**
   - **Happy**
   - **Neutral**
3. **Execution on Device 1:** the entire processing workflow occurs locally to ensure speed and security in handling sensitive data.

---

### **3. Human-Machine Interaction**
Based on the classification output, Pepper adopts specific interaction strategies to improve the user's emotional well-being:

- **Sad:**
  - Pepper provides a selection of jokes and light-hearted stories to entertain the user.
  - If sadness persists, it can offer a short motivational story.
- **Angry:**
  - Suggests a guided meditation session (short or long) with breathing exercises.
  - Can play relaxing sounds such as ocean waves or rainfall to promote relaxation.
- **Happy:**
  - Reinforces positive emotions through music and dance.
  - Pepper performs specific movements synchronized with the user's chosen music.
- **Neutral:**
  - The user can choose from three options:
    1. Jokes and entertainment.
    2. Meditation.
    3. Music and dance.
    4. Interactive quiz using a tablet (to be implemented).

---

### **4. Process Repetition (Optional)**
- After the interaction, the user can choose to repeat the process to assess the effect of their engagement with Pepper.
- A new EEG and audio/video acquisition is performed to analyze emotional state variations.
- Data is saved and compared with the previous prediction to monitor the system’s effectiveness in improving user well-being.

---

## **Conclusion**
This system integrates advanced technologies for emotion acquisition and analysis, offering an adaptive and personalized interaction. Through a continuous learning cycle, Pepper adapts to user needs, progressively improving interaction quality and promoting emotional well-being.

