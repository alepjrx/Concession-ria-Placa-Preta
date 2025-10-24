document.addEventListener('DOMContentLoaded', () => {
    
//url do endpoint da nossa API que lista os carros
    const apiUrl = 'http://127.0.0.1:8000/carros/';

//usamos a id que foi definida no html para pegar a caixa dos carros
    const carrosContainer = document.getElementById('carros-container');

//função para adicionar os listeners (escutadores de clique)
    function adicionarListenersDeletar() {
        const botoesDeletar = document.querySelectorAll('.btn-deletar');

        botoesDeletar.forEach(botao => {
            botao.addEventListener('click', () => {
                const carroId = botao.dataset.id;

                if (confirm(`Tem certeza que deseja deletar o carro com ID ${carroId}?`)){
                    fetch(`${apiUrl}${carroId}`, {
                        method: 'DELETE',
                    })
                    .then(response => {
                        if (!response.ok){
                            throw new Error('Falha ao deletar o carro.');
                        }

                        alert('Carro deletado com sucesso!');
                        location.reload();
                    })
                    .catch(error => {
                        console.error('Erro ao deletar:', error);
                        alert('Não foi possível deletar o carro');
                    });
                }
            });
        });
    }

//fetch é a ferramenta do js pra fazer as requisições da api, é o que o /docs faz por baixo dos panos
    fetch(apiUrl)
        .then(response => {
            if (!response.ok){
                throw new Error(`Erro na requisição: ${response.status}`);
            }
            return response.json();
        })
        .then(listaDeCarros => {

//a segunda etapa nos dá os dados em json (a lista de carros)

//primeiro limpamos a mensagem "Carregando estoque...""
            carrosContainer.innerHTML = '';

//se a lista estiver vazia, tratamos isso
            if (listaDeCarros.length === 0){
                carrosContainer.innerHTML = '<p>Nenhum carro no estoque no momento.</p>';
                return;
            }
//pra cada carro na lista
            listaDeCarros.forEach(carro => {
//criamos um novo elemento html
                const card = document.createElement('div');
//adicionamos uma classe css pra estilizar depois
                card.className = 'card-carro';
//montamos o conteudo html do card com os dados do carro
                card.innerHTML = `
                    <h3>${carro.marca} ${carro.modelo}</h3>
                    <p>Ano: ${carro.ano}</p>
                    <p>Preço: R$ ${carro.preco.toLocaleString('pt-BR')}</p>
                    <button class="btn-deletar" data-id="${carro.id}">Deletar Carro</button>
                `;

                carrosContainer.appendChild(card);
            });

            // Chamamos a função para adicionar os listeners DEPOIS que os cards foram criados.
            adicionarListenersDeletar();
        })
        .catch(error => {
//apanhar um erro que pode rolar tipo de API fora do ar etc
            console.error('Falha ao buscar carros: ', error);
            carrosContainer.innerHTML = '<p>Não foi possível carregar o estoque. Verifique se a API está no ar.</p>';
        });
});