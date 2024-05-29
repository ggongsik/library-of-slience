document.getElementById('recordButton').addEventListener('click', function() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            const audioChunks = [];
            mediaRecorder.start();

            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000);  // Stop recording after 5 seconds

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks);
                sendDataToServer(audioBlob);
            };

            document.getElementById('status').textContent = "Recording for 5 seconds...";
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
        document.getElementById('status').textContent = "Prediction: " + data.classification;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById('status').textContent = "Failed to send audio.";
    });
}
