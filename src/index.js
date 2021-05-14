let wrapper = document.getElementById('wrapper')
let control = document.getElementById('button1')

control.addEventListener('click', () => {
    wrapper.classList.remove('in-greeting');
    wrapper.classList.toggle('in-game');
    wrapper.classList.toggle('in-result');
})