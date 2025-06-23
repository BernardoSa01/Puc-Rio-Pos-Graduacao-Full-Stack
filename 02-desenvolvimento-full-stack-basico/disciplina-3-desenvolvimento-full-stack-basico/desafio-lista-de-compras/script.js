// Create a mew item in the list
function newElement() {
  let li = document.createElement('li')
  let inputValue = document.getElementById('newInput').value
  let t = document.createTextNode(inputValue)

  li.appendChild(t)

  if (inputValue === '') {
    alert('Escreva o nome de um item!')
  } else {
    document.getElementById('myList').appendChild(li)
  }

  document.getElementById('newInput').value = ''
}