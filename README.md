# Atividade Prática 1 (Computação Gráfica, DCC UFRJ, 2021.1 remoto)

Este trabalho foi desenvolvido com o intuito de praticar os conhecimentos adiquiridos durante o curso de Computação Gráfica. O código foi escrito utilizando Python 3.7.9, com a biblioteca NumPy.

Para propósito de organização e encapsulamento, o trabalho foi desenvolvido utilizando a programação orientada a objetos, e as classes forem distribuidas por diversos arquivos. Este README irá detalhar a implementação escolhida. Para o propósito de documentação e prática com o Python, foi feito uso extensivo da biblioteca "typing".

## Rodando o programa

Para rodar o trabalho, basta executar o arquivo "main.py" utilizando o Python e seguir as instruções que serão disponibilizadas no console.

## Implementação das primitivas gráficas

As primitivas foram implementadas como classes, disponíveis dentro do pacote "primitives". As classes implementadas foram Circle, Polygon e ConvexPolygon. Elas extendem a classe abstrata Primitive.

### Circle

Para determinar se um ponto está dentro de um círculo, é verificado, utilizando a função umpy.lingalg.norm(), se a distância entre o ponto e o centro do círculo é menor que o raio do círculo. Para círculos que sofreram alguma transformação afim, é calculada a inversa da transformação afim e esta é aplicada ao ponto que está sendo verificado. A distância entre esse ponto transformado e o centro do círculo é então calculada.

### Polygon

Para determinar se um ponto está dentro de um polígono qualquer, utilizamos o algoritmo de *winding number*. Para polígonos transformados, guardamos os seus vértices transformados e rodamos o algoritmo usando esses novos pontos.

### ConvexPolygon

Essa classe é utilizada para triângulos. Para verificar se um ponto P está contido no polígino convexo, utilizamos a técnica do produto vetorial (verificamos se os produtos vetoriais entre todas as arestas AB do polígono e os vetores AP têm o mesmo sinal).

## Implementação da bounding box

A bounding box de uma primitiva é representada pela classe BoundingBox. Está contém apenas os valores máximos e mínimos das componentes, para cada dimensão, entre todos os pontos contidos na primitiva. Essa classe também oferece um método para a aplicação de uma transformação afim.

## Implementação das transformações afins

As transformações afins são representadas pela classe AffineTransform, cujo método apply irá aplicar a transformação em um vetor 2D (adicionando uma coordenada homogênea e depois removendo-a quando o vetor resultante é retornado).
