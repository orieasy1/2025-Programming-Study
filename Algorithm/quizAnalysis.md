# Basic Graph

그래프: 노드와 에지로 구성된 집합

- 노드: 데이터를 표현하는 단위
- 에지: 노드를 연결

Implement a Java program using the classes AdjList, AdjMatrix, and IncMatrix to construct a complete graph with 3 nodes. 
3개의 노드로 완전한 그래프 구성

A complete graph is a simple undirected graph in which a unique edge connects every pair of distinct vertices. 완전 그래프는 고유한 엣지가 모든 서로 다른 정점 쌍을 연결하는 단 순 무방향 그래프이다. Your implementation should confirm that the graph has been built correctly by utilizing each graph representation's toString() method. 각 그래프 표현의 toString() 방법을 활용하여 그래프가 올바르게 구축되었는지 확인해야 합니다.

Students will write a Java program named CompleteGraphTest that initializes three graph representations and populates them to form a complete graph with 3 nodes.

**Expected Result**

Adjacency List Representation:

[0]: (0->1): 1.0 (0->2): 1.0

[1]: (1->0): 1.0 (1->2): 1.0

[2]: (2->0): 1.0 (2->1): 1.0

Adjacency Matrix Representation:

0.00     1.00     1.00

1.00     0.00     1.00

1.00     1.00     0.00

Incidence Matrix Representation:

-1.00  -1.00   1.00   0.00   1.00   0.00

1.00   0.00  -1.00  -1.00   0.00   1.00

0.00   1.00   0.00   1.00  -1.00  -1.00

---

정점이 3개일 경우 연결 가능한 정점 쌍: (0,1) (0,2) (1,2) →  총 3개의 간선

무방향 그래프이므로 양방향으로 표현해야함: 0→1, 1→0 둘다 표현해야한다는 뜻

- `AdjList`, `AdjMatrix`, `IncMatrix`를 실제로 객체로 생성하고 사용해야 함
- `addEdge(i, j, w)` 메서드를 올바르게 호출해야 올바른 구조가 출력됨

`CompleteGraphTest.java`

```java
public class CompleteGraphTest {
    public static void main(String[] args) {
        int numNodes = 3;
        int numEdges = numNodes * (numNodes - 1) / 2;

        // 각 그래프 표현 객체 생성
        AdjList adjListGraph = new AdjList(numNodes);
        AdjMatrix adjMatrixGraph = new AdjMatrix(numNodes);
        IncMatrix incMatrixGraph = new IncMatrix(numNodes, numEdges);

        // 완전 그래프 구성
        int edgeCount = 0;
        for (int i = 0; i < numNodes; i++) {
            for (int j = i + 1; j < numNodes; j++) {
                adjListGraph.addEdge(i, j, 1.0);
                adjListGraph.addEdge(j, i, 1.0);

                adjMatrixGraph.addEdge(i, j, 1.0);
                adjMatrixGraph.addEdge(j, i, 1.0);

                incMatrixGraph.addEdge(i, j, 1.0); 
                
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

```

| 그래프 타입 | addEdge 호출 횟수 | 이유 |
| --- | --- | --- |
| `adjListGraph` | 2번 (`i→j`, `j→i`) | **인접 리스트**는 간선을 한쪽 방향만 저장하므로, **무방향 표현을 위해 양방향 모두 수동 추가**해야 함 |
| `adjMatrixGraph` | 2번 (`i→j`, `j→i`) | **인접 행렬**도 한 방향만 `matrix[i][j]`에 기록되므로, **대칭을 위해 `matrix[j][i]`도 따로 설정**해야 함 |
| `incMatrixGraph` | ❗1번 (`i→j`) | **부착 행렬**은 하나의 간선 열에 출발점/도착점을 모두 기록함. 즉, `m[i][cur] = -1`, `m[j][cur] = +1`으로 양쪽 정보가 **한 번에 처리**됨 |

`AdjList.java`

```java
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
```

`AdjMatrix.java`

```java
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
```

`IncMatrix.java`

```java
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
```