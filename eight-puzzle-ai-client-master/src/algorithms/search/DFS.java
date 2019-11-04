package algorithms.search;

import algorithms.Algorithm;
import algorithms.Node;

import java.util.Stack;

public class DFS implements Algorithm {
    private int depth = 0;
    private Stack<Node> nodeStack = new Stack<>();
    private Node initialNode;

    @Override
    public String makeMove(String[][] grid) {
        String result = null;
        if (this.initialNode == null) {
            createInitialNode(grid);
            findPath();
        }
        return result;
    }

    private void createInitialNode(String[][] grid) {
        this.initialNode = new Node(null, null, grid, 0);
        nodeStack.push(this.initialNode);
    }

    private void findPath() {

    }
}
