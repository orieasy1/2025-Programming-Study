import java.util.*;

public class AdjMatrix implements Graph<Edge> {
    // 정점 간의 연결(간선) 정보를 2차원 배열(matrix)로 저장
    private double[][] matrix;
    // 정점 개수
    private int numVertices;

    /* 생성자
     * 정점 수를 받아 인접 행렬 초기화
     * 모든 값을 0.0으로 초기화하여 간선이 없음을 나타냄
     */
    public AdjMatrix(int numVertices) {
        this.numVertices = numVertices;
        matrix = new double[numVertices][numVertices];
        for (int i = 0; i < numVertices; i++) {
            Arrays.fill(matrix[i], 0.0);
        }
    }

    /* 간선 edge 추가
     * 유효한 정점 번호인지 확인
     * 정점 u에서 정점 v로 가는 간선의 가중치 weight를 설정
     */
    @Override
    public void addEdge(int u, int v, double weight) {
        if (u < 0 || u >= numVertices || v < 0 || v >= numVertices) {
            throw new IllegalArgumentException("Vertex number out of bounds");
        }
        matrix[u][v] = weight; // Set weight for the directed edge
    }

    // Checks if there is an edge between two vertices
    public boolean hasEdge(int u, int v) {
        return matrix[u][v] != 0;
    }

    // Returns the weight of the edge between two vertices
    public double getEdgeWeight(int u, int v) {
        return matrix[u][v];
    }

    // Returns a string representation of the adjacency matrix
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < numVertices; i++) {
            for (int j = 0; j < numVertices; j++) {
                sb.append(String.format("%8.2f", matrix[i][j])).append(" ");
            }
            sb.append("\n");
        }
        return sb.toString();
    }
}