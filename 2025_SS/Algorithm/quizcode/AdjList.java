import java.util.ArrayList;
import java.util.List;

public class AdjList<T extends Edge> implements Graph {
    // 각 정점에 대해 연결된 간선 edge들의 리스트
    private List<List<T>> adjList;

    /* 생성자
        * 그래프를 정점 개수 numVertices로 초기화
        * 각 정점 i마다 빈 리스트를 생성하여 초기화
        * 결과적으로 adjList는 numVertices개의 리스트를 가지며, 아래처럼 구성됨
        * [ [], [], [], ..., [] ]
     */
    public AdjList(int numVertices) {
        adjList = new ArrayList<>(numVertices);
        for (int i = 0; i < numVertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }

    // edge 간선 추가: 정점 u에서 정점 v로 가는 간선(가중치 w)을 추가
    public void addEdge(int u, int v, double w) {
        adjList.get(u).add((T) new Edge(u, v, w, null));
    }

    // Returns a string representation of the adjacency list
    public String toString() {
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < adjList.size(); i++) {
            result.append("\n[").append(i).append("]: ");
            for (T edge : adjList.get(i)) {
                result.append(edge).append(" ");
            }
        }
        return result.toString();
    }
}