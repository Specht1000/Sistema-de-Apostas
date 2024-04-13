
const numerosDiv = document.getElementById("numeros");
const nomeInput = document.getElementById("nome"); // Assumindo que você tem um input com id 'nome'
const cpfInput = document.getElementById("cpf"); // Assumindo que você tem um input com id 'cpf'
const numerosEscolhidosInput =
document.getElementById("numeros_escolhidos");
const form = document.getElementById("apostaForm"); // Assumindo que o id do seu formulário é 'apostaForm'
let numeros_escolhidos = [];
const surpresinhaBtn = document.getElementById("surpresinhaBtn");

surpresinhaBtn.addEventListener("click", () => {

  numeros_escolhidos = []; // Limpa os números escolhidos pelo usuário

    while(numeros_escolhidos.length < 5){
      const numeros_sorteados = Math.floor(Math.random() * 50) + 1; // Gera números aleatório entre 1 e 50
      if(!numeros_escolhidos.includes(numeros_sorteados)) { // não pode ter números repetidos
        numeros_escolhidos.push(numeros_sorteados); // Coloca na lista
      }
    }

    document.querySelectorAll(".numero-btn").forEach((btn) => { // Atualiza a seleção de botões na interface
      if(numeros_escolhidos.includes(parseInt(btn.textContent))) {
        btn.classList.add("selected");
      } 
      else{
            btn.classList.remove("selected");
      }
    });

        numerosEscolhidosInput.value = numeros_escolhidos.join(","); // Atribui o input do usuário com os números escolhidos
        form.querySelector('input[type="submit"]').disabled = false;
});

function toggleNumeroSelecionado(numero){
  const i = numeros_escolhidos.indexOf(numero);
    if(i > -1){
      numeros_escolhidos.splice(i, 1); // Remove o número se já escolhido pelo usuário
    }
    else if(numeros_escolhidos.length < 5){
      numeros_escolhidos.push(numero); // Adiciona o número se menos de 5 números foram escolhidos
    }

    document.querySelectorAll(".numero-btn").forEach((btn) => { // Atualiza a exibição dos botões
      if(numeros_escolhidos.includes(parseInt(btn.textContent))) {
        btn.classList.add("selected");
      }
      else{
        btn.classList.remove("selected");
      }
    });

    numerosEscolhidosInput.value = numeros_escolhidos.join(","); // Atribui o input do usuário com os números escolhidos
    form.querySelector('input[type="submit"]').disabled =
    numeros_escolhidos.length !== 5;
}

for(let i = 1; i <= 50; i++){ // Cria 50 botões para os números de aposta organizados em 5 linhas de 10
  if(i % 10 === 1) {
    var linha = document.createElement("div");
    linha.classList.add("linha-numeros");
    numerosDiv.appendChild(linha);
}

    const btn = document.createElement("button");
    btn.textContent = i;
    btn.classList.add("numero-btn");
    btn.type = "button";
    btn.onclick = () => toggleNumeroSelecionado(i);
    linha.appendChild(btn);
}

      // Intercepta o evento de submissão do formulário e envia os dados usando fetch
form.addEventListener("submit", function (e) {
  e.preventDefault(); // Impede o envio padrão do formulário

  const nome = nomeInput.value;
  const cpf = cpfInput.value;
  const numeros = numeros_escolhidos.map(Number); // Converte os números escolhidos para inteiros
  const regexNome = /^[A-Za-z\s]+$/; // Verificar se o nome contém apenas letras e espaços
  // Expressão regular para verificar o CPF (exatamente 11 dígitos)
  const regexCpf = /^\d{11}$/; // Verifica se o CPF só tem digitos de 11 números

  if (!regexNome.test(nome)) {// Verifica se o nome é válido
      alert("O nome deve conter apenas letras e espaços.");
      return; 
  }
  if (!regexCpf.test(cpf)) { // Verifica se o CPF é válido
      alert("O CPF deve conter exatamente 11 números.");
      return;
  }

  fetch("/registrar_aposta", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({ nome, cpf, numeros }),
  })
    .then(response => response.json())
    .then(data => {
      alert(data.message);
        document.getElementById('mensagemSorteioContainer').style.display = 'none';
      })
});


document.getElementById("listarApostasBtn").addEventListener("click", function () {
  fetch("/listar_apostas")
      .then((response) => response.json())
      .then((apostas) => {
          const historico_div = document.getElementById("historicoApostas");
          historico_div.innerHTML = ""; // Limpa o histórico anterior

          apostas.forEach((aposta) => {
              const aposta_div = document.createElement("div");
              const numeros = typeof aposta.numeros === 'string' ? aposta.numeros.split(',') : aposta.numeros; // Converte um str parta vetor caso precise e os junta com vírgula
              aposta_div.innerHTML = `Nome: ${aposta.nome} | CPF: ${aposta.cpf} | Números: ${numeros.join(", ")} | Registro: ${aposta.numero_registro}`;
              historico_div.appendChild(aposta_div);
          });

          document.getElementById('historicoApostasContainer').style.display = 'block'; // Mostra o container do histórico de apostas
      })
      .catch((error) => { // Mensagens de erro
        alert(`Listagem não realizada. Nenhuma aposta registrada.`);
      });
});

document.getElementById('realizarSorteioBtn').addEventListener('click', function() {
  fetch('/realizar_sorteio')
      .then(response => response.json())
      .then(data => {  
          const mensagemFormatada = data.mensagem.replace(/\n/g, '<br>'); // Converte \n em <br> para ser lida em HTML
          const mensagemDiv = document.getElementById('mensagemSorteio'); // Encontra a div da mensagem e insere a mensagem formatada como HTML
          mensagemDiv.innerHTML = mensagemFormatada;  // Usa innerHTML para interpretar as tags <br>
          document.getElementById('mensagemSorteioContainer').style.display = 'block'; // Mostra o contêiner da mensagem
          document.getElementById('historicoApostasContainer').style.display = 'none'; // Oculta o histórico de apostas ao realizar o sorteio
      })
      .catch(error => {
          const mensagemDiv = document.getElementById('mensagemSorteio');
          mensagemDiv.textContent = 'Sorteio não realizado. Nenhuma aposta registrada.';
          document.getElementById('mensagemSorteioContainer').style.display = 'block';
      });
});