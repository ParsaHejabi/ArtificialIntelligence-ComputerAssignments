package algorithms;

public class Node {
    private static int mapSize;
    private Node parent;
    private String movement;
    private String[][] grid;
    private int xBlank, yBlank;
    private int level;

    public enum possibleMoves {
        LEFT, UP, RIGHT, DOWN
    };

    private static final String[][] finalGrid = {
            {"1", "2", "3"},
            {"4", "5", "6"},
            {"7", "8", " "}
    };

    public static final Node finalNode = new Node(null, null, Node.finalGrid, 0);

    public Node(Node parent, String movement, String[][] grid, int level) {
        if (mapSize == 0) {
            mapSize = grid.length;
        }
        this.parent = parent;
        this.movement = movement;
        this.grid = grid;
        int[] blankCoordinators = this.getXAndY(" ");
        this.xBlank = blankCoordinators[1];
        this.yBlank = blankCoordinators[0];
        this.level = level;
    }

    public Node getParent() {
        return parent;
    }

    public String getMovement() {
        return movement;
    }

    public String[][] getGrid() {
        return grid;
    }

    public int getXBlank() {
        return xBlank;
    }

    public int getYBlank() {
        return yBlank;
    }

    public int getLevel() {
        return level;
    }

    private int[] getXAndY(String num) {
        int[] result = new int[2];

        for (int i = 0; i < mapSize; i++) {
            for (int j = 0; j < mapSize; j++) {
                if (grid[i][j].equals(num)) {
                    result[0] = i;
                    result[1] = j;
                    break;
                }
            }
        }
        return result;
    }

    public static Node left(Node node) {
        if (node.getXBlank() == 0) {
            return node;
        } else {
            String[][] newGrid = Node.duplicateGrid(node.getGrid());
            String target = newGrid[node.getYBlank()][node.getXBlank() - 1];
            newGrid[node.getYBlank()][node.getXBlank() - 1] = " ";
            newGrid[node.getYBlank()][node.getXBlank()] = target;
            return new Node(node, "left", newGrid, node.level + 1);
        }
    }

    public static Node up(Node node) {
        if (node.getYBlank() == 0) {
            return node;
        } else {
            String[][] newGrid = Node.duplicateGrid(node.getGrid());
            String target = newGrid[node.getYBlank() - 1][node.getXBlank()];
            newGrid[node.getYBlank() - 1][node.getXBlank()] = " ";
            newGrid[node.getYBlank()][node.getXBlank()] = target;
            return new Node(node, "up", newGrid, node.level + 1);
        }
    }

    public static Node right(Node node) {
        if (node.getXBlank() == mapSize - 1) {
            return node;
        } else {
            String[][] newGrid = Node.duplicateGrid(node.getGrid());
            String target = newGrid[node.getYBlank()][node.getXBlank() + 1];
            newGrid[node.getYBlank()][node.getXBlank() + 1] = " ";
            newGrid[node.getYBlank()][node.getXBlank()] = target;
            return new Node(node, "right", newGrid, node.level + 1);
        }
    }

    public static Node down(Node node) {
        if (node.getYBlank() == mapSize - 1) {
            return node;
        } else {
            String[][] newGrid = Node.duplicateGrid(node.getGrid());
            String target = newGrid[node.getYBlank() + 1][node.getXBlank()];
            newGrid[node.getYBlank() + 1][node.getXBlank()] = " ";
            newGrid[node.getYBlank()][node.getXBlank()] = target;
            return new Node(node, "down", newGrid, node.level + 1);
        }
    }

    private static String[][] duplicateGrid(String[][] grid) {
        String[][] newGrid = new String[mapSize][mapSize];
        for (int i = 0; i < mapSize; i++) {
            System.arraycopy(grid[i], 0, newGrid[i], 0, mapSize);
        }
        return newGrid;
    }

    @Override
    public boolean equals(Object obj) {
        Node inputNode;
        if (obj instanceof Node) {
            inputNode = (Node) obj;
        } else {
            return false;
        }
        for (int i = 0; i < mapSize; i++) {
            for (int j = 0; j < mapSize; j++) {
                if (!this.grid[i][j].equals(inputNode.grid[i][j])) {
                    return false;
                }
            }
        }
        return true;
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < mapSize; i++) {
            for (int j = 0; j < mapSize; j++) {
                result.append(this.grid[i][j]).append('\t');
            }
            result.append('\n');
        }
        return result.toString();
    }
}
