// Request notification permission on load
if ("Notification" in window && Notification.permission !== "granted" && Notification.permission !== "denied") {
    Notification.requestPermission();
}

// Store to track which reminders have been shown
let shownReminders = new Set();

async function fetchReminders() {
    try {
        const res = await fetch('/get-reminders');
        if (!res.ok) return;
        const list = await res.json();
        renderReminders(list);
    } catch (e) {
        console.error('Failed fetching reminders', e);
    }
}

function renderReminders(list) {
    const ul = document.getElementById('reminderList');
    ul.innerHTML = '';
    if (!list || list.length === 0) {
        ul.innerHTML = '<li class="list-group-item text-center">No reminders set.</li>';
        return;
    }
    list.forEach(r => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        const notes = r.notes ? (' — ' + r.notes) : '';
        li.innerHTML = `
            <div>
                <strong>${r.title}</strong> <br>
                <small>${r.type} • ${r.date} ${r.time}${notes}</small>
                ${r.notified ? '<br><span style="color: green; font-size: 0.8rem;">✓ Notified</span>' : ''}
            </div>
            <button class="btn btn-sm btn-danger" onclick="deleteReminder('${r.id}')" style="margin-left: 10px;">✕</button>
        `;
        ul.appendChild(li);
    });
}

async function deleteReminder(reminderId) {
    try {
        const res = await fetch(`/delete-reminder/${reminderId}`, { method: 'DELETE' });
        if (res.ok) {
            fetchReminders();
        }
    } catch (e) {
        console.error('Failed deleting reminder', e);
    }
}

async function checkForDueReminders() {
    try {
        const res = await fetch('/check-reminders');
        if (!res.ok) return;
        const dueReminders = await res.json();
        
        for (let r of dueReminders) {
            // Only show notification once per reminder
            if (!shownReminders.has(r.id)) {
                showReminderNotification(r);
                shownReminders.add(r.id);
                
                // Mark as notified on server
                try {
                    await fetch(`/mark-reminder-notified/${r.id}`, { method: 'POST' });
                } catch (e) {
                    console.error('Failed marking reminder as notified', e);
                }
            }
        }
    } catch (e) {
        console.error('Failed checking reminders', e);
    }
}

function showReminderNotification(reminder) {
    // Browser notification
    if (Notification.permission === "granted") {
        new Notification("⏰ " + reminder.title, {
            body: reminder.notes || "It's time for your reminder!",
            icon: "https://cdn-icons-png.flaticon.com/512/3602/3602123.png",
            tag: reminder.id // Prevent duplicates
        });
    }
    
    // Sound notification
    playNotificationSound();
    
    // Visual alert in page
    showPageAlert(reminder);
}

function playNotificationSound() {
    // Create a longer, pleasant notification sound (5-8 seconds)
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const now = audioContext.currentTime;
        
        // Create a pleasing multi-tone alert pattern
        const tones = [
            { freq: 800, duration: 0.5, delay: 0 },
            { freq: 600, duration: 0.3, delay: 0.6 },
            { freq: 800, duration: 0.5, delay: 1.2 },
            { freq: 600, duration: 0.3, delay: 1.8 },
            { freq: 800, duration: 0.5, delay: 2.4 },
            { freq: 700, duration: 1.0, delay: 3.2 },
            { freq: 600, duration: 0.3, delay: 4.4 },
            { freq: 800, duration: 0.5, delay: 5.0 },
            { freq: 600, duration: 0.3, delay: 5.6 },
            { freq: 700, duration: 1.5, delay: 6.2 }
        ];
        
        tones.forEach(tone => {
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.value = tone.freq;
            oscillator.type = 'sine';
            
            const startTime = now + tone.delay;
            const endTime = startTime + tone.duration;
            
            gainNode.gain.setValueAtTime(0.4, startTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, endTime);
            
            oscillator.start(startTime);
            oscillator.stop(endTime);
        });
    } catch (e) {
        console.log('Audio notification not available:', e);
    }
}


function showPageAlert(reminder) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-info alert-dismissible fade show';
    alert.style.cssText = 'position: fixed; top: 80px; right: 20px; z-index: 9999; min-width: 300px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);';
    alert.innerHTML = `
        <strong>⏰ Reminder!</strong><br>
        <p style="margin: 10px 0;">${reminder.title}</p>
        ${reminder.notes ? `<small>${reminder.notes}</small><br>` : ''}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alert);
    
    // Auto-remove after 10 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 10000);
}

// Enable notifications button
document.getElementById("enableNotifBtn").addEventListener('click', async function(){
    if (!('Notification' in window)) return alert('Notifications not supported in this browser.');
    const perm = await Notification.requestPermission();
    if (perm === 'granted') {
        this.innerText = '🔔 Notifications Enabled';
        this.classList.remove('btn-primary');
        this.classList.add('btn-success');
    } else {
        this.innerText = '🔕 Notifications Disabled';
        this.classList.remove('btn-primary');
        this.classList.add('btn-warning');
    }
});

// Form submission
document.getElementById("reminderForm").onsubmit = async function(e){
    e.preventDefault();
    const data = {
        type: document.getElementById("type").value,
        title: document.getElementById("title").value,
        date: document.getElementById("date").value,
        time: document.getElementById("time").value,
        notes: document.getElementById("notes").value
    };
    const statusMsg = document.getElementById("statusMsg");
    statusMsg.innerHTML = "<span class='text-info'>Setting reminder...</span>";
    try {
        const response = await fetch("/set-reminder", {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const resp = await response.json();
        if(resp.status === "success") {
            statusMsg.innerHTML = "<span class='text-success'>" + resp.message + "</span>";
            document.getElementById("reminderForm").reset();
            // Refresh list and reset the shown reminders for new one
            setTimeout(() => { fetchReminders(); }, 500);
        } else {
            statusMsg.innerHTML = "<span class='text-danger'>Failed to set reminder.</span>";
        }
    } catch (err) {
        console.error(err);
        statusMsg.innerHTML = "<span class='text-danger'>Error connecting to server.</span>";
    }
}

// Load reminders on page load
fetchReminders();

// Check for due reminders every 30 seconds
setInterval(checkForDueReminders, 30000);

// Also check immediately on page load
checkForDueReminders();
