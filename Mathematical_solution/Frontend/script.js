document.addEventListener('DOMContentLoaded', function() {
  if (typeof particlesJS !== 'undefined') {
    particlesJS('particles-js', {
      particles: {
        number: { value: 80, density: { enable: true, value_area: 800 } },
        color: { value: "#4895ef" },
        shape: { type: "circle" },
        opacity: { value: 0.5, random: true },
        size: { value: 3, random: true },
        line_linked: { enable: true, distance: 150, color: "#4895ef", opacity: 0.4, width: 1 },
        move: { enable: true, speed: 2, direction: "none", random: true, straight: false, out_mode: "out" }
      },
      interactivity: {
        detect_on: "canvas",
        events: {
          onhover: { enable: true, mode: "repulse" },
          onclick: { enable: true, mode: "push" }
        }
      }
    });
  }
  
  
  const textarea = document.getElementById('prompt');
  setTimeout(() => {
    textarea.focus();
    textarea.classList.add('animated', 'pulse');
  }, 1000);
});

async function submitPrompt(event) {
  if (event) event.preventDefault();
  
  const prompt = document.getElementById('prompt').value.trim();
  const statusDiv = document.getElementById('status');
  const video = document.getElementById('videoPreview');
  const videoContainer = document.querySelector('.video-container');
  
  
  video.src = '';
  videoContainer.classList.remove('show');
  
  try {
    const res = await fetch("http://localhost:8000/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt })
    });

    const data = await res.json();

    if (data.status === "success" && data.video_url) {
      
      const newVideo = document.createElement('video');
      newVideo.id = 'videoPreview';
      newVideo.controls = true;
      newVideo.src = data.video_url;
      
      
      videoContainer.innerHTML = '';
      videoContainer.appendChild(newVideo);
      
      newVideo.onloadeddata = () => {
        videoContainer.classList.add('show');
        statusDiv.innerHTML = `<i class="fas fa-check-circle"></i> Animation generated successfully!`;
        statusDiv.style.borderLeftColor = 'var(--success-color)';
        celebrate();
      };
      
      newVideo.onerror = () => {
        statusDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> Error loading video. Please try again.`;
        statusDiv.style.borderLeftColor = 'var(--error-color)';
      };
    } else {
      throw new Error(data.message || 'No video URL in response');
    }
  } catch (error) {
    console.error('Error:', error);
    statusDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${error.message}`;
    statusDiv.style.borderLeftColor = 'var(--error-color)';
  }
}

function loadExample(prompt) {
  const textarea = document.getElementById('prompt');
  textarea.value = prompt;
  
  
  textarea.classList.add('example-loaded');
  setTimeout(() => textarea.classList.remove('example-loaded'), 1000);
  
  textarea.focus();
}

function celebrate() {
  const container = document.querySelector('.container');
  
  
  for (let i = 0; i < 50; i++) {
    const confetti = document.createElement('div');
    confetti.classList.add('confetti');
    confetti.style.left = Math.random() * 100 + 'vw';
    confetti.style.backgroundColor = `hsl(${Math.random() * 360}, 100%, 50%)`;
    confetti.style.animationDuration = (Math.random() * 3 + 2) + 's';
    document.body.appendChild(confetti);
    

    setTimeout(() => {
      confetti.remove();
    }, 5000);
  }
  

  container.classList.add('pulse-animation');
  setTimeout(() => {
    container.classList.remove('pulse-animation');
  }, 1000);
}


document.head.insertAdjacentHTML('beforeend', `
  <style>
    .shake-animation {
      animation: shake 0.5s;
    }
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
      20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    .confetti {
      position: fixed;
      width: 10px;
      height: 10px;
      background-color: #f00;
      top: -10px;
      z-index: 999;
      animation: fall linear forwards;
    }
    @keyframes fall {
      to {
        transform: translateY(100vh) rotate(720deg);
        opacity: 0;
      }
    }
    .pulse-animation {
      animation: pulse 1s;
    }
    .example-loaded {
      animation: highlight 1s;
    }
    @keyframes highlight {
      0% { box-shadow: 0 0 0 0 rgba(72, 149, 239, 0.7); }
      70% { box-shadow: 0 0 0 10px rgba(72, 149, 239, 0); }
      100% { box-shadow: 0 0 0 0 rgba(72, 149, 239, 0); }
    }
  </style>
`);