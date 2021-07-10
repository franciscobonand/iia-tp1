## Introdução

Neste trabalho prático, buscou-se a consolidação dos conceitos e posterior implementação de diferentes algoritmos de busca em espaço de estados, de forma a desenvolver habilidades para realização de uma análise comparativa entre tais algoritmos.

Com esse intuito, foram implementados algoritmos de busca sem informação (busca em profundidade (DFS), busca em largura (BFS) e busca de custo uniforme (Dijkstra)) e de busca com informação (busca gulosa e busca A*) a fim de obter o caminho ótimo para diferentes partidas do clássico jogo Pacman.

Neste documento será discutida a implementação de cada um dos algoritmos, assim como será feita uma análise comparativa do tempo de execução e do número de estados expandidos por cada um em diferentes layouts do jogo. É válido ressaltar que um estado considerado a solução/objetivo quando a "comida" do Pacman se encontra nele.

## Metodologia

Todos os algoritmos descritos a seguir tem sua base de implementação similar. Entende-se como "base similar" o fato de que, a partir de uma posição inicial (coordenada (X, Y) que representa onde o Pacman começará no labirinto), são verificadas as próximas posições que o Pacman pode visitar - ou seja, as coordenadas (X, Y) vizinhas à posição atual e que são válidas (não são paredes e estão dentro do labirinto).

Essa verificação de próximas posições válidas é referida nesse documento como "expansão". Os estados expandidos são armazenados em alguma estrutura, que varia de algoritmo para algoritmo, de forma que possam ser posteriormente verificados e recursivamente expandidos com o intuito de encontrar o caminhamento ótimo para a solução. Cada estado **pode** ser associado a um custo para que o Pacman se locomova até ele, de forma que algoritmos que utilizam heurísticas possam ser implementados.

### DFS

O algoritmo de busca em profundidade não utiliza heurísticas, portando o custo associado a cada estado expandido não é levado em consideração (considera-se custo 1 para toda ação, independente das ações anteriores). Dessa forma, em sua implementação os estados expandidos são armazenados em uma estrutura de pilha, que garante a lógica First In First Out, fazendo com que os estados sejam explorados de maneira "profunda". Espera-se que o número de estados expandidos seja menor que dos demais algoritmos, porém a solução encontrada não é necessariamente ótima.   

### BFS

A busca em largura também não utiliza heurísticas e o custo associado a cada estado não é levado em consideração (considera-se custo 1 para toda ação, independente das ações anteriores). A diferença entre esses dois algoritmos dá-se na estrutura utilizada para armazenamento dos estados expandidos, sendo que no BFS estes são armazenados em uma fila (e não em uma pilha), garantindo a lógica Last In First Out. Dessa forma, os estados serão analisados "em largura", e espera-se que um maior número de estados sejam expandidos, e que a solução encontrada seja ótima.

### Custo Uniforme

A busca de custo uniforme é similar à BFS, porém o custo é levado em consideração, de forma que o custo para que Pacman se mova de um ponto A para um ponto B é igual à soma dos custos para chegar a A somado ao custo de ir de A para B, sendo que o custo de cada ação individual é 1. Ou seja, se para ir da posição inicial ao ponto A foram dados sete passos, o custo de ir de A para B será $7 + 1 = 8$ .

Como os custos agora são levados em consideração, os estados expandidos são analisados conforme o custo referente a cada um deles. Dessa forma, a estrutura utilizada para armazenamento dos estados expandidos é uma fila de prioridades, que garante que o próximo estado a ser explorado é aquele de menor custo. Espera-se que sejam expandidos menos estados que na BFS, e que a solução encontrada também seja ótima

### Busca gulosa

Na busca gulosa os custos de cada ação também são levados em consideração, e os estados expandidos são armazenados em uma fila de prioridades. Todavia, o custo de cada ação é definido apenas pela heurística utilizada, e não leva em consideração os custos das ações anteriores. Espera-se que o algoritmo implementado seja completo (que a solução, caso exista, seja encontrada), dado que a implementação garante que não *loops* não ocorrerão - um estado não será expandido e visitado mais de uma vez. Todavia não há garantias que a solução encontrada seja ótima.

### A*

O A* pode ser visto como a "junção" dos dois algoritmos descritos anteriormente, dado que os estados expandidos também são armazenados em uma fila de prioridades e que o custo associado a cada estado é o valor definido pela heurística somado ao custo de movimentação para chegar ao estado atual. Ou seja, se para ir da posição inicial a um ponto A foram dados sete passos e o valor da heurística para o estado A é $h(A) = 20$, o custo referente ao estado A é $7 + 20 = 27$ .

### Heurística proposta

Foi criada uma nova heurística para ser utilizada pelo algoritmo A* em labirintos que possuem um ou mais objetivos (labirintos com diversas "comidas" do Pacman). Essa heurística, denominada `foodHeuristic`, é simples e de fácil compreensão, e funciona da seguinte forma:

Primeiramente, recebe como entrada a coordenada (X, Y) do estado a ser analisado e uma matriz que descreve o labirinto (nela estão contidas as posições de cada uma das comidas do Pacman). Essa matriz, por sua vez, é convertida em uma lista de coordenadas (Xi, Yi) que representam as posições de cada um dos objetivos. O valor total da heurística é armazenado na variável `score`, que é inicialmente definida como zero.

Em seguida, itera-se por essa lista e, a cada iteração, calcula-se a [distância de Manhattan](https://pt.wikipedia.org/wiki/Geometria_do_t%C3%A1xi) entre o objetivo em questão e a coordenada (X, Y) do estado analisado, e soma-se esse resultado ao `score`. Após iterar por toda a lista, o valor de `score` é retornado.

Ou seja, o valor calculado pela heurística consiste no custo total de, saindo do estado analisado, atingir todos os objetivos do problema (ou "comidas" do labirinto). Essa heurística é admissível e consistente, dado que é basicamente a aplicação da heurística de distância de Manhattan, que é admissível e consistente, nos múltiplos objetivos do problema:

- **Admissível**, porque o custo real para atingir o objetivo em um jogo de Pacman é igual à distância de Manhattan entre a coordenada atual do Pacman e a coordenada da "comida" em um labirinto sem paredes. Em um labirinto com paredes, o custo real é maior do que a distância de Manhattan, dado que pode ser necessário dar mais passos para "contornar" uma parede.
- **Consistente**, porque a soma da distância de Manhattan com o custo para chegar no estado atual (número de passos) garantem que o caminho até determinado estado é ótimo/de menor custo.

## Análise Experimental

Primeiramente, serão analisados o custo de cada algoritmo e a quantidade de nós expandidos por cada um em três labirintos diferentes do jogo Pacman. Para os algoritmos que utilizam heurísticas, a distância de Manhattan foi a heurística escolhida para a análise.

Todas as instâncias do problema foram executadas em um laptop Intel Inspiron 5590, com 16GB de memória RAM e processador Intel I7-10510U 4,9GHz.

### Tiny Maze

![image-20210710162222704](/home/franciscobonand/.config/Typora/typora-user-images/image-20210710162222704.png)

![image-20210710161623762](/home/franciscobonand/.config/Typora/typora-user-images/image-20210710161623762.png) 

### Medium Maze

![image-20210710162345535](/home/franciscobonand/.config/Typora/typora-user-images/image-20210710162345535.png)

![image-20210710161656955](/home/franciscobonand/.config/Typora/typora-user-images/image-20210710161656955.png)

### Big Maze

![image-20210710162427485](/home/franciscobonand/.config/Typora/typora-user-images/image-20210710162427485.png)

![o](/home/franciscobonand/.config/Typora/typora-user-images/image-20210710161754961.png)

#### Análise dos resultados acima

Os resultados exibidos nas tabelas e gráficos acima ficaram de acordo com o esperado e descrito no tópico "Metodologia". A busca em profundidade e a busca gulosa foram as que tiveram um menor número de nós expandidos, mas também pode ser observado que elas não necessariamente resultam em uma solução ótima/de menor custo (como demonstrado no labirinto Medium Maze). Além disso, dentre os algoritmos ótimos, todos realmente encontraram a solução ótima/de custo mínimo, e o A* foi aquele que demandou um menor número de estados expandidos para encontrar tal solução. 

Vale ressaltar que a coluna "Score" nas tabelas é referente à pontuação total da partida de Pacman, e apesar de não ter sido utilizada nos gráficos devido à sua redundância com a coluna "Cost", ela reitera que os algoritmos DFS e busca gulosa não encontram necessariamente uma solução ótima.

#### Heurística criada

A heurística `foodHeuristic` implementada, que se baseia na distância de Manhattan, apresentou resultados positivos e surpreendentes. Para o labirinto Tricky Search, foram expandidos apenas 5423 estados em um período de 2.2 segundos resultando em um custo total de 60, e para o labirinto Medium Search foram expandidos 4826 estados em um período de 2.7 segundos resultando em um custo total de 994. Seguem os resultados:

**Tricky Search:**

![image-20210710164749969](/home/franciscobonand/.config/Typora/typora-user-images/image-20210710164749969.png)

**Medium Search:**

![image-20210710164810950](/home/franciscobonand/.config/Typora/typora-user-images/image-20210710164810950.png)

## Conclusão

Este trabalho possibilitou um entendimento mais profundo de cada um dos algoritmos de busca estudados em aula, assim como reiterou a teoria ensinada de cada um dos algoritmos. Pode-se observar de forma prática os pontos positivos e negativos de cada algoritmo, assim como compará-los utilizando dados e problemas reais.

Além disso, incentivou a pesquisa e análise para implementação de uma nova heurística, que se mostrou como algo desafiador e que demanda diversas "revisitas", de forma a testar novas ideias e remodelagens para otimizar o resultado obtido.

## Bibliografia

- Slides e videoaulas da disciplina
- Diversas referências ao problema do Pacman em Python:
  - https://github.com/jacobic/Pac-ManAI
  - https://github.com/thiadeliria/Pacman
  - https://www.cs.utexas.edu/~pstone/Courses/343spring10/assignments/search/search.html
  - https://www.programmersought.com/article/16466070876/
  - https://stackoverflow.com/questions/62223346/python-pacman-heuristic-is-not-consistent
  - https://courses.cs.washington.edu/courses/cse473/18wi/assignments/project1/project.html



