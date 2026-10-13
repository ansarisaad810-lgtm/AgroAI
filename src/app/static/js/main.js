let currentLocation = "Bhilai, Chhattisgarh";
let lastAIResponseText = "";

function manualLocationSelect(loc) {
    currentLocation = loc;
    document.getElementById('locationDisplay').innerText = loc;
}

function autoDetectLocation() {
    if (navigator.geolocation) {
        document.getElementById('locationDisplay').innerText = "Detecting...";
        navigator.geolocation.getCurrentPosition(
            (position) => {
                currentLocation = `Lat ${position.coords.latitude.toFixed(2)}, Lon ${position.coords.longitude.toFixed(2)} (Bhilai Region)`;
                document.getElementById('locationDisplay').innerText = "Detected Location";
            },
            (error) => {
                currentLocation = "Bhilai, Chhattisgarh";
                document.getElementById('locationDisplay').innerText = currentLocation;
                alert("Location access defaulted to Bhilai, CG.");
            }
        );
    } else {
        alert("Geolocation not supported by browser.");
    }
}

function startVoice() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.lang = 'hi-IN';
        recognition.start();

        recognition.onresult = function(event) {
            document.getElementById('voiceInput').value = event.results[0][0].transcript;
        };
    } else {
        alert("Voice input not supported in this browser.");
    }
}

// FEATURE: Text-to-Speech (TTS) Engine for illiterate farmers
function speakAIResponse() {
    if (!lastAIResponseText) {
        alert("No AI response to speak yet!");
        return;
    }

    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        let cleanText = lastAIResponseText.replace(/<[^>]*>?/gm, '');
        let utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        window.speechSynthesis.speak(utterance);
    } else {
        alert("Text-to-speech audio output is not supported in this browser.");
    }
}

function renderMarkdownToHTML(text) {
    let html = text
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h3>$1</h3>')
        .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
        .replace(/^\- (.*$)/gim, '<li>$1</li>')
        .replace(/\n\n/g, '<br><br>');

    return html;
}

async function sendToGroq() {
    let input = document.getElementById('voiceInput').value.trim();
    if (!input) return;

    let responseContainer = document.getElementById('aiResponse');
    responseContainer.innerHTML = "⏳ <em>Connecting to AgroAI...</em>";

    try {
        let res = await fetch('/api/groq', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                prompt: input,
                location: currentLocation 
            })
        });
        
        let data = await res.json();
        if (data.response) {
            lastAIResponseText = data.response;
            let formattedHTML = renderMarkdownToHTML(data.response);
            
            responseContainer.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong>🌾 AgroAI Response:</strong>
                    <button class="btn btn-sm btn-green" onclick="speakAIResponse()">🔊 Listen (Awaaz)</button>
                </div>
                <hr>
                ${formattedHTML}
            `;
            responseContainer.scrollTop = 0;
        } else {
            responseContainer.innerText = "Error: Could not retrieve response.";
        }
    } catch (err) {
        responseContainer.innerText = "Network Error: Could not connect to AgroAI backend.";
    }
}

function calculateFertilizer() {
    let crop = document.getElementById('npkCrop').value;
    let acres = document.getElementById('npkAcres').value;

    fetch('/npk_calculator', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `crop=${encodeURIComponent(crop)}&acres=${encodeURIComponent(acres)}`
    })
    .then(res => res.json())
    .then(data => {
        let r = data.result;
        if (r) {
            document.getElementById('npkResult').innerHTML = `
                <p><strong>Required Urea:</strong> ${r.urea_kg} kg</p>
                <p><strong>Required DAP:</strong> ${r.dap_kg} kg</p>
                <p><em>Nutrient breakdown: N: ${r.n_element}kg, P: ${r.p_element}kg, K: ${r.k_element}kg</em></p>
            `;
        }
    });
}

function addCrop() {
    let cropName = document.getElementById('cropSelect').value;
    fetch('/add_crop', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'crop_name=' + encodeURIComponent(cropName)
    }).then(res => res.json()).then(data => location.reload());
}

function removeCrop(cropName) {
    fetch('/remove_crop', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'crop_name=' + encodeURIComponent(cropName)
    }).then(res => res.json()).then(data => location.reload());
}
