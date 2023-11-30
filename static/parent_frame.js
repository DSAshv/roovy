let playerExpanded = false;

function togglePlayerHeight() {
    var player = document.getElementById('player');
    var playerContent = document.getElementById('playerContent');
    playerExpanded = !playerExpanded;
    player.style.height = playerExpanded ? '90vh' : '50px';
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
    changeAudioSource(response[0]);
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
