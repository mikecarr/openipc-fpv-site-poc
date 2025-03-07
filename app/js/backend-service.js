/**
 * API Service for OpenIPC
 * This provides a simple interface for interacting with the backend APIs
 */

class ApiService {
    constructor(baseUrl = '/api') {
        this.baseUrl = baseUrl;
    }

    /**
     * Fetch system information
     */
    async getSystemInfo() {
        try {
            const response = await fetch(`${this.baseUrl}/system-info`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching system info:', error);
            throw error;
        }
    }

    /**
     * Get wireless settings
     */
    async getWirelessSettings() {
        try {
            const response = await fetch(`${this.baseUrl}/wireless-settings`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching wireless settings:', error);
            throw error;
        }
    }

    /**
     * Update wireless settings
     */
    async updateWirelessSettings(settings) {
        try {
            const response = await fetch(`${this.baseUrl}/wireless-settings`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(settings)
            });
            return await response.json();
        } catch (error) {
            console.error('Error updating wireless settings:', error);
            throw error;
        }
    }

    /**
     * Execute a system command
     */
    async executeCommand(command) {
        try {
            const response = await fetch(`${this.baseUrl}/execute`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ command })
            });
            return await response.json();
        } catch (error) {
            console.error('Error executing command:', error);
            throw error;
        }
    }

    /**
     * Get system uptime
     */
    async getUptime() {
        try {
            const response = await fetch(`${this.baseUrl}/uptime`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching uptime:', error);
            throw error;
        }
    }

    /**
     * Get system resource usage (CPU, memory)
     */
    async getResourceUsage() {
        try {
            const response = await fetch(`${this.baseUrl}/resources`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching resource usage:', error);
            throw error;
        }
    }
}

// Export the API service
window.ApiService = ApiService;
