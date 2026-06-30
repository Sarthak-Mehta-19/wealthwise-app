document.addEventListener('DOMContentLoaded', () => {
    // 1. Visit Tracking Logic
    let visits = parseInt(localStorage.getItem('ww_visit_count') || '0');
    visits++;
    localStorage.setItem('ww_visit_count', visits);

    // 2. Banner Injection Engine (Fires on 1st visit, and every 5th visit if denied)
    const shouldShowBanner = (Notification.permission !== 'granted') && (visits === 1 || visits % 5 === 0);

    if (shouldShowBanner) {
        // Find the main content area of whatever page they are on to inject the banner
        const dashboardMain = document.querySelector('.dashboard-main-big-head') || document.querySelector('.dashboard-main');
        
        if (dashboardMain) {
            const bannerHTML = `
                <div class="notification-promo-banner" id="notifBanner" style="background: linear-gradient(135deg, #f59e0b, #ea580c); color: white; padding: 16px 24px; border-radius: 12px; margin: 24px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 10px 15px -3px rgba(245, 158, 11, 0.3); animation: slideDown 0.5s ease-out forwards;">
                    <div class="notif-promo-text">
                        <h4 style="margin: 0 0 6px 0; font-size: 16px; font-weight: 800;">🔔 Don't let your money get lonely!</h4>
                        <p style="margin: 0; font-size: 13px; font-weight: 500;">Enable notifications to get quirky AI updates, group challenge alerts, and perfectly timed saving reminders.</p>
                    </div>
                    <div class="notif-promo-actions" style="display: flex; gap: 16px; align-items: center;">
                        <button id="dismissNotifBtn" style="background: transparent; border: none; color: rgba(255,255,255,0.8); font-size: 13px; font-weight: 600; cursor: pointer; text-decoration: underline;">Maybe Later</button>
                        <button id="enableNotifBtn" style="background: white; color: #ea580c; border: none; padding: 8px 16px; border-radius: 8px; font-size: 13px; font-weight: 800; cursor: pointer;">Enable Alerts</button>
                    </div>
                </div>
            `;
            
            dashboardMain.insertAdjacentHTML('afterend', bannerHTML);

            document.getElementById('dismissNotifBtn').addEventListener('click', () => {
                document.getElementById('notifBanner').style.display = 'none';
            });

            document.getElementById('enableNotifBtn').addEventListener('click', async () => {
                // Request standard browser permissions (Will work perfectly on Render's HTTPS)
                const permission = await Notification.requestPermission();
                if (permission === 'granted') {
                    document.getElementById('notifBanner').style.display = 'none';
                    fireWelcomeNotification();
                }
            });
        }
    }

    // 3. The Quirky Zomato-Style Dispatcher
    const quirkyPrompts = [
        { title: "Your Piggy Bank is staring at you... 🐷", body: "It's feeling a little empty today. Drop ₹500 in your Emergency Fund before it gets angry." },
        { title: "Cheetah mode activated! 🐆", body: "Your group is saving so fast! Be the hero and push the fund past 80%." },
        { title: "Our AI ran the numbers 🧮", body: "If you skip ordering takeout tonight, you'll hit your financial goal 3 days early. You got this!" }
    ];

    function fireWelcomeNotification() {
        new Notification("Aw yeah! We're connected. 🚀", {
            body: "Get ready for the best financial nudges of your life. We promise not to spam.",
            icon: "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
        });
    }

    // Random test firing mechanism for active sessions
    if (Notification.permission === 'granted') {
        const randomDelay = Math.floor(Math.random() * (45000 - 15000 + 1) + 15000); // Fires between 15 and 45 seconds
        setTimeout(() => {
            const randomPrompt = quirkyPrompts[Math.floor(Math.random() * quirkyPrompts.length)];
            new Notification(randomPrompt.title, {
                body: randomPrompt.body,
                icon: "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
            });
        }, randomDelay);
    }
});