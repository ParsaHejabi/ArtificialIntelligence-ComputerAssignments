package algorithms.search;

import algorithms.Algorithm;
import algorithms.Node;

import java.util.LinkedList;
import java.util.Queue;
import java.util.Stack;

public class BFS implements Algorithm {
    private Queue<Node> frontier = new LinkedList<>();
    private Queue<Node> explored = new LinkedList<>();
    private Stack<String> routes = new Stack<>();
    private Node initialNode;

    @Override
    public String makeMove(String[][] grid) {
        String result;
        if (this.initialNode == null) {
            createInitialNode(grid);
            findPath();
        }
        result = routes.pop();
        return result;
    }

    private void createInitialNode(String[][] grid) {
        this.initialNode = new Node(null, null, grid, 0);
        frontier.add(this.initialNode);
    }

    private void findPath() {
        while (!frontier.isEmpty()) {
            Node node = frontier.remove();
            explored.add(node);
            Node child = null;
            for (Node.possibleMoves move : Node.possibleMoves.values()) {
                switch (move) {
                    case LEFT:
                        child = Node.left(node);
                        break;
                    case UP:
                        child = Node.up(node);
                        break;
                    case RIGHT:
                        child = Node.right(node);
                        break;
                    case DOWN:
                        child = Node.down(node);
                        break;
                }
                if (!(frontier.contains(child) || explored.contains(child))) {
                    if (Node.finalNode.equals(child)) {
                        Node n = child;
                        while (n.getParent() != null) {
                            routes.push(n.getMovement());
                            n = n.getParent();
                        }
                        return;
                    }
                    frontier.add(child);
                }
            }
        }
    }
}
