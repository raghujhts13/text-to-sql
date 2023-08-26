function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const time = `${hours}:${minutes}:${seconds}`;
    
    document.getElementById('clock').textContent = time;
  }
  
  // Update the clock every second
  setInterval(updateClock, 1000);
  
  // Initial call to set the time immediately
  updateClock();
  