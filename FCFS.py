import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.*;

abstract class Vehicle {
    private String ownerName;
    private String plateNumber;

    public Vehicle(String ownerName, String plateNumber) {
        this.ownerName = ownerName;
        this.plateNumber = plateNumber;
    }

    public String getOwnerName() {
        return ownerName;
    }

    public String getPlateNumber() {
        return plateNumber;
    }

    public abstract String getVehicleType();

    public abstract double getParkingRate();
}
class Car extends Vehicle {

    public Car(String owner, String plate) {
        super(owner, plate);
    }

    @Override
    public String getVehicleType() {
        return "Car";
    }

    @Override
    public double getParkingRate() {
        return 20.00;
    }
}
class Motorcycle extends Vehicle {

    public Motorcycle(String owner, String plate) {
        super(owner, plate);
    }

    @Override
    public String getVehicleType() {
        return "Motorcycle";
    }

    @Override
    public double getParkingRate() {
        return 15.00;
    }
}
class ParkingTransaction {

    Vehicle vehicle;
    String slotNumber;
    String personnel;

    LocalDateTime timeIn;
    LocalDateTime timeOut;

    double totalFee;

    public ParkingTransaction(
        Vehicle vehicle,
        String slotNumber,
        String personnel
    ) {
        this.vehicle = vehicle;
        this.slotNumber = slotNumber;
        this.personnel = personnel;
        this.timeIn = LocalDateTime.now();
    }

    public void calculateFee() {

        timeOut = LocalDateTime.now();

        long minutes = Duration.between(
            timeIn, timeOut
        ).toMinutes();

        long hours = Math.max(1, (minutes + 59) / 60);

        totalFee = hours * vehicle.getParkingRate();
    }
}
public class SmartParkingSystem {

    static Scanner sc = new Scanner(System.in);

    static final String USERNAME = "admin";
    static final String PASSWORD = "12345";

    static ArrayList<ParkingTransaction> activeVehicles =
        new ArrayList<>();

    static ArrayList<ParkingTransaction> history =
        new ArrayList<>();

    static String[] carSlots = {
        "C01", "C02", "C03", "C04", "C05"
    };

    static String[] motorcycleSlots = {
        "M01", "M02", "M03", "M04", "M05"
    };

    static DateTimeFormatter formatter =
        DateTimeFormatter.ofPattern(
            "MMM dd, yyyy hh:mm:ss a"
        );

    static boolean login() {

        System.out.println("\n==================================");
        System.out.println(" SMART PARKING MANAGEMENT SYSTEM");
        System.out.println("==================================");

        for (int attempt = 1; attempt <= 3; attempt++) {

            System.out.print("\nUsername: ");
            String user = sc.nextLine();

            System.out.print("Password: ");
            String pass = sc.nextLine();

            if (user.equals(USERNAME) &&
                pass.equals(PASSWORD)) {

                System.out.println("\nLogin Successful!");
                System.out.println("Welcome, Parking Personnel!");

                return true;

            } else {

                System.out.println("\nInvalid username or password.");
                System.out.println("Attempts left: " +
                    (3 - attempt));
            }
        }

        System.out.println("\nAccess Denied!");
        return false;
    }

    static void dashboard() {

        int choice;

        do {

            System.out.println("\n==================================");
            System.out.println("          MAIN DASHBOARD");
            System.out.println("==================================");
            System.out.println("1. Register Vehicle / Time-In");
            System.out.println("2. View Parking Slots");
            System.out.println("3. Vehicle Time-Out");
            System.out.println("4. View Active Vehicles");
            System.out.println("5. Transaction History");
            System.out.println("6. Logout");
            System.out.println("==================================");

            System.out.print("Enter choice: ");
            choice = readNumber();

            switch (choice) {

                case 1:
                    registerVehicle();
                    break;

                case 2:
                    viewSlots();
                    break;

                case 3:
                    timeOutVehicle();
                    break;

                case 4:
                    viewActiveVehicles();
                    break;

                case 5:
                    viewHistory();
                    break;

                case 6:
                    System.out.println(
                        "\nLogging out..."
                    );
                    break;

                default:
                    System.out.println(
                        "\nInvalid choice!"
                    );
            }

        } while (choice != 6);
    }

    static void registerVehicle() {

        System.out.println("\n==================================");
        System.out.println("       VEHICLE REGISTRATION");
        System.out.println("==================================");

        System.out.print("Owner's Name: ");
        String owner = sc.nextLine().trim();

        System.out.print("Plate Number: ");
        String plate = sc.nextLine().trim().toUpperCase();

        if (owner.isEmpty() || plate.isEmpty()) {
            System.out.println("Please complete all information.");
            return;
        }

        for (ParkingTransaction t : activeVehicles) {

            if (t.vehicle.getPlateNumber().equalsIgnoreCase(plate)) {
                System.out.println(
                    "Vehicle is already parked!"
                );
                return;
            }
        }

        System.out.println("\nVehicle Type:");
        System.out.println("1. Car");
        System.out.println("2. Motorcycle");

        System.out.print("Select Type: ");
        int type = readNumber();

        Vehicle vehicle;

        if (type == 1) {
            vehicle = new Car(owner, plate);

        } else if (type == 2) {
            vehicle = new Motorcycle(owner, plate);

        } else {
            System.out.println("Invalid vehicle type!");
            return;
        }

        String slot = findAvailableSlot(
            vehicle.getVehicleType()
        );

        if (slot == null) {

            System.out.println(
                "\nNo available parking slot!"
            );
            return;
        }

        ParkingTransaction transaction =
            new ParkingTransaction(
                vehicle,
                slot,
                USERNAME
            );

        activeVehicles.add(transaction);

        System.out.println("\n==================================");
        System.out.println("       VEHICLE SUCCESSFULLY PARKED");
        System.out.println("==================================");

        System.out.println("Owner: " + owner);
        System.out.println("Plate Number: " + plate);
        System.out.println("Vehicle Type: " +
            vehicle.getVehicleType());
        System.out.println("Assigned Slot: " + slot);
        System.out.println("Time-In: " +
            transaction.timeIn.format(formatter));

        System.out.println("Parking Rate: PHP " +
            vehicle.getParkingRate() + " per hour");

        System.out.println("Parking Ticket Generated!");
    }
    static String findAvailableSlot(String type) {

        String[] slots;

        if (type.equals("Car")) {
            slots = carSlots;
        } else {
            slots = motorcycleSlots;
        }

        for (String slot : slots) {

            boolean occupied = false;

            for (ParkingTransaction t : activeVehicles) {

                if (t.slotNumber.equals(slot)) {
                    occupied = true;
                    break;
                }
            }

            if (!occupied) {
                return slot;
            }
        }

        return null;
    }

    static void viewSlots() {

        System.out.println("\n==================================");
        System.out.println("        PARKING SLOT STATUS");
        System.out.println("==================================");

        System.out.println("\nCAR PARKING SLOTS:");

        displaySlotStatus(carSlots);

        System.out.println("\nMOTORCYCLE PARKING SLOTS:");

        displaySlotStatus(motorcycleSlots);

    }

    static void displaySlotStatus(String[] slots) {

        for (String slot : slots) {

            boolean occupied = false;

            for (ParkingTransaction t : activeVehicles) {

                if (t.slotNumber.equals(slot)) {
                    occupied = true;
                    break;
                }
            }

            System.out.println(
                slot + " : " +
                (occupied ? "OCCUPIED" : "AVAILABLE")
            );
        }
    }

    static void timeOutVehicle() {

        System.out.println("\n==================================");
        System.out.println("          VEHICLE TIME-OUT");
        System.out.println("==================================");

        System.out.print("Enter Plate Number: ");

        String plate = sc.nextLine().trim();

        ParkingTransaction selected = null;

        for (ParkingTransaction t : activeVehicles) {

            if (t.vehicle.getPlateNumber()
                .equalsIgnoreCase(plate)) {

                selected = t;
                break;
            }
        }

        if (selected == null) {

            System.out.println(
                "\nVehicle record not found!"
            );
            return;
        }

        selected.calculateFee();

        System.out.println("\nVehicle Found!");

        System.out.println(
            "Owner: " + selected.vehicle.getOwnerName()
        );

        System.out.println(
            "Plate Number: " +
            selected.vehicle.getPlateNumber()
        );

        System.out.println(
            "Parking Slot: " + selected.slotNumber
        );

        System.out.println(
            "Time-In: " +
            selected.timeIn.format(formatter)
        );

        System.out.println(
            "Time-Out: " +
            selected.timeOut.format(formatter)
        );

        System.out.println(
            "Total Parking Fee: PHP " +
            String.format("%.2f", selected.totalFee)
        );

        System.out.println("\nGenerate Receipt? (Y/N)");
        String answer = sc.nextLine();

        if (answer.equalsIgnoreCase("Y")) {

            generateReceipt(selected);

            history.add(selected);

            activeVehicles.remove(selected);

            System.out.println(
                "\nTransaction Completed Successfully!"
            );

            System.out.println(
                "Parking Slot " + selected.slotNumber +
                " is now AVAILABLE."
            );

        } else {

            System.out.println(
                "\nTransaction cancelled. " +
                "Vehicle remains parked."
            );
        }
    }
    static void generateReceipt(
        ParkingTransaction t
    ) {

        System.out.println("\n");
        System.out.println("==================================");
        System.out.println("       PARKING OFFICIAL RECEIPT");
        System.out.println("==================================");

        System.out.println("Owner Name: " +
            t.vehicle.getOwnerName());

        System.out.println("Vehicle Type: " +
            t.vehicle.getVehicleType());

        System.out.println("Plate Number: " +
            t.vehicle.getPlateNumber());

        System.out.println("Parking Slot: " +
            t.slotNumber);

        System.out.println("----------------------------------");

        System.out.println("Date: " +
            t.timeIn.toLocalDate());

        System.out.println("Time-In: " +
            t.timeIn.format(formatter));

        System.out.println("Time-Out: " +
            t.timeOut.format(formatter));

        System.out.println("----------------------------------");

        System.out.println("Parking Rate: PHP " +
            String.format("%.2f",
                t.vehicle.getParkingRate()));

        System.out.println("TOTAL FEE: PHP " +
            String.format("%.2f", t.totalFee));

        System.out.println("----------------------------------");

        System.out.println("Personnel on Duty: " +
            t.personnel);

        System.out.println("Thank you for parking!");

        System.out.println("==================================");
    }

    static void viewActiveVehicles() {

        System.out.println("\n==================================");
        System.out.println("          ACTIVE VEHICLES");
        System.out.println("==================================");

        if (activeVehicles.isEmpty()) {

            System.out.println("No vehicles currently parked.");
            return;
        }

        for (ParkingTransaction t : activeVehicles) {

            System.out.println("\nOwner: " +
                t.vehicle.getOwnerName());

            System.out.println("Plate: " +
                t.vehicle.getPlateNumber());

            System.out.println("Type: " +
                t.vehicle.getVehicleType());

            System.out.println("Slot: " +
                t.slotNumber);

            System.out.println("Time-In: " +
                t.timeIn.format(formatter));
        }
    }

    static void viewHistory() {

        System.out.println("\n==================================");
        System.out.println("        TRANSACTION HISTORY");
        System.out.println("==================================");

        if (history.isEmpty()) {

            System.out.println("No completed transactions.");
            return;
        }

        for (ParkingTransaction t : history) {

            System.out.println("\nOwner: " +
                t.vehicle.getOwnerName());

            System.out.println("Plate: " +
                t.vehicle.getPlateNumber());

            System.out.println("Type: " +
                t.vehicle.getVehicleType());

            System.out.println("Slot: " +
                t.slotNumber);

            System.out.println("Fee: PHP " +
                String.format("%.2f", t.totalFee));

            System.out.println("Time-Out: " +
                t.timeOut.format(formatter));

            System.out.println("----------------------------------");
        }
    }

    static int readNumber() {

        while (true) {

            try {

                int number = Integer.parseInt(
                    sc.nextLine()
                );

                return number;

            } catch (NumberFormatException e) {

                System.out.print(
                    "Invalid input! Enter a number: "
                );
            }
        }
    }

    public static void main(String[] args) {

        System.out.println("\n");
        System.out.println("********************************");
        System.out.println(" SMART PARKING MANAGEMENT SYSTEM");
        System.out.println("********************************");

        if (login()) {

            dashboard();

        }

        System.out.println(
            "\nThank you for using Smart Parking System!"
        );

        sc.close();
    }
}
