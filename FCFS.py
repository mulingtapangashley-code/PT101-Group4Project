import java.util.*;

public class FCFS  {

    static class Process {
        String id;
        int arrivalTime;
        int burstTime;
        int completionTime;
        int turnaroundTime;
        int waitingTime;
        int responseTime;

        Process(String id, int at, int bt) {
            this.id = id;
            this.arrivalTime = at;
            this.burstTime = bt;
        }
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.println("==================================");
        System.out.println("     FCFS CPU SCHEDULING");
        System.out.println("==================================");

        System.out.print("Enter number of processes: ");
        int n = sc.nextInt();

        while (n <= 0) {
            System.out.print("Enter a valid number: ");
            n = sc.nextInt();
        }

        Process[] p = new Process[n];

        for (int i = 0; i < n; i++) {

            System.out.println("\nProcess " + (i + 1));

            System.out.print("Process ID: ");
            String id = sc.next();

            System.out.print("Arrival Time: ");
            int at = sc.nextInt();

            System.out.print("Burst Time: ");
            int bt = sc.nextInt();

            while (at < 0 || bt <= 0) {
                System.out.println("Invalid input!");

                System.out.print("Arrival Time: ");
                at = sc.nextInt();

                System.out.print("Burst Time: ");
                bt = sc.nextInt();
            }

            p[i] = new Process(id, at, bt);
        }

        Arrays.sort(p, Comparator.comparingInt(
            process -> process.arrivalTime
        ));

        int time = 0;

        double totalCT = 0;
        double totalTAT = 0;
        double totalWT = 0;
        double totalRT = 0;

        for (int i = 0; i < n; i++) {

            Process current = p[i];

            if (time < current.arrivalTime) {
                time = current.arrivalTime;
            }

            current.responseTime = time - current.arrivalTime;

            time += current.burstTime;

            current.completionTime = time;

            current.turnaroundTime =
                current.completionTime - current.arrivalTime;

            current.waitingTime =
                current.turnaroundTime - current.burstTime;

            totalCT += current.completionTime;
            totalTAT += current.turnaroundTime;
            totalWT += current.waitingTime;
            totalRT += current.responseTime;
        }

        System.out.println("\n==================================");
        System.out.println("           GANTT CHART");
        System.out.println("==================================");

        int currentTime = 0;

        System.out.print("+");

        for (Process process : p) {
            int width = Math.max(7, process.id.length() + 2);

            if (currentTime < process.arrivalTime) {
                int idleWidth = Math.max(7, 7);

                for (int j = 0; j < idleWidth; j++) {
                    System.out.print("-");
                }

                System.out.print("+");
                currentTime = process.arrivalTime;
            }

            for (int j = 0; j < width; j++) {
                System.out.print("-");
            }

            System.out.print("+");
        }

        System.out.println();

        currentTime = 0;
        System.out.print("|");

        for (Process process : p) {

            if (currentTime < process.arrivalTime) {
                System.out.printf("%-7s|", "IDLE");
                currentTime = process.arrivalTime;
            }

            int width = Math.max(7, process.id.length() + 2);
            int left = (width - process.id.length()) / 2;

            for (int j = 0; j < left; j++)
                System.out.print(" ");

            System.out.print(process.id);

            for (int j = left + process.id.length(); j < width; j++)
                System.out.print(" ");

            System.out.print("|");

            currentTime += process.burstTime;
        }

        System.out.println();

        System.out.print("+");

        currentTime = 0;

        for (Process process : p) {

            if (currentTime < process.arrivalTime) {
                for (int j = 0; j < 7; j++)
                    System.out.print("-");

                System.out.print("+");
                currentTime = process.arrivalTime;
            }

            int width = Math.max(7, process.id.length() + 2);

            for (int j = 0; j < width; j++)
                System.out.print("-");

            System.out.print("+");

            currentTime += process.burstTime;
        }

        System.out.println();

        currentTime = 0;
        System.out.print("0");

        for (Process process : p) {

            if (currentTime < process.arrivalTime) {
                System.out.printf("%8d", process.arrivalTime);
                currentTime = process.arrivalTime;
            }

            currentTime += process.burstTime;

            System.out.printf("%8d", currentTime);
        }

        System.out.println("\n\n==================================");
        System.out.println("         PROCESS TABLE");
        System.out.println("==================================");

        System.out.printf("%-10s %-5s %-5s %-5s %-5s %-5s %-5s%n",
            "Process", "AT", "BT", "CT", "TAT", "WT", "RT");

        for (Process process : p) {

            System.out.printf("%-10s %-5d %-5d %-5d %-5d %-5d %-5d%n",
                process.id,
                process.arrivalTime,
                process.burstTime,
                process.completionTime,
                process.turnaroundTime,
                process.waitingTime,
                process.responseTime
            );
        }

        System.out.println("\n==================================");
        System.out.println("         AVERAGE RESULTS");
        System.out.println("==================================");

        System.out.printf("Average CT  : %.2f%n", totalCT / n);
        System.out.printf("Average TAT : %.2f%n", totalTAT / n);
        System.out.printf("Average WT  : %.2f%n", totalWT / n);
        System.out.printf("Average RT  : %.2f%n", totalRT / n);

        System.out.println("\nFCFS Scheduling Completed!");

        sc.close();
    }
}
