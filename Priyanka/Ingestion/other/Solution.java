import java.util.*;

public class Solution {
    // Main solution method
    private static String solution(String s1, String s2) {
        int n = s1.length();
        int m = s2.length();
        int len = n + m - 1;
        StringBuilder text = new StringBuilder(len);
        text.append('0');
        for (int i = 1; i < len; i++) {
            text.append('0');
        }

        for (int i = 0; i < m; i++) {
            if (s2.charAt(i) == 'T') {
                for (int j = 0; j < n; j++) {
                    if (text.charAt(i + j) != '0' && text.charAt(i + j) != s1.charAt(j)) {
                        return "-1";
                    }
                    text.setCharAt(i + j, s1.charAt(j));
                }
            }
        }

        List<Integer> next = findNext(s1);
        List<List<Pair>> sls = new ArrayList<>();
        for (int i = 0; i <= len; i++) {
            sls.add(new ArrayList<>(Collections.nCopies(len + 1, new Pair(-1, '-'))));
        }

        Queue<Integer> queue = new LinkedList<>();
        queue.add(0);

        for (int i = 0; i < len; i++) {
            char start = text.charAt(i);
            char end = text.charAt(i);
            if (text.charAt(i) == '0') {
                start = 'A';
                end = 'B';
            }

            int queueSize = queue.size();
            for (int j = 0; j < queueSize; j++) {
                int x = queue.poll();
                for (char c = start; c <= end; c++) {

                    int y;
                    if (x == n)
                        y = next.get(x - 1);
                    else
                        y = x;

                    while (y > 0 && c != s1.charAt(y)) {
                        y = next.get(y - 1);
                    }

                    int temp;
                    if (c == s1.charAt(y))
                        temp = (y + 1);
                    else
                        temp = 0;

                    if ((i >= n - 1 && s2.charAt(i - n + 1) == 'F' && temp == n)
                            || sls.get(i + 1).get(temp).s1 >= 0) {
                        continue;
                    }
                    sls.get(i + 1).set(temp, new Pair(x, c));
                    if (i + 1 == len) {
                        return search(sls, len, temp);
                    }
                    queue.add(temp);
                }
            }
        }

        return "-1";
    }

    // Main method to run the solution
    public static void main(String[] args) {
        System.out.println(solution("BDEF", "FFTF"));
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

    // Method for depth-first search
    private static String search(List<List<Pair>> sls, int len, int curr) {
        if (len == 0)
            return "";
        Pair pair = sls.get(len).get(curr);
        return search(sls, len - 1, pair.s1) + pair.s2;
    }
}
