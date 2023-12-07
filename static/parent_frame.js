let playerExpanded = false;

function togglePlayerHeight() {
    var player = document.getElementById('player');
    var playerContent = document.getElementById('playerContent');
    var audioPlayer = document.getElementById('audioPlayer');

    playerExpanded = !playerExpanded;
    player.style.height = playerExpanded ? '87vh' : '50px';
    audioPlayer.style.width = playerExpanded ? '80%' : '50%';
    playerContent.style.display = playerExpanded ? 'flex' : 'none';
    const expandButton = document.getElementById('expand');
    expandButton.classList.toggle('expanded', playerExpanded);
}

function playSong(songId) {
    fetch(`/play_song/${songId}`, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        startPlay(data);
        togglePlayPause()
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function startPlay(response) {
    document.getElementById('playerContent').innerHTML = response[1];
    if (response[0]!=""){
        changeAudioSource(response[0]);
    }
    togglePlayerHeight();
}

function changeAudioSource(newSource) {
    var audioPlayer = document.getElementById('audioPlayer');
    audioPlayer.src = newSource;
    audioPlayer.load();
}

function togglePlayPause() {
    var audioPlayer = document.getElementById('audioPlayer');
    if (audioPlayer.paused) {
        audioPlayer.play();
    } else {
        audioPlayer.pause();
    }
}

function toggleMuteUnmute() {
    var audioPlayer = document.getElementById('audioPlayer');
    audioPlayer.muted = !audioPlayer.muted;
}

document.addEventListener('DOMContentLoaded', function () {
    var flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(function (message) {
        setTimeout(function () {
            dismissFlashMessage(message);
        }, 5000);
    });
});

function dismissFlashMessage(message) {
    message.style.opacity = '0';
    setTimeout(function () {
        message.style.display = 'none';
    }, 300);
}

document.addEventListener('DOMContentLoaded', function() {
        var currentPath = window.location.pathname;
        var hiddenPaths = ["/admin-songs", "/accounts", "/admin-overview"];
        if (hiddenPaths.includes(currentPath)) {
            document.getElementById('player').style.display = 'none';
            document.getElementById('search').style.display = 'none';
        }
    });