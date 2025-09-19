public class IncMatrix implements Graph {
    // 정점 x 간선 수의 2차원 인시던스 행렬
    private double[][] m;
    // 현재 추가된 간선 개수, 새로운 간선이 열로 추가될 때마다 증가
    private int cur;

    /* 생성자
     * 정점 수 numVertices와 간선 수 numEdges를 받아 인시던스 행렬 초기화
     * m[i][j]는 i번 정점이 j번 edge와 어떤 관계인지 나타넴
     */
    public IncMatrix(int numVertices, int numEdges) {
        m = new double[numVertices][numEdges];
        cur = 0;
    }

    /* 간선 추가
     * 정점 u에서 v로 가는 간선 추가
     * 방향을 명시하기 위해 부호 사용
     * m[u][cur]는 간선의 꼬리(출발점)로서 음수로 저장
     * m[v][cur]는 간선의 머리(도착점)로서 양수로 저장
     */
    public void addEdge(int u, int v, double weight) {
        m[u][cur] = -weight; // Use negative weight for the tail
        m[v][cur] = weight;  // Use positive weight for the head
        cur++;
    }

    // Returns a string representation of the incidence matrix
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (double[] row : m) {
            for (double value : row) {
                sb.append(String.format("%6.2f ", value));
            }
            sb.append("\n");
        }
        return sb.toString();
    }
}