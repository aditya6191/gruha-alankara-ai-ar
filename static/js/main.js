// Main JavaScript file for Gruha Alankara interactions

/**
 * Access the user's camera safely via WebRTC API
 */
async function startCamera() {
    const videoElement = document.getElementById('camera-feed');
    const arOverlay = document.getElementById('ar-overlay');
    
    // Check if browser supports media devices
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert("Your browser does not support camera access or you're not on a secure (HTTPS) connection.");
        return;
    }

    try {
        const constraints = {
            video: { facingMode: "environment" } // Prefer back camera on mobile
        };
        
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        videoElement.srcObject = stream;
        videoElement.style.display = 'block';
        arOverlay.style.display = 'block';
        
    } catch (err) {
        console.error("Error accessing the camera: ", err);
        if (err.name === 'NotAllowedError') {
             alert("Camera access denied. Please grant permissions in your browser settings.");
        } else if (err.name === 'NotFoundError') {
             alert("No camera device found. Please ensure a camera is connected.");
        } else {
             alert("Could not access camera due to a browser or hardware issue.");
        }
    }
}

/**
 * Show the loading spinner when the design form is submitted
 */
function showLoader() {
    const loader = document.getElementById('loading-overlay');
    const btn = document.getElementById('generate-btn');
    const form = document.getElementById('design-form');
    
    // Simple frontend validation before blocking the UI
    if (form && form.checkValidity()) {
        if(loader) loader.style.display = 'block';
        if(btn) {
             btn.disabled = true;
             btn.textContent = 'Processing...';
        }
        form.submit();
    } else {
        form.reportValidity();
    }
}

// Handle Design form style selection
document.addEventListener('DOMContentLoaded', () => {
    const styleCards = document.querySelectorAll('.style-card');
    const styleInput = document.getElementById('style_preference');

    if (styleCards.length > 0 && styleInput) {
        styleCards.forEach(card => {
            card.addEventListener('click', () => {
                // Clear previous selection
                styleCards.forEach(c => c.classList.remove('selected'));
                // Add new selection
                card.classList.add('selected');
                styleInput.value = card.getAttribute('data-style');
            });
        });
    }

    // Handle view toggles in preview page
    const btn2d = document.getElementById('btn-2d');
    const btnAr = document.getElementById('btn-ar');
    const view2d = document.getElementById('view-2d');
    const viewAr = document.getElementById('view-ar');

    if (btn2d && btnAr && view2d && viewAr) {
        btn2d.addEventListener('click', () => {
            btn2d.classList.add('active');
            btnAr.classList.remove('active');
            view2d.style.display = 'block';
            viewAr.style.display = 'none';
        });

        btnAr.addEventListener('click', () => {
             // startCamera is called via onclick on the button itself
             btnAr.classList.add('active');
             btn2d.classList.remove('active');
             viewAr.style.display = 'block';
             view2d.style.display = 'none';
        });
    }

    // Handle furniture booking from preview sidebar
    const bookBtn = document.getElementById('book-furniture-btn');
    if (bookBtn) {
        bookBtn.addEventListener('click', async () => {
            bookBtn.disabled = true;
            const originalText = bookBtn.textContent;
            bookBtn.textContent = 'Booking...';

            try {
                const response = await fetch('/api/book', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ furniture_item_id: 1 })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || 'Booking failed');
                }

                alert(`Booking #${data.booking_id} confirmed.\nBuddy: ${data.buddy_says}`);
            } catch (error) {
                console.error('Error while booking furniture:', error);
                alert('Could not complete booking. Please try again.');
            } finally {
                bookBtn.disabled = false;
                bookBtn.textContent = originalText;
            }
        });
    }

    // Home page: handle "Upload Room Photo" button
    const homeUploadBtn = document.getElementById('home-upload-btn');
    const homeUploadInput = document.getElementById('home-room-photo');
    const homeUploadForm = document.getElementById('home-upload-form');

    if (homeUploadBtn && homeUploadInput && homeUploadForm) {
        homeUploadBtn.addEventListener('click', (event) => {
            event.preventDefault();
            homeUploadInput.click();
        });

        homeUploadInput.addEventListener('change', () => {
            if (homeUploadInput.files && homeUploadInput.files.length > 0) {
                homeUploadForm.submit();
            }
        });
    }
});
