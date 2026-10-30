// Gesture Controls Dashboard Logic

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const engineStatusDot = document.getElementById('engineStatusDot');
    const engineStatusText = document.getElementById('engineStatusText');
    
    const videoStream = document.getElementById('videoStream');
    const streamOfflineOverlay = document.getElementById('streamOfflineOverlay');
    const toggleEngineBtn = document.getElementById('toggleEngineBtn');
    const restartStreamBtn = document.getElementById('restartStreamBtn');
    
    const teleFps = document.getElementById('teleFps');
    const fpsGauge = document.getElementById('fpsGauge');
    const teleHand = document.getElementById('teleHand');
    const teleHandLabel = document.getElementById('teleHandLabel');
    const teleGesture = document.getElementById('teleGesture');
    const teleGestureDetail = document.getElementById('teleGestureDetail');
    const teleAction = document.getElementById('teleAction');
    const teleActionTime = document.getElementById('teleActionTime');
    
    const volumeSlider = document.getElementById('volumeSlider');
    const volVal = document.getElementById('volVal');
    
    const configForm = document.getElementById('configForm');
    const configSaveStatus = document.getElementById('configSaveStatus');
    
    const logTerminal = document.getElementById('logTerminal');
    const clearLogsBtn = document.getElementById('clearLogsBtn');
    
    const galleryGrid = document.getElementById('galleryGrid');
    const screenshotCount = document.getElementById('screenshotCount');
    
    // Lightbox Elements
    const imageModal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImg');
    const modalCaption = document.getElementById('modalCaption');
    const modalClose = document.getElementById('modalClose');

    let eventSource = null;
    let isEngineActive = false;

    // Initialize Page
    loadConfig();
    loadScreenshots();
    setupEventSSE();

    // Toggle Tracking Engine Action
    toggleEngineBtn.addEventListener('click', async () => {
        try {
            toggleEngineBtn.disabled = true;
            toggleEngineBtn.innerText = 'WAITING FOR ENGINE...';
            
            const response = await fetch('/api/toggle', { method: 'POST' });
            const data = await response.json();
            
            isEngineActive = data.engine_active;
            updateEngineUI(isEngineActive);
            addTerminalLine(`[SYSTEM] Tracking engine toggled. Active: ${isEngineActive}`, 'system-msg');
        } catch (error) {
            console.error('Failed to toggle tracking engine:', error);
            addTerminalLine(`[SYSTEM] ERROR: Failed to toggle tracking engine`, 'error-msg');
        } finally {
            toggleEngineBtn.disabled = false;
        }
    });

    // Reload Video Stream Action
    restartStreamBtn.addEventListener('click', () => {
        addTerminalLine('[SYSTEM] Reloading camera stream...', 'system-msg');
        if (isEngineActive) {
            // Append random query param to prevent caching
            videoStream.src = `/api/video_feed?t=${Date.now()}`;
            showOfflineOverlay(false);
        } else {
            addTerminalLine('[SYSTEM] Cannot reload stream because camera engine is stopped', 'error-msg');
        }
    });

    // Clear event terminal logs view
    clearLogsBtn.addEventListener('click', () => {
        logTerminal.innerHTML = '';
        addTerminalLine('[SYSTEM] Logs view cleared.', 'system-msg');
    });

    // Handle Manual Volume Control Slider input
    volumeSlider.addEventListener('input', async (e) => {
        const val = e.target.value;
        volVal.innerText = `${val}%`;
        
        // Push volume command to backend
        try {
            await fetch('/api/volume', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ value: parseInt(val) })
            });
        } catch (error) {
            console.error('Error updating manual volume:', error);
        }
    });

    // Submit Config Form Settings
    configForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        configSaveStatus.innerText = 'Saving configurations...';
        configSaveStatus.style.color = 'var(--neon-yellow)';
        
        const formData = new FormData(configForm);
        const configData = {};
        formData.forEach((value, key) => {
            // Convert numbers
            if (key === 'camera_index') {
                configData[key] = parseInt(value);
            } else if (key === 'detection_confidence' || key === 'cooldown') {
                configData[key] = parseFloat(value);
            } else {
                configData[key] = value;
            }
        });

        try {
            const response = await fetch('/api/config', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(configData)
            });
            
            if (response.ok) {
                configSaveStatus.innerText = 'All settings saved & applied!';
                configSaveStatus.style.color = 'var(--neon-green)';
                addTerminalLine('[SYSTEM] New configurations updated successfully', 'system-msg');
                
                setTimeout(() => {
                    configSaveStatus.innerText = 'All settings synced';
                    configSaveStatus.style.color = 'var(--text-muted)';
                }, 3000);
            } else {
                throw new Error('Config save response error');
            }
        } catch (error) {
            console.error('Failed to save config:', error);
            configSaveStatus.innerText = 'ERROR saving settings';
            configSaveStatus.style.color = 'var(--neon-red)';
            addTerminalLine('[SYSTEM] ERROR: Failed to apply new configurations', 'error-msg');
        }
    });

    // Fetch Configurations from Backend
    async function loadConfig() {
        try {
            const response = await fetch('/api/config');
            const data = await response.json();
            
            document.getElementById('cameraIndex').value = data.camera_index;
            document.getElementById('detectionConfidence').value = data.detection_confidence;
            document.getElementById('cooldownTime').value = data.cooldown;
            document.getElementById('chatgptUrl').value = data.chatgpt_url;
            document.getElementById('youtubeUrl').value = data.youtube_url;
            
            addTerminalLine('[SYSTEM] Configurations successfully loaded from source', 'system-msg');
        } catch (error) {
            console.error('Error loading config:', error);
            addTerminalLine('[SYSTEM] ERROR: Unable to load configurations from backend', 'error-msg');
        }
    }

    // Load list of screenshots saved
    async function loadScreenshots() {
        try {
            const response = await fetch('/api/screenshots');
            const files = await response.json();
            
            galleryGrid.innerHTML = '';
            screenshotCount.innerText = `${files.length} screenshot${files.length !== 1 ? 's' : ''}`;
            
            if (files.length === 0) {
                galleryGrid.innerHTML = '<div class="no-screenshots">No screenshots saved yet. Show Peace gesture to capture!</div>';
                return;
            }

            files.forEach(filename => {
                const item = document.createElement('div');
                item.className = 'gallery-item';
                
                // Clicking item opens full light box preview
                item.addEventListener('click', (e) => {
                    if (e.target.classList.contains('delete-btn')) return; // Avoid triggering lightbox on delete click
                    openLightbox(`/screenshots/${filename}`, filename);
                });

                item.innerHTML = `
                    <img src="/screenshots/${filename}" alt="${filename}">
                    <div class="gallery-overlay">
                        <button class="delete-btn" title="Delete Screenshot">&times;</button>
                    </div>
                `;
                
                // Set delete handler
                item.querySelector('.delete-btn').addEventListener('click', async (e) => {
                    e.stopPropagation();
                    if (confirm(`Delete screenshot "${filename}"?`)) {
                        await deleteScreenshot(filename);
                    }
                });

                galleryGrid.appendChild(item);
            });
        } catch (error) {
            console.error('Error loading screenshots:', error);
        }
    }

    // Delete screenshot call
    async function deleteScreenshot(filename) {
        try {
            const response = await fetch(`/api/screenshots/${filename}`, { method: 'DELETE' });
            if (response.ok) {
                addTerminalLine(`[SYSTEM] Deleted screenshot: ${filename}`, 'system-msg');
                loadScreenshots();
            } else {
                throw new Error('Delete response not OK');
            }
        } catch (error) {
            console.error('Failed to delete screenshot:', error);
            addTerminalLine(`[SYSTEM] ERROR: Failed to delete screenshot: ${filename}`, 'error-msg');
        }
    }

    // Lightbox modal view control
    function openLightbox(src, caption) {
        imageModal.style.display = 'flex';
        modalImg.src = src;
        modalCaption.innerText = caption;
    }

    modalClose.addEventListener('click', () => {
        imageModal.style.display = 'none';
    });

    imageModal.addEventListener('click', (e) => {
        if (e.target === imageModal) {
            imageModal.style.display = 'none';
        }
    });

    // Connect Server-Sent Events (SSE) Stream
    function setupEventSSE() {
        if (eventSource) {
            eventSource.close();
        }

        addTerminalLine('[SYSTEM] Initiating Server Event Connection...', 'system-msg');
        eventSource = new EventSource('/api/events');

        eventSource.onopen = () => {
            addTerminalLine('[SYSTEM] Connected to Event Stream successfully!', 'system-msg');
        };

        eventSource.onerror = (e) => {
            console.error('Event stream connection error:', e);
            addTerminalLine('[SYSTEM] Warning: Event Stream disconnected. Retrying...', 'error-msg');
            
            // Show engine offline
            updateEngineUI(false);
            showOfflineOverlay(true);
        };

        // Handle SSE updates
        eventSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                
                if (data.type === 'telemetry') {
                    // Update stats
                    teleFps.innerText = data.fps.toFixed(1);
                    fpsGauge.style.width = `${Math.min(100, (data.fps / 30) * 100)}%`;
                    
                    teleHand.innerText = data.hand.toUpperCase();
                    teleHandLabel.innerText = data.hand !== 'NONE' ? 'Hand detected in frame' : 'No hand detected';
                    
                    teleGesture.innerText = data.gesture.toUpperCase();
                    teleGestureDetail.innerText = getGestureDescription(data.gesture);
                    
                    const oldAction = teleAction.innerText;
                    teleAction.innerText = data.action.toUpperCase();
                    
                    if (data.action !== 'NONE' && data.action !== 'WAITING...' && data.action !== oldAction) {
                        teleActionTime.innerText = new Date().toLocaleTimeString();
                        
                        // If screenshot taken, reload screenshots gallery
                        if (data.action.includes('Saved')) {
                            addTerminalLine(`[ACTION] ${data.action}`, 'action-msg');
                            setTimeout(loadScreenshots, 1000); // Small timeout to ensure file is saved on disk
                        } else {
                            addTerminalLine(`[ACTION] Triggered: ${data.action}`, 'action-msg');
                        }
                    } else if (data.action === 'NONE' || data.action === 'WAITING...') {
                        teleActionTime.innerText = '-';
                    }

                    // Update UI Volume (only if not actively sliding slider manually to avoid cursor jumps)
                    if (document.activeElement !== volumeSlider) {
                        volumeSlider.value = data.volume;
                        volVal.innerText = `${data.volume}%`;
                    }

                    isEngineActive = data.engine_active;
                    updateEngineUI(isEngineActive);
                    showOfflineOverlay(!isEngineActive);
                } 
                else if (data.type === 'log') {
                    // Logs from backend
                    let logType = 'system-msg';
                    if (data.message.includes('| ACTION |')) logType = 'action-msg';
                    else if (data.message.includes('| GESTURE |')) logType = 'gesture-msg';
                    else if (data.message.includes('| ERROR |') || data.message.includes('| WARNING |')) logType = 'error-msg';
                    
                    addTerminalLine(data.message, logType);
                }
            } catch (err) {
                console.error('Error parsing SSE event details:', err);
            }
        };
    }

    // Terminal helper
    function addTerminalLine(text, className) {
        const line = document.createElement('div');
        line.className = `term-line ${className}`;
        line.innerText = text;
        logTerminal.appendChild(line);
        
        // Auto scroll to bottom
        logTerminal.scrollTop = logTerminal.scrollHeight;
        
        // Prune logs if too many lines
        if (logTerminal.children.length > 200) {
            logTerminal.removeChild(logTerminal.firstChild);
        }
    }

    // Toggle offline overlay on video tag
    function showOfflineOverlay(isOffline) {
        if (isOffline) {
            streamOfflineOverlay.style.opacity = '1';
            streamOfflineOverlay.style.pointerEvents = 'auto';
        } else {
            streamOfflineOverlay.style.opacity = '0';
            streamOfflineOverlay.style.pointerEvents = 'none';
        }
    }

    // Adjust engine indicators
    function updateEngineUI(isActive) {
        if (isActive) {
            engineStatusDot.className = 'pulse-dot active';
            engineStatusText.innerText = 'SYSTEM ACTIVE';
            toggleEngineBtn.className = 'btn btn-primary btn-glow';
            toggleEngineBtn.innerText = 'STOP GESTURE RUNNER';
        } else {
            engineStatusDot.className = 'pulse-dot inactive';
            engineStatusText.innerText = 'SYSTEM STOPPED';
            toggleEngineBtn.className = 'btn btn-success btn-glow';
            toggleEngineBtn.innerText = 'START GESTURE RUNNER';
        }
    }

    // Map gesture name to descriptions
    function getGestureDescription(gesture) {
        switch (gesture.toUpperCase()) {
            case 'PINCH': return 'Pinch gesture (adjusting volume)';
            case 'THUMB_UP': return 'Thumbs Up detected (opening ChatGPT)';
            case 'PEACE': return 'Peace sign detected (taking Screenshot)';
            case 'ROCK': return 'Rock sign detected (opening YouTube)';
            case 'FIST': return 'Fist closed (locked status)';
            case 'OPEN_HAND': return 'Open palm detected';
            case 'UNKNOWN': return 'No recognized pattern';
            default: return 'Idle state';
        }
    }
});
