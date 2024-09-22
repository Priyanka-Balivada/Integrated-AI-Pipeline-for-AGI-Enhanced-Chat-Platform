import java.util.*;

public class Solution1 {
    // Method to compute the "next" array used in the KMP algorithm
    private static List<Integer> findNext(String pat) {
        int n = pat.length();
        List<Integer> next = new ArrayList<>(Collections.nCopies(n, 0));
        int len = 0;
        for (int i = 1; i < n;) {
            if (pat.charAt(i) == pat.charAt(len)) {
                ++len;
                next.set(i, len);
                i++;
            } else if (len == 0) {
                i++;
            } else {
                len = next.get(len - 1);
            }
        }
        return next;
    }

    // Method for breadth-first search
    private static String bfs(List<List<Pair>> dp, int len, int n) {
        Queue<State> queue = new LinkedList<>();
        queue.add(new State(0, ""));
        Set<State> visited = new HashSet<>();
        visited.add(new State(0, ""));

        while (!queue.isEmpty()) {
            State state = queue.poll();
            int curr = state.index;
            String path = state.path;

            if (path.length() == len) {
                return path;
            }

            char from = (path.length() < len && dp.get(path.length()).get(curr).s2 == '0') ? 'A'
                    : dp.get(path.length()).get(curr).s2;
            char to = from == '0' ? 'B' : from;

            for (char c = from; c <= to; c++) {
                int y = (curr == n) ? findNext(dp.get(0).get(0).s2 + "").get(curr - 1) : curr;
                while (y > 0 && c != dp.get(0).get(y).s2) {
                    y = findNext(dp.get(0).get(0).s2 + "").get(y - 1);
                }
                int temp = (c == dp.get(0).get(y).s2) ? (y + 1) : 0;
                if ((path.length() >= n - 1 && dp.get(path.length() - n + 1).get(temp).s2 == 'F' && temp == n)
                        || dp.get(path.length() + 1).get(temp).s1 >= 0) {
                    continue;
                }
                dp.get(path.length() + 1).set(temp, new Pair(curr, c));
                if (path.length() + 1 == len) {
                    return path + c;
                }
                State newState = new State(temp, path + c);
                if (!visited.contains(newState)) {
                    visited.add(newState);
                    queue.add(newState);
                }
            }
        }

        return "-1";
    }

    // Main solution method
    private static String solution(String s1, String s2) {
        int n = s1.length();
        int m = s2.length();
        int len = n + m - 1;
        StringBuilder r = new StringBuilder(len);
        r.append('0');
        for (int i = 1; i < len; i++) {
            r.append('0');
        }

        for (int i = 0; i < m; i++) {
            if (s2.charAt(i) == 'T') {
                for (int j = 0; j < n; j++) {
                    if (r.charAt(i + j) != '0' && r.charAt(i + j) != s1.charAt(j)) {
                        return "-1";
                    }
                    r.setCharAt(i + j, s1.charAt(j));
                }
            }
        }

        List<Integer> next = findNext(s1);
        List<List<Pair>> dp = new ArrayList<>();
        for (int i = 0; i <= len; i++) {
            dp.add(new ArrayList<>(Collections.nCopies(len + 1, new Pair(-1, '-'))));
        }

        return bfs(dp, len, n);
    }

    // Main method to run the solution
    public static void main(String[] args) {
        System.out.println(solution("ABCA", "TFFF"));
    }

    // Helper class to store a pair of values
    private static class Pair {
        int s1;
        char s2;

        Pair(int s1, char s2) {
            this.s1 = s1;
            this.s2 = s2;
        }
    }

    // Helper class for BFS state
    private static class State {
        int index;
        String path;

        State(int index, String path) {
            this.index = index;
            this.path = path;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o)
                return true;
            if (o == null || getClass() != o.getClass())
                return false;
            State state = (State) o;
            return index == state.index && path.equals(state.path);
        }

        @Override
        public int hashCode() {
            return Objects.hash(index, path);
        }
    }
}
