# HeartTrack (HTK) – Real-Time Cardiovascular Monitoring Device  

## Description  
**HeartTrack (HTK)** is an innovative device designed for real-time cardiovascular health monitoring. The project integrates the **AD8232 ECG sensor** to detect the heart's electrical activity and the **MAX30102 Pulse Oximeter** to measure blood oxygen levels (SpO₂). The device provides comprehensive analysis of heart rhythm and oxygenation, identifying anomalies such as arrhythmias, tachycardia, bradycardia, or early signs of myocardial infarction.  

## Key Features  
- **ECG Monitoring**: Detects cardiac abnormalities by analyzing the heart's electrical signals.  
- **Pulse Oximetry**: Measures blood oxygen saturation (SpO₂) and identifies associated risks.  
- **Automated Alerts**: Sends email notifications if abnormal values are detected.  
- **Portability**: Compact and user-friendly design, suitable for patients, athletes, or anyone monitoring their heart health.  
- **User-Friendly Interface**: Dual-screen display and simple button navigation.  

## Components & Technologies  
- **Hardware**:  
  - Raspberry Pi 4 and Raspberry Pi Pico for processing.  
  - AD8232 ECG sensor and MAX30102 Pulse Oximeter.  
  - Display screens, buttons, vibration sensor, and buzzer.  
- **Software**:  
  - Advanced algorithms for detecting P, Q, R, S, T points and ST segment.  
  - Neurokit2 library for ECG data processing.  
  - Threshold-based alert system.  

## Objectives  
- Preventing cardiovascular diseases through early diagnosis.  
- Providing an accessible and easy-to-use device for daily monitoring.  
- Improving quality of life through rapid intervention in case of anomalies.  

## Future Improvements  
- Developing a mobile app for real-time monitoring and notifications.  
- Enhancing the design for a more compact and comfortable experience.  
- Implementing automatic data transmission to healthcare providers.  

## Project Team  
- **Former Members**:  
  - Stamate Narcis (Device programming & construction) | **[Github Profile]**(https://github.com/n41ilexz)  
  - Frunză Mario-Eduard (Design & project presentation)  

## Resources  
- [AD8232 Sensor Documentation](https://www.analog.com/en/products/ad8232.html)  
- [MAX30102 Sensor Documentation](https://www.maximintegrated.com/en/products/MAX30102)  
- [Neurokit2 Library](https://neurokit2.readthedocs.io/)  

## License  
This project is available under the MIT License. See the [LICENSE](LICENSE) file for details.  

---  
For more information, explore the repository or contact us via the [Issues](https://github.com/username/HeartTrack/issues) section. Contributions are welcome! 🚀
