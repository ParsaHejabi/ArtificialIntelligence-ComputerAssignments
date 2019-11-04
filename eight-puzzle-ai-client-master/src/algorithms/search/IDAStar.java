package algorithms.search;

import algorithms.AStarNode;
import algorithms.Algorithm;

import java.util.PriorityQueue;
import java.util.Stack;

public class IDAStar implements Algorithm {
    private PriorityQueue<AStarNode> frontier = new PriorityQueue<>((o1, o2) -> Integer.compare(o2.getH() + o2.getLevel(), o1.getH() + o1.getLevel()));
    private Stack<String> routes = new Stack<>();
    private AStarNode initialNode;

    @Override
    public String makeMove(String[][] grid) {
        String result;
        if (this.initialNode == null) {
            createInitialNode(grid);
            search();
        }
        result = routes.pop();
        return result;
    }

    private void createInitialNode(String[][] grid) {
        this.initialNode = new AStarNode(null, null, grid, 0);
        frontier.add(this.initialNode);
    }

    private void search() {
        int currentFBound = initialNode.getH();
        while (currentFBound != Integer.MAX_VALUE) {
            int newFBound = findPath(currentFBound);

            if (newFBound == 0) {
                return;
            }

            currentFBound = newFBound;
        }
    }

    private int findPath(int currentFBound) {
        if (!frontier.isEmpty()) {
            AStarNode aStarNode = frontier.peek();
            if (aStarNode.getLevel() + aStarNode.getH() > currentFBound) {
                return aStarNode.getLevel() + aStarNode.getH();
            }
            if (AStarNode.finalNode.equals(aStarNode)) {
                AStarNode n = aStarNode;
                while (n.getParent() != null) {
                    routes.push(n.getMovement());
                    n = n.getParent();
                }
                return 0;
            }
            int newFBound = Integer.MAX_VALUE;
            AStarNode child = null;
            for (AStarNode.possibleMoves move : AStarNode.possibleMoves.values()) {
                switch (move) {
                    case LEFT:
                        child = AStarNode.left(aStarNode);
                        break;
                    case UP:
                        child = AStarNode.up(aStarNode);
                        break;
                    case RIGHT:
                        child = AStarNode.right(aStarNode);
                        break;
                    case DOWN:
                        child = AStarNode.down(aStarNode);
                        break;
                }
                if (!frontier.contains(child)) {
                    frontier.add(child);
                    int minFOverBound = findPath(currentFBound);
                    if (minFOverBound == 0) {
                        return 0;
                    }
                    if (minFOverBound < newFBound) {
                        newFBound = minFOverBound;
                    }
                    frontier.poll();
                }
            }
            return newFBound;
        } else {
            return Integer.MAX_VALUE;
        }
    }
}
