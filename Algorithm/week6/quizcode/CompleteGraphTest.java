public class CompleteGraphTest {
    public static void main(String[] args) {
        int numNodes = 3;
        int numEdges = numNodes * (numNodes - 1) / 2;

        // 각 그래프 표현 객체 생성
        AdjList adjListGraph = new AdjList(numNodes);
        AdjMatrix adjMatrixGraph = new AdjMatrix(numNodes);
        IncMatrix incMatrixGraph = new IncMatrix(numNodes, numEdges);  // 수정 포인트

        // 완전 그래프 구성
        int edgeCount = 0;
        for (int i = 0; i < numNodes; i++) {
            for (int j = i + 1; j < numNodes; j++) {
                adjListGraph.addEdge(i, j, 1.0);
                adjListGraph.addEdge(j, i, 1.0);

                adjMatrixGraph.addEdge(i, j, 1.0);
                adjMatrixGraph.addEdge(j, i, 1.0);

                incMatrixGraph.addEdge(i, j, 1.0);  // 한 번만 추가
                edgeCount++;
            }
        }

        // 출력
        System.out.println("Adjacency List Representation:");
        System.out.println(adjListGraph.toString());

        System.out.println("\nAdjacency Matrix Representation:");
        System.out.println(adjMatrixGraph.toString());

        System.out.println("\nIncidence Matrix Representation:");
        System.out.println(incMatrixGraph.toString());
    }
}
