import java.util.ArrayList;
import java.util.List;

public class AdjList<T extends Edge> implements Graph {
    // 모든 간선의 리스트
    private List<List<T>> adjList;

    /* 생성자
     * 그래프의 정점 수를 받아 인접리스트를 초기화
     * 각 정점마다 빈 리스트를 생성하여 간선을 저장할 준비를 함
     * [ [], [], [], [], [] ] 해당 형태의 리스트를 생성
     */
    public AdjList(int numVertices) {
        adjList = new ArrayList<>(numVertices);
        for (int i = 0; i < numVertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }

    /* 단방향 간선을 추가하는 메소드
     * u: 시작 정점, v: 도착 정점, w: 가중치
     * 주어진 정점 u에서 v로 가는 간선을 추가
     * edge 객체를 생성하여 해당 정점의 리스트에 추가
     */
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

	@Override
	public int[] bfs(int start) {
		// TODO Auto-generated method stub
		return null;
	}

    @Override
    public int[] dfs(int start) {
        // 정점 방문 여부 저장, 중복 방문 방지
        boolean[] visited = new boolean[adjList.size()];
        // 탐색 순서를 저장하는 동적 리스트
        List<Integer> traversal = new ArrayList<>();
        // DFS 알고리즘의 실제 로직이 수행되는 재귀 함수 호출
        dfsRecursive(start, visited, traversal);

        // 리스트를 배열로 변환
        // 반환 형식을 요구된 int[]로 맞추기 위해 변환
        int[] result = new int[traversal.size()];
        for (int i = 0; i < traversal.size(); i++) {
            result[i] = traversal.get(i);
        }
        return result;
    }

    // 깊이 우선 탐색 재귀 함수
    private void dfsRecursive(int current, boolean[] visited, List<Integer> traversal) {
        //현재 정점을 방문 표시
        visited[current] = true;
        // 현재 정점을 방문 순서에 기록
        traversal.add(current);

        // 현재 정점과 연결된 모든 간선을 순회
        for (T edge : adjList.get(current)) {
            int neighbor = edge.getHead(); // 간선의 도착 정점
            // 방문하지 않은 정점인 경우에만 재귀 호출(DFS 재귀탐색 수행)
            if (!visited[neighbor]) {
                dfsRecursive(neighbor, visited, traversal);
            }
        }
    }

}