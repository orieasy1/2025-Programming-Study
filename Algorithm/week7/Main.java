import java.util.Arrays;
public class Main {
	public static void main(String[] args) {
        // Create a graph with 5 vertices
        AdjList<Edge> graph = new AdjList<>(5);
        graph.addEdge(0, 1, 1.0);
        graph.addEdge(0, 2, 1.0);
        graph.addEdge(1, 3, 1.0);
        graph.addEdge(1, 4, 1.0);
        graph.addEdge(2, 4, 1.0);

        System.out.println("Graph Representation:");
        System.out.println(graph);

        int[] dfsResult = graph.dfs(0);
        System.out.println("DFS Traversal from vertex 0:");
        System.out.println("[0, 1, 3, 4, 2]: "+Arrays.toString(dfsResult));
    }
}
