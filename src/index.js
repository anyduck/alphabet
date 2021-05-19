let wrapper = document.getElementById('wrapper')
let buttons = [
  document.getElementById('button0'),
  document.getElementById('button1'),
  document.getElementById('button2'),
  document.getElementById('button3'),
]
let task = document.getElementById('task')
let progress = document.getElementById('progress')
let game_score = document.getElementById('game-score')
let result_score = document.getElementById('result-score')
let share_score = document.getElementById('share-score')
let table = document.getElementById('table')

const params = new URLSearchParams(window.location.search);

const user_id = params.get('user_id');
const inline_message_id = params.get('inline_message_id');

let alphabet = [...
  "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
];
let DEFAULT_TIME = 10;
let time = 10;
let score = 0;
let max_score = 0;


function random(a, b) {
  return Math.floor(Math.random() * (b - a)) + a;
}

function empty(div) {
  while (div.firstChild) {
    div.removeChild(div.firstChild);
  }
}


class Question {
  constructor() {
      this.length = random(2, 5);
      let start = random(0, alphabet.length - length);
      this.question = alphabet.slice(start, start + this.length);
      this.answers = Array.from(this.new_answer(start, 4));
      let correct_answer = random(0, this.question.length);
      this.correct_answer = random(0, 4);
      this.answers[this.correct_answer] = this.question[correct_answer];
      this.question[correct_answer] = '_';
    }
    * new_answer(start, n) {
      let answers = [...alphabet];
      answers.splice(start, this.length);
      for (let i = 0; i < n; i++) {
        yield answers.splice(random(0, answers.length), 1)[0]
      }
    }
  display() {
    empty(task);
    for (let letter of this.question) {
      task.innerHTML += `<span class="letter">${letter}</span>`;
    }
    buttons.forEach((button, index) => {
      console.log(button)
      console.log(button.getElementsByClassName('icon-letter'))
      button.getElementsByClassName('icon-letter')[0].textContent = this.answers[index];
    })
  }
  answer(number) {
      console.log("clicked")
    if (number == this.correct_answer) {
      time = Math.max(time+2, DEFAULT_TIME);
      score +=1;
      game_score.textContent = score;
    } else {
      time -= 1;
    }
  }
}


let question;
let timer;

function is_game() {
  return wrapper.classList.contains('in-game');
}

buttons.forEach((button, index) => {
  button.addEventListener('click', () => {
    if (is_game()) {
      question.answer(index);
      question = new Question();
      question.display();
    }
  })
})

buttons[0].addEventListener('click', () => {
  if (!is_game()) {
    question = new Question();
    question.display();
    timer = setInterval(on_tick, 150);
    wrapper.classList.remove('in-greeting');
    wrapper.classList.toggle('in-game');
    wrapper.classList.toggle('in-result');
    table.classList.remove('show');
    share_score.classList.remove('show');
  }
})

share_score.addEventListener('click', () => {
    TelegramGameProxy.shareScore()
})


function on_tick() {
  if (time <= 0) {
    progress.style.width = '0%';
    on_end();
  }
  time -= .15;
  progress.style.width = Math.min(time * 100 / DEFAULT_TIME, 100).toFixed(2) + '%';

}

async function on_end() {
    clearInterval(timer);
    progress.style.width = '100%';
    result_score.textContent = score;
    game_score.textContent = 0;
    time = DEFAULT_TIME;
    wrapper.classList.toggle('in-game');
    wrapper.classList.toggle('in-result');
    
    
    const url=`/api/alphabet_battle/set_score?user_id=${user_id}&inline_message_id=${inline_message_id}&score=${score}`;
    
    if (score > max_score) {
        max_score = score;
        share_score.classList.add('show');
        await fetch(url, {method: 'POST'});
    }
    score = 0;
    await get_table();
}


async function get_table() {
    empty(table)
    const url=`/api/alphabet_battle/get_high_scores?user_id=${user_id}&inline_message_id=${inline_message_id}`;
    let response = await fetch(url);

    if (response.ok) {
        for (let record of await response.json()) {
            if (record.user.id == user_id) {
                max_score = record.score;
            }
            table.innerHTML += `<li class="row ${(record.user.id == user_id) ? "you" : ""}"><span class="position">${record.position}.</span><span class="score">${record.score}</span><div class="name">${record.user.first_name} ${record.user.last_name}</div></li>`;
        }
        table.classList.add('show');
    }
}

get_table();