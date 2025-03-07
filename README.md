# OpenIPC Web UI Development Environment

This project provides a Docker-based development environment for creating a lightweight web UI for OpenIPC devices. It allows you to develop on your local machine and sync changes to your device.

## Features

- Tab-based navigation UI with sidebar
- Responsive design that works on various device sizes
- Camera, Wireless, Telemetry, Firmware and System settings
- Real-time resource monitoring
- Lightweight implementation that works well on resource-constrained devices

## Setup

1. Clone this repository
2. Configure your device settings in the `.env` file (created by setup.sh)
3. Start the Docker environment:
   ```bash
   docker-compose up -d
   ```

## Configuration

The project uses a `.env` file to configure device connection settings. Edit this file to match your OpenIPC device:

```
# OpenIPC Web UI Configuration
DEVICE_IP=192.168.1.10     # Your device's IP address
DEVICE_USER=root           # SSH username
DEVICE_PATH=/usr/share/www # Path to deploy web files
LOCAL_PATH=/app/           # Local development path
WATCH_INTERVAL=2           # File watching interval (seconds)
```

## Development Workflow

### Local Development

1. Edit files in the `app` directory
2. Visit `http://localhost:8080` in your browser to see changes
3. The development server will serve your files locally

### Syncing to Your Device

#### One-time sync:

```bash
docker-compose exec sync /scripts/sync-to-device.sh
```

You can override the settings from the `.env` file by passing arguments:
```bash
docker-compose exec sync /scripts/sync-to-device.sh 192.168.1.100 root /custom/path
```

#### Watch for changes and auto-sync:

```bash
docker-compose exec sync /scripts/watch-sync.sh
```

This will watch for file changes and automatically sync them to your device.

## Backend Server

The project includes a lightweight Python HTTP server (`server.py`) that serves both static files and API endpoints. Copy this to your device and run it:

```bash
scp scripts/server.py root@${DEVICE_IP}:/usr/bin/
ssh root@${DEVICE_IP} "chmod +x /usr/bin/server.py && /usr/bin/server.py"
```

You can add this to your device's startup scripts to run it automatically.

## Project Structure

```
.
├── .env                # Environment configuration
├── app/                # Web application files
│   ├── css/            # CSS stylesheets
│   ├── js/             # JavaScript files
│   ├── img/            # Images including OpenIPC logo
│   └── index.html      # Main HTML file
├── scripts/            # Utility scripts
│   ├── sync-to-device.sh     # Sync files to device
│   ├── watch-sync.sh         # Watch and sync
│   └── server.py             # Backend API server
├── docker-compose.yml  # Docker configuration
└── setup.sh            # Initial setup script
```

## UI Design

The UI is designed with a sidebar navigation pattern similar to the original OpenIPC interface:

- **Left sidebar**: Contains navigation tabs for different sections
- **Content area**: Shows the currently selected section
- **Responsive**: Adjusts to different screen sizes, with a collapsed sidebar on mobile

## Optimizing for Resource-Constrained Devices

The web UI is designed to be lightweight and efficient for devices with limited resources:

1. Uses CDN for Bootstrap and Bootstrap Icons to reduce local file size
2. Minimal JavaScript with no heavy frameworks
3. Simple CSS that extends Bootstrap's functionality
4. Static HTML that works without client-side rendering
5. Efficient API calls that only fetch required data

## Security Considerations

- The server implementation includes comments about security, but for a production environment, you should enhance security measures
- The `executeCommand` function in the server is particularly sensitive and should be carefully restricted in production
- Consider adding authentication for the API endpoints in a real deployment

## Customization

You can customize this starter template by:

1. Modifying the HTML/CSS/JS in the `app` directory
2. Adding additional API endpoints to the server
3. Extending the functionality based on your specific requirements

## Troubleshooting

If you encounter issues with syncing:
- Ensure SSH keys are properly set up
- Check network connectivity to the device
- Verify the user has appropriate permissions on the device
- Check your `.env` configuration