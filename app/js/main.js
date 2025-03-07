document.addEventListener('DOMContentLoaded', () => {
    // Initialize API service (if available)
    let api;
    try {
        api = new ApiService('/api');
    } catch (e) {
        console.log('API service not available, running in demo mode');
    }
    
    // Setup event handlers for form elements
    setupFormHandlers();
    
    // Function to set up form handlers
    function setupFormHandlers() {
        // Power range slider - update displayed value
        const powerSlider = document.getElementById('power');
        if (powerSlider) {
            // Find the next element after the label "Power" that contains the value
            const powerValueDisplay = powerSlider.parentElement.querySelector('span');
            
            powerSlider.addEventListener('input', () => {
                if (powerValueDisplay) {
                    powerValueDisplay.textContent = powerSlider.value;
                }
            });
        }
        
        // Camera save button
        const cameraSaveBtn = document.getElementById('camera-save');
        if (cameraSaveBtn) {
            cameraSaveBtn.addEventListener('click', async () => {
                const settings = {
                    frames: document.getElementById('frames').value,
                    bitrate: document.getElementById('bitrate').value,
                    record: document.getElementById('record').checked,
                    audio: document.getElementById('audio').checked,
                    sample: document.getElementById('sample').value
                };
                
                console.log('Camera settings:', settings);
                await saveSettings('camera', settings, cameraSaveBtn);
            });
        }
        
        // Wireless save button
        const wirelessSaveBtn = document.getElementById('wireless-save');
        if (wirelessSaveBtn) {
            wirelessSaveBtn.addEventListener('click', async () => {
                const settings = {
                    channel: document.getElementById('channel').value,
                    power: document.getElementById('power').value,
                    stbc: document.getElementById('stbc').checked,
                    ldpc: document.getElementById('ldpc').checked
                };
                
                console.log('Wireless settings:', settings);
                await saveSettings('wireless', settings, wirelessSaveBtn);
            });
        }
    }
    
    // Function to save settings
    async function saveSettings(type, settings, button) {
        if (!button) return;
        
        const originalText = button.innerHTML;
        button.innerHTML = 'Saving...';
        button.disabled = true;
        
        try {
            // Simulate API call with a delay
            await new Promise(resolve => setTimeout(resolve, 500));
            
            /* Real API call would look like this:
            const endpoint = `/api/${type}-settings`;
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(settings)
            });
            
            const data = await response.json();
            if (!data.success) throw new Error(data.message || 'Failed to save settings');
            */
            
            // For demo purposes, just show an alert
            alert(`${type.charAt(0).toUpperCase() + type.slice(1)} settings saved successfully`);
        } catch (error) {
            console.error(`Error saving ${type} settings:`, error);
            alert(`Failed to save ${type} settings: ${error.message}`);
        } finally {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }
});