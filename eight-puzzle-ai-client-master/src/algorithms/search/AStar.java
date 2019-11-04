package algorithms.search;

import algorithms.AStarNode;
import algorithms.Algorithm;

import java.util.*;

public class AStar implements Algorithm {
    private PriorityQueue<AStarNode> frontier = new PriorityQueue<>((o1, o2) -> Integer.compare(o2.getH() + o2.getLevel(), o1.getH() + o1.getLevel()));
    private Queue<AStarNode> explored = new LinkedList<>();
    private Stack<String> routes = new Stack<>();
    private AStarNode initialNode;

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
        this.initialNode = new AStarNode(null, null, grid, 0);
        frontier.add(this.initialNode);
    }

    private void findPath() {
        while (!frontier.isEmpty()) {
            AStarNode aStarNode = frontier.poll();
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
                if (!(frontier.contains(child) || explored.contains(child))) {
                    if (AStarNode.finalNode.equals(child)) {
                        AStarNode n = child;
                        while (n.getParent() != null) {
                            routes.push(n.getMovement());
                            n = n.getParent();
                        }
                        return;
                    }
                    boolean goodChild1 = true;
                    for (AStarNode node :
                            frontier) {
                        if (node.getLevel() == child.getLevel() && node.getH() < child.getH()) {
                            goodChild1 = false;
                            break;
                        }
                    }
                    if (!goodChild1) {
                        continue;
                    }
                    boolean goodChild2 = true;
                    for (AStarNode node :
                            explored) {
                        if (node.getLevel() == child.getLevel() && node.getH() < child.getH()) {
                            goodChild2 = false;
                            break;
                        }
                    }
                    if (!goodChild2) {
                        continue;
                    }
                    frontier.add(child);
                }
            }
            explored.add(aStarNode);
        }
    }
}
