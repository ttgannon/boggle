let $submitGuess = $('#submitGuess');

// clearInterval(setInterval(timer, 1000))

let intervalId;

$(document).ready(function() {
    let counter = parseInt($('#counter').text());
    let intervalId;
    startGame();
  
    function startGame() {
      intervalId = setInterval(timer, 1000);
    }
  
    async function timer() {
      counter -= 1;
      let $counter = $('#counter');
      $counter.text(counter);
      console.log(counter);
      if (counter === 0) {
        clearInterval(intervalId);
        $submitGuess.prop('disabled', true);
        endGame();
      }
    }
  });

function changeScore($guess) {
    let $score = $('#score');
    let score = parseInt($score.text());
    let new_score = $guess.val().length;
    score += new_score;
    $score.text(score);
}


$(document).on('click', '#submitGuess', async function(e) {
    e.preventDefault();
    let $guess = $('#guess');
    let axiosResp = await axios.get('/guess', { params: { guess: $guess.val() }});
    if (axiosResp.data.result === "not-word") {
        alert("That is not a word, please try again.")
    }
    else if  (axiosResp.data.result === "not-on-board") {
        alert("That word is not on this board. Please try again.")
    }
    else {
        changeScore($guess);
    }
})

async function endGame() {
    await axios.post('/game_played', { 
        gameplay: 1,
        score: $('#score').text()
     });
}


    