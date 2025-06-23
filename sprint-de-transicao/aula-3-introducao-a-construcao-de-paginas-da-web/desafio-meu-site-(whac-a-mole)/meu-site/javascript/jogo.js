/*    Variáveis    */

// Quantidade de acertos
var acertos
acertos = 0 

// Quantidade de toupeiras perdidas
var perdidos = 0 

// Quantidade de marteladas erradas
var errados = 0 

// Tempo entre cada toupeira sair do buraco (em 'ms')
var intervalo = 5000 

// Tempo que a toupeira ficará fora do buraco (em 'ms')
var janela = 2000

// Timer que controla o tempo da toupeira fora do buraco 
var timer = null 

/*    Eventos    */

onload = function () {
  document.getElementById('start').addEventListener('click', start)
  document.getElementById('idGramado').addEventListener('mousedown', marteloBaixo)
  document.getElementById('idGramado').addEventListener('mouseup', marteloCima)
  document.getElementById('buraco0').addEventListener('click', martelada)
  document.getElementById('buraco1').addEventListener('click', martelada)
  document.getElementById('buraco2').addEventListener('click', martelada)
  document.getElementById('buraco3').addEventListener('click', martelada)
  document.getElementById('buraco4').addEventListener('click', martelada)
}


/*    Funções    */

function start() { 
  var botao = document.getElementById('start')

  botao.removeEventListener('click', start)
  botao.disable = true

  sobeToupeira()
}

function sobeToupeira() {
  var buraco = Math.floor(Math.random() * 5)
  var objBuraco = document.getElementById('buraco' + buraco) 
  objBuraco.src = 'images/hole-mole.png'
  timer = setTimeout(tiraToupeira, janela, buraco)
  setTimeout(sobeToupeira, intervalo) 
}

function tiraToupeira(buraco) {
  var objBuraco = document.getElementById('buraco' + buraco)
  objBuraco.src = 'images/hole.png'
  perdidos++
  mostraPontuacao()  
}

function mostraPontuacao() {
  mostraPontuacaoDe('acertos', acertos)
  mostraPontuacaoDe('perdidos', perdidos)
  mostraPontuacaoDe('errados', errados)
  mostraPontuacaoDe('saldo', Math.max(acertos - perdidos - errados, 0))
}

function mostraPontuacaoDe(display, valor) {
  // Pegando as imagens
  let objCentena = document.getElementById(display).firstChild
  let objDezena = objCentena.nextSibling
  let objUnidade = objDezena.nextSibling

  // Calcula o valor de cada algarismo
  let centena = parseInt(valor/100)
  let dezena = parseInt((valor/10) % 10)
  let unidade = (valor % 10)

  // Muda a imagem e o valor do atributo para leitores de tela
  objCentena.src = 'images/caractere_' + centena + '.gif'
  objCentena.alt = centena 

  objDezena.src = 'images/caractere_' + dezena + '.gif'
  objDezena.alt = dezena

  objUnidade.src = 'images/caractere_' + unidade + '.gif'
  objUnidade.alt = unidade 
}

function marteloBaixo() {
  document.getElementById('idGramado').style.cursor = 'url(images/hammerDown.png), default'
}

function marteloCima() {
  document.getElementById('idGramado').style.cursor = 'url(images/hammer.png), default'
}

function martelada(evento) {
  if (evento.target.src.includes('hole-mole')) {
    // Acertou
    acertos++ 
    evento.target.src = 'images/hole.png'
    clearTimeout(timer)
  } else {
    // Errou
    errados++
  }
  mostraPontuacao()
}
