document.getElementById('recordButton').addEventListener('click', function() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            const audioChunks = [];
            mediaRecorder.start();

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000); // 5초 후에 녹음 중지

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks);
                sendDataToServer(audioBlob);
                audioChunks = []; 
            });

            
            document.getElementById('status').textContent = "Recording for 5 seconds...";
        }).catch(error => {
            console.error("음성권한이 필요합니다.", error);
        });
});

function sendDataToServer(audioBlob) {
    const formData = new FormData();
    formData.append("audio_data", audioBlob);
    fetch("/audio/upload-audio/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.predicted_probabilities) {
            document.getElementById('status').textContent = "Prediction: " + data.predicted_probabilities.join(', ');
        } else {
            document.getElementById('status').textContent = "Error: " + data.error;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById('status').textContent = "Failed to send audio.";
    });
}
