public class Edge implements Comparable<Edge> {
    int u, v;
    double weight;
    Edge next;

    // Constructor initializes an edge with vertices and weight
    public Edge(int x, int y, double w, Edge next) {
        this.u = x;
        this.v = y;
        this.weight = w;
        this.next = next;
    }

    // Returns the tail vertex of the edge
    public int getTail() {
        return u;
    }

    // Returns the head vertex of the edge
    public int getHead() {
        return v;
    }

    // Returns the weight of the edge
    public double getWeight() {
        return weight;
    }

    // Compares edges based on their weights
    public int compareTo(Edge e) {
        return Double.compare(this.weight, e.weight);
    }

    // Returns a string representation of the edge
    public String toString() {
        return "(" + u + "->" + v + "): " + weight;
    }
}