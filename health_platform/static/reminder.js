let reminders = JSON.parse(localStorage.getItem("reminders") || "[]");

// ✅ Enable Notifications button
document.getElementById("enableNotifBtn").addEventListener("click", async () => {
    if (!("Notification" in window)) {
        alert("❌ Your browser does not support notifications.");
        return;
    }

    let permission = await Notification.requestPermission();

    if (permission === "granted") {
        new Notification("✅ Notifications Enabled", {
            body: "You will now receive health reminders.",
            icon: "/static/bell.png" // optional custom icon
        });
    } else if (permission === "denied") {
        alert("❌ You blocked notifications. Enable them in browser settings.");
    } else {
        alert("ℹ️ Notification permission dismissed.");
    }
});

// Handle form submission
document.getElementById("reminderForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const reminder = {
        id: Date.now(),
        type: document.getElementById("type").value,
        title: document.getElementById("title").value,
        date: document.getElementById("date").value,
        time: document.getElementById("time").value,
        repeat: document.getElementById("repeat").value,
        advance: parseInt(document.getElementById("advance").value || 0),
        notes: document.getElementById("notes").value,
        done: false
    };

    reminders.push(reminder);
    localStorage.setItem("reminders", JSON.stringify(reminders));
    document.getElementById("statusMsg").innerText = "✅ Reminder set!";
    renderReminders();
    e.target.reset();
});

// Render reminders
function renderReminders() {
    const list = document.getElementById("reminderList");
    list.innerHTML = "";
    reminders.forEach(r => {
        const li = document.createElement("li");
        li.className = "list-group-item";
        li.innerHTML = `
            <div>
              <strong>${r.title}</strong> (${r.type})<br>
              <small>${r.date} ${r.time} ${r.notes ? "- " + r.notes : ""}</small>
            </div>
            <div class="reminder-actions">
              <button class="btn btn-sm btn-primary" onclick="snoozeReminder(${r.id})">Snooze</button>
              <button class="btn btn-sm btn-success" onclick="markDone(${r.id})">Done</button>
            </div>
        `;
        list.appendChild(li);
    });
}

// Snooze: +5 min
function snoozeReminder(id) {
    reminders = reminders.map(r => {
        if (r.id === id) {
            let d = new Date(`${r.date}T${r.time}`);
            d.setMinutes(d.getMinutes() + 5);
            r.date = d.toISOString().split("T")[0];
            r.time = d.toTimeString().slice(0,5);
        }
        return r;
    });
    localStorage.setItem("reminders", JSON.stringify(reminders));
    renderReminders();
}

// Mark as done
function markDone(id) {
    reminders = reminders.filter(r => r.id !== id);
    localStorage.setItem("reminders", JSON.stringify(reminders));
    renderReminders();
}

// Check reminders
function checkReminders() {
    let now = new Date();
    let currentDate = now.toISOString().split("T")[0];
    let currentTime = now.getHours().toString().padStart(2,"0")+":"+now.getMinutes().toString().padStart(2,"0");

    reminders.forEach(r => {
        let reminderTime = new Date(`${r.date}T${r.time}`);
        reminderTime.setMinutes(reminderTime.getMinutes() - (r.advance || 0));

        let reminderDate = reminderTime.toISOString().split("T")[0];
        let reminderClock = reminderTime.getHours().toString().padStart(2,"0")+":"+reminderTime.getMinutes().toString().padStart(2,"0");

        if (reminderDate === currentDate && reminderClock === currentTime && !r.done) {
            triggerReminder(r);

            if (r.repeat === "daily") {
                let d = new Date(`${r.date}T${r.time}`);
                d.setDate(d.getDate()+1);
                r.date = d.toISOString().split("T")[0];
            } else if (r.repeat === "weekly") {
                let d = new Date(`${r.date}T${r.time}`);
                d.setDate(d.getDate()+7);
                r.date = d.toISOString().split("T")[0];
            } else {
                r.done = true;
            }

            localStorage.setItem("reminders", JSON.stringify(reminders));
            renderReminders();
        }
    });
}

// Trigger reminder
function triggerReminder(reminder) {
    let msg = `${reminder.type}: ${reminder.title} at ${reminder.time}`;
    if ("Notification" in window && Notification.permission === "granted") {
        new Notification("⏰ Health Reminder", { body: msg });
    } else {
        alert(msg);
    }
    let audio = new Audio("/static/notify.mp3");
    audio.play();
    if (navigator.vibrate) navigator.vibrate([300,200,300]);
}

// Run every 30s
setInterval(checkReminders, 30000);

renderReminders();
