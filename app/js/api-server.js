/**
 * Simplified API Service for OpenIPC
 */
class ApiService {
    constructor(baseUrl = '/api') {
        this.baseUrl = baseUrl;
    }

    /**
     * Get camera settings
     */
    async getCameraSettings() {
        return this._fetchData('camera-settings');
    }

    /**
     * Update camera settings
     */
    async updateCameraSettings(settings) {
        return this._postData('camera-settings', settings);
    }

    /**
     * Get wireless settings
     */
    async getWirelessSettings() {
        return this._fetchData('wireless-settings');
    }

    /**
     * Update wireless settings
     */
    async updateWirelessSettings(settings) {
        return this._postData('wireless-settings', settings);
    }

    /**
     * Helper method for GET requests
     */
    async _fetchData(endpoint) {
        try {
            const response = await fetch(`${this.baseUrl}/${endpoint}`);
            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Error fetching from ${endpoint}:`, error);
            throw error;
        }
    }

    /**
     * Helper method for POST requests
     */
    async _postData(endpoint, data) {
        try {
            const response = await fetch(`${this.baseUrl}/${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Error posting to ${endpoint}:`, error);
            throw error;
        }
    }
}